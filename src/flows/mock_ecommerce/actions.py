import math
import time
import numpy as np
from pymongo import MongoClient

from src.flows.action import Action
from src.flows.common_actions import ajax_complete
from settings import BASKETSIZE_LAMBDA, PREFSHAPEPARAMS, SHOP_SIZE, CAMPAIGN_PROP, CAMPAIGN_BOUNCE_PROB
from scipy.stats import poisson
from scipy.stats import beta
from scipy.stats import uniform

from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Navigate_To_Landing_Page(Action):

    name = "Navigate To Landing Page"

    def __init__(self, user):
        Action.__init__(self, user)

    def _record_log_values(self):
        self.user.log['in_campaign'] = 0
        self.user.log['bounced'] = 0

    def _proc(self):
        driver = self.user.webdriver
        url = self.user.landing_page
        driver.get(url)
        #WebDriverWait(driver, 10).until(ajax_complete, "Timeout waiting for page to load")
        self.user.append_to_history(url)
        in_campaign = uniform.rvs(size=1)[0]
        if in_campaign < CAMPAIGN_PROP:
            camp_btn = driver.find_element_by_xpath('''//*[text() = 'Click Here For Campaign']''')
            camp_btn.click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '''//*[text() = 'MongoMart']'''))  # Should follow this
            )
            self.user.log['in_campaign'] = 1
            if uniform.rvs(size=1)[0] < CAMPAIGN_BOUNCE_PROB:
                self.user.log['bounced'] = 1
            else:
                pass
        else:
            driver.get("http://localhost:3000")
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '''//*[text() = 'MongoMart']'''))  # Should follow this
            )
        self.user.append_to_history(driver.current_url)

class Empty_Cart(Action):

    name = "Empty Cart"

    def __init__(self, user):
        Action.__init__(self, user)

    def _record_log_values(self):
        self.user.log['empty_cart_start'] = 0

    def _proc(self):
        client = MongoClient()
        db = client.mongomart
        result = db.cart.delete_many({})
        assert db.cart.count() == 0
        self.user.log['empty_cart_start'] = 1

class Select_Items(Action):

    name = "Select Items"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        if self.user.log['in_campaign'] == 0:
            num_items = poisson.rvs(BASKETSIZE_LAMBDA,1)
            self.user.log['num_items'] = num_items
            if num_items < 1:
                self.user.log['bounced'] = 1
            else:
                ALPHA,BETA = PREFSHAPEPARAMS['ALPHA'],PREFSHAPEPARAMS['BETA']
                item_ids = [int(math.floor(x)) + 1 for x in list(beta.rvs(ALPHA, BETA, size=num_items)*SHOP_SIZE)]
                self.user.log['items_chosen'] = item_ids
                self.user.item_ids = item_ids
        else:
            self.user.log['items_chosen'] = [1,1,1,1,1]
            self.user.item_ids = [1,1,1,1,1]



class Add_Items_To_Cart(Action):

    name = "Add Items To Cart"

    def __init__(self, user):
        Action.__init__(self, user)

    def _record_log_values(self):
        self.user.log['items_added'] = []

    def _proc(self):
        driver = self.user.webdriver
        self.user.append_to_history(driver.current_url)
        item_ids = self.user.item_ids

        for item_id in item_ids:
            for i in range(0, 100):
                page_num = 1
                while True:
                    try:
                        #print "Looking for item: " + str(item_id)
                        prod_btn_element = driver.find_element_by_xpath('//a[@href="/item/' + str(int(item_id)) + '"]')
                    except NoSuchElementException:
                        next_pg_btn = driver.find_element_by_xpath('//a[@href="/?page=' + str(page_num) + '&category=All"]')
                        next_pg_btn.click()
                        assert "?page=" + str(page_num) + "&category=All" in driver.current_url
                        WebDriverWait(driver, 10).until(
                            elements_have_css_class(By.CLASS_NAME, 'btn-primary')
                        )
                        self.user.append_to_history(driver.current_url)
                        page_num += 1
                        continue
                    break
                break
            prod_btn_element.click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary")) #fix this?
                )
            self.user.append_to_history(driver.current_url)
            assert 'item' in driver.current_url
            self.user.append_to_history(driver.current_url)
            add_btn_element = driver.find_element_by_class_name("btn-primary")
            add_btn_element.click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "navbar-brand"))
                )
            self.user.log['items_added'].append(item_id)
            self.user.append_to_history(driver.current_url)
            home_btn_element = driver.find_element_by_class_name("navbar-brand")
            home_btn_element.click()

class elements_have_css_class(object):
  """An expectation for checking that an element has a particular css class.

  locator - used to find the element
  returns the WebElement once it has the particular css class
  """
  def __init__(self, locator, css_class):
    self.locator = locator
    self.css_class = css_class

  def __call__(self, driver):
    #element = driver.find_element(*self.locator)   # Finding the referenced element
    elements = driver.find_elements(self.locator, self.css_class)
    #if self.css_class in element.get_attribute("class"):
    #    return element
    #else:
    #    return False
    return elements

class Proceed_To_Checkout(Action):

    name = "Proceed To Checkout"

    def __init__(self, user):
        Action.__init__(self, user)

    def _record_log_values(self):
        self.user.log['checked_out'] = 0

    def _proc(self):
        driver = self.user.webdriver
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,'//a[@href="/cart"]')) #Should follow this
        )
        self.user.append_to_history(driver.current_url)
        btn_success_element = driver.find_element_by_xpath('//a[@href="/cart"]')
        btn_success_element.click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,'''//*[text() = 'Proceed to Checkout']''')) #Should follow this
        )
        self.user.append_to_history(driver.current_url)
        self._assert_correct_cart()
        checkout_btn = driver.find_element_by_xpath('''//*[text() = 'Proceed to Checkout']''')
        checkout_btn.click()

    def _assert_correct_cart(self):
        target_items = self.user.item_ids
        client = MongoClient()
        db = client.mongomart
        cart_items = []
        cart = list(db.cart.find())[0]['items']
        for dict in cart:
            cart_items.append(np.repeat(dict['_id'],dict['quantity']).tolist())
        flat_cart_items = [item for sublist in cart_items for item in sublist]
        assert str(sorted(target_items)) == str(sorted(flat_cart_items))


class Execute_Purchase(Action):

    name = "Execute Purchase"

    def __init__(self, user):
        Action.__init__(self, user)

    def _record_log_values(self):
        self.user.log['purchase_executed'] = 0

    def _proc(self):
        driver = self.user.webdriver
        assert 'checkout' in driver.current_url
        self.user.append_to_history(driver.current_url)
        card_number = driver.find_element_by_id('card-number')
        card_number.send_keys('2314 2414 2325 2345')
        card_holder = driver.find_element_by_id('card-holder')
        card_holder.send_keys("John Doe")
        card_month = driver.find_element_by_id('card-month')
        card_month.send_keys('02')
        card_year = driver.find_element_by_id('card-year')
        card_year.send_keys('19')
        card_cvc = driver.find_element_by_id('card-cvc')
        card_cvc.send_keys('343')
        card_btn = driver.find_element_by_id('card-btn')
        card_btn.click()
        self.user.log['purchase_executed'] = 1
        time.sleep(1)

class Leave_After_Confirmation(Action):

    name = "Leave After Confirmation"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,'//a[@href="https://bootstrapcreative.com/"]'))
        )
        self.user.append_to_history(driver.current_url)
        assert 'confirmation' in driver.current_url