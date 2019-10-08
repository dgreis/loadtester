import importlib

from src.actions.action import Action
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from settings import SETTINGS
import numpy as np

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


#TODO: fix this event. It looks broken.
def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")
    except WebDriverException:
        pass
    #    print "Got here "

class Possibly_Search(Action):

    name = "Possibly Search"

    def __init__(self, user):
        default_action_route = "No Search"
        self.action_route = default_action_route
        #user_override code here
        if SETTINGS['EXPERIMENT_ACTIVE']:
            USER_EXPERIMENT_SETTINGS = user.USER_EXPERIMENT_SETTINGS
            prob = USER_EXPERIMENT_SETTINGS['default']['execute_search']
            if np.random.uniform(0,1,1) < prob:
                self.action_route = 'Execute Search'
        Action.__init__(self, user)

    def _proc(self):
        #TODO: Possibly sub-class Action with Router?
        action_route = self.action_route
        action_class_name = action_route.replace(' ', '_')
        ecommerce_module = importlib.import_module('src.actions.common_actions')
        Action_Class = getattr(ecommerce_module,action_class_name)
        user = self.user
        user.do(Action_Class)

class Execute_Search(Action):

    name = "Execute Search"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        url = SETTINGS['SEARCH_ENGINE_URL']
        driver.get(url)
        campaign_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Click Here For Campaign"))
        )
        campaign_button.click()

class No_Search(Action):

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        pass

class Navigate_To_Landing_Page(Action):

    name = "Navigate To Landing Page"

    def __init__(self, user):
        Action.__init__(self, user)


    def _proc(self):
        driver = self.user.webdriver
        url = self.user.landing_page
        driver.get(url)
        #WebDriverWait(driver, 10).until(ajax_complete, "Timeout waiting for page to load")
        self.user.append_to_history(url)

class Click_Through_GTM_Preview_Mode(Action):

    name = "Click Through GTM Preview Mode"

    def __init__(self, user):
        Action.__init__(self, user)


    def _proc(self):
        driver = self.user.webdriver
        WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, SETTINGS["GTM_PASSTHROUGH_LINK"]))
        ).click()

class Bounce(Action):

    name = "Bounce"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        self.user.log['bounced']  = 1

class Navigate_Back(Action):

    name = "Navigate Back"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        driver.back()
        self.user.append_to_history(driver.current_url)


class Leave_Site(Action):

    name = "Leave Site"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        driver.quit()


class Determine_Treatment(Action):

    name = "Determine Treatment"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        driver.execute_script('var expVar = gaData[' + '"' + GA_TRACKING_ID + '"' + ']["experiments"];\
                               var trtmt = expVar[Object.keys(expVar)[0]];\
                               window.trtmt = trtmt;')
        var_idx = int(driver.execute_script('return trtmt;'))
        trtmt = variant_list[var_idx]
        self.user.trtmt = trtmt
        self.user.log['trtmt'] = trtmt