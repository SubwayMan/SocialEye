from flask import Flask
# import picamera
import time

app = Flask(__name__)

@app.route('/')
def index():
  return 'testing'

app.run(host='0.0.0.0', port=81)

# use picamera to record
with picamera.PiCamera() as camera:
    camera.start_recording('video.h264')  
    camera.stop_recording()


def generate_frames():
    cap = cv2.VideoCapture('video.h264')  # path to video file
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                break
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame') 

# get the info from the video from pi and save it

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


