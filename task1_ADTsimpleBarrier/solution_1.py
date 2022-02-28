from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex

from fei.ppds import print

class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        # ...

    def wait(self):
        # ...
        pass


def barrier_example(barrier, thread_id):
    sleep(randint(1, 10) / 10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("vlakno %d po bariere" % thread_id)


# priklad pouzitia ADT SimpleBarrier
sb = SimpleBarrier(5)