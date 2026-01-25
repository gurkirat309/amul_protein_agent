from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time

# --------------- CONFIG ---------------
URL = "https://shop.amul.com/en/browse/protein"
PINCODE = "560060"

TARGET_PRODUCTS = [
    "Amul High Protein Rose Lassi, 200 mL | Pack of 30",
    "Amul High Protein Milk, 250 mL | Pack of 8",
    "Amul High Protein Blueberry Shake, 200 mL | Pack of 8"
]

SENDER = SENDER
APP_PASSWORD = PASS
RECEIVER = RECEIVER

# --------------- EMAIL FUNCTION ---------------
def send_email(product):
    subject = f"🎉 {product} is now AVAILABLE!"
    body = f"Good news! The product '{product}' is now available.\n\nCheck here: {URL}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = RECEIVER

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER, APP_PASSWORD)
            server.send_message(msg)
        print(f"✅ Email sent for {product}")
    except Exception as e:
        print("❌ Email sending failed:", e)

# --------------- MAIN CHECK FUNCTION ---------------
def check_availability():
    print(" Checking product availability...")

    options = Options()
    options.add_argument("--headless")  # Run Chrome invisibly
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(URL)
    time.sleep(3)

    # Step 1: Enter pincode
    try:
        pin_input = driver.find_element(By.ID, "pincode-input")
        pin_input.clear()
        pin_input.send_keys(PINCODE)
        time.sleep(1)

        apply_button = driver.find_element(By.XPATH, "//button[contains(text(),'Apply')]")
        apply_button.click()
        time.sleep(5)
    except Exception:
        print("⚠️ Pincode input not found — maybe already set.")

    # Step 2: Scrape HTML
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    found_any = False
    products = soup.find_all("div", class_="product-item")

    for p in products:
        name_tag = p.find("a", class_="product-title")
        if not name_tag:
            continue
        product_name = name_tag.text.strip()

        if product_name in TARGET_PRODUCTS:
            found_any = True
            if p.find("div", class_="out-of-stock"):
                print(f"❌ {product_name} - OUT OF STOCK")
            else:
                print(f"✅ {product_name} - AVAILABLE")
                send_email(product_name)

    if not found_any:
        print("⚠️ No target products found on page.")

# --------------- LOOP ---------------
if __name__ == "__main__":
    while True:
        check_availability()
        print(" Waiting 20 seconds before next check...\n")
        time.sleep(2000)
