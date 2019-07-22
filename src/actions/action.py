import numpy as np
import importlib

from settings import SETTINGS

class Action(object):

    def __init__(self,user):
        self.user = user
        self._record_log_values()
        if self.user.log['bounced'] == 1:
            pass
        else:
            self._proc()
        self._check_console_for_errors(self.user.webdriver)


    def _record_log_values(self):
        pass

    #TODO: Make this abstract?
    def _proc(self):
        pass

    def _check_console_for_errors(self,driver):
        brow_log = driver.get_log('browser')
        for m in brow_log:
            if 'SyntaxError' in m['message']:
                raise JavaSyntaxException

class Router(Action):

    def __init__(self, user):
        USER_EXPERIMENT_SETTINGS = user.USER_EXPERIMENT_SETTINGS
        class_name = self.name.replace(" ","_").lower()
        default_action_route = USER_EXPERIMENT_SETTINGS['default'][class_name][0][0]
        self.action_route = default_action_route
        if SETTINGS['EXPERIMENT_ACTIVE']:
            USER_EXPERIMENT_SETTINGS = user.USER_EXPERIMENT_SETTINGS
            prob = USER_EXPERIMENT_SETTINGS['default'][class_name][0][1]
            thresh = np.random.uniform(0,1,1)[0]
            i = 0
            while thresh > prob:
                i += 1
                self.action_route = USER_EXPERIMENT_SETTINGS['default'][class_name][i][0]
                prob = prob + USER_EXPERIMENT_SETTINGS['default'][class_name][i][1]
        Action.__init__(self, user)

    def _proc(self):
        action_class_name = ('_').join([x.capitalize() for x in self.action_route.split('_')])
        actions_module = importlib.import_module('src.actions')
        actions_submodules = filter(lambda x: '__' not in x, dir(actions_module))
        for submodule in actions_submodules:
            try:
                Action_Class = getattr(getattr(actions_module,submodule), action_class_name)
                break
            except AttributeError:
                pass
        user = self.user
        user.do(Action_Class)


class JavaSyntaxException(Exception):

    def __init__(self):
        pass


