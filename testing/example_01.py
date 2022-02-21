from collections import Counter
from fei.ppds import Mutex, Thread
import time


class Shared:
    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elms = [0] * size


def do_count(shared):

    while shared.counter != shared.end:
        shared.elms[shared.counter] += 1
        shared.counter += 1


# time when program starts
start_time = time.time()

shared = Shared(1000000)

t1 = Thread(do_count, shared)
t2 = Thread(do_count, shared)

t1.join()
t2.join()

# printed execution elapsed time
print("%s seconds" % (time.time() - start_time))

counter = Counter(shared.elms)
print(counter.most_common())
