import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('-dl', '--distortion_level', type=int, default=4, help='Intensity Level of Distortion (1 - 9), Note: 7.7, 8.6, 9.7 are denoted as 7,8,9 respectively')
parser.add_argument('-f', '--output_format', type=str, default="svg", help='Output Format, supported: svg or png')
parser.add_argument('-dir', '--output_dir', type=str, default="./output", help='Output Location of Stimuli Images')
parser.add_argument('-o', '--original', type=str, default="triangle", help='Original Form, supported: triangle, diamond, M, F, rand')
parser.add_argument('-nd', '--num_distortions', type=int, default=10, help='Number of Distortion Images to create (default 10)')
FLAGS = parser.parse_args()

origin_dimension = 30

def create_stimuli():
    """

    :return:
    """
    origin_points_x, origin_points_y = create_origin_points()
    plot_stimuli(origin_points_x, origin_points_y, FLAGS.original + "_original")

    for i in range(0, FLAGS.num_distortions):
        distorted_points_x, distorted_points_y = distort_points(origin_points_x, origin_points_y)
        plot_stimuli(distorted_points_x, distorted_points_y, FLAGS.original + "_distorted_l" + str(FLAGS.distortion_level)+ "_" + str(i))


def create_origin_points():
    """

    :return:
    """
    if FLAGS.original == "triangle":
        return np.array([-9, -3, 3, 9, -6, 6, -3, 3, 0]), np.array([-9, -9, -9, -9, -3, -3, 3, 3, 9])


def plot_stimuli(x, y, name):
    """

    :param x:
    :param y:
    :return:
    """
    if not os.path.exists(FLAGS.output_dir):
        os.makedirs(FLAGS.output_dir)

    plt.axis("equal")
    plt.axis("off")
    plt.scatter(x, y)
    plt.savefig(os.path.join(FLAGS.output_dir, name + "." + FLAGS.output_format))

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
        distortion_area = get_distortion_area(FLAGS.distortion_level - 1)
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