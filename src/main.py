from os.path import isfile
from typing import Tuple

from scraper import fetch_notifications
from mailer import send_notification

LAST_COUNT_FILE = "last_count.csv"


def check_new_notifications() -> Tuple[bool, dict[str, str]]:
    """
    Returns a boolean to indicate whether there are new notifications or not, along with the dictionary containing new
    notifications if any.
    """
    notifications = fetch_notifications()

    # On initialization, we'll assume we've already sent out emails for all existing notifications because assuming
    # otherwise would just spam the mailing list subscribers.
    if not isfile(LAST_COUNT_FILE):
        with open(LAST_COUNT_FILE, "w") as file:
            file.write(str(len(notifications)))
        return False, {}

    with open(LAST_COUNT_FILE, "r+") as file:
        last_count = int(file.read())
        new_count = len(notifications)

        assert new_count >= last_count
        if new_count == last_count:
            return False, {}

        file.seek(0)
        file.write(str(new_count))
        return True, dict(list(notifications.items())[:new_count - last_count])


def main():
    new_notifications, notifications = check_new_notifications()
    if new_notifications:
        for description, url in notifications:
            send_notification(description, url)


if __name__ == "__main__":
    main()
