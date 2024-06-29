import smtplib, ssl
import os, sys
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

port = 465  # using SMTP_SSL()
password = os.getenv("GMAIL_PWD")

sender_gmail = os.getenv("GMAIL_USERNAME")
recepient_gmail = sys.argv[1]
subject = "Test Message from Muchemi"
body = """
<html>
  <body>
    <h1>Obama Inaugural Address</h1>
    <p><i>20th January 2009</i></p>
    <p>My fellow citizens:</p>
    <p>I stand here today humbled by the task before us, grateful for the trust you have bestowed, mindful of the sacrifices borne by our ancestors. I thank President Bush for his service to our nation, as well as the generosity and cooperation he has shown throughout this transition.</p>
    <p>Forty-four Americans have now taken the presidential oath. The words have been spoken during rising tides of prosperity and the still waters of peace. Yet, every so often the oath is taken amidst gathering clouds and raging storms. At these moments, America has carried on not simply because of the skill or vision of those in high office, but because We the People have remained faithful to the ideals of our forbearers, and true to our founding documents.</p>
    <p>So it has been. So it must be with this generation of Americans.</p>
    <p>Thank you. God bless you and God bless the United States of America.</p>
  </body>
</html>
"""


msg = MIMEMultipart()
msg["From"] = sender_gmail
msg["To"] = recepient_gmail
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))


# Create secure ssl context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port=port, context=context) as server:
    server.login(sender_gmail, password)
    server.sendmail(sender_gmail, recepient_gmail, msg.as_string())
    print("Email sent successfully")
