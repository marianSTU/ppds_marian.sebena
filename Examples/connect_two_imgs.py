"""
Authors: Mgr. Ing. Matúš Jókay, PhD.
         Bc. Marián Šebeňa
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
"""
from __future__ import division
from numba import cuda
import math
import matplotlib.pyplot as plt


@cuda.jit
def my_kernel_2d(data1, data2):
    """
    Function count average RGB pixels values on
    pixels with equal index

    :param data1: image 1 converted to array
    :param data2: image 2 converted to array
    :return:
    """
    x, y = cuda.grid(2)
    x_max, y_max, z = data1.shape

    if x < x_max and y < y_max:
        data1[x][y][0] = (data2[x][y][0] + data1[x][y][0]) / 2
        data1[x][y][1] = (data2[x][y][1] + data1[x][y][1]) / 2
        data1[x][y][2] = (data2[x][y][2] + data1[x][y][2]) / 2


def main():
    """
    Main function of program reads image to np array,
    declare threads per block, blocks axis per grid
     and show converted image

    :return:
    """
    img_array = plt.imread("imgs_to_process/my_team.jpg")
    img_array2 = plt.imread("imgs_to_process/vnt.jpg")

    tpb = (16, 16)

    bpg_x = math.ceil(img_array.shape[0] / tpb[0])
    bpg_y = math.ceil(img_array.shape[1] / tpb[1])
    bpg = (bpg_x, bpg_y)

    my_kernel_2d[bpg, tpb](img_array, img_array2)

    plt.imshow(img_array)
    plt.axis('off')
    plt.show()

main()
