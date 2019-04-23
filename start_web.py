import atexit
import json

from flask import Flask, render_template, Response
import cv2

from tablesoccer import Controller
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template("base.html")


def gen(image):
    while True:
        frame = controller.snapshots.get(image)
        if frame is not None:
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')


@app.route('/video/<feed>')
def video(feed):
    return Response(gen(feed),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/recalculate')
def recalculate():
    controller.schedule_recalculation()

    return "ok"


@app.route('/stats')
@cross_origin()
def stats():
    return json.dumps(controller.get_stats())


if __name__ == '__main__':
    source_type = 'webcam'
    path = 1

    controller = Controller(source_type=source_type,
                            paths={"camera_top": 1, "camera_home": 0},
                            arduino_config={"port": "COM3", "features": ["display", "sound"]},
                            debug=True)
    controller.start()

    atexit.register(lambda: controller.stop())

    app.run(host='0.0.0.0')

