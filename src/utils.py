import importlib
import inspect
from settings import SETTINGS
from selenium.common.exceptions import ElementClickInterceptedException

def init_settings():
    FLOW_NAME = SETTINGS['FLOW_NAME']
    flow_settings_loc = 'src.flows.' + FLOW_NAME + '.flow_settings'
    flow_settings = importlib.import_module(flow_settings_loc)
    for k,v in flow_settings.__dict__.items():
        if '__' not in k:
            SETTINGS[k] = v
        else:
            pass
    if SETTINGS['EXPERIMENT_ACTIVE']:
        EXPERIMENT_NAME = SETTINGS['EXPERIMENT_NAME']
        experiment_settings_loc = 'src.experiments.' + EXPERIMENT_NAME
        experiment_settings_mod = importlib.import_module(experiment_settings_loc)
        SETTINGS['USER_EXPERIMENT_SETTINGS'] = getattr(experiment_settings_mod, 'USER_EXPERIMENT_SETTINGS')
    else:
        SETTINGS['USER_EXPERIMENT_SETTINGS'] = dict()

def load_flow(FLOW_NAME):
    flow_module = importlib.import_module('src.flows.' + FLOW_NAME + '.flow')
    return flow_module.flow

def get_args( class_, method):
    target = getattr(class_,method)
    args = getattr(inspect.getargspec(target),'args')
    return args[1:]

def expand_shadow_node(driver, shadow_node):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', shadow_node)
    return shadow_root

def safe_click(driver, element):
    try:
        element.click()
    except ElementClickInterceptedException:
        js = "arguments[0].click();"
        driver.execute_script(js, element)
