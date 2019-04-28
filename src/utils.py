import importlib
import inspect
from settings import SETTINGS

def init_settings():
    FLOW_NAME = SETTINGS['FLOW_NAME']
    flow_settings_loc = 'src.flows.' + FLOW_NAME + '.flow_settings'
    flow_settings = importlib.import_module(flow_settings_loc)
    for k,v in flow_settings.__dict__.items():
        if '__' not in k:
            SETTINGS[k] = v
        else:
            pass
    pass

def load_flow(FLOW_NAME):
    flow_module = importlib.import_module('src.flows.' + FLOW_NAME + '.flow')
    return flow_module.flow

def get_args( class_, method):
    target = getattr(class_,method)
    args = getattr(inspect.getargspec(target),'args')
    return args[1:]