import time
import logging

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.common.exceptions import WebDriverException
from settings import URL, variant_list, variant_thresholds


def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")
    except WebDriverException:
        pass

class User:

    def __init__(self,user_id):
        self.user_id = user_id
        self.webdriver = webdriver.Chrome()
        #self.page = None
        self.trtmt = None
        #self.clicked = 0

        self._navigate_to_landing_page(URL)
        self._det_trtmt()

    def _navigate_to_landing_page(self,url):
        driver = self.webdriver
        driver.get(url)
        WebDriverWait(driver, 10).until(ajax_complete, "Timeout waiting for page to load")
        #print("jQuery.active: " + str(driver.execute_script("return jQuery.active")))



    def _det_trtmt(self):
        driver = self.webdriver
        driver.execute_script("var chosenVariation = cxApi.chooseVariation(); window.trtmt = chosenVariation;")
        var_idx = driver.execute_script('return trtmt;')
        self.trtmt = variant_list[var_idx]


    #    page = self.page
    #    key = page.split('8888')[1].split('?')[0]
    #    variant = variant_map[key]
    #    self.trtmt = variant

    def navigate_to_url(self,URL):
        driver = self.webdriver
        driver.get(URL) #will this update or do I need to reassign?
        self.page = driver.current_url

    def do(self,action):
        action(self)

    def log(self):
        logging.info(str(self.user_id) + ',' + self.trtmt + ',' + str(self.click_button) + ',')

    def quit(self):
        driver = self.webdriver
        driver.close()
        driver.quit()


if __name__ == "__main__":
    user = User()
    user.act()