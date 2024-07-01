import os, sys
import ssl, smtplib
from dotenv import load_dotenv
from mail_ssl import MIMEMultipart, MIMEText

load_dotenv()

port = 587  # for TLS
smtp_server = "smtp.gmail.com"
password = os.getenv('GMAIL_PWD')
sender_gmail = os.getenv('GMAIL_USERNAME')
email_recepient = sys.argv[1]

# create a secure ssl context
context = ssl.create_default_context()

msg = MIMEMultipart()
msg["From"] = sender_gmail
msg["To"] = email_recepient
msg["Subject"] = "This email was sent via TLS"

msg_body = """
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
msg.attach(MIMEText(msg_body, "plain"))

try:
    server = smtplib.SMTP(smtp_server, port=port)
    # server.ehlo()
    server.starttls(context=context)
    # server.ehlo()
    server.login(sender_gmail, password=password)
    server.sendmail(sender_gmail, email_recepient, msg.as_string())
except Exception as e:
    print(e)
