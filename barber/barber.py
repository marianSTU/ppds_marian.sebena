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

    def __init__(self):
        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)


def get_haircut(i):
    print(f'CUSTOMER: {i} getting haircut')
    sleep(0.02)


def cut_hair():
    print("BARBER: cutting hair")
    sleep(0.02)


def balk(i):
    print(f'\nCUSTOMER: {i} waiting room is full')
    sleep(randint(25, 30) / 100)


def growing_hair():
    # print(f'CUSTOMER: {i} now I my hairstyle is OK')
    sleep(0.06)


def customer(i, shared):

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
    while True:
        shared.customer.wait()
        shared.barber.signal()

        cut_hair()

        shared.customer_done.wait()
        shared.barber_done.signal()


def main():
    shared = Shared()
    customers = []
    for i in range(C):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)
    for t in customers + [hair_stylist]:
        t.join()


# Init constants C= number of customers
C = 5
N = 3

if __name__ == "__main__":
    main()
