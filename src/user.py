import time
import logging

from random import uniform
from selenium import webdriver
from settings import variant_map, variant_thresholds


class User:

    def __init__(self,user_id):
        self.user_id = user_id
        self.webdriver = webdriver.Chrome()
        self.page = None
        self.treatment = None
        self.clicked = 0

    def det_trtmt(self):
        page = self.page
        key = page.split('8888')[1].split('?')[0]
        variant = variant_map[key]
        self.trtmt = variant

    def navigate_to_url(self,URL):
        driver = self.webdriver
        driver.get(URL) #will this update or do I need to reassign?
        self.page = driver.current_url


    def act(self):
        driver = self.webdriver

        trtmt = self.trtmt
        prob = uniform(0,1)
        thresh = variant_thresholds[trtmt]
        if prob <= thresh:
            button_element = driver.find_element_by_id("mybutton")
            button_element.click()
            self.clicked = 1
        else:
            pass

    def log(self):
        logging.info(str(self.user_id) + ',' + self.trtmt + ',' + str(self.clicked) + ',')

    def quit(self):
        driver = self.webdriver
        driver.close()
        driver.quit()


if __name__ == "__main__":
    user = User()
    user.act()