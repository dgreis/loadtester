import logging
import time
import sys

from global_settings import N, LOGGING_FORMAT, REPO_LOC, FLOW
from src.flows.action import JavaSyntaxException
from user import User

sys.path.append(REPO_LOC + '/src/flows/' + FLOW)
from flow import flow

logging.basicConfig(filename='experiment.log',
                    level=logging.INFO,
                    format=LOGGING_FORMAT,
                    #filemode='w',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

#experiment = [Navigate_To_Landing_Page, Determine_Treatment, Click_Button]


def main():
    t0 = time.time()
    for i in range(N):
        user = User(user_id = i)
        for action in flow:
#            try:
                user.do(action)
#            except Exception as e:
#                exception_class = type(e).__name__
#                if exception_class == "JavaSyntaxException":
#                   raise JavaSyntaxException
#                user.log['exception'] = exception_class
#                user.log['stop_step'] = action.name
#                break
        user.quit()
        user.output_log()
        if (i+1) % 5 == 0:
            elapsed_time = str(round(time.time() - t0, 3))
            print "Finished processing user number " + str(i+1) + "/" + str(N) + " in " + elapsed_time + " sec."
            t0 = time.time()



main()