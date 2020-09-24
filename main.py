from flask import Flask, Response
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate_frame(camera):
    while True:
        ret, img = camera.read()
        ret, jpg = cv2.imencode('.jpg', img)
        frame = jpg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video.mjpg')
def video_feed():
    camera = cv2.VideoCapture(0)
    return Response(generate_frame(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("yes")
    app.run(host='0.0.0.0', port="8080", debug=True)