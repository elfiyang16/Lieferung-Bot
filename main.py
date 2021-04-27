import smtplib
import ssl
import schedule
import time
import os
import io
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from PIL import Image


email = config("EMAIL")
pwd = config("PASSWORD")
PATH = os.path.join("/Users/elfi/elfi/Lieferung-Bot/chromedriver")

# global vars
grocery_url = "https://www.tesco.com/groceries/en-GB/slots/delivery"


def init(grocery_url):
    print("Preparing the Tesco Delivery Bot==========")
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--force-device-scale-factor = 1.5")

    options.add_argument("window-size=1920x1080")
    browser = webdriver.Chrome(options=options, executable_path=PATH, service_args=[
        "--log-path=./Logs/chrome.log"])
    # browser.maximize_window()
    browser.execute_script("window.scrollTo(50,200)")
    # browser.execute_script('document.body.style.zoom = "30%"')

    browser.get(grocery_url)
    return browser


def login(browser):
    username_field = browser.find_element_by_id("username")
    username_field.send_keys(email)
    pwd_field = browser.find_element_by_id('password')
    pwd_field.send_keys(pwd)

    login_btn = browser.find_element_by_class_name("ui-component__button")
    login_btn.click()
    print("Your bot is logged in=============\n")


def check_slots(browser):
    browser.implicitly_wait(15)
    change_slot_type_xpath = "//*[@class='group-selector--container']//*[@class='group-selector--list-item'][2]//a"
    screenshot_path = "//*[@id = 'slot-matrix']"
    change_slot_type = browser.find_element(By.XPATH, change_slot_type_xpath)
    change_slot_type.click()
    time.sleep(10)
    screenshot_el = browser.find_element(By.XPATH, screenshot_path)

    for tab in range(1, 4):
        tab_path = f"//*[@id= 'slot-matrix']//ul[@class = 'tabs-header-container']/li[{tab}]"
        tab_path_clickable = f"//*[@id= 'slot-matrix']//ul[@class = 'tabs-header-container']/li[{tab}]"

        try:
            clickable_tab = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, tab_path)))
            tab_title = clickable_tab.find_element_by_xpath(
                ".//a").get_attribute('innerHTML')
            clickable_tab.click()
            browser.implicitly_wait(25)
            image = screenshot_el.screenshot_as_png
            imageStream = io.BytesIO(image)
            im = Image.open(imageStream)
            im.save(f"Tesco-{tab_title}.png")
            # or without the Pillow package:
            # with open("element.png", "wb") as elem_file:
            #     elem_file.write(button_element.screenshot_as_png)

            # browser.get_screenshot_as_file(f"Tesco-{tab_title}.png")
            # driver.save_screenshot(‘/ Screenshots/foo.png’)
            time.sleep(2)
        except Exception as e:
            print(e)
            print(f"{tab_title} does not respond")

    available_times = ['09:00 - 13:00', '10:00 - 14:00', '11:00 - 15:00', '12:00 - 16:00',
                       '13:00 - 17:00', '14:00 - 18:00', '15:00 - 19:00', '16:00 - 20:00', '17:00 - 21:00',
                       '18:00 - 22:00']

    # for slot in available_times:
    #     book(slot, browser)

    print("I'm going to wait before I close the window")
    time.sleep(10)


def book(slot, browser):

    available_slots = get_available_slots(browser, slot)
    preferred_slot = None

    # try:
    #     preferred_slot = browser.find_element(By.XPATH, preferred_slot_xpath)
    # except:
    #     print('No slot for: ', slot)

    # if preferred_slot:
    #     print(preferred_slot.get_attribute("innerHTML"))
    # preferred_slot.click()
    # send_email()
    # return


def get_available_slots_screenshots(browser, slot):
    slot_list_xpath = "//*[@id='slot-matrix']/div[3]/div[2]/div/div/div[1]/div[@class='slot-list']/ul"

    available_slot_items_path = "//*[@id='slot-matrix']/div[3]/div[2]/div/div/div[1]/div[2]/ul/li[@class='slot-list--item available']"

    available_slot_items = browser.find_elements_by_xpath(
        available_slot_items_path)
    for item in available_slot_items:
        available_slot_item_time = item.find_element_by_xpath(
            ".//span[@class='slot-list--times']").get_attribute('innerHTML')
        print("available_slot_item_time", available_slot_item_time)

    # return "//table[@class='slot-grid__table'][1]//th[contains(.,'" + slot + "')]/following-sibling::td//*[@class='slot-grid--item available slot-grid--item-oop808']//button"


def main():
    browser = init(grocery_url)
    login(browser)
    check_slots(browser)


if __name__ == "__main__":
    main()
