"""
Credit: https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
"""
from imutils.video import VideoStream
import imutils
import cv2


class MotionDetector:
    def __init__(self, source, min_area=500):
        self.min_area = min_area

        self.vs = VideoStream(src=source).start()
        self.baseline = None  # baseline frame
        self.latest_frame = None  # for snapshot
        self.latest_diff = None  # for snapshot
        self.update_baseline()

    def __get_frame(self):
        frame = self.vs.read()
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        return gray

    def update_baseline(self):
        """
        Read from camera and take the content as the 'baseline', i.e. without anything in the picture.
        We use this baseline to calculate if something new is in the picture.
        """
        self.baseline = self.__get_frame()

    def motion_detected(self):
        self.latest_frame = self.__get_frame()
        frame = self.latest_frame

        # compute the absolute difference between the current frame and first frame
        frameDelta = cv2.absdiff(self.baseline, frame)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the threshold image to fill in holes, then find contours on threshold image
        thresh = cv2.dilate(thresh, None, iterations=2)

        self.latest_diff = thresh

        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        for c in contours:
            if cv2.contourArea(c) >= self.min_area:
                return True

        return False
