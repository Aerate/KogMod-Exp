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
parser.add_argument('-l', '--load_randoms', type=bool, default=True,
                    help='Wheter to load existing random values or not')
FLAGS = parser.parse_args()

def create_stimuli():
    """
    Creates a set of original + distorted point picture stimuli according to the given configuration parameters
    :return: Avergae distortion over all distorted images
    """
    origin_points_x, origin_points_y = create_origin_points()
    plot_stimuli(origin_points_x, origin_points_y, FLAGS.original + "_original")

    sum_distortion_all_pics = 0.0
    for i in range(0, FLAGS.num_distortions):
        distorted_points_x, distorted_points_y, average_distortion = distort_points(origin_points_x, origin_points_y)
        avgdis_string = "%.2f" % average_distortion
        plot_stimuli(distorted_points_x, distorted_points_y, FLAGS.original + "_distorted_l" +
                     str(FLAGS.distortion_level) + "_avgDis(" + avgdis_string + ")_" + str(i))
        sum_distortion_all_pics += average_distortion

    return sum_distortion_all_pics / FLAGS.num_distortions


def create_origin_points():
    """
    Definition of original point data.
    :return: Original point locations
    """
    if FLAGS.original == "triangle":
        return np.array([-9, -3, 3, 9, -6, 6, -3, 3, 0]), np.array([-9, -9, -9, -9, -3, -3, 3, 3, 9])
    if FLAGS.original == "diamond":
        return np.array([0, -5, 5, -10, 10, -5, 5, 0]), np.array([-10, -5, -5, 0, 0, 5, 5, 10])
    if FLAGS.original == "M":
        return np.array([-8, -8, -8, -4, 0, 4, 8, 8, 8]), np.array([-8, 0, 8, 4, 0, 4, 8, 0, -8])
    if FLAGS.original == "F":
        return np.array([-4, -4, -4, -4, -2, -2, 0, 0, 2]), np.array([-6, -2, 2, 6, 2, 6, 2, 6, 6])
    if FLAGS.original == "random":
        if FLAGS.load_randoms:
            if os.path.isfile('./xs.npy'):
                xs = np.load("./xs.npy")
            else:
                xs = np.random.randint(-15, 16, size=10)
                np.save("./xs.npy", xs)

            if os.path.isfile('./ys.npy'):
                ys = np.load("./ys.npy")
            else:
                ys = np.random.randint(-15, 16, size=10)
                np.save("./ys.npy", ys)

            return xs, ys
        else:
            xs = np.random.randint(-15, 16, size=10)
            ys = np.random.randint(-15, 16, size=10)
            np.save("./xs.npy", xs)
            np.save("./ys.npy", ys)
        return xs, ys


def plot_stimuli(x, y, name):
    """
    Plots point data as scatter plot.
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
    plt.figure(figsize=(8, 8), dpi=80)
    plt.axis("equal")
    plt.axis("off")
    plt.xticks([])
    plt.yticks([])
    plt.scatter(x_corner, y_corner, color='white')
    plt.scatter(x, y, color='black')
    plt.savefig(os.path.join(FLAGS.output_dir, name + "." + FLAGS.output_format))
    plt.gcf().clear()


def distort_points(xs, ys):
    """
    Distorts the given x/y coordinated according to probabilities given by the applied distortion level
    :param xs:
    :param ys:
    :return:
    """
    distorted_xs = np.copy(xs)
    distorted_ys = np.copy(ys)

    distortion_sum = 0.0

    if FLAGS.distortion_level <= 8:
        for i in range(0, len(xs)):
            distortion_offset_x, distortion_offset_y = get_distortion_offsets(FLAGS.distortion_level)
            distorted_xs[i] += distortion_offset_x
            distorted_ys[i] += distortion_offset_y
            distortion_sum += np.sqrt(np.square(distortion_offset_x) + np.square(distortion_offset_y))

    else:
        for i in range(0, len(xs)):
            #Equally probable redistribution within the 900 original cells (30x30 grid)
            distorted_xs[i] = np.random.randint(-15, 16)
            distorted_ys[i] = np.random.randint(-15, 16)
            distortion_sum += np.sqrt(np.square(xs[i] - distorted_xs[i]) + np.square(ys[i] - distorted_ys[i]))

    average_distortion = distortion_sum / len(xs)
    return distorted_xs, distorted_ys, average_distortion


def get_distortion_offsets(distortion_level):
    """
    Calculates distortion offset for single point according to the probabilities implied by the distortion level
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
            return generate_offset(2, 5)
        elif distortion_area == 4:
            return generate_offset(5, 10)

    elif distortion_level == 8:
        #Equally probable distortion within 400 cells
        x_offset = np.random.randint(-10, 11)
        y_offset = np.random.randint(-10, 11)
        return x_offset, y_offset


def get_distortion_area(distortion_level):
    """
    Randomly chooses applied distortion area implied by the probability table in
    https://www.researchgate.net/publication/17137983_Perceived_Distance_and_the_Classification_of_Distorted_Patterns
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

    rand = np.random.rand(1) * 1000
    counter = 0.0;
    for i in range(5):
        counter += probability_table[distortion_level - 1, i] * 1000
        if rand < counter:
            return i


def generate_offset(inner_bound, outer_bound):
    """
    Generates random offset such that the offset remains within the defined bounds
    (length of offset vector is greater than inner bound and smaller the outer bound)
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


def write_stats(avg_dis):
    file = open(os.path.join(FLAGS.output_dir, "stats.txt"), "w")
    file.write("Successfully created Stimuli: \n")
    file.write("\tOriginal Form: " + FLAGS.original + "\n")
    file.write("\tNumber of Distortion-Images: " + str(FLAGS.num_distortions) + "\n")
    file.write("\tDistortion Level: " + str(FLAGS.distortion_level) + "\n")
    file.write("Average distortion over all generated Images: \n")
    file.write("\t%.2f (Distance/Dot)" % avg_dis)
    file.close()


#Execute main
AVERAGE_DISTORTION = create_stimuli()
print("Successfully created Stimuli: ")
print("\tOriginal Form: " + FLAGS.original)
print("\tNumber of Distortion-Images: " + str(FLAGS.num_distortions))
print("\tDistortion Level: " + str(FLAGS.distortion_level))
print("Average distortion over all generated Images: ")
print("\t%.2f (Distance/Dot)" % AVERAGE_DISTORTION)
write_stats(AVERAGE_DISTORTION)
