"""
Authors: Mgr. Ing. Matúš Jókay, PhD.
         Bc. Marián Šebeňa
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
"""

from fei.ppds import Semaphore, Mutex, print, Thread
from time import sleep
from random import randint


class SimpleBarrier(object):
    """
    Class implements barrier synchronization
    """
    def __init__(self, N):
        """
        Initialize other synchronization objects

        :param N: number of threads
        """
        self.N = N
        self.cnt = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self, each=None, last=None,  each_cook=None, last_cook=None):
        """
        Wait method secure hold execution after all threads arrive

        :param each: ID of savage
        :param last: ID of last savage before release
        :param each_cook: ID of cook
        :param last_cook: ID of last savage before release
        :return:
        """
        self.mutex.lock()
        self.cnt += 1
        if each:
            print(f'{each} we are {self.cnt}')
        if each_cook:
            print(each_cook)
        if self.cnt == self.N:
            if last:
                print(f'{last} we are {self.cnt}')
            if last_cook:
                print(last_cook)
            self.cnt = 0
            self.barrier.signal(self.N)
        self.mutex.unlock()
        self.barrier.wait()


class Shared(object):
    """
    Class that implements synchronization objects and counters
    """
    def __init__(self, m):
        """
        Class constructor initialize  creates semaphore
        for 2 states of pot, creates Mutex object, and
        creates barrier object for savages and cook

        :param m: capacity of pot
        """
        self.servings = m
        self.mutex = Mutex()
        self.mutex_cooks = Mutex()
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)

        self.b1 = SimpleBarrier(N)
        self.b2 = SimpleBarrier(N)

        self.b1_cooks = SimpleBarrier(C)
        self.b2_cooks = SimpleBarrier(C)


def eat(i):
    """
    Function implements eating simulation.

    :param i: ID of savage thread
    :return:
    """
    print(f"Savage {i}: is eating")
    sleep(randint(50, 200) / 100)


def savage(i, shared):
    """
    Function represents taking portions and eating
    by savages. When pot is empty last savage wakes
    all cook and all waits until pot is again full.

    :param i: ID of savage thread
    :param shared: Object shared
    :return:
    """
    sleep(randint(1, 100) / 100)
    while True:
        shared.b1.wait()
        shared.b2.wait(each=f'savage {i}: before dinner',
                       last=f'savage {i}: WE ARE ALL')
        shared.mutex.lock()
        if shared.servings == 0:
            print(f"savage {i}: pot is empty\n")
            shared.empty_pot.signal(C)
            shared.full_pot.wait()
        print(f"savage {i}: take from pot")
        shared.servings -= 1
        shared.mutex.unlock()
        eat(i)


def cook(j, shared):
    """
    Function represents cooking when pot is empty.
    Cook wake up when savege informs that pot is empty then
    cook make pot full and tell it to savages and sleep again.

    :param j: ID of cook thread
    :param shared: Object shared
    :return:
    """
    shared.empty_pot.wait()
    while True:
        shared.b1_cooks.wait()
        shared.b2_cooks.wait(each_cook=f'cook {j}: before cooking',
                             last_cook=f'cook {j}: LETS GO COOKING\n')
        shared.mutex_cooks.lock()
        if shared.servings == M:
            print(f'cook {j}: pot is FULL')
            shared.full_pot.signal()
            shared.empty_pot.wait()
        print(f"Cook {j}: cooking")
        sleep(randint(50, 200) / 100)
        shared.servings += 1
        shared.mutex_cooks.unlock()


def main():
    """
    Threads initializing function
    :return:
    """
    shared = Shared(0)
    savages_and_cook = []
    for i in range(N):
        savages_and_cook.append(Thread(savage, i, shared))
    for j in range(C):
        savages_and_cook.append(Thread(cook, j, shared))
    for t in savages_and_cook:
        t.join()


# Init constants M = size of pot, C= number of cook
# and N = number of savages
N = 9
C = 3
M = 18

if __name__ == "__main__":
    main()
