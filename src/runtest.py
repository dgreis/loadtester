import logging
import time

from settings import SETTINGS
from utils import init_settings, load_flow
from user import User
from src.actions.action import JavaSyntaxException

init_settings()

LOGGING_FORMAT = SETTINGS['LOGGING_FORMAT']
logging.basicConfig(filename='experiment.log',
                    level=logging.INFO,
                    format=LOGGING_FORMAT,
                    #filemode='w',
                    datefmt='%m/%d/%Y %I:%M:%S %p')



def main():
    t0 = time.time()
    FLOW_NAME = SETTINGS['FLOW_NAME']
    flow = load_flow(FLOW_NAME)
    N = SETTINGS['N']
    for i in range(N):
        user = User(user_id = i)
        for action in flow:
            try:
                user.do(action)
            except Exception as e:
                exception_class = type(e).__name__
                if exception_class == "JavaSyntaxException":
                    raise JavaSyntaxException
                user.log['exception'] = exception_class
                user.log['stop_step'] = action.name
                break
        user.quit()
        user.output_log()
        if (i+1) % 5 == 0:
            elapsed_time = str(round(time.time() - t0, 3))
            print "Finished processing user number " + str(i+1) + "/" + str(N) + " in " + elapsed_time + " sec."
            t0 = time.time()



main()