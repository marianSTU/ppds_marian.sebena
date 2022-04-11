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
    _ids = count(0)

    def __init__(self, function):
        self.id = next(self._ids)
        self.function = function
        self.send_value = None

    def run(self):
        return self.function.send(self.send_value)


class Scheduler(object):
    def __init__(self):
        self.tasks_queue = Queue()

    def new(self, fun):
        new = Task(fun)
        self.schedule(new)

    def schedule(self, task):
        self.tasks_queue.put(task)

    def mainloop(self):
        while True:
            try:
                task = self.tasks_queue.get()
                task.run()
                self.tasks_queue.task_done()
                self.schedule(task)
            except StopIteration:
                continue


def foo():
    while True:
        print("FOO: Before 1. yield ")
        yield
        print("FOO: Before 2. yield")
        yield


def bar():
    while True:
        print("BAR: Before 1. yield ")
        yield


def flee():
    while True:
        print("FLEE: Before 1. yield ")
        yield
        print("FLEE: Before 2. yield ")
        yield
        print("FLEE: Before 3. yield ")
        yield


def main():
    scheduler = Scheduler()

    scheduler.new(foo())
    scheduler.new(bar())
    scheduler.new(flee())

    scheduler.mainloop()


if __name__ == '__main__':
    main()
