from typing import Any
from website.config import raspy_addr, get_direction, topic
from website.extensions import socketio, temp
from flask import request
from website.mqtt_client import mqtt_client
from threading import Event, Lock
import cv2
import base64
from website.routes import raspy



@socketio.on('connect')
def handle_connect():
    addr = request.environ['REMOTE_ADDR']
    print(addr + " has connected")


@socketio.on('disconnect')
def handle_disconnect():
    print('Device disconnected')

@socketio.on("image")
def receive_image(image):
    print('Data received')
    try:
        image = raspy.get_pre_img()
        if image is None:
            return
        processed_img_data = base64.b64encode(image).decode()

        # Prepend the base64-encoded string with the data URL prefix
        b64_src = "data:image/jpg;base64,"
        processed_img_data = b64_src + processed_img_data

        # Send the processed image back to the client
        socketio.emit("processed_image", processed_img_data)
    except Exception as e:
        print(e)