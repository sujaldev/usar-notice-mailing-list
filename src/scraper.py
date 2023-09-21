"""
This module deals with scrapping the university website to check for new notifications, if there exist new ones, it
extracts the description and the URL (can be None) for all new entries to a dict. It does so by keeping count of how
many notifications it saw during the last check and compares that to the number of notifications currently present.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

URL = "https://sites.google.com/view/ggsipuedc/notice-board"
IFRAME_XPATH = "/html/body/div[1]/div/div[2]/div[3]/div/div[1]/section[6]/div[2]/div/div/div/div/div[2]//iframe"
ANCHOR_XPATH = "/html/body/table/tbody[2]/tr/td[2]/a"


def fetch_notifications() -> dict[str, str]:
    driver = webdriver.Remote("http://selenium:4444", options=webdriver.ChromeOptions())
    driver.get(URL)

    try:
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, IFRAME_XPATH)))
    finally:
        driver.switch_to.frame(driver.find_element(By.XPATH, IFRAME_XPATH))
        driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe"))
        driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe"))
        notifications = {
            elem.get_attribute("innerText").strip(): elem.get_attribute("href") for elem in
            driver.find_elements(By.XPATH, ANCHOR_XPATH)
        }
        driver.quit()

    return notifications


if __name__ == "__main__":
    print(fetch_notifications())
