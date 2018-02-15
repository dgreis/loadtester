import logging
import time

from settings import N, LOGGING_FORMAT
from user import User
from action import JavaSyntaxException
from common_actions import Navigate_To_Landing_Page, Determine_Treatment
from experiments.click_button import Click_Button
from experiments.funnel_test import Wait_For_Pic, Possibly_Bounce, Click_Add_To_Cart, Wait_To_Claim_Gift, Claim_Gift

logging.basicConfig(filename='experiment.log',
                    level=logging.INFO,
                    format=LOGGING_FORMAT,
                    filemode='w',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

#experiment = [Navigate_To_Landing_Page, Determine_Treatment, Click_Button]
experiment = [Navigate_To_Landing_Page,
              Determine_Treatment,
              Click_Button,
              Wait_For_Pic,
              Possibly_Bounce,
              Click_Add_To_Cart,
              Wait_To_Claim_Gift,
              Claim_Gift]


def main():
    t0 = time.time()
    for i in range(N):
        user = User(user_id = i)
        for action in experiment:
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