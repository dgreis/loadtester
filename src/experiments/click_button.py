from random import uniform

from action import Action
from settings import variant_click_thresholds

class Click_Button(Action):

    def __init__(self,user):
        Action.__init__(self,user)
        self.user.log['click_button'] = 0
        self.user.log['bounced'] = 0
        self._proc()


    def _proc(self):
        trtmt = self.user.trtmt
        prob = uniform(0, 1)
        #prob = 0 for testing
        thresh = variant_click_thresholds[trtmt]
        if prob <= thresh:
            button_element = self.user.webdriver.find_element_by_id("mybutton")
            button_element.click()
            self.user.log['click_button'] = 1
        else:
            self.user.log['bounced'] = 1


