import logging
import time

from settings import N, URL, LOGGING_FORMAT
from user import User
from experiments.click_button import click_button

logging.basicConfig(filename='experiment.log',
                    level=logging.INFO,
                    format=LOGGING_FORMAT,
                    filemode='w',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

experiment = [click_button]


def main():
    t0 = time.time()
    for i in range(N):
        user = User(user_id = i)
        for action in experiment :
            user.do(action)
        pass
        user.quit()
        user.log()
    #if i % 50 == 0:  #This didn't work TODO: figure it out
    #    elapsed_time = str(round(time.time() - t0, 3))
    #    print "Finished with user number " + str(i) + "/" + str(N) + " in " + elapsed_time + " sec."
    #    t0 = time.time()



main()