from collections import Counter
from fei.ppds import Mutex, Thread


class Shared:
    """"Object Shared for multiple threads using demonstration"""

    def __init__(self, size):
        """"Shared class constructor"""

        self.counter = 0
        self.end = size
        self.elms = [0] * size


def do_count(shared):
    """Function which increments shared counter and fill array of elms"""

    while True:
        mutex.lock()
        if shared.counter < shared.end:
            shared.elms[shared.counter] += 1
            shared.counter += 1
            mutex.unlock()
        else:
            # If some thread own lock -> unlock it, to avoid deadlock
            mutex.unlock()
            break


shared = Shared(1000000)

mutex = Mutex()

t1 = Thread(do_count, shared)
t2 = Thread(do_count, shared)

t1.join()
t2.join()

counter = Counter(shared.elms)
print(counter.most_common())
