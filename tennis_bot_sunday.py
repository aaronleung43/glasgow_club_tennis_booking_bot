from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
load_dotenv()

def is_tomorrow_sunday():
    # website will take out sunday and date if today is sat,this is for returning 'tomorrow' text for searching
    today = datetime.today()
    return 5 == today.weekday()
        
def closest_sunday():
    # weekday from 0 -6,adjust here and constant TARGET_DAY to book different weekday 
    today = datetime.today()
    days_til_sunday = 6 - today.weekday()
    # if today is sunday, book next sunday
    if days_til_sunday ==0:
        days_til_sunday = 7
    sunday = today + timedelta(days=days_til_sunday)
    sunday_in_format = sunday.strftime(f"{sunday.day} %B %Y")
    print(f"Closest date is {sunday_in_format}")
    return sunday_in_format

def accept_cookies():
    # try to accept cookie when it exist
    try:
        print("--------------------")
        print("Trying to see if there is any cookies.")
        wait = WebDriverWait(driver,2)
        accept_cookie = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"button[id='accept-consent']")))
        accept_cookie.click()
        print("cookies accepted")
    except (NoSuchElementException, TimeoutException):
        print("--------------------")
        print("No cookies found.")
        pass
    
def login(wait,driver,MY_EMAIL,MY_PASSWORD):
    print("--------------------")
    print("Trying to Login.")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"img[class^='header-logo']")))
    email = driver.find_element(By.CSS_SELECTOR,value="input[name='email']")
    email.clear()
    email.send_keys(MY_EMAIL)
    password = driver.find_element(By.CSS_SELECTOR,value="input[name='password']")
    password.clear()
    password.send_keys(MY_PASSWORD)
    login_button = driver.find_element(By.CSS_SELECTOR,value="button[id^='login-submit']")
    login_button.click()
    # timeout counter 123
    clear_filter = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[id^='reset-filters']")))
    print("--------------------")
    print("Login successfully")
    
def provide_filter(wait,driver):
    print("--------------------")
    print("Trying to provide filter.")
    # auto type in filter
    activity = driver.find_element(By.CSS_SELECTOR,value="input[id='activityIds']")
    activity.send_keys(ACTIVITY)
    activity_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Courts & Pitches')]")))
    activity_button.click()

    calendar = driver.find_element(By.CSS_SELECTOR,value="button[aria-label='Open calendar']")
    calendar.click()
    date = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,f"td[aria-label='{CLOSEST_SUNDAY}']")))
    date.click()

    three_oclock_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"option[value='15']")))
    three_oclock_button.click()
    search_court = driver.find_element(By.CSS_SELECTOR,value="button[id='submit-filters-btn']")
    search_court.click()
    print("--------------------")
    print("Searching with filter")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"h2[class^='activity-search__search-results-']")))
    
def search_availability(wait,driver):
    # not assuming first result will be first sunday even we put filter on
    print("--------------------")
    print("Searching for closest sunday.")
    all_days = driver.find_elements(By.CSS_SELECTOR,value="h2[class^='activity-search__search-results-']")
    for day in all_days:
        if is_tomorrow_sunday():
            print("Tomorrow is Sunday, searching for 'Tomorrow' in text")
            if "Tomorrow" == day.text:
                first_sunday = day
                break
        else: 
            if TARGET_DAY in day.text:
                first_sunday = day
                break
        
    first_sunday_parent = first_sunday.find_element(By.XPATH,value="..")
    all_activity = first_sunday_parent.find_elements(By.TAG_NAME,value="li")
    print("--------------------")
    print("Searching for tennis court booking option.")
    if all_activity:
        for activity in all_activity:
            if LOCATION in activity.text and "Tennis Court Bookings" in activity.text:
                search_availability_button = activity.find_element(By.CSS_SELECTOR,value="button[id^='view-activity']")
                search_availability_button.click()
                break
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h2[class^='activity-calendar']")))
        print("--------------------")
        print("Tennis court option chose")
    else:
        print("No activity found")

def get_court_name(targer_court_number):
    # return court number as str
    return f"Court {targer_court_number}"
def find_available_slots(target_court):
    # check if the time in TARGET_TIME and court in target court are both free
    all_result = []
    for each_time in TARGET_START_TIME:
        print("--------------------")
        print(f"Searching for {target_court} time : {each_time}.")
        all_h2 = driver.find_elements(By.CSS_SELECTOR,value="h2[class^='activity-calendar-']")
        for h2 in all_h2:
            if h2.text.strip() == each_time:
                target_h2 = h2
                target_parent = target_h2.find_element(By.XPATH,value="./ancestor::div[@class='activity-calendar-timetable__list-container']")
                all_court= target_parent.find_elements(By.CSS_SELECTOR,value="ol li")
                if all_court:
                    for court in all_court:
                        if target_court in court.text and "Book now" in court.text:
                            all_result.append(court)
                            print(f"✅ {target_court} for {each_time} space found!")
                        else:
                            print(f"❌{target_court} for {each_time} space not found!")
    if len(all_result) == len(TARGET_START_TIME):
        # return elements to book
        return all_result
    else:
        return False
                        
