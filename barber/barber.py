"""
Authors: Mgr. Ing. Matúš Jókay, PhD.
         Bc. Marián Šebeňa
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
"""

from fei.ppds import Semaphore, Mutex, Thread, print
from time import sleep
from random import randint


class Shared(object):
    """
    Class that implements synchronization objects and counters
    """
    def __init__(self):
        """
       Class constructor initialize  creates 4 semaphore's
       for barber and customer states, creates Mutex object, and
       waiting room counter
       """
        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)


def get_haircut(i):
    """
    Function get_haircut simulates time when customer
    gets haircut

        :param i: identification number of customer thread
        :return:
    """
    print(f'\nCUSTOMER: {i} gets haircut')
    sleep(randint(5, 10) / 100)

def cut_hair():
    """
    Function get_haircut simulates time when barber
    cuts customer's hair
    """
    print("\nBARBER: cuts hair")
    sleep(randint(5, 10) / 100)

def balk(i):
    """
    Function balk represents situation when waiting room is full,
    so he have to wait to get in,

        :param i: identification number of customer thread
        :return:
    """
    print(f'CUSTOMER: {i} waiting room is full')
    sleep(randint(20, 25) / 100)


def growing_hair():
    # print(f'CUSTOMER: {i} now I my hairstyle is OK')
    sleep(0.08)


def customer(i, shared):
    """
    Function represents customers behaviour. Customer come to waiting if room is full sleep.
    Wake up barber and waits for invitation from barber. Then gets new haircut. After it both
    both wait to complete their work. At the end waits to hair grow again

        :param i: ID of customer
        :param shared: object of class shared
        :return:
    """
    while True:
        shared.mutex.lock()
        if shared.waiting_room == N:
            shared.mutex.unlock()
            balk(i)
        else:
            shared.waiting_room += 1
            shared.mutex.unlock()

            print(f"CUSTOMER: {i} is in the room")
            shared.customer.signal()
            shared.barber.wait()

            get_haircut(i)

            shared.customer_done.signal()
            shared.barber_done.wait()
            shared.waiting_room -= 1
            growing_hair()


def barber(shared):
    """
    Function barber represents barber. Barber is sleeping, when customer
    come to get new hair wakes up barber. Barber cuts customer hair and both wait
    to complete their work.

        :param shared:
        :return:
    """
    while True:
        shared.customer.wait()
        shared.barber.signal()

        cut_hair()

        shared.customer_done.wait()
        shared.barber_done.signal()


def main():
    """
    Threads initializing function
        :return:
    """
    shared = Shared()
    customers = []
    for i in range(C):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)
    for t in customers + [hair_stylist]:
        t.join()


# Init constants C= number of customers, N waiting room capacity
C = 5
N = 3

if __name__ == "__main__":
    main()
