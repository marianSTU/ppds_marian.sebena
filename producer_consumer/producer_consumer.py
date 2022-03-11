"""
Authors: Mgr. Ing. Matúš Jókay, PhD.
         Bc. Marián Šebeňa
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
"""
from random import randint
from time import sleep
from fei.ppds import Mutex, Semaphore, Thread
import matplotlib.pyplot as plt
import time


class Shared(object):
    """
    Class shared represents storage of items.Contains actual
    number of items in storage, number of produced items and
    number of exported items

        :parameter n: size of storage
    """
    def __init__(self, n):
        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(n)
        self.items = Semaphore(0)
        self.storage = 0
        self.items_produced = 0
        self.items_exported = 0


def producer(shared):
    """
    Function represents producer of items. When thread "produce"
    item (represent by sleep function) storage and produced items
    are incremented by 1.

        :param shared: object instance of class Shared
    """
    while True:
        sleep(randint(1, 10)/250)
        shared.items_produced += 1
        shared.free.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        shared.storage += 1
        shared.mutex.unlock()
        shared.items.signal()


def consumer(shared):
    """
        Function represents consumer(purchaser) of items. When thread "consume"
        item storage is decremented by 1 and produced items
        are incremented by 1.

            :param shared: object instance of class Shared
        """
    while True:
        shared.items.wait()
        shared.items_exported += 1
        if shared.finished:
            break
        shared.mutex.lock()
        shared.storage -= 1
        shared.mutex.unlock()
        shared.free.signal()
        sleep(randint(1, 10) / 250)


def plot(data):
    """
    Function that plot 3d graph of addiction

        :param data: array of addicted points
    """
    x = [x[0] for x in data]
    y = [y[1] for y in data]
    z = [z[2] for z in data]

    ax = plt.axes(projection='3d')
    ax.plot_trisurf(x, y, z, cmap='Oranges', edgecolor='none')
    ax.set_title('Graph')
    ax.set_xlabel('number of producers')
    ax.set_ylabel('items_exported_per_sec')
    ax.set_zlabel('items_produced_per_sec')
    plt.show()


def main():
    """
    Main function implements options of finding best sizes of producers and consumers
    """
    searches = 10
    storage_size = 10
    data = []
    # grid search
    for i in range(1, 10):
        for j in range(searches):
            start_time = time.time()
            s = Shared(storage_size)
            # number of consumers is still same size, producers rise
            cons = [Thread(consumer, s) for _ in range(3)]
            prod = [Thread(producer, s) for _ in range(i)]
            sleep(5)
            s.finished = True

            # free all waiting threads
            s.items.signal(100)
            s.free.signal(100)
            [t.join() for t in cons + prod]

            items_produced = s.items_produced
            items_exported = s.items_exported

            # calculation of items produced/exported per second
            end_time = time.time() - start_time
            production_per_sec = items_produced / end_time
            export_per_sec = items_exported / end_time
            # append points to data array due to graph plotting
            data.append([i, export_per_sec, production_per_sec])
    plot(data)


main()
