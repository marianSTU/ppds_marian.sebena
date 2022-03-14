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
    # synchronization objects initialization
    access_data = Semaphore(1)
    turnstile = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_sensor = Lightswitch()
    valid_data_h = Event()
    valid_data_p = Event()
    valid_data_t = Event()

    # threads creating
    for monitor_id in range(8):
        Thread(monitor, monitor_id, valid_data_h,
               valid_data_p, valid_data_t, turnstile,
               ls_monitor, access_data)
    for sensor_id in range(3):
        Thread(sensor, sensor_id, valid_data_h,
               valid_data_p, valid_data_t, turnstile,
               ls_sensor, access_data)


def monitor(monitor_id, valid_data_h, valid_data_p,
            valid_data_t, turnstile, ls_monitor, access_data):
    """
        Function represents monitor in power nuclear station.

        :parameter monitor_id: identification number of monitor thread
        :parameter valid_data_h: event object
                                 validate control rod insertion depth
        :parameter valid_data_p: event object
                                 validate coolant flow
        :parameter valid_data_t: event object
                                 validate coolant temperature
        :parameter turnstile: semaphore object
        :parameter ls_monitor: lightswitch object
        :parameter access_data: semaphore object
    """

    # control if all sensors collected data
    valid_data_p.wait()
    valid_data_t.wait()
    valid_data_h.wait()

    while True:
        sleep(randint(40, 50) / 1000)
        turnstile.wait()
        number_reading_monitors = ls_monitor.lock(access_data)
        turnstile.signal()

        print(f'monitor_id "{monitor_id:02d}": '
              f'reading monitors number ={number_reading_monitors:2d}')
        ls_monitor.unlock(access_data)


def sensor(sensor_id, valid_data_h, valid_data_p,
           valid_data_t, turnstile, ls_sensor, access_data):
    """
        Function represents data collecting sensor in power
        nuclear station.

        :parameter sensor_id: identification number of sensor thread
        :parameter valid_data_h: event object
                                 validate control rod insertion depth
        :parameter valid_data_p: event object
                                 validate coolant flow
        :parameter valid_data_t: event object
                                 validate coolant temperature
        :parameter turnstile: semaphore object
        :parameter ls_sensor: lightswitch object
        :parameter access_data: semaphore object
    """

    while True:
        # time to next actualization
        sleep(randint(50, 60) / 1000)
        turnstile.wait()
        turnstile.signal()

        number_writing_sensors = ls_sensor.lock(access_data)
        # sensor with id 0 is control rod insertion depth sensor
        # with 20/25ms writing time
        if sensor_id == 0:
            writing_time = randint(20, 25) / 1000
        else:
            writing_time = randint(10, 20) / 1000

        print(f'sensor_id"{sensor_id:02d}": '
              f'writing sensors number= {number_writing_sensors:02d},'
              f'writing time={writing_time:5.3f}')
        # actualization time
        sleep(writing_time)

        # after when all sensors collects data monitor could continue
        if sensor_id == 0:
            valid_data_h.signal()
        if sensor_id == 1:
            valid_data_t.signal()
        if sensor_id == 2:
            valid_data_p.signal()

        ls_sensor.unlock(access_data)


if __name__ == '__main__':
    init()
