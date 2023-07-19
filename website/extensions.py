from flask_socketio import SocketIO
from flask_mqtt import Mqtt
from website.temp import Temp


# Objects for enabling flask-socketio
mqtt_client = Mqtt()
socketio = SocketIO()

temp = Temp()
