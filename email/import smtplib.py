import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import os

def read_recipients(file_path):
    recipients = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            recipients.append(row)
    return recipients

def send_email(smtp_server, smtp_port, smtp_username, smtp_password, sender_email, recipient_email, subject, body):
    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    # Compose email
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Attach body text
    message.attach(MIMEText(body, 'plain'))

    # Send email
    server.sendmail(sender_email, recipient_email, message.as_string())

    # Disconnect from the server
    server.quit()

def main():
    # SMTP Server settings (change these to your email provider's settings)
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.your-email-provider.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 465))
    smtp_username = os.environ.get('SMTP_USERNAME', 'your_username')
    smtp_password = os.environ.get('SMTP_PASSWORD', 'your_password')

    # Sender email address
    sender_email = os.environ.get('SENDER_EMAIL', 'your_email@example.com')

    # Read recipients from CSV file
    file_path = os.path.join(os.path.dirname(__file__), 'recipients.csv')
    recipients = read_recipients(file_path)

    # Email content
    subject = 'Personalized Subject'
    common_body = 'Hello {},\n\nThis is a personalized email for you!\n\nBest regards,\nYour Name'

    for recipient in recipients:
        # Customize email body for each recipient
        body = common_body.format(recipient['Name'])

        # Send email
        send_email(smtp_server, smtp_port, smtp_username, smtp_password, sender_email,
                   recipient['Email'], subject, body)

        print(f"Email sent to {recipient['Name']} ({recipient['Email']})")

if __name__ == "__main__":
    main()
    
