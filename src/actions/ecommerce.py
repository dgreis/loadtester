from action import Action
from common_actions import ajax_complete, Navigate_Back
from helpers import DB
from utils import get_args

from scipy.stats import poisson
from scipy.stats import beta

import math
import time

from settings import SETTINGS
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class Select_Items(Action):

    name = "Select Items"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        # if self.user.log['in_campaign'] == 0:
        BASKETSIZE_LAMBDA = SETTINGS['BASKETSIZE_LAMBDA']
        TEST = SETTINGS['TEST']
        if not TEST:
            num_items = poisson.rvs(BASKETSIZE_LAMBDA,1)
        else:
            num_items = 1
        self.user.log['num_items'] = num_items
        if num_items < 1:
            self.user.log['bounced'] = 1
        else:
            PREFSHAPEPARAMS = SETTINGS['PREFSHAPEPARAMS']
            SHOP_SIZE = SETTINGS['SHOP_SIZE']
            ALPHA,BETA = PREFSHAPEPARAMS['ALPHA'],PREFSHAPEPARAMS['BETA']
            user_idxs = [int(math.floor(x)) + 1 for x in list(beta.rvs(ALPHA, BETA, size=num_items)*SHOP_SIZE)]
            #self.user.log['items_chosen'] = item_ids
            #self.user.item_ids = item_ids
            db = DB()
            PRODUCT_ALIAS_QUERY = SETTINGS['PRODUCT_ALIAS_QUERY']
            db.execute_query(PRODUCT_ALIAS_QUERY)
            contents = db.query_contents
            product_ids = sorted(contents.iloc[:,0])
            try:
                user_item_ids = [product_ids[idx] for idx in user_idxs]
            except IndexError:
                assert 1 == 0
            USE_ONLY_PRODUCT_IDS = SETTINGS['USE_ONLY_PRODUCT_IDS']
            if not USE_ONLY_PRODUCT_IDS:
                product_lookup_map = dict(zip(contents.iloc[:,0], contents.iloc[:,1]))
            else:
                product_lookup_map = dict(zip(user_item_ids, user_item_ids))
            user_items = dict()
            for id in user_item_ids:
                if user_items.has_key(id):
                    user_items[id]['quant'] = user_items[id]['quant'] + 1
                else:
                    user_items[id] = {'name': product_lookup_map[id], 'quant': 1}
            self.user.user_items = user_items
        # else:
        #     self.user.log['items_chosen'] = [1,1,1,1,1]
        #     self.user.item_ids = [1,1,1,1,1]

class Navigate_To_Product_Page(Action):

    name = "Navigate To Product Page"

    def __init__(self, user, product_name):
        self.product_name = product_name
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        product_name = self.product_name
        url = SETTINGS['TLD'] + '/product/' + product_name
        driver.get(url)
        WebDriverWait(driver, 10).until(ajax_complete, "Timeout waiting for page to load")
        self.user.append_to_history(url)

class Update_Quantity_On_Product_Page(Action):

    name = "Update Quantity On Product Page"

    def __init__(self, user, quantity):
        self.quantity = quantity
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        quantity_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "quantity")))
        quantity_element.clear()
        quantity = self.quantity
        quantity_element.send_keys(quantity)

class Add_Item_To_Cart_From_Product_Page(Action):

    name = "Add Item To Cart From Product Page"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        add_to_cart_btn = driver.find_element_by_name("add-to-cart")
        add_to_cart_btn.click()

class View_And_Add_Products_To_Cart(Action):

    name = "View And Add Products To Cart"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        user = self.user
        user_items = user.user_items
        sub_actions = [ Navigate_To_Product_Page
                       ,Update_Quantity_On_Product_Page
                       ,Add_Item_To_Cart_From_Product_Page
                       ,Navigate_Back
                      ]
        for id in user_items:
            product_name = user_items[id]['name']
            quantity = user_items[id]['quant']
            for sub_action in sub_actions:
                additional_args = filter( lambda x: x != 'user', get_args(sub_action, '__init__'))
                kwargs = dict([(k,locals()[k]) for k in additional_args])
                user.do(sub_action, **kwargs)

class View_Cart(Action):

    name = "View Cart"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Cart'))
        ).click()

class Possibly_Redeem_Coupon(Action):

    name = "Possibly Redeem Coupon"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        hidden_coupon = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID, "hidden-coupon"))
        ).text
        WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.NAME, 'coupon_code'))
        ).send_keys(hidden_coupon)
        WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.ID, 'apply_coupon_button'))
        ).click()
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'woocommerce-message'))
        )

class Proceed_To_Checkout(Action):

    name = "Proceed To Checkout"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        checkout_link_element  = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Checkout")))
        checkout_link_element.click()
        self.user.append_to_history(driver.current_url)

class Fill_Out_Personal_Information(Action):

    name = "Fill Out Personal Information"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        #First Name
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'billing_first_name'))
        ).send_keys('John')
        #Last Name
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'billing_last_name'))
        ).send_keys('Doe')
        for letter in "United":
            choose_country = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'select2-selection')))
            choose_country.send_keys(letter)
            driver
        choose_country.send_keys("  ") #This is a bug. You have to send two spaces to get one
        for letter in "States":
            choose_country.send_keys(letter)
        choose_country.send_keys(Keys.RETURN)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'billing_address_1'))
        ).send_keys("426 Evergreen Terrace")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'billing_city'))
        ).send_keys("Ojai")
        state_list_filter = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[@aria-labelledby="select2-billing_state-container"]')))
        state_list_filter.send_keys("California")
        WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                    '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'billing_postcode'))
        ).send_keys("93023")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'billing_phone'))
        ).send_keys("8885554582")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'billing_email'))
        ).send_keys("sample@email.com")

class Fill_Out_Stripe_CC_Details(Action):

    name = "Execute Stripe Purchase"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        assert 'checkout' in driver.current_url

        time.sleep(2)
        driver.switch_to.frame(
            frame_reference=driver.find_element(By.XPATH, '//iframe[@name="__privateStripeFrame8"]'))
        #Card Number
        for char in '4242424242424242':
            card_number = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME,'cardnumber'))
            )
            card_number.send_keys(char)
            time.sleep(.1)
        driver.switch_to.default_content()
        #ExpDate
        driver.switch_to.frame(
            frame_reference=driver.find_element(By.XPATH, '//iframe[@name="__privateStripeFrame9"]'))
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'exp-date'))
        ).send_keys('0221')
        driver.switch_to.default_content()
        #CVC
        driver.switch_to.frame(
            frame_reference=driver.find_element(By.XPATH, '//iframe[@name="__privateStripeFrame10"]'))
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'cvc'))
        ).send_keys('343')
        driver.switch_to.default_content()

class Place_Order(Action):

    name = "Place Order"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'place_order'))
        ).click()
        self.user.log['purchase_executed'] = 1


class Leave_After_Confirmation(Action):

    name = "Leave After Confirmation"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        WebDriverWait(driver, 10).until(
            EC.url_contains('order-received')
        )
        self.user.append_to_history(driver.current_url)
