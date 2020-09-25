from flask import Flask, Response
import cv2
import threading

app = Flask(__name__)
camera = cv2.VideoCapture(0)
img = None

def video_thread(camera):
    while True:
        global img
        ret, img = camera.read()

@app.route('/')
def index():
    return render_template('index.html')

def generate_frame():
    while True:
        ret, jpg = cv2.imencode('.jpg', img)
        frame = jpg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/stream.mjpg')
def video_feed():
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("Starting Camera Server...")
    camThread = threading.Thread(target=video_thread, args=(camera,))
    camThread.setDaemon(True)
    camThread.start()
    app.run(host='0.0.0.0', port="5510")