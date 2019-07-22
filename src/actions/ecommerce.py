from action import Action, Router
from common_actions import ajax_complete, Navigate_Back
from helpers import Container
from utils import get_args

from scipy.stats import poisson
from scipy.stats import beta
from numpy.random import uniform

import math
import time
import importlib

from settings import SETTINGS
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

PERSONAL_INFO = {
    'First Name': 'John',
    'Last Name': 'Doe',
    'Street': '14 Gundawara St',
    'City': 'Point Cook',
    'State': 'Victoria',
    'Country': 'Australia',
    'Zip': '2229',
    'Phone': '8884852895',
    'Email': 'sample@email.com'
}


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
            pb_kwargs = {'_'.join(k.lower().split('_')[1:]) : v for k, v in SETTINGS.items() if k.startswith('PRODUCT')}
            db = Container(**pb_kwargs)
            db.gather_contents()
            contents = db.contents
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
        url = SETTINGS['TLD'] + SETTINGS['INVENTORY_URL_PREFIX'] + product_name
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
        quantity = self.quantity
        quantity_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((SETTINGS['UPDATE_QUANTITY_BY'],
                                            SETTINGS['UPDATE_QUANTITY_TEXT']))
        )
        if quantity != 1:
            quantity_element.clear()
            quantity_element.send_keys(quantity)
        else:
            pass

class Add_Item_To_Cart_From_Product_Page(Action):

    name = "Add Item To Cart From Product Page"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        add_to_cart_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((SETTINGS['ADD_TO_CART_BY'],
                                            SETTINGS['ADD_TO_CART_TEXT'])
                                           ))
        add_to_cart_btn.click()
        pass

class View_And_Add_Products_To_Cart(Action):

    name = "View And Add Products To Cart"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        user = self.user
        user_items = user.user_items
        sub_action_names = SETTINGS['SEQUENCE_VIEW_ADD_PRODUCTS']
        sub_actions = list()
        for sa in sub_action_names:
            sub_actions.append(eval(sa))
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
        default_action_route = "Redeem Coupon"
        #user_override code here
        if SETTINGS['EXPERIMENT_ACTIVE']:
            USER_EXPERIMENT_SETTINGS = user.USER_EXPERIMENT_SETTINGS
            driver = user.webdriver
            driver.execute_script('var expVar = gaData[' + '"' + SETTINGS['GA_TRACKING_ID'] + '"' + ']["experiments"];\
                                   var trtmt = expVar[Object.keys(expVar)[0]];\
                                   window.trtmt = trtmt;')
            var_idx = int(driver.execute_script('return trtmt;'))
            variant_name = USER_EXPERIMENT_SETTINGS.keys()[var_idx]
            variant_info = USER_EXPERIMENT_SETTINGS[variant_name]
            self.action_route = self._det_action(variant_info)
        else:
            self.action_route = default_action_route
        Action.__init__(self, user)
        self.user.log['variant'] = variant_name

    def _det_action(self, variant_info):
        cum = 0
        unif_rv = uniform()
        for k in variant_info:
            cum = cum + variant_info[k]
            if unif_rv < cum:
                break
        return k

    def _proc(self):
        #TODO: Possibly sub-class Action with Router?
        action_route = self.action_route
        action_class_name = action_route.replace(' ', '_')
        ecommerce_module = importlib.import_module('src.actions.ecommerce')
        Action_Class = getattr(ecommerce_module,action_class_name)
        user = self.user
        user.do(Action_Class)

class Miss_Coupon(Action):

    name = "Miss Coupon"

    def __init__(self,user):
         Action.__init__(self,user)

    def _proc(self):
        self.user.log['action'] = 'Miss Coupon'

class Redeem_Coupon(Action):

    name = "Redeem Coupon"

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
        self.user.log['action'] = "Redeem Coupon"

class Mess_Up_Coupon(Action):

    name = "Mess Up Coupon"

    def __init(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.NAME, 'coupon_code'))
        ).send_keys('notacoupon')
        WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.ID, 'apply_coupon_button'))
        ).click()
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'woocommerce-error'))
        )
        self.user.log['action'] = "Mess Up Coupon"

class Possibly_Proceed_To_Checkout(Router):

    name = "Possibly Proceed To Checkout"

    def __init__(self, user):
        Router.__init__(self, user)

class Proceed_To_Checkout(Action):

    name = "Proceed To Checkout"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        time.sleep(1)
        checkout_link_element  = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((SETTINGS['CHECKOUT_ELEMENT_BY'],
                                            SETTINGS['CHECKOUT_ELEMENT_TEXT'])))
        checkout_link_element.click()
        self.user.append_to_history(driver.current_url)

class Fill_Out_Personal_Information(Action):

    name = "Fill Out Personal Information"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        for field,id_text in SETTINGS['PERSONAL_INFO_ELEMENT_ID_MAP'].items():
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, id_text))
            ).send_keys(PERSONAL_INFO[field])
        #Country
        for letter in PERSONAL_INFO['Country']:
            choose_country = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((SETTINGS['BILLING_COUNTRY_BY']
                                               ,SETTINGS['BILLING_COUNTRY_TEXT'])))
            choose_country.send_keys(letter)
        #choose_country.send_keys("  ") #This is a bug. You have to send two spaces to get one
        #for letter in "States":
        #    choose_country.send_keys(letter)
        choose_country.send_keys(Keys.RETURN)
        #State
        for char in PERSONAL_INFO['State']:
            state_list_filter = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((SETTINGS['BILLING_STATE_FILTER_BY'],
                                                SETTINGS['BILLING_STATE_FILTER_TEXT'])))
            state_list_filter.send_keys(char)
        WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((SETTINGS['BILLING_STATE_SELECT_BY'],
                    SETTINGS['BILLING_STATE_SELECT_TEXT']))).click()

class Continue_To_Payment_Method(Action):

    name = "Continue To Payment Method"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID,'continue_button'))).click()

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

class Fill_Out_Bogus_Gateway_Details(Action):

    name = "Execute Bogus Gateway Purchase"
    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        driver.switch_to.frame(
            frame_reference=driver.find_element(By.XPATH, "//iframe[@title='Field container for: Card number']"))
        WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID,'number'))).send_keys(1)
        driver.switch_to.default_content()
        driver.switch_to.frame(
            frame_reference=driver.find_element(By.XPATH, "//iframe[@title='Field container for: Name on card']"))
        WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.NAME,'name'))).send_keys('Bogus Gateway')
        driver.switch_to.default_content()
        driver.switch_to.frame(
            frame_reference=driver.find_element(By.XPATH, "//iframe[@title='Field container for: Expiration date (MM / YY)']"))
        WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID,'expiry'))).send_keys('02/22')
        driver.switch_to.default_content()
        driver.switch_to.frame(
            frame_reference=driver.find_element(By.XPATH, "//iframe[@title='Field container for: Security code']"))
        WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID,'verification_value'))).send_keys('111')
        driver.switch_to.default_content()

class Possibly_Place_Order(Router):

    name = "Possibly Place Order"

    def __init__(self, user):
        Router.__init__(self, user)

class Place_Order(Action):

    name = "Place Order"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        time.sleep(1)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, SETTINGS['PLACE_ORDER_BUTTON_ID']))
        ).click()
        self.user.log['purchase_executed'] = 1

class Leave_After_Confirmation(Action):

    name = "Leave After Confirmation"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        WebDriverWait(driver, 10).until(
            EC.url_contains(SETTINGS['CONFIRMATION_URL_TEXT'])
        )
        self.user.append_to_history(driver.current_url)
