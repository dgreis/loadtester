from action import Action
from settings import variant_bounce_thresholds, TLD

from random import uniform
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Wait_For_Pic(Action):

    name = "Wait For Pic"

    def __init__(self,user):
        Action.__init__(self,user)

    def _proc(self):
        driver = self.user.webdriver
        self.user.append_to_history(driver.current_url)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "default_image"))
        )
        try:
            assert self.user.webdriver.current_url == TLD + '/' + 'conversion.html'
        except:
            pass


class Possibly_Bounce(Action):

    name = "Possibly Bounce"

    def __init__(self,user):
        Action.__init__(self,user)

    def _proc(self):
        assert self.user.webdriver.current_url == TLD + '/' + 'conversion.html'
        trtmt = self.user.trtmt
        prob = uniform(0, 1)
        thresh = variant_bounce_thresholds[trtmt]
        if prob <= thresh:
            self.user.log['bounced'] = 1
        else:
            pass

class Click_Add_To_Cart(Action):

    name = "Click Add To Cart"

    def __init__(self,user):
        Action.__init__(self,user)

    def _record_log_values(self):
        self.user.log['added_to_cart'] = 0

    def _proc(self):
        button_element = self.user.webdriver.find_element_by_id("addtocart")
        button_element.click()
        self.user.log['added_to_cart'] = 1


class Wait_To_Claim_Gift(Action):

    name = "Wait To Claim Gift"

    def __init__(self,user):
        Action.__init__(self,user)

    def _proc(self):
        driver = self.user.webdriver
        self.user.append_to_history(driver.current_url)
        assert driver.current_url.split('?')[0] == TLD + '/' + 'thankyou.html'
        #WebDriverWait(driver, 10).until(
        #    EC.element_to_be_clickable((By.ID, "thankyou"))
        #    )
        try:
            WebDriverWait(driver, 10).until(gtm_loaded, "Timeout waiting for gtm to load")
        except TimeoutException:
            print driver.get_log('browser')
            raise Exception


def gtm_loaded(driver):
    try:
        return True == driver.execute_script('return google_tag_manager.dataLayer["gtmLoad"];')
    except WebDriverException:
        pass
        #    print "Got here "


class Claim_Gift(Action):

    name = "Claim Gift"

    def __init__(self,user):
        Action.__init__(self,user)

    def _record_log_values(self):
        self.user.log['claimed_gift'] = 0

    def _proc(self):
        button_element = self.user.webdriver.find_element_by_id("thankyou")
        button_element.click()
        self.user.log['claimed_gift'] = 1


