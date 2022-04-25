"""
Authors: Bc. Marián Šebeňa
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2022
License: MIT
"""
import time
import matplotlib.pyplot as plt


def grayscale(img_array):
    """
    Function converts pixels from RGB to grayscale
    by NTSC formula: 0.299 ∙ Red + 0.587 ∙ Green + 0.114 ∙ Blue.
    :param img_array: image converted to array
    :return:
    """
    for x in range(len(img_array)):
        for y in range(len(img_array[0])):
            img_array[x][y] = 0.299 * img_array[x][y][0] + \
                              0.587 * img_array[x][y][1] + \
                              0.114 * img_array[x][y][2]


def main():
    """
    Main function of programs reads image
    to np array, count execution time and
    show converted image

    :return:
    """
    img_array = plt.imread("imgs_to_process/my_team.jpg")

    start = time.time()
    grayscale(img_array)
    print(f'Execution time on CPU {time.time()-start}s')

    plt.imshow(img_array)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    main()
