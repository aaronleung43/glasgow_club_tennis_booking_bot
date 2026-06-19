# Glasgow Club Tennis Court Automation Bot
A python script using Selenium to book tennis court in glasgow club
## ⚠️ Quick Notes on Booking Logic

Before running the script, please note that it is configured with the following fixed schedule parameters:
* **Target Time:** Automatically looks for and books a continuous 2-hour slot from **15:00 to 17:00** (composed of two 1-hour sessions at 15:00 and 16:00).
* **Target Day (Closest Sunday):** * If executed between **Monday and Saturday**, the script will automatically target the upcoming Sunday of the current week.
  * If executed on a **Sunday**, it will automatically calculate dates and target the Sunday of the *following* week to prevent same day bookings.


An advanced, production-ready web automation script built with Python and Selenium WebDriver. This project was independently engineered to streamline and secure tennis court bookings at the Glasgow Club  under high-demand environments. 

## 🚀 Key Engineering Highlights

## 💡 How I Solved the Booking Problems (Logics Included)

When I manually booked courts, I faced several issues. Here is how I used Python code to solve them:

### 1. Handling Dynamic Web Pages (No Hardcoded Sleeps)
The Glasgow Club website takes time to load different elements. Instead of using generic time delays (like `time.sleep`), I used Selenium’s `WebDriverWait` and `expected_conditions`. This ensures the bot clicks buttons the exact millisecond they become available, making it faster and less likely to crash.

### 2. Smart Date Calculation
The website changes its text UI based on the day (for example, displaying "Tomorrow" instead of the actual date if today is Saturday). I wrote specific date-handling logic (`closest_sunday()` and `is_tomorrow_sunday()`) so the bot always finds the correct upcoming Sunday regardless of which day the script runs.

### 3. Automatically Trying Alternative Courts (The Loop)
Popular courts get fully booked in seconds. To prevent the script from stopping if Court 4 is full, I implemented a `while` loop. If Court 4 is unavailable for my target 2-hour slot (`15:00 - 17:00`), the bot automatically backtracks and checks Court 3, then Court 2, then Court 1 until it successfully adds available slots to the basket.

### 4. Handling Bank 3DS Verification (Human-in-the-Loop)
Because booking requires payment, the bank often triggers a 3D Secure verification (SMS / Banking App approve). I wrote a 60-second waiting loop (`wait_3ds`) that pauses the script, allowing me to manually approve the payment on my phone before the script automatically verifies and prints the final booking confirmation summary.

### 5. Security & Privacy
To keep my personal details safe, I use a `.env` file and `python-dotenv` to store my login email, password, and card details locally. These sensitive data files are excluded from GitHub, meaning the code is shared publicly without exposing my personal information.

---
---

## 🛠️ Technology Stack
* **Language:** Python 3
* **Automation Framework:** Selenium WebDriver
* **Environment Configuration:** python-dotenv
* **Testing & Infrastructure:** Chrome WebDriver with persistent user-data profiles

## 📦 Local Installation & Setup

## 📦 How to Setup and Run Locally

Follow these steps to configure and run the booking bot on your local machine:

### 1. Install Required Libraries
This script requires **Selenium** for browser automation and **python-dotenv** to securely handle credentials. Open your terminal or command prompt in the project folder and run:

```bash pip3 install selenium python-dotenv```

### 2. Configure Your Environment Variables (.env)
  Create a new file named .env in the root directory of this project.
  Open the file with any text editor and fill in your details using the exact format below:
EMAIL=your_glasgow_club_email@example.com
PASSWORD=your_secure_password
CREDITCARD=1234567812345678
EXPIRY_DAY=MMYY
CVV=123
Note: The .env file is included in .gitignore and will never be pushed to GitHub, ensuring your payment and login details remain 100% private and safe.

### 3. Run the script
```python3 tennis_bot_sunday.py```

## 🔮 Planned Future Upgrades (Roadmap)

To further improve the robustness and flexibility of this script, I plan to implement the following upgrades:

* **Dynamic Time & Court Parameterization:** Migrate fixed constants (like times and location) into environment variables or a CLI argument parser, allowing users to choose custom booking slots without modifying the core code.
* **Robust Basket Data Validation:** Enhance the validation logic (`check_basket_data`) by converting web data strings into strict datetime objects, protecting the script from runtime bugs if the web portal slightly modifies its text UI layout.
* **Notification System:** Integrate a Discord webhook or Telegram bot API to automatically send a confirmation message and booking reference screenshot directly to my phone upon success or failure.
