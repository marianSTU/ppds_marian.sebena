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

from fei.ppds import Thread, Mutex, Semaphore, Event
from fei.ppds import print
from random import randint
from time import sleep

class SimpleBarrier:
    """
    Class SimpleBarrier represent barrier implemented by event

    Parameters:
        N - number of threads
    """

    def __init__(self, N):
        self.N = N
        self.C = 0
        self.M = Mutex()
        self.T = Event()

    def wait(self):
        self.T.clear()
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0
            self.T.signal()
        self.M.unlock()
        self.T.wait()


def compute_fibonacci(barrier, barrier2, i):
    """
    Unfinished function to compute fibonacci
    """

    sleep(randint(1,10)/10)
    # barrier.wait()
    fib_seq[i+2] = fib_seq[i] + fib_seq[i+1]
    # barrier2.wait()


THREADS = 7
fib_seq = [0] * (THREADS + 2)
fib_seq[1] = 1

sb = SimpleBarrier(THREADS)
sb2 = SimpleBarrier(THREADS)

threads = [Thread(compute_fibonacci, sb, sb2, i) for i in range(THREADS)]
[t.join() for t in threads]

print(fib_seq)