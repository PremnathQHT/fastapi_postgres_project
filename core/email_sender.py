import smtplib
import ssl
from email.message import EmailMessage

def send_otp_email(receiver_email, otp):
    # Email details
    email_sender = "creativepremnath@gmail.com"
    email_password = "wfixgwdomxiagrze"  # Use app password or secure method
    email_receiver = receiver_email
    subject = 'Your OTP Verification Code'

    # Create HTML content with OTP placeholder
    html_content = f"""<!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background-color: #28a745;
                color: #ffffff;
                padding: 15px;
                border-radius: 8px 8px 0 0;
                text-align: center;
            }}
            .content {{
                padding: 20px;
            }}
            .footer {{
                font-size: 12px;
                color: #888888;
                text-align: center;
                padding: 15px;
            }}
            .otp-code {{
                font-size: 24px;
                font-weight: bold;
                color: #28a745;
                text-align: center;
                margin: 20px 0;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                color: #ffffff;
                background-color: #28a745;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 10px;
            }}
            .button:hover {{
                background-color: #218838;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>OTP Verification</h1>
            </div>
            <div class="content">
                <p>Hello,User</p>
                <p>Your One-Time Password (OTP) for verification is:</p>
                <div class="otp-code">{otp}</div>
                <p>Please enter this OTP in the application to complete your verification. This code is valid for 1 minute.</p>
                <p>If you did not request this, please ignore this email or contact support.</p>
            </div>
            <div class="footer">
                <p>Thank you for using our service!</p>
                <p>Your Company | 123 Main Street, City, State, ZIP</p>
                <p><strong>Please do not reply to this email. This mailbox is not monitored.</strong></p>
            </div>
        </div>
    </body>
    </html>
    """


    # Create the email message
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(html_content, subtype='html')  # Set content as HTML

    # Set up the SSL context
    context = ssl.create_default_context()

    # Send the email using Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def send_welcome_email(receiver_email, user_name):
    # Email details
    email_sender = "creativepremnath@gmail.com"
    email_password = "wfixgwdomxiagrze"  # Use app password or secure method
    email_receiver = receiver_email
    subject = 'Welcome to Our Service'

    # Create HTML content with user's name and login button
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }}
        .container {{
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            background-color: #28a745; /* Green theme */
            color: #ffffff;
            padding: 15px;
            border-radius: 8px 8px 0 0;
            text-align: center;
        }}
        .content {{
            padding: 20px;
        }}
        .footer {{
            font-size: 12px;
            color: #888888;
            text-align: center;
            padding: 15px;
        }}
        .welcome-message {{
            font-size: 18px;
            margin-bottom: 20px;
        }}
        .button {{
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: #ffffff !important; /* Force font color to white */
            background-color: #28a745;
            text-decoration: none;
            border-radius: 5px;
            text-align: center;
        }}
        .button:hover {{
            background-color: #218838; /* Darker green on hover */
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome, {user_name}!</h1>
        </div>
        <div class="content">
            <p class="welcome-message">We're excited to have you on board. Your account has been successfully created.</p>
            <p>You can now log in and start using our service:</p>
            <div style="text-align: center;">
                <a href="https://yourwebsite.com/login" class="button">Login to Your Account</a>
            </div>
            <p>If you did not create this account, please contact our support team immediately.</p>
        </div>
        <div class="footer">
            <p>Thank you for choosing our service!</p>
            <p>Your Company | 123 Main Street, City, State, ZIP</p>
            <p><strong>Please do not reply to this email. This mailbox is not monitored.</strong></p>
        </div>
    </div>
</body>
</html>
"""



    # Create the email message
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(html_content, subtype='html')  # Set content as HTML

    # Set up the SSL context
    context = ssl.create_default_context()

    # Send the email using Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())     