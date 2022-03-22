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
from fei.ppds import print, Semaphore, Thread, Mutex


class Shared(object):
    def __init__(self):
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)

        self.pusherTobacco = Semaphore(0)
        self.pusherMatch = Semaphore(0)
        self.pusherPaper = Semaphore(0)

        self.mutex = Mutex()
        self.isTobacco = 0
        self.isMatch = 0
        self.isPaper = 0

        self.made_tobacco = 0
        self.made_match = 0
        self.made_paper = 0



def agent_1(shared):
    while True:
        sleep(randint(0, 10)/100)
        # shared.agentSem.wait()
        print("agent: tobacco, paper ==> smoker 'match'")
        shared.tobacco.signal()
        shared.paper.signal()


def agent_2(shared):
    while True:
        sleep(randint(0, 10)/100)
        # shared.agentSem.wait()
        print("agent: paper, match ==> smoker 'tobacco'")
        shared.paper.signal()
        shared.match.signal()


def agent_3(shared):
    while True:
        sleep(randint(0, 10)/100)
        # shared.agentSem.wait()
        print("agent: tobacco, match ==> smoker 'paper'")
        shared.match.signal()
        shared.tobacco.signal()


def make_cigarette(name):
    print(f"{name} makes cigarette")
    sleep(randint(0, 10)/100)


def smoke(name):
    print(f"{name} smokes")
    sleep(randint(0, 10)/100)


def smoker_match(shared):
    while True:
        sleep(randint(0, 10)/100)
        shared.pusherMatch.wait()
        make_cigarette("match")
        shared.made_match += 1
        print(f"cigarettes made: tobacco:{shared.made_tobacco} "
              f"paper:{shared.made_paper} match:{shared.made_match}")
        smoke("smoker match")


def smoker_tobacco(shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusherTobacco.wait()
        make_cigarette("tobacco")
        shared.made_tobacco += 1
        print(f"cigarettes made: tobacco:{shared.made_tobacco} "
              f"paper:{shared.made_paper} match:{shared.made_match}")
        smoke("smoker tobacco")


def smoker_paper(shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusherPaper.wait()
        make_cigarette("paper")
        shared.made_paper += 1
        print(f"cigarettes made: tobacco:{shared.made_tobacco} "
              f"paper:{shared.made_paper} match:{shared.made_match}")
        smoke("smoker paper")


def pusher_match(shared):
    while True:
        shared.match.wait()
        shared.mutex.lock()
        if shared.isPaper:
            shared.isPaper -= 1
            shared.pusherTobacco.signal()
        elif shared.isTobacco:
            shared.isTobacco -= 1
            shared.pusherPaper.signal()
        else:
            shared.isMatch += 1
        shared.mutex.unlock()


def pusher_paper(shared):
    while True:
        shared.paper.wait()
        shared.mutex.lock()
        if shared.isTobacco:
            shared.isTobacco -= 1
            shared.pusherMatch.signal()
        elif shared.isMatch:
            shared.isMatch -= 1
            shared.pusherTobacco.signal()
        else:
            shared.isPaper += 1
        shared.mutex.unlock()


def pusher_tobacco(shared):
    while True:
        shared.tobacco.wait()
        shared.mutex.lock()
        if shared.isPaper:
            shared.isPaper -= 1
            shared.pusherMatch.signal()
        elif shared.isMatch:
            shared.isMatch -= 1
            shared.pusherPaper.signal()
        else:
            shared.isTobacco += 1
        shared.mutex.unlock()


def main():
    shared = Shared()

    smokers = [Thread(smoker_match, shared), Thread(smoker_tobacco, shared), Thread(smoker_paper, shared)]
    pushers = [Thread(pusher_match, shared), Thread(pusher_paper, shared), Thread(pusher_tobacco, shared)]
    agents = [Thread(agent_1, shared), Thread(agent_2, shared), Thread(agent_3, shared)]

    for t in smokers+agents+pushers:
        t.join()


if __name__ == "__main__":
    main()
