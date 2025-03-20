import time, redis, os
import ssl, smtplib
from dotenv import load_dotenv
from logger.logger import logger
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# create redis client
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

STREAM_NAME = "shopsmart:mail"
GROUP_NAME = "shopsmart:mail_group"
CONSUMER_NAME = "alpha"

load_dotenv()

# Create consumer group
try:
    redis_client.xgroup_create(STREAM_NAME, GROUP_NAME, id="0", mkstream=True)
except Exception as e:
    pass

SENDER_EMAIL = os.getenv("GMAIL_USERNAME")
PASSWORD = os.getenv("GMAIL_PWD")
PORT = 465


def send_email(address, subject, body) -> None:
    msg = MIMEMultipart()
    msg["from"] = SENDER_EMAIL
    msg["to"] = address
    msg["subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port=PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, address, msg.as_string())

        logger.info(f'Email sent to {address} successfully!')


while True:
    try:
        messages = redis_client.xreadgroup(
            GROUP_NAME, CONSUMER_NAME, {STREAM_NAME: ">"}, count=1, block=5000
        )

        if not messages:
            time.sleep(3)

        if messages:
            for stream, msg_list in messages:
                for msg_id, msg in msg_list:
                    logger.info(f'Processing message: {msg_id}, email: {msg["email"]}')
                    send_email(msg["email"], msg["subject"], msg["body"])
                    redis_client.xack(STREAM_NAME, GROUP_NAME, msg_id)
    except Exception as e:
        logger.error(f"Error reading message: {e}")
