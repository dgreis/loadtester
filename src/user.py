import logging

from selenium import webdriver
import chromedriver_binary
from settings import SETTINGS

class User:

    def __init__(self,user_id):
        self.user_id = user_id
        self.webdriver = webdriver.Chrome()
        self.webdriver.implicitly_wait(0)
        self.landing_page = SETTINGS['TLD']
        self.trtmt = None
        self.log = dict()
        self.log['bounced'] = 0
        self.log['exception'] = 'None'
        self.log['stop_step'] = 'None'
        self.browser_history = list()


    def do(self,action,**kwargs):
        action(self,**kwargs)

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