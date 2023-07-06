import cv2
from flask import Flask, render_template, Response, request, jsonify
from events import socketio, get_temp
from config import live_video_url, graph_url, raspy_addr


# Objects for enabling flask-socketio
app = Flask(__name__)
socketio.init_app(app)


def generate_frames(video_url):
    # Open the webcam
    cap = cv2.VideoCapture(video_url)  # Change the parameter to the appropriate camera index if needed

    while True:
        # Read frame from the camera
        success, frame = cap.read()

        if not success:
            break

        # Convert the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)

        if not ret:
            break

        # Yield the output frame in the byte format
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # Release the camera and close the window
    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    return render_template('stream.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/live_cam')
def video_feed():
    return Response(generate_frames(live_video_url), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/plot_graph')
def plot_graph():
    return Response(generate_frames(graph_url), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/live_temp')
def update_temp():
    temp = get_temp()
    return jsonify(temp=temp)
