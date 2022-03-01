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


def compute_fibonacci(i):
    fib_seq[i+2] = fib_seq[i] + fib_seq[i+1]


THREADS = 10
fib_seq = [0] * (THREADS + 2)
fib_seq[1] = 1
# sb = SimpleBarrier(THREADS)


threads = [Thread(compute_fibonacci, i) for i in range(THREADS)]
[t.join() for t in threads]

print(fib_seq)