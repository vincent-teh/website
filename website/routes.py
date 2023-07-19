import cv2
from flask import render_template, Response, request, jsonify, Blueprint
from website.config import live_video_url, graph_url, update_direction, topic
from random import randint
from website.extensions import temp
from website.mqtt_client import mqtt_client
import time
from website.raspy import Raspy

main = Blueprint("main", __name__)
raspy = Raspy()

'''
    Overload this function for performing image detection
    The detection should also call update drection function before yeilding
    the frames.
'''
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

        # Update the direction variable
        update_direction(randint(0, 9))
        # Yield the output frame in the byte format
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # Release the camera and close the window
    cap.release()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/stream')
def stream():
    return render_template('stream.html')

@main.route('/graph')
def graph():
    return render_template('graph.html')

@main.route('/live_cam')
def video_feed():
    return Response(generate_frames(live_video_url), mimetype='multipart/x-mixed-replace; boundary=frame')

@main.route('/plot_graph')
def plot_graph():
    def my_frame():
        while True:
            frame = raspy.get_post_img()
            if frame is not None:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                pass
    return Response(my_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@main.route('/live_temp')
def update_temp():
    return jsonify(temp=temp.get_temp(), power=temp.get_power())
