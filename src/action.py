from selenium.common.exceptions import NoSuchElementException

class Action:

    def __init__(self,user):
        self.user = user
        if self.user.log['bounced'] == 1:
            pass
        else:
            try:
                self._proc()
            except NoSuchElementException as e:
                print e.message

    def _record_log_values(self):
        pass

    def _proc(self):
        pass




