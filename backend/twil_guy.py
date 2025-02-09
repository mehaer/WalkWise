from twilio.rest import Client

# for the account information
import os
from dotenv import load_dotenv

# Your Account SID and Auth Token from twilio.com/console
load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(account_sid, auth_token)

def send_emergency_text(phone_numbers, message, twilio_phone_number=TWILIO_PHONE_NUMBER):
    for number in phone_numbers:
        message = client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=number
        )
        print(f"Message sent to {number}: {message.sid}")

if __name__ == "__main__":
    phone_numbers = ['+919082835960']  # Add your phone numbers here
    # prabhat india number
    # phone_numbers = ['+19293284667', '+17324138344', '+1844370696', '+18483360259', '+18485651384', '+16097215316']  # Add your phone numbers here
    # Naman, Vaiswi, Kareena, Prabhat, Aiman, Mehaer
    emergency_message = "This is an emergency alert. Please take immediate action. Jai Mahishmati!"
    send_emergency_text(phone_numbers, emergency_message)