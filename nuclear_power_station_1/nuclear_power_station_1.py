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
    """
        LightSwitch object that represent change between more semaphores.
    """
    def __init__(self):
        """
            Initialize instance of class with mutex lock and counter
        """
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, sem):
        """
            Method Lock lock all threads in object of semaphore

                :parameter sem: object of semaphore
                :return counter: actual number of threads which have access to class instance
        """
        self.mutex.lock()
        counter = self.counter
        self.counter += 1
        if self.counter == 1:
            sem.wait()
        self.mutex.unlock()
        return counter

    def unlock(self, sem):
        """
            Method Lock lock all threads in object of semaphore

                :parameter sem: object of semaphore
        """
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            sem.signal()
        self.mutex.unlock()


def init():
    """
        Function init initialize basic synchronization objects and
        creates sensor/monitor threads.
    """

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
    """
        Function represents monitor in power nuclear station.
    
        :parameter monitor_id: identification number of monitor thread
        :parameter valid_data: event object
        :parameter turnstile: semaphore object
        :parameter ls_monitor: lightswitch object
        :parameter access_data: semaphore object
    """
    valid_data.wait()

    while True:
        sleep(0.5)
        turnstile.wait()
        number_reading_monitors = ls_monitor.lock(access_data)
        turnstile.signal()

        print(f'monitor_id "{monitor_id:02d}": '
              f'number of reading monitors ={number_reading_monitors:2d}\n')
        ls_monitor.unlock(access_data)


def sensor(sensor_id, valid_data, turnstile, ls_sensor, access_data):
    """
            Function represents data collecting sensor in power nuclear station.

            :parameter sensor_id: identification number of sensor thread
            :parameter valid_data: event object
            :parameter turnstile: semaphore object
            :parameter ls_sensor: lightswitch object
            :parameter access_data: semaphore object
        """
    while True:
        turnstile.wait()
        turnstile.signal()

        number_writing_sensors = ls_sensor.lock(access_data)
        writing_time = randint(10, 15) / 1000

        print(f'sensor_id"{sensor_id:02d}": '
              f'number of writing sensors= {number_writing_sensors:02d}, '
              f'writing time={writing_time:5.3f} \n')
        sleep(writing_time)
        valid_data.signal()
        ls_sensor.unlock(access_data)


if __name__ == '__main__':
    init()
