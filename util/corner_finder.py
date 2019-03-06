"""
This utility class is used to calculate the actual location of the corners of the table.
Since the camera is not fixed in a 100% correct angle, we want to locate the corners to be able to do a transformation
of the images. This helps getting a better representation of the environment.

The main function is calculate_corners. Using the center of the board and a row of players, it calculates the
location of the corners.
"""
import cv2
import numpy as np
import math


def calculate_linear_parameters(p1, p2):
    """
    Simple helper function to calculate a and b in the linear function y=ax+b
    :param p1: Point one on the line
    :param p2: Point two on the line
    :return: a and b in y=ax+b
    """
    # y = ax + b
    # a = (y2-y1)/(x2-x1)
    a = (p2[1] - p1[1]) / (p2[0] - p1[0])
    # b = y - ax
    b = p1[1] - a * p1[0]

    return a, b


def angle_between(v1, v2):
    """
    We use the fact that atan2(x1*y2-y1*x2,x1*x2+y1*y2) calculates the angle in a range from -180 to 180.
    In other words we both get the angle and direction.
    """
    return math.atan2(v1[0] * v2[1] - v1[1] * v2[0], v1[0] * v2[0] + v1[1] * v2[1])


def rotate_vector(vector, radians):
    """
    Rotate a vector by an angle using the formula:
    * x' = x cos θ − y sin θ
    * y' = x sin θ + y cos θ

    :param vector: The vector to rotate
    :param radians: The angle in radians
    :return: A rotated vector
    """

    return np.array([
        vector[0] * np.cos(radians) - vector[1] * np.sin(radians),
        vector[0] * np.sin(radians) + vector[1] * np.cos(radians)
    ])


def rotate90_and_extend(vector, extension_length):
    """
    Rotate a vector 90 degrees and change its length. This is used to 'jump' from corner to corner.
    :param vector: The vector to be rotated
    :param extension_length: The new length
    :return: A rotated and extended vector
    """
    vec_length = np.linalg.norm(vector)
    extension = extension_length / vec_length

    return np.array([-vector[1], vector[0]]) * extension


