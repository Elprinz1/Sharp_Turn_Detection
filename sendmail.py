import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



# Usage for Gmail
email_subject = "Sharp Turn Detected!"

smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = os.environ('<email_address>')  # Replace with your email address
sender_password = os.environ('<password>') # Replace with your password

def send_email(to_email, body, subject = email_subject, 
               smtp_server=smtp_server, smtp_port=smtp_port, 
               sender_email=sender_email, sender_password=sender_password):
    # Create a MIMEText object
    message = MIMEMultipart()
    message['From'] = '<Sender>'  # Replace with your name
    message['To'] = ', '.join(to_email)
    message['Subject'] = subject

    # Attach the body to the email
    message.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Login to the email account
            server.starttls()
            server.login(sender_email, sender_password)

            # Send the email
            server.sendmail(sender_email, to_email, message.as_string())
            
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

