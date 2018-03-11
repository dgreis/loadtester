import math
from pymongo import MongoClient

from src.flows.action import Action
from settings import BASKETSIZE_LAMBDA, PREFSHAPEPARAMS, SHOP_SIZE, TLD
from scipy.stats import poisson
from scipy.stats import beta

from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class Empty_Cart(Action):
    client = MongoClient()
    db = client.mongomart
    result = db.cart.delete_many({})
    assert db.cart.count() == 0

class Select_Items(Action):

    name = "Select Items"

    def __init__(self, user):
        Action.__init__(self, user)

    def _record_log_values(self):
        self.user.log['bounced'] = 0

    def _proc(self):
        driver = self.user.webdriver
        self.user.append_to_history(driver.current_url)
        num_items = poisson.rvs(BASKETSIZE_LAMBDA,1)
        self.user.log['num_items'] = num_items
        if num_items < 1:
            self.user.log['bounced'] = 1
        else:
            ALPHA,BETA = PREFSHAPEPARAMS['ALPHA'],PREFSHAPEPARAMS['BETA']
            item_ids = [int(math.floor(x)) for x in list(beta.rvs(ALPHA, BETA, size=num_items)*SHOP_SIZE)]
            self.user.log['items_chosen'] = item_ids
            self.user.item_ids = item_ids



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
                        print "Looking for item: " + str(item_id)
                        prod_btn_element = driver.find_element_by_xpath('//a[@href="/item/' + str(int(item_id)) + '"]')
                    except NoSuchElementException:
                        next_pg_btn = driver.find_element_by_xpath('//a[@href="/?page=' + str(page_num) + '&category=All"]')
                        next_pg_btn.click()
                        assert "?page=" + str(page_num) + "&category=All" in driver.current_url
                        WebDriverWait(driver, 10).until(
                            elements_have_css_class(By.CLASS_NAME, 'btn-primary')
                        )
                        page_num += 1
                        continue
                    break
                break
            prod_btn_element.click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary")) #fix this?
                )
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

    #Proceed_To_Checkout
    #Execute_Purchase
    #Leave_After_Confirmation