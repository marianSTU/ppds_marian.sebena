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
    Using async programming.

Data Copyright: NHL and the NHL Shield are registered trademarks of the
    National Hockey League. NHL and NHL team marks are the property of
    the NHL and its teams. © NHL 2022. All Rights Reserved.
"""
import aiohttp
import asyncio
import time


async def get_franchise(queue, task_id):
    """
    Native coroutine that make a async get request to gain data
    about NHL Team with team_id. This id get from queue

    :param queue: queue with NHL teams id from 1 to 39
    :param task_id: identification of currently running task
    :return:
    """
    while not queue.empty():
        url = await queue.get()

        time_start = time.perf_counter()
        print(f'TASK ID: {task_id} RUNS')

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                franchise = await resp.json()
                print(f'TASK ID: {task_id} '
                      f'OUTPUT: Team name: {franchise["franchises"][0]["teamName"]} '
                      f'Location: {franchise["franchises"][0]["locationName"]} '
                      f'EXECUTION TIME: {time.perf_counter() - time_start:.1f}s')


async def main():
    """
    Main function of application count execution time,
    fill work queue and runs tasks

    :return:
    """
    start_time = time.time()
    work_queue = asyncio.Queue()

    for team_id in range(1, 40):
        url = f'https://statsapi.web.nhl.com/api/v1/franchises/{team_id}'
        await work_queue.put(url)

    await asyncio.gather(
        get_franchise(work_queue, "[0]"),
        get_franchise(work_queue, "[1]"),
    )
    print(f'Program execution time {time.time() - start_time} seconds')


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
