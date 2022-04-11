"""
Authors: Mgr. Ing. Matúš Jókay, PhD.
         Bc. Marián Šebeňa
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
"""

class Fibonacci(object):
    def __init__(self, limit):
        self.limit = limit
        self.a = 0
        self.b = 1
        self.cnt = 1
        self.limit = limit

    def __next__(self):
        if self.cnt > self.limit:
            raise StopIteration

        self.a, self.b = self.b, self.a + self.b
        self.cnt += 1

        return self.b

    def __iter__(self):
        return self


def foo(limit):
    cnt = 1
    a, b = 0, 1
    while True:
        if cnt > limit:
            return
            # raise GeneratorExit
        a, b = b, a + b
        cnt +=1
        yield b


fy = foo(3)
try:
    print(next(fy))
    print(next(fy))
    print(next(fy))
    print(next(fy))
except StopIteration:
    print('Vycerpane')

