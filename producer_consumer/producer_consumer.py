from random import randint
from time import sleep
from fei.ppds import Mutex, Semaphore, Thread, print


class Shared(object):
    def __init__(self, N):
        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(N)
        self.items = Semaphore(0)
        self.storage = 0


def producer(shared):
    while True:
        sleep(randint(1, 10)/10)
        shared.free.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        sleep(randint(1, 10) / 100)
        shared.storage += 1
        shared.mutex.unlock()
        shared.items.signal()


def consumer(shared):
    while True:
        shared.items.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        sleep(randint(1, 10) / 100)
        shared.storage -= 1
        shared.mutex.unlock()
        shared.items.signal()
        sleep(randint(1, 10) / 10)


def main():
    s = Shared(10)
    c = [Thread(consumer, s) for _ in range(1)]
    p = [Thread(producer, s) for _ in range(2)]
    sleep(5)
    s.finished = True
    print("caka na dokoncenie")
    s.items.signal(100)
    s.free.signal(100)
    [t.join() for t in c+p]
    print(s.storage)
    print("koniec programu")


main()
