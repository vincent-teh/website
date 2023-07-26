import socketio
import max6675
from time import sleep
import RPi.GPIO as GPIO
from paho.mqtt import client as mqtt_client

# set the pin for communicate with MAX6675
cs  = 26
sck = 23
so  = 21
addr_server = "http://192.168.137.1:5000/"
pin = 23
direction = 0

sio = socketio.Client()

# Modify this function to read the temperature from the max6675
def update_temp():
    global cs
    while True:
        num = max6675.read_temp(cs)
        print("Sending: ", num)
        sio.emit('update_temp', {"temp": num})
        sio.sleep(1)

# @sio.event
# def connect():
#     print("Connection established")
#     update_temp()

# @sio.event
# def disconnect():
#     print(addr_server, "disconnected")

# @sio.on('update_direction')
# def printdata(data):
#     global direction
#     print("Received: ", data)
#     direction = data['direction']


broker = '192.168.137.1'
port = 1883

def on_message(client, userdata, msg):
    if msg.topic == 'DIRECTION':
        direction = msg.payload
        if direction is None:
            return
        direction = int(direction)
        if direction == 2:
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe('DIRECTION')
        print(f"Connected to MQTT Broker on topic: DIRECTION")
    else:
        print("Failed to connect, return code %d\n", rc)

def connect_mqtt():
    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    return client


if __name__ == "__main__":
    # GPIO.setmode(GPIO.BCM)
    # Set the pin as an output
    GPIO.setup(pin, GPIO.OUT)
    max6675.set_pin(cs, sck, so, 1)
    client = connect_mqtt()

    client.loop_start()
    try:
        while True:
            client.publish('TEMP', max6675.read_temp(cs))
            sleep(2)

    except KeyboardInterrupt:
        # Clean up GPIO on keyboard interrupt
        GPIO.cleanup()
        client.loop_stop()
        client.disconnect()
