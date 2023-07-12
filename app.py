import cv2
from flask import render_template, Response, request, jsonify
from events import socketio, get_temp, get_power
from config import live_video_url, graph_url, update_direction, topic
from random import randint
from extensions import app, mqtt_client
from time import sleep

socketio.init_app(app)
mqtt_client.init_app(app)


'''
    MQTT publish is a blocking operation.
    Looping through a publish event will the system failed to send system
    level acknowledgement.
    It is advisable to never put loop pulish here.
'''
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected")
    else:
        print('Bad connection. Code:', rc)

@mqtt_client.on_disconnect()
def handle_disconnect():
    print('Device disconnect')

@mqtt_client.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )

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
    power = get_power()
    return jsonify(temp=temp, power=power)
