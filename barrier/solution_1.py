"""
Authors: Mgr. Ing. Matúš Jókay, PhD.
         Bc. Marián Šebeňa
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket
-bariera-%f0%9f%9a%a7/?%2F
"""

from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, Event
from fei.ppds import print


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.C = 0
        self.M = Mutex()
        self.T = Semaphore(0)

    def wait(self):
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0
            self.T.signal(self.N)
        self.M.unlock()
        self.T.wait()


def barrier_example(barrier, thread_id):
    sleep(randint(1, 10) / 10)
    print("Thread no. %d before barrier" % thread_id)
    barrier.wait()
    print("Thread no. %d after barrier" % thread_id)


# priklad pouzitia ADT SimpleBarrier
sb = SimpleBarrier(10)

threads = [Thread(barrier_example, sb, i) for i in range(10)]
[t.join() for t in threads]


