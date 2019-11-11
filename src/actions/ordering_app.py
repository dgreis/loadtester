from action import Action, Router
from common_actions import ajax_complete, Navigate_Back
from utils import get_args, expand_shadow_node, safe_click
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
    NoSuchElementException, ElementNotVisibleException, ElementClickInterceptedException, \
    StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
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
        ml = driver.find_element_by_xpath('/html/body/div/div[2]/layout-container/pane-left/div[2]/div/nav/menu-list')
        ml_root = driver.execute_script('return arguments[0].shadowRoot',ml)
        category_name = self.category_name
        section_headers = ml_root.find_elements_by_class_name("category-name")
        assert len(filter(lambda x: x.get_attribute('innerText') == category_name, section_headers)) > 0
        section_header = filter(lambda x: x.text == category_name, section_headers)[0]
        time.sleep(1.5)
        try:
            section_header.click()
        except ElementClickInterceptedException:
            #js = "var aa=document.getElementById('input-blocker');aa.parentNode.removeChild(aa)"
            js = "arguments[0].click();"
            driver.execute_script(js, section_header)
        item_name = self.item_name
        time.sleep(1)
        item_divs = ml_root.find_elements_by_class_name("item-name")
        chosen_item = filter(lambda x: x.get_attribute('innerText') == item_name, item_divs)[0]
        time.sleep(1.5)
        try:
            chosen_item.click()
        except ElementClickInterceptedException:
            js = "arguments[0].click();"
            driver.execute_script(js, chosen_item)


class Toa_Add_Item_To_Cart_From_Product_Page(Action):

    name = "Toa Add Item To Cart From Product Page"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((SETTINGS['ADD_TO_CART_BY'],
                                            SETTINGS['ADD_TO_CART_TEXT'])
                                           ))
        len_cart = len(driver.find_elements_by_class_name('cart-item'))
        shadow_root = expand_shadow_node(driver, driver.find_element(SETTINGS['ADD_TO_CART_BY'],SETTINGS['ADD_TO_CART_TEXT']))
        try:
            item_form_submit_button = expand_shadow_node(driver, shadow_root.find_element_by_tag_name('item-form-submit-button'))
            action_button = expand_shadow_node(driver, item_form_submit_button.find_element_by_tag_name('action-button'))
            add_button = action_button.find_element_by_class_name('button')
            safe_click(driver, add_button)
        except StaleElementReferenceException:
            shadow_root = expand_shadow_node(driver, driver.find_element(SETTINGS['ADD_TO_CART_BY'], SETTINGS['ADD_TO_CART_TEXT']))
            item_form_submit_button = expand_shadow_node(driver, shadow_root.find_element_by_tag_name('item-form-submit-button'))
            action_button = expand_shadow_node(driver, item_form_submit_button.find_element_by_tag_name('action-button'))
            add_button = action_button.find_element_by_class_name('button')
            safe_click(driver, add_button)
        #try:
        #    assert len(driver.find_elements_by_class_name('cart-item')) > len_cart
        #except AssertionError:
        #    assert 1 == 0


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
                       Toa_Add_Item_To_Cart_From_Product_Page]
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
        for i in range(4):
            shadow_root = expand_shadow_node(driver,driver.find_elements_by_class_name('cart-item')[0].find_element_by_tag_name('cart-action-buttons'))
            quantity_widget = expand_shadow_node(driver, shadow_root.find_element_by_tag_name('quantity-widget'))
            increment_button = quantity_widget.find_element_by_class_name('increment')
            safe_click(driver, increment_button)
            time.sleep(1.5)
        #driver.find_elements_by_class_name('cart-item')[2].send_keys("Remove")
        shadow_root = expand_shadow_node(driver,driver.find_elements_by_class_name('cart-item')[2].find_element_by_tag_name('cart-action-buttons'))
        trash_element = expand_shadow_node(driver, shadow_root.find_element_by_tag_name('trash-svg'))
        trash_svg = trash_element.find_element_by_tag_name('svg')
        actions = ActionChains(driver)
        actions.click(trash_svg).perform()

class Possibly_Toa_Proceed_To_Checkout(Router):

    name = "Possibly TOA Proceed To Checkout"

    def __init__(self, user):
        Router.__init__(self, user)

class Toa_Proceed_To_Checkout(Action):

    name = "Toa_Proceed To Checkout"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        time.sleep(1)
        checkout_root  = expand_shadow_node(driver,WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((SETTINGS['CHECKOUT_ELEMENT_BY'],
                                            SETTINGS['CHECKOUT_ELEMENT_TEXT']))))
        action_button_div = expand_shadow_node(driver, checkout_root.find_element_by_tag_name('action-button'))
        button = action_button_div.find_element_by_class_name('button')
        safe_click(driver, button)
        self.user.append_to_history(driver.current_url)

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
            checkout_form = expand_shadow_node(driver, WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'checkout-form'))
            ))
            checkout_form.find_element_by_id(id_text).send_keys(PERSONAL_INFO[field])
        checkout_form = expand_shadow_node(driver, WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'checkout-form'))
        ))
        action_button = expand_shadow_node(driver, checkout_form.find_elements('tag name','action-button')[1])
        pay_there_button = action_button.find_element_by_class_name('button')
        safe_click(driver, pay_there_button)

class Toa_Place_Order(Action):

    name = "Toa Place Order"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        time.sleep(1)
        checkout_form = expand_shadow_node(driver, WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'checkout-form'))))
        action_button = expand_shadow_node(driver, checkout_form.find_element_by_id('send-button-wrapper').find_element_by_tag_name('action-button'))
        send_button = action_button.find_element_by_class_name('button')
        safe_click(driver, send_button)

        self.user.log['purchase_executed'] = 1