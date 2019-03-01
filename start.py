import os

import cv2
import imutils
from imutils.video import WebcamVideoStream, FPS
import numpy as np

from tablesoccer import SoccerField
from yolo.test import darknet
from util.camera import get_image


def setup_window(name, x, y):
    cv2.namedWindow(name)
    cv2.moveWindow(name, x, y)


setup_window("CNN", 0, 0)
setup_window("Environment", 0, 500)
setup_window("Statistics", 500, 0)

playing = True

cwd = os.getcwd() + "/yolo"
os.chdir(cwd)

CONFIG = cwd + "/yolov3-tablesoccer.cfg"
WEIGHTS = cwd + "/model/tablesoccer-v1.weights"
DATA = cwd + "/tablesoccer.data"
THRESH = 0.25

source_type = 'video'
path = '/Users/asj/Downloads/tracking-example.mp4'

if source_type == 'webcam':
    source = WebcamVideoStream(int(path)).start()
elif source_type == 'video':
    source = cv2.VideoCapture(path)
else:
    raise NameError("Unknown source_type: %s" % source_type)

fps = FPS().start()

field = SoccerField()

while True:
    for i in range(10):
        frame = get_image(source)
    frame = imutils.resize(frame, width=400)

    result = darknet.performDetect(frame, thresh=THRESH, makeImageOnly=True, configPath=CONFIG, weightPath=WEIGHTS,
                                   metaPath=DATA)

    img = cv2.cvtColor(result["image"], cv2.COLOR_BGR2RGB)
    cv2.imshow('CNN', img)
    field.calc_field(result["detections"])

    env = np.zeros((250, 400, 3), np.uint8)
    env = field.draw(env)

    cv2.imshow('Environment', env)

    cv2.waitKey(1)
