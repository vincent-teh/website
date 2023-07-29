from flask import Flask
from website.config import broker_url
from website.mqtt_client import mqtt_client, temp
from website.routes import main, raspy
from website.events import socketio
import threading
from time import sleep

def publish_direction():
    while True:
        data = raspy.get_direction()
        mqtt_client.publish('DIRECTION', data)
        if data[0] == 'n':
            temp.start_plant()
        sleep(2)


def create_app():
    app = Flask(__name__)
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.config['MQTT_BROKER_URL'] = broker_url
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
    app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
    app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
    app.config['MQTT_TLS_ENABLED'] = False  # If your server supports TLS, set it True

    app.register_blueprint(main)


    # Run image processing in background
    raspy.thread['thread'] = threading.Thread(target=raspy.detect_image)
    raspy.thread['event'].set()
    raspy.thread['thread'].start()

    mqtt_client.init_app(app)
    socketio.init_app(app)

    mqtt_thread = threading.Thread(target=publish_direction)
    mqtt_thread.start()

    return app
