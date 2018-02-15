import logging

from selenium import webdriver
from settings import TLD, variant_list

class User:

    def __init__(self,user_id):
        self.user_id = user_id
        self.webdriver = webdriver.Chrome()
        self.webdriver.implicitly_wait(0)
        self.landing_page = TLD
        self.trtmt = None
        self.log = dict()
        self.log['bounced'] = 0
        self.log['exception'] = 'None'
        self.log['stop_step'] = 'None'
        self.browser_history = list()


        #self._navigate_to_landing_page(TLD)
        #self._det_trtmt()

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