from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0

from src.flows.action import Action
#from src.global_settings import GA_TRACKING_ID


def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")
    except WebDriverException:
        pass
    #    print "Got here "

class Navigate_To_Landing_Page(Action):

    name = "Navigate To Landing Page"

    def __init__(self, user):
        Action.__init__(self, user)


    def _proc(self):
        driver = self.user.webdriver
        url = self.user.landing_page
        driver.get(url)
        WebDriverWait(driver, 10).until(ajax_complete, "Timeout waiting for page to load")
        self.user.append_to_history(url)

class Determine_Treatment(Action):

    name = "Determine Treatment"

    def __init__(self, user):
        Action.__init__(self, user)

    def _proc(self):
        driver = self.user.webdriver
        driver.execute_script('var expVar = gaData[' + '"' + GA_TRACKING_ID + '"' + ']["flows"];\
                               var trtmt = expVar[Object.keys(expVar)[0]];\
                               window.trtmt = trtmt;')
        var_idx = int(driver.execute_script('return trtmt;'))
        trtmt = variant_list[var_idx]
        self.user.trtmt = trtmt
        self.user.log['trtmt'] = trtmt