"""
This module deals with scrapping the university website to check for new notifications, if there exist new ones, it
extracts the description and the URL (can be None) for all new entries to a dict. It does so by keeping count of how
many notifications it saw during the last check and compares that to the number of notifications currently present.
"""

import os
from io import StringIO
from typing import Tuple
from urllib.request import urlopen

from lxml import html
from lxml.etree import XPath

GENERAL_URL = "https://sites.google.com/view/ggsipuedc/notice-board"
EXAMINATION_URL = "https://sites.google.com/view/ggsipuedc/examinations/examination-notices"
LAST_COUNT_FILE = "data/last_count.csv"


def fetch_notifications(url) -> dict[str, str]:
    # Returns a dictionary containing notification descriptions as the key, and it's corresponding URL as the value.
    data_code = html.parse(urlopen(url)).xpath("//@data-code")[0]
    anchors = XPath("//tbody/tr/td[2]/a")(html.parse(StringIO(data_code)))
    return {anchor.text.strip(): anchor.get("href") for anchor in anchors}


def fetch_new_notifications() -> Tuple[bool, dict[str, str]]:
    gen_notifs, exam_notifs = fetch_notifications(GENERAL_URL), fetch_notifications(EXAMINATION_URL)
    new_gen_count, new_exam_count = len(gen_notifs), len(exam_notifs)

    # On initialization, we'll assume we've already sent out emails for all existing notifications because assuming
    # otherwise would just spam the mailing list subscribers.
    if not os.path.isfile(LAST_COUNT_FILE):
        with open(LAST_COUNT_FILE, "w") as file:
            file.write(f"{new_gen_count},{new_exam_count}")
        return False, {}

    with open(LAST_COUNT_FILE) as file:
        last_gen_count, last_exam_count = [int(count) for count in file.read().strip().split(",")]

    assert (new_gen_count >= last_gen_count) and (new_exam_count >= last_exam_count)

    with open(LAST_COUNT_FILE, "w") as file:
        file.write(f"{new_gen_count},{new_exam_count}")

    return (
        (new_gen_count > last_gen_count) or (new_exam_count > last_exam_count),
        dict(list(gen_notifs.items())[:new_gen_count - last_gen_count]) |
        dict(list(exam_notifs.items())[:new_exam_count - last_exam_count])
    )


if __name__ == "__main__":
    has_new, notifications = fetch_new_notifications()
    if has_new:
        for description, link in notifications.items():
            print(f"{description} : '{link}'")
