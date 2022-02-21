from collections import Counter
from fei.ppds import Thread


class Shared:
    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elms = [0]


def do_count(shared):
    while shared.counter != shared.end:
        shared.elms[shared.counter] += 1
        shared.counter += 1


shared = Shared(1000)

t1 = Thread(do_count, shared)
t1.join()

counter = Counter(shared.elms)
print(counter.most_common())
