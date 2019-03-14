import cv2
import imutils

from tablesoccer import Controller


def setup_window(name, x, y):
    cv2.namedWindow(name)
    cv2.moveWindow(name, x, y)


setup_window("Raw image", 0, 0)
setup_window("Environment", 0, 500)
setup_window("Transformed image", 500, 0)

source_type = 'webcam'
path = 0
imwrite = True

d = Controller(source_type, path, debug=True)
d.start()

while True:
    raw = d.snapshots.get("RAW_DETECTIONS")
    calc = d.snapshots.get("CORNER_CALC")
    transformed = d.snapshots.get("TRANSFORMED")
    env = d.snapshots.get("ENVIRONMENT")

    if raw is not None:
        cv2.imshow('Raw image', raw)
        if imwrite: cv2.imwrite('raw.jpg', raw)

    if env is not None:
        cv2.imshow('Environment', env)
        if imwrite: cv2.imwrite('env.jpg', env)

    if transformed is not None:
        cv2.imshow('Transformed image', imutils.resize(transformed, width=250))
        if imwrite: cv2.imwrite('transformed.jpg', transformed)

    cv2.waitKey(1)




playing = True


if source_type == 'webcam':
    source = WebcamVideoStream(int(path)).start()
elif source_type == 'video':
    source = cv2.VideoCapture(path)
else:
    raise NameError("Unknown source_type: %s" % source_type)

fps = FPS().start()

field = SoccerField()
detector = Detector()

i = 0

DEBUG = True
YOLO_SIZE = (416, 416)

while True:
    frame = get_image(source)
    frame = imutils.resize(frame, width=400)

    if detector.corners is None or i == 0:
        detector.calculate_field(frame)

    if DEBUG:
        img = cv2.resize(frame.copy(), YOLO_SIZE)
        if detector.corners is not None:
            for c in detector.corners:
                img = cv2.circle(img, (int(c[0]), int(c[1])), 2, (255, 255, 120), 2)
        cv2.imshow('Raw image', img)

    if detector.corners is not None:
        if DEBUG:
            cv2.imshow('Calc image', detector.calc_image)

        field.update(detector)

        transformed = cv2.resize(frame, YOLO_SIZE)
        transformed = four_point_transform(transformed, np.array(detector.corners))

        detector.detect(transformed)
        cv2.imshow('Transformed image', cv2.cvtColor(detector.raw_image, cv2.COLOR_BGR2RGB))

    env = np.zeros((YOLO_SIZE[0], YOLO_SIZE[1], 3), np.uint8)
    env = field.draw(env)
    cv2.imshow('Environment', env)

    cv2.waitKey(1)

    i += 1

    if i % 100 == 0:
        i = 0

