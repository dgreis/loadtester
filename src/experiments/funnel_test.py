from action import Action
from settings import variant_bounce_thresholds, TLD

from random import uniform
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Wait_For_Pic(Action):

    def __init__(self,user):
        Action.__init__(self,user)
        #if self.user.log['bounced'] == 1:
        #    pass
        #else:
        #    self._proc()


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

    def __init__(self,user):
        Action.__init__(self,user)
        #if self.user.log['bounced'] == 0:
        #    self._proc()
        #else:
        #    pass

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

    def __init__(self,user):
        Action.__init__(self,user)
        #self.user.log['added_to_cart'] = 0
        #if self.user.log['bounced'] == 1:
        #    pass
        #else:
        #    self._proc()

    def _record_log_values(self):
        self.user.log['added_to_cart'] = 0

    def _proc(self):
        button_element = self.user.webdriver.find_element_by_id("addtocart")
        button_element.click()
        self.user.log['added_to_cart'] = 1


class Wait_To_Claim_Gift(Action):

    def __init__(self,user):
        Action.__init__(self,user)
        #if self.user.log['bounced'] == 1:
        #    pass
        #else:
        #    self._proc()

    def _proc(self):
        driver = self.user.webdriver
        self.user.append_to_history(driver.current_url)
        try:
            assert driver.current_url.split('?')[0] == TLD + '/' + 'thankyou.html'
        except:
            pass
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "thankyou"))
            )


class Claim_Gift(Action):

    def __init__(self,user):
        Action.__init__(self,user)
        #self.user.log['claimed_gift'] = 0
        #if self.user.log['bounced'] == 1:
        #    pass
        #else:
        #    self._proc()

    def _record_log_values(self):
        self.user.log['claimed_gift'] = 0

    def _proc(self):
        button_element = self.user.webdriver.find_element_by_id("thankyou")
        button_element.click()
        self.user.log['claimed_gift'] = 1


