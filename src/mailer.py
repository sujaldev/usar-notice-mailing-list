# This module deals with sending out emails to all subscribers in the mailing list.

import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To, Bcc, Subject, HtmlContent, Personalization

SENDER = "usar@xserv.dev"
SENDGRID_KEY = os.environ.get("SENDGRID_KEY")

if not os.path.isfile("data/emails.csv"):
    open("data/emails.csv", "w").close()
with open("data/emails.csv") as file:
    RECIPIENTS = list(dict.fromkeys(file.read().strip().splitlines()))


def send_notification(description: str, url: str = None) -> None:
    body = "<html><body>" + (description if url is None else f"<a href='{url}'>{description}</a>") + "</body></html>"
    subject = description[:72] + ("..." if len(description) > 72 else "")
    message = Mail(
        from_email=From(SENDER, "USAR Unofficial"),
        subject=Subject(subject),
        html_content=HtmlContent(body),
    )
    personalization = Personalization()
    personalization.add_to(To("usar@sujal.dev"))  # apparently it does not work without a `To` field
    for recipient in RECIPIENTS:
        personalization.add_bcc(Bcc(recipient))
    message.add_personalization(personalization)

    SendGridAPIClient(SENDGRID_KEY).send(message)


def send_confirmation(email_address: str, addition: bool = True) -> None:
    body = "<html><body>" \
           f"Your email address was <b>{'added to' if addition else 'removed from'}</b> USAR's unofficial mailing " \
           f"list. If this was done in error or if you wish to {'unsubscribe' if addition else 'subscribe again'}, " \
           f"you can send an email to " \
           f"<a href='mailto:usar@xserv.dev'>usar@xserv.dev</a> containing the keyword " \
           f"<em>{'remove' if addition else 'add'}</em> in the <em>subject.</em>" \
           "</body></html>"
    subject = f"You were {'added to' if addition else 'removed from'} USAR's unofficial mailing list."
    message = Mail(
        from_email=From(SENDER, "USAR Unofficial"),
        to_emails=To(email_address),
        subject=Subject(subject),
        html_content=HtmlContent(body),
    )

    SendGridAPIClient(SENDGRID_KEY).send(message)
