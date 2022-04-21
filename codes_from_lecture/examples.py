"""
Authors: Mgr. Ing. Matúš Jókay, PhD.
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
"""

import queue


def task(name, work_queue):
    if work_queue.empty():
        print(f"Task {name} nothing to do")
    else:
        while not work_queue.empty():
            count = work_queue.get()
            total = 0
            print(f"Task {name} running")
            for x in range(count):
                total += 1
            print(f"Task {name} total: {total}")


def main():
    work_queue = queue.Queue()

    # Do fronty dame objekty na spracovanie (cisla)
    for work in [15, 10, 5, 2]:
        work_queue.put(work)

    # Pripravime dve synchronne ulohy
    tasks = [(task, "One", work_queue), (task, "Two", work_queue)]

    # Spustime pripravene ulohy
    for t, n, q in tasks:
        t(n, q)


if __name__ == "__main__":
    main()