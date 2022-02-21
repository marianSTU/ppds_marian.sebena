from fei.ppds import Mutex, Thread
import time


class Shared:
    """"Object Shared for multiple threads using demonstration"""

    def __init__(self, size):
        """"Shared class constructor"""

        self.counter = 0
        self.end = size
        self.elms = [0] * size


def do_count_outside_loop(shared):
    """
    Function which increments shared counter and fill array of elms.

    Lock whole loop.
    """
    mutex.lock()
    while shared.counter < shared.end:
        shared.elms[shared.counter] += 1
        shared.counter += 1
    mutex.unlock()


def do_count_inside_loop(shared):
    """
    Function which increments shared counter and fill array of elms.

    Lock part of loop. Every iteration execute another thread.
    """
    while True:
        mutex.lock()
        if shared.counter < shared.end:
            shared.elms[shared.counter] += 1
            shared.counter += 1
            mutex.unlock()
        else:
            mutex.unlock()
            break


mutex = Mutex()

""" Part for first type of solution: Lock outside of while loop """

start_time = time.time()
shared = Shared(10_000_000)

t1 = Thread(do_count_outside_loop, shared)
t2 = Thread(do_count_outside_loop, shared)

t1.join()
t2.join()

# printed execution elapsed time
print("%s sec: lock outside loop" % (time.time() - start_time))

""" Part for second type of solution: Lock inside a loop """

start_time = time.time()
shared = Shared(10_000_000)

t1 = Thread(do_count_inside_loop, shared)
t2 = Thread(do_count_inside_loop, shared)

t1.join()
t2.join()

# printed execution elapsed time
print("%s sec: lock inside loop" % (time.time() - start_time))

