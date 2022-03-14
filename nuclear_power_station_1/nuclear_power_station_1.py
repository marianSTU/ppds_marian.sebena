"""
Authors: Mgr. Ing. Matúš Jókay, PhD.
         Bc. Marián Šebeňa
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
"""

from fei.ppds import Mutex, Event, Semaphore, Thread, print
from time import sleep
from random import randint


class Lightswitch:
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, sem):
        self.mutex.lock()
        counter = self.counter
        self.counter += 1
        if self.counter == 1:
            sem.wait()
        self.mutex.unlock()
        return counter

    def unlock(self, sem):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            sem.signal()
        self.mutex.unlock()


def init():
    access_data = Semaphore(1)
    turnstile = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_sensor = Lightswitch()
    valid_data = Event()

    for monitor_id in range(2):
        Thread(monitor, monitor_id, valid_data, turnstile, ls_monitor, access_data)
    for sensor_id in range(11):
        Thread(sensor, sensor_id, valid_data, turnstile, ls_sensor, access_data)


def monitor(monitor_id, valid_data, turnstile, ls_monitor, access_data):
    valid_data.wait()

    while True:
        sleep(0.5)
        turnstile.wait()
        number_reading_monitors = ls_monitor.lock(access_data)
        turnstile.signal()

        print(f'monit "{monitor_id:02d}": '
              f'pocet citajucich monitorov={number_reading_monitors:2d}\n')
        ls_monitor.unlock(access_data)


def sensor(sensor_id, valid_data, turnstile, ls_sensor, access_data):
    while True:
        turnstile.wait()
        turnstile.signal()

        number_writing_sensors = ls_sensor.lock(access_data)
        writing_time = randint(10, 15) / 1000

        print(f'cidlo"{sensor_id:02d}": '
              f'pocet zapisujucich cidiel= {number_writing_sensors:02d}, '
              f'trvanie zapisu={writing_time:5.3f} \n')
        sleep(writing_time)
        valid_data.signal()
        ls_sensor.unlock(access_data)


if __name__ == '__main__':
    init()
