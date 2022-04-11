"""
Authors: Mgr. Ing. Matúš Jókay, PhD.
         Bc. Marián Šebeňa
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
"""


def cat(f, next_fnc):
    for line in f:
        next_fnc.send(line)
    next_fnc.close()


def grep(substring, next_fnc):
    try:
        while True:
            line = (yield)
            next_fnc.send(line.count(substring))
    except GeneratorExit:
        next_fnc.close()


def wc(substring):
    n = 0
    try:
        while True:
            n += (yield)
    except GeneratorExit:
        print(substring, n, flush=True)


if __name__ == "__main__":
    f = open("find", "r")
    substring = "b"

    w = wc(substring)
    next(w)
    g = grep(substring, w)
    next(g)

    cat(f, g)

