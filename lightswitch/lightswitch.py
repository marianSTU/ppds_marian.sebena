"""
Authors: Mgr. Ing. Matúš Jókay, PhD.
         Bc. Marián Šebeňa
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
"""
from fei.ppds import Mutex


class LightSwitch(object):
    """
        LightSwitch object that represent between more semaphores.
    """

    def __init__(self):
        """
            Initialize instance of class with mutex lock and counter
        """
        self.counter = 0
        self.mutex = Mutex()

    def lock(self, semaphore):
        """
            Method Lock lock all threads in object of semaphore
                :parameter semaphore: object of semaphore
        """
        self.mutex.lock()
        if not semaphore.counter:
            semaphore.wait()
        self.counter += 1
        self.mutex.unlock()

    def unlock(self, semaphore):
        """
            Method Lock lock all threads in object of semaphore
                :parameter semaphore: object of semaphore
        """
        self.mutex.lock()
        self.counter -= 1
        if not semaphore.counter:
            semaphore.signal()
        self.mutex.unlock()
