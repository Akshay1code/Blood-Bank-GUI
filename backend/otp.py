import random
import time
import smtplib
from email.message import EmailMessage
user_dict={}

def verify_otp(otp_entry,email):
    print(user_dict,otp_entry)
    if otp_entry == user_dict[email]['otp']:
        return True
    else: 
        return False

def generate_otp(name,email):

    global user_dict
    user_dict[email]={"otp":str(random.randint(100000,1000000)),"time":time.time()}

    SENDER_EMAIL = "menonakshaydb@gmail.com"
    APP_PASSWORD = "xqzsnwjrnsrmydnm"   # step-0 me jo mila
    RECEIVER_EMAIL = email  # apna ya dost ka

    msg = EmailMessage()
    msg["Subject"] = "RedLink Blood App OTP Verification"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    msg.set_content(
        f"Hello User {name}👋\n\nYour OTP for RedLink Email Verification is {user_dict[email]['otp']}.\nOtp will expire under 5-minutes\n\nThanks and Regards RedLink Developer."
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

    print("✅ Email sent successfully")

def delete_current_user(name,email):
    del user_dict[email]
    generate_otp(name,email)
        
        