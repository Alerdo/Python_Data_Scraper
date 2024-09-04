import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from BaseScraper import filters_applied, locations
import os
from dotenv import load_dotenv

# Loading environment variables from the .env file

load_dotenv()

# These variables are being extracted from an ".env file" which I have not comited to github
sender_email = os.getenv('SENDER_EMAIL')
sender_authenticator = os.getenv('SENDER_AUTHENTICATOR')
receiver = os.getenv('RECEIVERS')


template = """

        <html>
    <head></head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 20px auto; color: #333; padding: 20px; max-width: 600px; width: 100%; box-sizing: border-box;">
        <div style="padding: 15px; background-color: #ffffff; border-radius: 8px; box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1); margin-bottom: 40px;">
            <h1 style="font-size: 22px; margin-bottom: 10px; color: #333;">{title}</h1>
            <p style="margin: 5px 0; font-size: 16px; color: #555;">Price: {price}</p>
            <p style="margin: 5px 0; font-size: 16px; color: #555;">Location: {location}</p>
            <p style="margin: 5px 0; font-size: 16px; color: #555;">Website: {website}</p>

            <p style="margin: 15px 0; font-size: 16px;">
                <a href="{url}" style="color: #1a73e8; text-decoration: none;">More details</a>
            </p>
            <p style="margin: 15px 0 0 15px;">
                <img src="{photo}" alt="Property photo" style="max-width: 100%; height: auto; border-radius: 5px; box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);">
            </p>
        </div>
    </body>
    </html>

        """

def send_email(listings):
    # Sender and receiver emails
    sender_address = sender_email
    sender_pass = sender_authenticator
    receivers = receiver

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = ", ".join(receivers)
    message['Subject'] = 'Automated Email - Property Search Result'   # The subject line

    # Prepare email content with listings
    content = []

    # Add each listing into the HTML template
    for listing in listings:
        listing_content = template.format(**listing)
        if listing_content:
            content.append(listing_content)

    # Join all listings into one content block
    full_content = ''.join(content)

    # The header of the email
    cities = ", ".join([city.title() for city in locations])
    min_price = f"€{filters_applied['min_price']:,}"
    max_price = f"€{filters_applied['max_price']:,}"
    websites = filters_applied["websites"]

    mail_content = f'''
        <div>
            <p style="font-size: 18px;">Hello,</p>
            <p style="font-size: 18px; ">This is an automated email. Here is your daily update of properties for {cities}, Albania:</p>
            <p style="margin-top: 0px; font-size: 18px; ">Results showing for {min_price} - {max_price} found on {websites} </p>
            <div style="font-size: 18px;">
                {full_content}
            </div>
        </div>
    '''

    # Attach the body with the msg instance
    message.attach(MIMEText(mail_content, 'html'))

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # Gmail SMTP server and port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receivers, text)
    session.quit()
    print('Mail Sent Successfully')