def calculate_corners(center, player_row, board_shape, image_shape, canvas=None, debug=False):
    board_width = board_shape[0]
    board_height = board_shape[1]

    image_height = image_shape[1]

    # calculate a and b from y=ax+b using first and last player in row
    a, b = calculate_linear_parameters(player_row[0], player_row[-1])

    # create vector from top to bottom of screen going through the players
    # - the actual rotation of the board
    player_top = np.array([-b / a, 0])
    player_bottom = np.array([(image_height - b) / a, image_height])

    if canvas is not None:
        cv2.line(canvas, pt1=tuple(player_top.astype(int)), pt2=tuple(player_bottom.astype(int)), color=(255, 255, 120), thickness=1)

    # vertical line to calculate angle
    vertical_top = np.array([player_row[0][0], 0])
    vertical_bottom = np.array([player_row[0][0], image_height])

    if canvas is not None:
        cv2.line(image, pt1=tuple(vertical_top.astype(int)), pt2=tuple(vertical_bottom.astype(int)), color=(255, 255, 120), thickness=1)

    # angle between true rotation and vertical
    angle = angle_between(vertical_top - vertical_bottom, player_top - player_bottom)

    if debug:
        print("Radians=%s\nDegrees=%s" % (angle, angle * 180 / math.pi))
    if canvas is not None:
        cv2.line(image,
                 pt1=(center[0], center[1]),
                 pt2=(center[0], int(center[1] - (board_height / 2))),
                 color=(120, 255, 255), thickness=1)

    # vector from center, extended vertically to the top
    top_middle = np.array([center[0], int(center[1] - (board_height / 2))])
    vec = center - top_middle

    # rotate this vector using calculated true angle
    rotated_vec = rotate_vector(vec, angle)
    if debug:
        print("Rotated vector: %s" % (rotated_vec,))

    # find the actual middle point of the top border of the table
    corrected_line_center = center - rotated_vec

    if canvas is not None:
        cv2.circle(image, tuple(corrected_line_center.astype(int)), 2, (255, 180, 255), 2)
        cv2.line(image, pt1=tuple(center.astype(int)), pt2=tuple(corrected_line_center.astype(int)),
                 color=(180, 255, 255), thickness=2)

    # calculate all the corners by continuously rotating 90 degrees and adjusting the vector length
    tl_rot = corrected_line_center + rotate90_and_extend(rotated_vec, board_width / 2) #* [1, -1]
    bl_rot = tl_rot + rotate90_and_extend(corrected_line_center - tl_rot, board_height)
    br_rot = bl_rot + rotate90_and_extend(tl_rot - bl_rot, board_width)
    tr_rot = br_rot + rotate90_and_extend(bl_rot - br_rot, board_height)

    if canvas is not None:
        cv2.circle(image, tuple(tl_rot.astype(int)), 2, (255, 180, 255), 2)
        cv2.line(image, pt1=tuple(corrected_line_center.astype(int)), pt2=tuple(tl_rot.astype(int)), color=(180, 255, 255), thickness=2)
        cv2.circle(image, tuple(bl_rot.astype(int)), 2, (255, 180, 255), 2)
        cv2.line(image, pt1=tuple(tl_rot.astype(int)), pt2=tuple(bl_rot.astype(int)), color=(180, 255, 255), thickness=2)
        cv2.circle(image, tuple(br_rot.astype(int)), 2, (255, 180, 255), 2)
        cv2.line(image, pt1=tuple(bl_rot.astype(int)), pt2=tuple(br_rot.astype(int)), color=(180, 255, 255), thickness=2)
        cv2.circle(image, tuple(tr_rot.astype(int)), 2, (255, 180, 255), 2)
        cv2.line(image, pt1=tuple(br_rot.astype(int)), pt2=tuple(tr_rot.astype(int)), color=(180, 255, 255), thickness=2)

    if debug:
        print("TL 2: %s" % (tl_rot,))
        print("BL 2: %s" % (bl_rot,))
        print("BR 2: %s" % (br_rot,))
        print("TR 2: %s" % (tr_rot,))

    return tl, tr, br, bl


if __name__ == "__main__":
    image = np.zeros((250, 400, 3), np.uint8)

    mode = 1

    # two different board positions, rotated different way
    if mode == 1:
        tl = (2, 20)
        tr = (380, 4)
        br = (399, 214)
        bl = (21, 230)

        p1 = (252, 40)
        p2 = (255, 110)
        p3 = (258, 180)

    else:
        tl = (21, 4)
        tr = (399, 20)
        br = (380, 230)
        bl = (2, 214)

        p1 = (258, 40)
        p2 = (255, 110)
        p3 = (252, 180)

    # calculate the actual board size based on the coordinates
    WIDTH = math.sqrt((tr[0] - tl[0])**2 + (tr[1] - tl[1])**2)
    HEIGHT = math.sqrt((bl[0] - tl[0])**2 + (bl[1] - tl[1])**2)

    print("SIZE=(%s,%s)" % (WIDTH, HEIGHT))

    center = np.array([197, 119])

    # draw the board
    corners = [tl, tr, br, bl]
    for i in range(len(corners)):
        p = corners[i]
        p_next = corners[(i + 1) % len(corners)]
        cv2.circle(image, (p[0], p[1]), 2, (120, 255, 255), 2)
        cv2.line(image, pt1=(p[0], p[1]), pt2=(p_next[0], p_next[1]), color=(70, 255, 255), thickness=1)

    cv2.circle(image, (center[0], center[1]), 10, (120, 255, 255), 2)

    for p in [p1, p2, p3]:
        cv2.circle(image, (p[0], p[1]), 2, (255, 120, 255), 2)

    # calculate corners (and draw them)
    tl, tr, br, bl = calculate_corners(center, [p1, p2, p3], (WIDTH, HEIGHT), (400, 250), image, True)

    # show the result
    while True:
        cv2.imshow('Image', image)
        cv2.waitKey(1000)
