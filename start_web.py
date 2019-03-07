import atexit

from flask import Flask, render_template_string, Response
import cv2

from tablesoccer import Controller

app = Flask(__name__)


@app.route('/')
def index():
    return render_template_string("""<html>
  <head>
    <title>Stream Table Soccer</title>
  </head>
  <body>
    <h1>TRANSFORMED</h1>
    <img src="{{ url_for('video', feed='TRANSFORMED') }}">
    <h1>ENVIRONMENT</h1>
    <img src="{{ url_for('video', feed='ENVIRONMENT') }}">
  </body>
</html>""")


def gen(image):
    while True:
        frame = d.snapshots.get(image)
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
    d.schedule_recalculation()

    return "ok"


if __name__ == '__main__':
    source_type = 'webcam'
    path = 0

    d = Controller(source_type, path, debug=True)
    d.start()

    atexit.register(lambda: d.stop())

    app.run(host='0.0.0.0')

