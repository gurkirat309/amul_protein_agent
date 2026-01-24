import smtplib
from dotenv import load_dotenv

from agent import SENDER


load_dotenv()

# --- CONFIG ---
SENDER_EMAIL = SENDER
SENDER_PASSWORD = PASS 
RECEIVER_EMAIL = RECEIVER
# --------------

def send_email(subject, message):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            email_message = f"Subject: {subject}\n\n{message}"
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email_message)
            print("✅ Email sent successfully! The email bot is working perfectly fine !!!")
    except Exception as e:
        print(f" Error: {e}")

# --- TEST ---
send_email("Simple automated text mail sent")
