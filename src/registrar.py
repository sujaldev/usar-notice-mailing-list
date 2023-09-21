"""
This module handles all the registration/removal logic for subscribers of the mailing list. Anyone sending an email to
the address "usar.unofficial@gmail.com" with "add" anywhere in the subject of the email (case-insensitive), will be
added to the mailing list. For removals, the keyword is "remove". This approach is simple, convenient and deals with
authentication automatically (because if someone can send out emails from your address, you've got bigger problems :).
"""

import os
import email
import imaplib

EMAIL = "usar.unofficial@gmail.com"
PASSWORD = os.environ.get("PASSWORD")
CSV_PATH = "data/emails.csv"


def process_registrations_and_removals():
    with imaplib.IMAP4_SSL("imap.gmail.com") as imap:
        imap.login(EMAIL, PASSWORD)
        status, _ = imap.select("INBOX")
        assert status == "OK"

        status, uids = imap.search(None, "(UNSEEN)")
        assert status == "OK"

        uids = uids[0].decode().split()
        for uid in uids:
            status, mail = imap.fetch(uid, "(RFC822)")
            assert status == "OK"

            mail = email.message_from_bytes(mail[0][1])
            sender, operation = mail.get("From"), mail.get("Subject").lower()
            if "<" in sender:
                sender = sender.split("<")[1][:-1]

            # Moving to trash instead of deleting to keep a log and recover if errors occur.
            imap.store(uid, "+X-GM-LABELS", "\\Trash")

            with open(CSV_PATH) as file:
                emails = [e for e in dict.fromkeys(file.read().strip().splitlines()) if e]
                if sender not in emails and "add" in operation:
                    emails.append(sender)
                elif sender in emails and "remove" in operation:
                    emails.remove(sender)

            with open(CSV_PATH, "w") as file:
                file.write("\n".join(emails) + "\n")
