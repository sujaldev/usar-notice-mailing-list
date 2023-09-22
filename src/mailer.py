# This module deals with sending out emails to all subscribers in the mailing list.

import os
import smtplib
from email.mime.text import MIMEText

SENDER = "usar.unofficial@gmail.com"
PASSWORD = os.environ.get("PASSWORD")

if not os.path.isfile("data/emails.csv"):
    open("data/emails.csv", "w").close()
with open("data/emails.csv") as file:
    RECIPIENTS = list(dict.fromkeys(file.read().strip().splitlines()))


def send_notification(description: str, url: str = None) -> None:
    body = description if url is None else f"<a href='{url}'>{description}</a>"
    msg = MIMEText(f"<html><body>{body}</body></html>", "html")
    msg['Subject'] = description[:72] + ("..." if len(description) > 72 else "")
    msg['From'] = f"USAR Unofficial <{SENDER}>"
    msg['Bcc'] = ', '.join(RECIPIENTS)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.send_message(msg)


def send_confirmation(email_address: str, addition: bool = True) -> None:
    body = f"Your email address was <b>{'added to' if addition else 'removed from'}</b> USAR's unofficial mailing " \
           f"list. If this was done in error or if you wish to {'unsubscribe' if addition else 'subscribe again'}, " \
           f"you can send an email to " \
           f"<a href='mailto:usar.unofficial@gmail.com'>usar.unofficial@gmail.com</a> containing the keyword " \
           f"<em>{'remove' if addition else 'add'}</em> in the <em>subject.</em>"
    msg = MIMEText(f"<html><body>{body}</body></html>", "html")
    msg['Subject'] = f"You were {'added to' if addition else 'removed from'} USAR's unofficial mailing list."
    msg['From'] = f"USAR Unofficial <{SENDER}>"
    msg['To'] = email_address

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.send_message(msg)
