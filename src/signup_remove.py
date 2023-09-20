import os
import imaplib
import email

EMAIL = "usar.unofficial@gmail.com"
PASSWORD = os.environ.get("PASSWORD")

with imaplib.IMAP4_SSL("imap.gmail.com") as imap:
    imap.login(EMAIL, PASSWORD)
    status, _ = imap.select("INBOX")
    assert status == "OK"
    status, uids = imap.search(None, "(UNSEEN)")
    assert status == "OK"

    for uid in uids[0].decode().split():
        status, mail = imap.fetch(uid, "(RFC822)")
        assert status == "OK"

        mail = email.message_from_bytes(mail[0][1])
        sender, operation = mail.get("From"), mail.get("Subject").lower()
        if "<" in sender:
            sender = sender.split("<")[1][:-1]
        imap.store(uid, "+X-GM-LABELS", "\\Trash")

        with open("emails.csv", "r+") as file:
            emails = list(dict.fromkeys(file.read().splitlines()))
            if sender not in emails and "add" in operation:
                emails.append(sender)
            elif sender in emails and "remove" in operation:
                emails.remove(sender)
            file.seek(0)
            file.truncate()
            file.writelines("\n".join(emails) + "\n")
