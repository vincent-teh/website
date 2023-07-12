from flask_socketio import SocketIO
from flask import Flask
from flask_mqtt import Mqtt
from config import broker_url

# Objects for enabling flask-socketio
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

mqtt_client = Mqtt()
socketio = SocketIO()
