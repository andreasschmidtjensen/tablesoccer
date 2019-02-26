# NOTE: Run this from parent directory (python test/webcam.py) to makesure tablesoccer.names is found
# this is based on: https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import cv2
from darknet import performDetect
import os
cwd = os.getcwd()

config = cwd + "/yolov3-tablesoccer.cfg"
weights = cwd + "/weights/yolov3-tablesoccer_last.weights"
data = cwd + "/tablesoccer.data"
thresh = 0.25

print(data)

vs = WebcamVideoStream(src=0).start()
fps = FPS().start()

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    result = performDetect(frame, thresh=thresh, makeImageOnly=True, configPath=config, weightPath=weights, metaPath=data)

    cv2.imshow('YOLO', cv2.cvtColor(result["image"], cv2.COLOR_BGR2RGB))
    cv2.waitKey(1)
    
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()