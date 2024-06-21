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
        I can swallow a bottle of alcohol and I'll feel like Godzilla
        Better hit the deck like the card dealer
        My whole squad's in here, walkin' around the party
        A cross between a zombie apocalypse and B-Bobby, "The
        Brain" Heenan which is probably the same reason I wrestle with mania
        Shady's in this bitch, I'm posse'd up
        Consider it to cross me a costly mistake
        If they sleepin' on me, the hoes better get insomnia, ADHD, Hydroxycut
        Pass the Courvoisi' (hey, hey)
        In AA, with an AK, melee, finna set it like a play date
        Better vacate, retreat like a vacay, mayday (ayy)
        This beat is cray-cray, Ray J, H-A-H-A-H-A
        Laughin' all the way to the bank, I spray flames
        They cannot tame or placate the (ayy)
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
