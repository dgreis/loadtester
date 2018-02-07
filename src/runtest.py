import logging
import time

from settings import N, LOGGING_FORMAT
from user import User
from experiments.click_button import Click_Button
from experiments.funnel_test import Wait_For_Pic, Possibly_Bounce, Click_Add_To_Cart, Wait_To_Claim_Gift, Claim_Gift

logging.basicConfig(filename='experiment.log',
                    level=logging.INFO,
                    format=LOGGING_FORMAT,
                    filemode='w',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

#experiment = [Click_Button]
experiment = [Click_Button, Wait_For_Pic, Possibly_Bounce, Click_Add_To_Cart, Wait_To_Claim_Gift, Claim_Gift]


def main():
    t0 = time.time()
    for i in range(N):
        user = User(user_id = i)
        for action in experiment:
            user.do(action)
        user.quit()
        user.output_log()
        if (i+1) % 5 == 0:  #This didn't work TODO: figure it out
            elapsed_time = str(round(time.time() - t0, 3))
            print "Finished with user number " + str(i+1) + "/" + str(N) + " in " + elapsed_time + " sec."
            t0 = time.time()



main()