def add_court_to_basket(wait,driver,list_of_elements):
    print("--------------------")
    print("Adding court to basketball")
    for element in list_of_elements:
            booking_court_button = element.find_element(By.CSS_SELECTOR,value="button[id^='book-slot-']")
            booking_court_button.click()

            add_to_basket_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[id^='add-to-basket']")))
            add_to_basket_button.click()

            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"button[id='added-to-basket-btn']")))
            close_button = driver.find_element(By.CSS_SELECTOR,value="button[id='close-activity-in-basket-slot-btn']")
            close_button.click()
            wait.until(lambda d: "This slot is unavailable" in element.text)
            print("--------------------")
            print("✅ Count have been added to basket")
            
def clean_court_name(court_str):
    cleaned = court_str.lower().strip()
    cleaned = cleaned.replace("tennis hall court", "tennis court")
    cleaned = " ".join(cleaned.split())
    return cleaned
def check_basket_data(wait,driver):
    # TODO  Future upgrade: data from web may not stable,may change to in to compare
    basket_page = driver.find_element(By.CSS_SELECTOR,value="a[href='/book/basket']")
    basket_page.click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[id='continue-to-payment-btn']")))
    basket_data = []
    all_booking = driver.find_elements(By.TAG_NAME,value="app-card")
    for booking in all_booking:
        court_text_basket = booking.find_element(By.CSS_SELECTOR,value="div[class='basket-item-booking-location']").text
        date_time_text_basket = booking.find_element(By.CSS_SELECTOR,value="div[class='basket-item-booking-datetime']").text
        apart = date_time_text_basket.split()
        basket_data.append(
            {"court" : clean_court_name(court_text_basket.split("/")[0].strip()),
            "location" : court_text_basket.split("/")[1].strip(),
            "start" : apart[4],
            "end" : apart[6],
            "date" : f"{apart[1]} {apart[2].strip(',')} {apart[3]}" 
            }
        )
    return basket_data

def expected_data(TARGET_START_TIME,TARGET_END_TIME,TARGET_COURT_NUMBER,LOCATION,CLOSEST_SUNDAY):
    expect_data_dict = []
    for start,end in zip(TARGET_START_TIME,TARGET_END_TIME):
        expect_data_dict.append(
            {"court" : f"tennis court {TARGET_COURT_NUMBER}",
            "location" : LOCATION,
            "start" : start,
            "end" : end,
            "date" : CLOSEST_SUNDAY
            }
        )
    return expect_data_dict

def process_payment(wait,driver,MY_CARD,EXPIRY_DAY,CVV):
    payment_button = driver.find_element(By.CSS_SELECTOR,value="button[id='continue-to-payment-btn']")
    payment_button.click()

    iframe = wait.until(EC.presence_of_element_located((By.ID, "hostedfield-frame-1")))
    driver.switch_to.frame(iframe)
    print("--------------------")
    print("Start to type card detail...")
    card_input = wait.until(EC.presence_of_element_located((By.NAME,"cardNumber")))
    card_input.clear()
    for num in MY_CARD:
        # avoid type too fast
        card_input.send_keys(num)
        time.sleep(0.01)
        
    driver.switch_to.default_content()  
    iframe2 = wait.until(EC.presence_of_element_located((By.ID,"hostedfield-frame-2")))
    driver.switch_to.frame(iframe2)
    print("Start to type expiry date...")
    expiry_input = driver.find_element(By.NAME,value="cardExpiryDate")
    expiry_input.clear()
    for num in EXPIRY_DAY:
        expiry_input.send_keys(num)
        time.sleep(0.01)
        
    driver.switch_to.default_content()
    iframe3 = wait.until(EC.presence_of_element_located((By.ID,"hostedfield-frame-3")))
    driver.switch_to.frame(iframe3)
    
    print("Start to type CVV...")
    cvv_input = driver.find_element(By.NAME,value="cardCVV")
    cvv_input.clear()
    for num in CVV:
        cvv_input.send_keys(num)
        time.sleep(0.01)
    
    driver.switch_to.default_content()
    
    pay_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"button[aria-disabled='false']")))
    pay_button.click()
    print("--------------------")
    print("Paying...")

def wait_for_payment_result(wait, driver):
    print("Waiting for payment result...")
    try:
        wait.until(
            lambda d: (
                "Booking Confirmed" in d.page_source
                or "Payment Failed" in d.page_source
                or "Declined" in d.page_source
                or "3D Secure" in d.page_source
            )
        )
    except TimeoutException:
        return "UNKNOWN"

    page = driver.page_source

    if "Booking Confirmed" in page:
        return "SUCCESS"

    if "Payment Failed" in page or "Declined" in page:
        return "FAILED"

    if "3D Secure" in page or "Authentication" in page:
        return "3DS"
    
    else:
        return "UNKNOWN"

