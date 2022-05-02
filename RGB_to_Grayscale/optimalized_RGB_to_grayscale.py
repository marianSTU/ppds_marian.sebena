"""
Authors: Mgr. Ing. Matúš Jókay, PhD.
         Ing. Roderik Plozsek
         Bc. Marián Šebeňa
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
"""

from __future__ import division
import time
from numba import cuda
import math
import matplotlib.pyplot as plt
import numpy as np

ARRAYS = 6


@cuda.jit
def my_kernel_2d(data):
    """
    Function converts pixels from RGB to grayscale using GPU
    by NTSC formula: 0.299 ∙ Red + 0.587 ∙ Green + 0.114 ∙ Blue.
    :param data: image converted to array
    :return:
    """
    x, y = cuda.grid(2)
    x_max, y_max, rgb = data.shape

    if x < x_max and y < y_max:
        data[x][y] = 0.299 * data[x][y][0] + 0.587 * data[x][y][1] + 0.114 * data[x][y][2]


def main():
    """
    Main function of programs reads image to array,
    declare threads per block, blocks axis per grid,
    declare streams, secure data sending between device
    and host, count execution time by events for each stream
    and secure async run
    :return:
    """
    img_array = plt.imread("imgs_to_process/large.jpg")
    # image array will be split to 6 smaller arrays
    data = [[], [], [], [], [], []]
    data_gpu = []
    gpu_out = []
    streams = []
    start_events = []
    end_events = []
    arrays_len = len(img_array) / ARRAYS
    k = 0
    cnt = 0

    for x in range(len(img_array)):
        if cnt == arrays_len:
            k += 1
            cnt = 0
        cnt += 1
        data[k].append(img_array[x])

    for _ in range(ARRAYS):
        streams.append(cuda.stream())
        start_events.append(cuda.event())
        end_events.append(cuda.event())

    for k in range(ARRAYS):
        data_gpu.append(cuda.to_device(data[k], stream=streams[k]))

    start = time.time()
    tpb = (32, 32)
    bpg_x = math.ceil(img_array.shape[0] / tpb[0])
    bpg_y = math.ceil(img_array.shape[1] / tpb[1])
    bpg = (bpg_x, bpg_y)

    for k in range(ARRAYS):
        start_events[k].record(streams[k])
        my_kernel_2d[bpg, tpb, streams[k]](data_gpu[k])

    for k in range(ARRAYS):
        end_events[k].record(streams[k])

    for k in range(ARRAYS):
        gpu_out.append(data_gpu[k].copy_to_host(stream=streams[k]))

    kernel_times = []

    for k in range(ARRAYS):
        kernel_times.append(cuda.event_elapsed_time(start_events[k], end_events[k]))

    print(f'Program duration: {time.time() - start}s')
    print('Mean kernel duration : %f ms' % np.mean(kernel_times))
    print('Mean kernel standard deviation : %f ms' % np.std(kernel_times))


if __name__ == '__main__':
    main()
