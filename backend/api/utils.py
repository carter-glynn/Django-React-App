from fpdf import FPDF
from twilio.rest import Client
from django.conf import settings
from datetime import datetime, timedelta
from .models import NotificationPreference, UserPhoneNumber
import logging
import os

# Get logger
logger = logging.getLogger("my logger")

# Create a handler
c_handler = logging.StreamHandler()

# link handler to logger
logger.addHandler(c_handler)

# Set logging level to the logger
logger.setLevel(logging.DEBUG) # <-- THIS!

def send_sms(phone, message):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=message,
        from_="+17756182701",
        to=phone,
    )

def schedule_notifications():
    preferences = NotificationPreference.objects.all()

    for preference in preferences:
        expiry_date = preference.item.warranty_expiration
        notify_when = preference.notify_when

        if notify_when == 'immediate':
            message = f"Reminder: {preference.item.name} is expiring soon!"
        elif notify_when == 'six_months' and datetime.now() >= expiry_date - timedelta(days=180):
            message = f"Reminder: {preference.item.name} will expire in 6 months."
        elif notify_when == 'one_month' and datetime.now() >= expiry_date - timedelta(days=30):
            message = f"Reminder: {preference.item.name} will expire in 1 month."
        elif notify_when == 'one_week' and datetime.now() >= expiry_date - timedelta(days=7):
            message = f"Reminder: {preference.item.name} will expire in 1 week."
        elif notify_when == 'day_of' and datetime.now().date() == expiry_date:
            message = f"Reminder: {preference.item.name} is expiring today!"
        else:
            continue  # Skip if not time for notification

        # Fetch the phone number from the related UserPhoneNumber model
        try:
            user_phone_number = UserPhoneNumber.objects.get(user=preference.user)
            phone_number = user_phone_number.phone_number
            send_sms(phone_number, message)  # Send SMS
        except UserPhoneNumber.DoesNotExist:
            logger.warning(f"No phone number found for user {preference.user.username}")
            continue  # Skip if no phone number is associated with the user 

def export_to_pdf(content, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(filename)
    print(f"Report saved as {filename}")