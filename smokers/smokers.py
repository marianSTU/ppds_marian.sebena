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
from fei.ppds import print, Semaphore, Thread


class Shared(object):
    def __init__(self):
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)
        self.agentSem = Semaphore(1)


def agent_1(shared):
    while True:
        sleep(randint(0, 10)/100)
        shared.agentSem.wait()
        print("agent: tobacco, paper")
        shared.tobacco.signal()
        shared.paper.signal()


def agent_2(shared):
    while True:
        sleep(randint(0, 10)/100)
        shared.agentSem.wait()
        print("agent: paper, match")
        shared.paper.signal()
        shared.match.signal()


def agent_3(shared):
    while True:
        sleep(randint(0, 10)/100)
        shared.agentSem.wait()
        print("agent: tobacco, match")
        shared.tobacco.signal()
        shared.match.signal()


def make_cigarette():
    sleep(randint(0, 10)/100)


def smoke(name):
    print(f"{name} smokes")
    sleep(randint(0, 10)/100)


def smoker_match(shared):
    while True:
        sleep(randint(0, 10)/100)
        shared.paper.wait()
        # print("paper: smoker_match")
        shared.tobacco.wait()
        make_cigarette()
        shared.agentSem.signal()
        smoke("smoker match")


def smoker_tobacco(shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.paper.wait()
        # print("paper: smoker_tobacco")
        shared.match.wait()
        make_cigarette()
        shared.agentSem.signal()
        smoke("smoker tobacco")


def smoker_paper(shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.match.wait()
        # print("match: smoker_paper")
        shared.tobacco.wait()
        make_cigarette()
        shared.agentSem.signal()
        smoke("smoker paper")


def main():
    shared = Shared()

    smokers = []
    smokers.append(Thread(smoker_match, shared))
    smokers.append(Thread(smoker_tobacco, shared))
    smokers.append(Thread(smoker_paper, shared))

    agents = []
    agents.append(Thread(agent_1, shared))
    agents.append(Thread(agent_2, shared))
    agents.append(Thread(agent_3, shared))

    for t in smokers+agents:
        t.join()


if __name__ == "__main__":
    main()
