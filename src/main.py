import os
import logging
from time import sleep

from mailer import send_notification
from scraper import fetch_new_notifications


def main():
    has_new, notifications = fetch_new_notifications()
    if has_new:
        for description, url in notifications.items():
            send_notification(description, url)


if __name__ == "__main__":
    while True:
        try:
            main()
            sleep(int(os.getenv("INTERVAL", 300)))
        except Exception as e:
            logging.error(e)
