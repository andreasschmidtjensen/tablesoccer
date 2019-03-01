import cv2
import imutils


def get_image(source):
    frame = source.read()

    if type(frame) == tuple:
        if frame[0]:
            frame = frame[1]
        else:
            print("**LOOPING VIDEO**")
            source.set(cv2.CAP_PROP_POS_FRAMES, 0)
            _, frame = source.read()

    image = imutils.resize(frame, width=400)
    return image
