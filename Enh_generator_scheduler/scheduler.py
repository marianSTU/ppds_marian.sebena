"""
Authors: Mgr. Ing. Matúš Jókay, PhD.
         Bc. Marián Šebeňa
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
"""

from itertools import count
from queue import Queue


class Task(object):
    """
        Scheduler object that represents wrapper for coroutine
    """
    _ids = count(0)

    def __init__(self, cor):
        """
        Initialize instance of scheduler

        :param cor: coroutine
        """
        self.id = next(self._ids)
        self.cor = cor
        self.send_value = None

    def run(self):
        """
        Method run executes the task to the next yield

        :return:
        """
        return self.cor.send(self.send_value)


class Scheduler(object):
    """
        Scheduler object that represents scheduler for coroutines
    """
    def __init__(self):
        """
        Initialize instance of scheduler
        """
        self.tasks_queue = Queue()

    def new(self, cor):
        """
        Method create new instance of task and send it to scheduler
        :param cor: coroutine
        :return:
        """
        new = Task(cor)
        self.schedule(new)

    def schedule(self, task):
        """
        Method schedule place a task into the queue.

        :param task: instance of Task class
        :return:
        """
        self.tasks_queue.put(task)

    def mainloop(self):
        """
        Main scheduler loop method. Manage tasks in queue and runs them.

        :return:
        """
        while True:
            try:
                task = self.tasks_queue.get()
                task.run()
                self.tasks_queue.task_done()
                self.schedule(task)
            except StopIteration:
                continue


def foo():
    """
    Function simulates first coroutine
    :return:
    """
    while True:
        print("FOO: Before 1. yield ")
        yield
        print("FOO: Before 2. yield")
        yield


def bar():
    """
    Function simulates second coroutine
    :return:
    """
    while True:
        print("BAR: Before 1. yield ")
        yield


def flee():
    """
    Function simulates third coroutine

    :return:
    """
    while True:
        print("FLEE: Before 1. yield ")
        yield
        print("FLEE: Before 2. yield ")
        yield
        print("FLEE: Before 3. yield ")
        yield


def main():
    """
    Main fuction creates instance of scheduler and 3 coroutines

    :return:
    """
    scheduler = Scheduler()

    scheduler.new(foo())
    scheduler.new(bar())
    scheduler.new(flee())

    scheduler.mainloop()


if __name__ == '__main__':
    main()
