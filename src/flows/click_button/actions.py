import signal

from random import uniform

from src.flows.action import Action
from src.flows.click_button.settings import variant_click_thresholds

class Click_Button(Action):

    name = "Click Button"

    def __init__(self,user):
        Action.__init__(self,user)

    def _record_log_values(self):
        self.user.log['click_button'] = 0

    def _proc(self):
        trtmt = self.user.trtmt
        prob = uniform(0, 1)
        #prob = 0 for testing
        thresh = variant_click_thresholds[trtmt]
        if prob <= thresh:
            button_element = self.user.webdriver.find_element_by_id("mybutton")
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(10)
            try:
                button_element.click()
            except Exception:
                print "click timeout"
            signal.alarm(0)
            self.user.log['click_button'] = 1
        else:
            self.user.log['bounced'] = 1


def handler(signum, frame):
    print "Forever is over!"
    raise Exception("end of time")