def process_payment_result(driver,payment_result):
    wait_3ds = WebDriverWait(driver, 60)
    if payment_result == "SUCCESS":
        print("✅ booked")
        return get_booking_detail(driver)
        
    elif payment_result == "FAILED":
        print(f"❌Payment failed on {datetime.today().date()}")
        driver.save_screenshot(f"Payment_failed_on_{datetime.today().date()}")        
        return False
    
    elif payment_result == "3DS":
        print("🔐Payment require verify")
        print("System will wait for 60 second for you to verrify on app.")
        try:
            wait_3ds.until(lambda d: "Booking Confirmed" in d.page_source)
            print("🎉 3DS verify confirmed！")
            return get_booking_detail(driver)
        except (TimeoutException):
            print("System waited too long, please try again")
            return False
        

    elif payment_result =="UNKNOWN":
        print(f"⚠️Unknown situation on {datetime.today().date()}")
        driver.save_screenshot(f"Unknown_situation_on_{datetime.today().date()}")
        return False
    
def get_booking_detail(driver):
    booked_cards = driver.find_elements(By.CSS_SELECTOR, "app-activity.basket-confirmation-booked-activity-card > div")
    confirmed_booking = []
    for card in booked_cards:
        raw_date_time = card.find_element(By.XPATH,value=".//p[contains(@class, 'activity-date')]").text
        start_time = card.find_element(By.XPATH,value=".//span[contains(@class, 'activity-time')]").text
        date = " ".join(raw_date_time.split()).replace(start_time, "").strip()
        booking_ref = card.find_element(By.XPATH,value=".//span[@class='activity-ref-id']").text
        confirmed_booking.append(
            {
                "date" : date,
                "time" : start_time,
                "booking_ref" : booking_ref
            }
        )
    return confirmed_booking

def get_summary(results):
    for result in results:
        print("==========Booking Summary==========")
        print(f"|  Date  :  {result["date"]}  |")
        print(f"|  Time  :  {result["time"]}                  |")
        print(f"|  Booking reference : {result["booking_ref"]}   |")
        print("====================================")
        
def logout(wait,driver):
    home_page = driver.find_element(By.CSS_SELECTOR,value="li[class^='navigation__item']")
    home_page.click()
    print("logging out")
    logout = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[id='user-navigation-logout-button']")))
    logout.click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='email']")))
    print("logout successfully")
            
URL = "https://glasgowclub.gladstonego.cloud/auth/login"
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver,10)
driver.get(url=URL)
MY_EMAIL = os.getenv("EMAIL")
MY_PASSWORD = os.getenv("PASSWORD")
MY_CARD = os.getenv("CREDITCARD")
EXPIRY_DAY = os.getenv("EXPIRY_DAY")
CVV = os.getenv("CVV")
ACTIVITY = "Courts & Pitches"
CLOSEST_SUNDAY = closest_sunday()
TARGET_DAY = "Sunday"
TARGET_START_TIME = ["15:00","16:00"]
TARGET_END_TIME = ["16:00","17:00"]
LOCATION = "Gorbals"
TARGET_COURT_NUMBER = [1,4,3,2]                                     

accept_cookies()
login(wait,driver,MY_EMAIL,MY_PASSWORD)
provide_filter(wait,driver)
search_availability(wait,driver)
COURT_NUMBER = None
space = None
for target in TARGET_COURT_NUMBER:
    # loop for court 1 > 4 > 3 > 2
    check_court_availability = find_available_slots(get_court_name(target))
    if check_court_availability:
        print(f"=====Adding court {target} to basket=====")
        add_court_to_basket(wait,driver,check_court_availability)
        space = True
        COURT_NUMBER = target
        break
    else:
        print(f"=====Court {target} don't have space=====")
        print(f"=====Trying to book another court=====")    
        
if space == None:
    print("All courts are full. Maybe next week")
else:
    expectation = expected_data(TARGET_START_TIME,TARGET_END_TIME,COURT_NUMBER,LOCATION,CLOSEST_SUNDAY)
    basket_data = check_basket_data(wait,driver)
    if expectation == basket_data:
        print("=====Data is match=====")
        process_payment(wait,driver,MY_CARD,EXPIRY_DAY,CVV)
        payment_result = wait_for_payment_result(wait,driver)
        results = process_payment_result(driver,payment_result)
        if results:
            get_summary(results)
        
        else:
            print("Please take a look of the screenshot that been taken")

    else:
        print("=====Data don't match=====")
        print(f"Expected data {expectation}")
        print(f"Actually basket data {basket_data}")

logout(wait,driver)
driver.close()
