import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--distortion_level', type=int, default=4, help='Intensity Level of Distortion')
FLAGS = parser.parse_args()

origin_dimension = 30

def create_stimuli():
    """

    :return:
    """
    number_of_points = origin_dimension * origin_dimension

    origin_points_x, origin_points_y = create_origin_points()

    distorted_points_x, distorted_points_y = distort_points(origin_points_x, origin_points_y)


    #final_plus_corner_x = np.append(origin_points_x,[-25,-25,25,25,-15,-15,15,15])
    #final_plus_corner_y = np.append(origin_points_y,[-25,25,-25,25,-15,15,-15,15])

    # Plot
    plot_stimuli(origin_points_x, origin_points_y, "original.png")
    plot_stimuli(distorted_points_x, distorted_points_y, "distorted.png")


def create_origin_points():
    """

    :return:
    """
    return np.array([-9, -3, 3, 9, -6, 6, -3, 3, 0]), np.array([-9, -9, -9, -9, -3, -3, 3, 3, 9])

def plot_stimuli(x, y, name):
    """

    :param x:
    :param y:
    :return:
    """
    plt.axis("equal")
    plt.axis("off")
    plt.scatter(x, y)
    plt.savefig(name)
    plt.gcf().clear()


def distort_points(xs, ys):
    """

    :param x:
    :param y:
    :return:
    """
    distorted_xs = np.copy(xs)
    distorted_ys = np.copy(ys)

    for i in range(0, len(xs)):
        distortion_area = get_distortion_area(3)
        distortion_offset_x, distortion_offset_y = get_distortion_offsets(distortion_area)
        distorted_xs[i] += distortion_offset_x
        distorted_ys[i] += distortion_offset_y

    return distorted_xs, distorted_ys

def get_distortion_area(distortion_level):
    """

    :param distorion_level:
    :return:
    """
    #Probability Table after
    probability_table = np.array([[.88, .1, .015, .004, .001],
                                 [.75, .15, .05, .03, .02],
                                 [.59, .20, .16, .03, .02],
                                 [.36, .48, .06, .05, .05],
                                 [.2, .3, .4, .05, .05],
                                 [0, .4, .32, .15, .13],
                                 [0, .24, .16, .3, .3]])
    table_index = 2
    rand = np.random.rand(1) * 1000
    counter = 0.0;
    for i in range(5):
        counter += probability_table[table_index,i] * 1000
        if rand < counter:
            return i


def get_distortion_offsets(distortion_area):
    """

    :param distortion_point:
    :return:
    """

    if distortion_area == 0:
        return 0,0
    elif distortion_area == 1:
        return generate_offset(0, 1)
    elif distortion_area == 2:
        return generate_offset(1, 2)
    elif distortion_area == 3:
        return generate_offset(2, 5)
    elif distortion_area == 4:
        return generate_offset(5,10)
    elif distortion_area == 5:
        return generate_offset(10,20)

def generate_offset(inner_bound, outer_bound):
    """

    :param inner_bound:
    :param outer_bound:
    :return:
    """
    offset_found = False
    if inner_bound == 0:
        while not offset_found:
            x_offset = np.random.randint(-outer_bound, outer_bound + 1)
            y_offset = np.random.randint(-outer_bound, outer_bound + 1)
            if not (x_offset == 0 and y_offset == 0):
                return x_offset, y_offset


    while not offset_found:
        x_offset = np.random.randint(-outer_bound, outer_bound + 1)
        y_offset = np.random.randint(-outer_bound, outer_bound + 1)

        if not ((x_offset <= inner_bound and x_offset >= -inner_bound) and (y_offset <= inner_bound and y_offset >= -inner_bound)):
            return x_offset, y_offset


create_stimuli()