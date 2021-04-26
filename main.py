import smtplib
import ssl
import schedule
import time
import os
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

email = config("EMAIL")
pwd = config("PASSWORD")
PATH = os.path.join("/Users/elfi/elfi/Lieferung-Bot/chromedriver")

# global vars
grocery_url = "https://www.tesco.com/groceries/en-GB/slots/delivery"


def init(grocery_url):
    print("Preparing the Tesco Delivery Bot==========")
    browser = webdriver.Chrome(PATH)
    browser.maximize_window()
    browser.get(grocery_url)
    return browser


def login(browser):
    username_field = browser.find_element_by_id("username")
    username_field.send_keys(email)
    pwd_field = browser.find_element_by_id('password')
    pwd_field.send_keys(pwd)
    print("pwd", pwd)

    login_btn = browser.find_element_by_class_name("ui-component__button")
    login_btn.click()
    print("Your bot is logged in=============\n")


def check_slots(browser):
    browser.implicitly_wait(15)
    change_slot_type_xpath = "//*[@class='group-selector--container']//*[@class='group-selector--list-item'][2]//a"
    change_slot_type = browser.find_element(By.XPATH, change_slot_type_xpath)
    print("Changed slot: ", change_slot_type.get_attribute("innerHTML"))
    change_slot_type.click()
    time.sleep(10)

    last_tab_xpath = "//*[@id='slot-matrix']//ul[@class='tabs-header-container']/li[3]"

    try:
        clickable_slot = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, last_tab_xpath)))
        clickable_slot.click()
        time.sleep(2)
    except:
        print("I didn't have what to click")

    available_times = ['09:00 - 13:00', '08:00 - 12:00', '10:00 - 14:00', '11:00 - 15:00', '12:00 - 16:00',
                       '13:00 - 17:00', '14:00 - 18:00', '15:00 - 19:00', '16:00 - 20:00', '17:00 - 21:00',
                       '18:00 - 22:00', '19:00 - 23:00']

    for slot in available_times:
        book(slot, browser)

    print("I'm going to wait before I close the window")
    time.sleep(20)


def book(slot, browser):
    preferred_slot_xpath = get_slot_path(slot)
    preferred_slot = None

    try:
        preferred_slot = browser.find_element(By.XPATH, preferred_slot_xpath)
    except:
        print('No slot for: ', slot)

    if preferred_slot:
        print(preferred_slot.get_attribute("innerHTML"))
        # preferred_slot.click()
        # send_email()
        # return


def get_slot_path(slot):
    return "//table[@class='slot-grid__table'][1]//th[contains(.,'" + slot + "')]/following-sibling::td//*[@class='slot-grid--item available slot-grid--item-oop808']//button"


def main():
    browser = init(grocery_url)
    login(browser)
    check_slots(browser)


if __name__ == "__main__":
    main()
