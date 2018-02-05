import logging
import time

from settings import N, URL, LOGGING_FORMAT
from user import User

logging.basicConfig(filename='experiment.log',
                    level=logging.INFO,
                    format=LOGGING_FORMAT,
                    filemode='w',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


def main():
    t0 = time.time()
    for i in range(N):
        user = User(user_id = i)
        user.navigate_to_url(URL)
        user.det_trtmt()
        user.act()
        user.quit()
        user.log()
    if i % 50 == 0:
        elapsed_time = str(round(time.time() - t0, 3))
        print "Finished with user number " + str(i) + "/" + str(N) + " in " + elapsed_time + " sec."
        t0 = time.time()



main()