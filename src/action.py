
class Action(object):

    def __init__(self,user):
        self.user = user
        self._record_log_values()
        if self.user.log['bounced'] == 1:
            pass
        else:
            #try:
                self._proc()
            #except (NoSuchElementException, TimeoutException, AssertionError) as e:
            #except Exception as e:
            #    template = "An exception of type {0} occurred."
            #    message = template.format(type(e).__name__)
            #    print message
        self._check_console_for_errors(self.user.webdriver)


    def _record_log_values(self):
        pass

    def _proc(self):
        pass

    def _check_console_for_errors(self,driver):
        brow_log = driver.get_log('browser')
        for m in brow_log:
            if 'SyntaxError' in m['message']:
                raise JavaSyntaxException


class JavaSyntaxException(Exception):

    def __init__(self):
        pass


