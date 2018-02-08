import logging

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.common.exceptions import WebDriverException
from settings import TLD, variant_list


def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")
    except WebDriverException:
        pass

class User:

    def __init__(self,user_id):
        self.user_id = user_id
        self.webdriver = webdriver.Chrome()
        self.trtmt = None
        self.log = dict()
        self.browser_history = list()


        self._navigate_to_landing_page(TLD)
        self._det_trtmt()

    def _navigate_to_landing_page(self,url):
        driver = self.webdriver
        driver.get(url)
        WebDriverWait(driver, 10).until(ajax_complete, "Timeout waiting for page to load")
        #print("jQuery.active: " + str(driver.execute_script("return jQuery.active")))
        self.append_to_history(url)


    def _det_trtmt(self):
        driver = self.webdriver
        driver.execute_script("var chosenVariation = cxApi.chooseVariation(); window.trtmt = chosenVariation;")
        var_idx = driver.execute_script('return trtmt;')
        trtmt = variant_list[var_idx]
        self.trtmt = trtmt
        self.log['trtmt'] = trtmt

    def do(self,action):
        action(self)

    def output_log(self):
        str_builder = ''
        for key,value in self.log.items():
            str_builder = str_builder + key + ':' + str(value) + ', '
        logging.info(str_builder)

    def append_to_history(self,url):
        self.browser_history.append(url)

    def quit(self):
        driver = self.webdriver
        driver.close()
        driver.quit()


if __name__ == "__main__":
    user = User()
    user.act()