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
    """
    Class SimpleBarrier represent barrier implemented by event.
    Threads waits while all of them arrive to barrier, then
    they are all released

    Parameters:
        N - number of threads
    """

    def __init__(self, N):
        self.N = N
        self.C = 0
        self.M = Mutex()
        self.T = Event()

    def wait(self):
        # clear released event flag
        self.T.clear()
        self.M.lock()
        self.C += 1
        self.M.unlock()
        if self.C == self.N:
            self.C = 0
            self.T.signal()
        self.T.wait()


def barrier_cycle(barrier1, barrier2, thread_id):
    """
        Function barrier_cycle represents never ending loop
        of threads iteration, used two barriers,
        when threads could continue executing only when
        all threads arrive to barrier

        Parameters:
            barrier - object of class SimpleBarrier
            thread_id - actual thread id
    """

    while True:
        before_barrier(thread_id)
        barrier1.wait()
        after_barrier(thread_id)
        barrier2.wait()


def before_barrier(thread_id):
    """
        Function before_barrier print actual thread
        when execute before barrier. Function sleep
        simulates critical area of program

        Parameters:
            thread_id - actual thread id
    """

    sleep(randint(1, 10) / 10)
    print(f"before barrier {thread_id}")


def after_barrier(thread_id):
    """
        Function before_barrier print actual thread
        when execute after barrier. Function sleep
        simulates critical area of program

        Parameters:
            thread_id - actual thread id
    """

    print(f"after barrier {thread_id}")
    sleep(randint(1, 10) / 10)


THREADS = 10
sb = SimpleBarrier(THREADS)
sb2 = SimpleBarrier(THREADS)

threads = [Thread(barrier_cycle, sb, sb2, i) for i in range(THREADS)]
[t.join() for t in threads]
