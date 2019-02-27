# NOTE: Run this from parent directory (python test/webcam.py) to makesure tablesoccer.names is found
# this is based on: https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import cv2
import darknet
import os
cwd = os.getcwd()

config = cwd + "/yolov3-tablesoccer.cfg"
weights = cwd + "/weights/yolov3-tablesoccer_6000.weights"
data = cwd + "/tablesoccer.data"
thresh = 0.25

vs = WebcamVideoStream(src=0).start()
fps = FPS().start()

try:
    netMain = darknet.load_net_custom(config.encode("ascii"), weights.encode("ascii"), 0, 1)
    out = cv2.VideoWriter(
                "output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30.0,
                (darknet.network_width(netMain), darknet.network_height(netMain)))

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        result = darknet.performDetect(frame, thresh=thresh, makeImageOnly=True, configPath=config, weightPath=weights, metaPath=data)

        img = cv2.cvtColor(result["image"], cv2.COLOR_BGR2RGB)
        cv2.imshow('YOLO', img)
        cv2.waitKey(1)

        out.write(img)
        
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

finally:   
    out.release()
    cv2.destroyAllWindows()
    vs.stop()