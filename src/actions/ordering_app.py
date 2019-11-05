from action import Action, Router
from common_actions import ajax_complete, Navigate_Back
from utils import get_args
from ecommerce import Add_Item_To_Cart_From_Product_Page

from scipy.stats import poisson
from scipy.stats import beta
from numpy.random import uniform

import math
import time
import importlib

from settings import SETTINGS
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException, \
    NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


PERSONAL_INFO = {
    'Name': 'John Doe',
    'Phone Number': '8479450777',
    'Email': 'daviddoesdatainc@gmail.com'
}

class Choose_Item(Action):

    name = "Choose Item"

    def __init__(self, user, category_name, item_name):
        self.category_name = category_name
        self.item_name = item_name
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID, 'menu-list'))
        )
        category_name = self.category_name
        #driver.refresh()
        #print "refreshed"
        # section_header = WebDriverWait(driver, 10).until(
        #         EC.element_to_be_clickable(('xpath',
        #                                     "//*[contains(text(), '" + category_name + "')]"))
        # )
        section_headers = driver.find_elements_by_class_name("section-title")
        try:
            assert len(filter(lambda x: x == category_name, section_headers)) > 0
        except AssertionError:
            pass
        section_header = filter(lambda x: x.text == category_name, section_headers)[0]
        #section_header = driver.find_element_by_xpath("//*[contains(text(), '" + category_name + "')]")
        time.sleep(1.5)
        try:
            section_header.click()
        except ElementNotVisibleException:
            #js = "var aa=document.getElementById('input-blocker');aa.parentNode.removeChild(aa)"
            js = "arguments[0].click();"
            driver.execute_script(js, section_header)
        item_name = self.item_name
        time.sleep(1)
        driver.find_element_by_link_text(item_name).click()
        section_headers = driver.find_elements_by_class_name("section-title")
        try:
            assert len(filter(lambda x: x == category_name, section_headers))
        except AssertionError:
            pass
        section_header = filter(lambda x: x.text == category_name, section_headers)[0]
        time.sleep(1.5)
        section_header.click()

class Possibly_Add_Menu_Items_To_Cart(Router):

    name = "Possibly Add Menu Items To Cart"

    def __init__(self, user):
        Router.__init__(self, user)

class Add_Menu_Items_To_Cart(Action):

    name = "Add Menu Items To Cart"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        user = self.user
        sub_actions = [Choose_Item,
                       Add_Item_To_Cart_From_Product_Page]
        menu_items = SETTINGS['MENU_ITEMS']
        for cat_item in menu_items:
            category_name = cat_item[0]
            item_name = cat_item[1]
            for sub_action in sub_actions:
                additional_args = filter( lambda x: x != 'user', get_args(sub_action, '__init__'))
                kwargs = dict([(k,locals()[k]) for k in additional_args])
                user.do(sub_action, **kwargs)

class Possibly_Adjust_Cart(Router):

    name = "Possibly Adjust Cart"

    def __init__(self, user):
        Router.__init__(self, user)

class Adjust_Cart(Action):

    name = "Adjust Cart"

    def __init__(self, user):
        Action.__init__(self, user)


    def _proc(self):
        driver = self.user.webdriver
        driver.find_elements_by_class_name('cart-qty')[0].send_keys(5)
        time.sleep(1)
        driver.find_elements_by_class_name('cart-qty')[2].send_keys("Remove")

class Possibly_Fill_In_Ordering_App_Payment_Details(Router):

    name = "Possibly Fill In Ordering App Payment Details"

    def __init__(self, user):
        Router.__init__(self, user)

class Fill_In_Ordering_App_Payment_Details(Action):

    name = "Ordering App Fill Out Personal Information"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        for field,id_text in SETTINGS['PERSONAL_INFO_ELEMENT_ID_MAP'].items():
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME,id_text))
            ).send_keys(PERSONAL_INFO[field])
        driver.switch_to.frame(
            frame_reference=driver.find_element(By.XPATH, '//iframe[@name="__privateStripeFrame5"]'))
        # Card Number
        for char in '4242424242424242':
            card_number = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, 'cardnumber'))
            )
            card_number.send_keys(char)
            time.sleep(.1)
        #driver.switch_to.default_content()
        # ExpDate
        #driver.switch_to.frame(
        #    frame_reference=driver.find_element(By.XPATH, '//iframe[@name="__privateStripeFrame9"]'))
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'exp-date'))
        ).send_keys('1225')
        #driver.switch_to.default_content()
        # CVC
        #driver.switch_to.frame(
        #    frame_reference=driver.find_element(By.XPATH, '//iframe[@name="__privateStripeFrame10"]'))
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'cvc'))
        ).send_keys('123')
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'postal'))
        ).send_keys('12345')
        driver.switch_to.default_content()

class Possibly_Pay_There_Ordering_App(Router):

    name = "Possibly Pay There Ordering App"

    def __init__(self, user):
        Router.__init__(self, user)


class Pay_There_Ordering_App(Action):

    name = "Pay There Ordering App"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        for field,id_text in SETTINGS['PERSONAL_INFO_ELEMENT_ID_MAP'].items():
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME,id_text))
            ).send_keys(PERSONAL_INFO[field])
        radio_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'pay_online_False'))
        )
        driver.execute_script("arguments[0].click();", radio_button)