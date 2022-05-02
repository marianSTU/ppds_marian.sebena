"""
Authors: Mgr. Ing. Matúš Jókay, PhD.
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
    Main function of programs reads image to np array,
    declare threads per block, blocks axis per grid,
    count execution time and show converted image
    :return:
    """
    img_array = plt.imread("imgs_to_process/large.jpg")
    start = time.time()

    tpb = (32, 32)
    bpg_x = math.ceil(img_array.shape[0] / tpb[0])
    bpg_y = math.ceil(img_array.shape[1] / tpb[1])
    bpg = (bpg_x, bpg_y)
    my_kernel_2d[bpg, tpb](img_array)
    print(f'Execution time with cuda {time.time()-start}s')

    plt.imshow(img_array)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    main()