"""
Authors: Mgr. Ing. Matúš Jókay, PhD.
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
"""


# Synchronous version with generators
import time
import queue


def task(name, queue):
    while not queue.empty():
        delay = queue.get()
        print(f"Task {name} running")
        time_start = time.perf_counter()
        time.sleep(delay)
        elapsed = time.perf_counter() - time_start
        print(f"Task {name} elapsed time: {elapsed:.1f}")
        yield


def main():
    # Create the queue of work
    work_queue = queue.Queue()

    # Put some work in the queue
    for work in [5, 1, 5, 2]:
        work_queue.put(work)

    tasks = [task("One", work_queue), task("Two", work_queue)]

    # Run the tasks
    done = False
    start_time = time.perf_counter()
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)
                if len(tasks) == 0:
                    done = True
    elapsed = time.perf_counter() - start_time
    print(f"\nTotal elapsed time: {elapsed:.1f}")


if __name__ == "__main__":
    main()

# Synchronous version

# import queue
#
#
# def task(name, work_queue):
#     if work_queue.empty():
#         print(f"Task {name} nothing to do")
#     else:
#         while not work_queue.empty():
#             count = work_queue.get()
#             total = 0
#             print(f"Task {name} running")
#             for x in range(count):
#                 total += 1
#             print(f"Task {name} total: {total}")
#
#
# def main():
#     work_queue = queue.Queue()
#
#     # Do fronty dame objekty na spracovanie (cisla)
#     for work in [15, 10, 5, 2]:
#         work_queue.put(work)
#
#     # Pripravime dve synchronne ulohy
#     tasks = [(task, "One", work_queue), (task, "Two", work_queue)]
#
#     # Spustime pripravene ulohy
#     for t, n, q in tasks:
#         t(n, q)
#
#
# if __name__ == "__main__":
#     main()