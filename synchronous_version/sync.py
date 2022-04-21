"""
Authors: Mgr. Ing. Matúš Jókay, PhD.
         Bc. Marián Šebeňa
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT

Application description: Printing all NHL teams(1918 to present) and
    their location from JSON available on website
    https://statsapi.web.nhl.com/api/v1/franchises/.
    Using sync programming.

Data Copyright: NHL and the NHL Shield are registered trademarks of the
    National Hockey League. NHL and NHL team marks are the property of
    the NHL and its teams. © NHL 2022. All Rights Reserved.
"""
import requests
import time


def get_franchise(team_id, task_id):
    """
    Coroutine that make a get request to gain data
    about NHL Team with team_id. Counts time of
    every request

    :param team_id: NHL team_id from 1 to 39
    :param task_id: identification of currently running task
    :return:
    """
    x = time.time()
    print(f'TASK ID: {task_id} RUNS')
    url = f'https://statsapi.web.nhl.com/api/v1/franchises/{team_id}'
    resp = requests.get(url)
    franchise = resp.json()
    print(f'TASK ID: {task_id} '
          f'OUTPUT: Team name: {franchise["franchises"][0]["teamName"]} '
          f'Location: {franchise["franchises"][0]["locationName"]} '
          f'EXECUTION TIME: {time.time() - x}s')


def main():
    """
    Main function of application count execution time
    and runs tasks
    :return:
    """
    start = time.time()
    for team_id in range(1, 40, 2):
        get_franchise(team_id, "[0]")
        # Secures last iteration, because there is not team with id = 41
        if team_id + 1 < 40:
            get_franchise(team_id + 1, "[1]")
    print(f'Program execution time {time.time() - start} seconds')


if __name__ == "__main__":
    main()
