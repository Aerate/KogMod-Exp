import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('-dl', '--distortion_level', type=int, default=4,
                    help='Intensity Level of Distortion (1 - 9), Note: 7.7, 8.6, 9.7 are denoted as 7,8,9 respectively')
parser.add_argument('-f', '--output_format', type=str, default="svg",
                    help='Output Format, supported: svg or png')
parser.add_argument('-dir', '--output_dir', type=str, default="./examples",
                    help='Output Location of Stimuli Images')
parser.add_argument('-o', '--original', type=str, default="triangle",
                    help='Original Form, supported: triangle, diamond, M, F, rand')
parser.add_argument('-nd', '--num_distortions', type=int, default=10,
                    help='Number of Distortion Images to create (default 10)')
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
        plot_stimuli(distorted_points_x, distorted_points_y, FLAGS.original + "_distorted_l" +
                     str(FLAGS.distortion_level)+ "_" + str(i))


def create_origin_points():
    """

    :return:
    """
    if FLAGS.original == "triangle":
        return np.array([-9, -3, 3, 9, -6, 6, -3, 3, 0]), np.array([-9, -9, -9, -9, -3, -3, 3, 3, 9])
    if FLAGS.original == "diamond":
        return np.array([0, -5, 5, -10, 10, -5, 5, 0]), np.array([-10, -5, -5, 0, 0, 5, 5, 10])
    if FLAGS.original == "M":
        return np.array([-8, -8, -8, -4, 0, 4, 8, 8, 8]), np.array([-8, 0, 8, 4, 0, 4, 8, 0, -8])
    if FLAGS.original == "F":
        return np.array([-6, -6, -6, -6, -2, -2, 2, 2, 6]), np.array([-6, -2, 2, 6, 2, 6, 2, 6, 6])
    if FLAGS.original == "random":
        return np.random.randint(-15, 16, size=10), np.random.randint(-15, 16, size=10)


def plot_stimuli(x, y, name):
    """

    :param x:
    :param y:
    :param name:
    :return:
    """
    if not os.path.exists(FLAGS.output_dir):
        os.makedirs(FLAGS.output_dir)

    x_corner = np.array([-25, -25, 25, 25])
    y_corner = np.array([-25, 25, -25, 25])

    axes = plt.gca()
    axes.set_xlim([-25, 25])
    axes.set_ylim([-25, 25])
    plt.axis("equal")
    plt.axis("off")
    plt.xticks([])
    plt.yticks([])
    plt.scatter(x, y, color='black')
    plt.scatter(x_corner, y_corner, color='white')
    plt.savefig(os.path.join(FLAGS.output_dir, name + "." + FLAGS.output_format))
    plt.gcf().clear()


def distort_points(xs, ys):
    """

    :param xs:
    :param ys:
    :return:
    """
    distorted_xs = np.copy(xs)
    distorted_ys = np.copy(ys)

    for i in range(0, len(xs)):
        distortion_offset_x, distortion_offset_y = get_distortion_offsets(FLAGS.distortion_level)
        distorted_xs[i] += distortion_offset_x
        distorted_ys[i] += distortion_offset_y

    return distorted_xs, distorted_ys


def get_distortion_offsets(distortion_level):
    """

    :param distortion_level:
    :return:
    """

    if distortion_level <= 7:
        distortion_area = get_distortion_area(distortion_level)

        if distortion_area == 0:
            return 0, 0
        elif distortion_area == 1:
            return generate_offset(0, 1)
        elif distortion_area == 2:
            return generate_offset(1, 2)
        elif distortion_area == 3:
            return generate_offset(2, 10)
        elif distortion_area == 4:
            return generate_offset(10, 20)


def get_distortion_area(distortion_level):
    """

    :param distortion_level:
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


#Execute main
create_stimuli()
print("Successfully created Stimuli: " + FLAGS.original)
