from fei.ppds import Semaphore, Mutex, print, Thread
from time import sleep
from random import randint

N = 3
M = 3


class SimpleBarrier(object):
    def __init__(self, N):
        self.N = N
        self.cnt = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self, each=None, last=None):
        self.mutex.lock()
        self.cnt += 1
        if each:
            print(f'{each} we are {self.cnt}')
        if self.cnt == self.N:
            if last:
                print(last)
            self.cnt = 0
            self.barrier.signal(self.N)
        self.mutex.unlock()
        self.barrier.wait()


class Shared(object):

    def __init__(self, m):
        self.servings = m
        self.mutex = Mutex()
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)

        self.b1 = SimpleBarrier(N)
        self.b2 = SimpleBarrier(N)



def eat(i):
    print(f"Savage {i}: is eating")
    sleep(randint(50, 200) / 100)


def savage(i, shared):
    sleep(randint(1, 100) / 100)
    while True:
        shared.b1.wait()
        shared.b2.wait(each=f'savage {i}: before dinner',
                       last=f'savage {i}: WE ARE ALL')
        shared.mutex.lock()
        if shared.servings == 0:
            print(f"savage {i}: pot is empty\n")
            shared.empty_pot.signal()
            shared.full_pot.wait()
        print(f"savage {i}: take from pot")
        shared.servings -= 1
        shared.mutex.unlock()
        eat(i)


def cook(shared):
    while True:
        shared.empty_pot.wait()
        print(f"Cook cooking\n")
        sleep(randint(50, 200) / 100)
        print(f"Cook: servings->pot")
        shared.servings += M
        shared.full_pot.signal()


def main():
    shared = Shared(0)
    savages = []
    for i in range(N):
        savages.append(Thread(savage,i, shared))
    savages.append(Thread(cook,shared))
    for t in savages:
        t.join()


if __name__ == "__main__":
    main()
