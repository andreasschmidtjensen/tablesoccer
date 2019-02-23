from darknet import performDetect
import cv2
import os

#darknet.exe detector test data/coco.data yolov3.cfg yolov3.weights -i 0 -thresh 0.25 dog.jpg -ext_output

DARKNET_DIR = os.environ['DARKNET_DIR']
print("DD: %s" % DARKNET_DIR)

os.chdir(DARKNET_DIR)

image_name = DARKNET_DIR + "/dog.jpg"
config = DARKNET_DIR + "/yolov3.cfg"
weights = DARKNET_DIR + "/yolov3.weights"
data = DARKNET_DIR + "/data/coco.data"

image = cv2.imread(image_name)
result = performDetect(image, makeImageOnly=True, configPath=config, weightPath=weights, metaPath=data)

cv2.imshow('YOLO', result["image"])
cv2.waitKey(0)
input('')

