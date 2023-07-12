from config import raspy_addr, get_direction, topic
from extensions import socketio, mqtt_client
from flask import request
from threading import Event, Lock

import sys

'''
    Objects for enabling threads
    e = thread event object
    l = thread lock object
    t= thread object
'''
t_raspy = {
    'thread': None,
    'event': Event(),
    'lock': Lock()
}

temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
power = 0
pid_prev_error = 0.0  # Previous error for derivative term


def get_temp():
    return temp

def get_power():
    return power

'''
    Change this function such that the socket will emit the correct direction to the raspy
'''
def handle_raspy():
    global t_raspy
    try:
        while t_raspy['event'].is_set():
            socketio.emit('update_direction', {'direction': get_direction()})
            socketio.sleep(1)
    finally:
        t_raspy['event'].clear()

# Overwrite this function for calculating the correct output power
def calc_power(_temp, _pid_prev_error):
    # PI-PD parameters
    Kp = 1.0  # Proportional gain
    Ki = 0.1  # Integral gain
    Kd = 0.1  # Derivative gain
    setpoint = 40.0  # Setpoint temperature (desired temperature)
    integral_limit = 100.0  # Integral term upper limit
    error = setpoint - _temp

    # Proportional term
    proportional = Kp * error

    # Integral term
    integral = Ki * error

    # Limit the integral term
    integral = max(-integral_limit, min(integral, integral_limit))

    # Derivative term
    derivative = Kd * (error - _pid_prev_error)
    _pid_prev_error = error

    # Calculate PI-PD output
    output = proportional + integral + derivative

    return output, _pid_prev_error

@socketio.on('connect')
def handle_connect():
    global t_raspy, temp
    addr = request.environ['REMOTE_ADDR']
    print(addr + " has connected", file=sys.stdout)
    # Case handling specific for raspy
    if addr == raspy_addr:
        print("Raspberry Pi has connected", file=sys.stdout)
        with t_raspy['lock']:
            if t_raspy['thread'] is None:
                t_raspy['event'].set()
                t_raspy['thread'] = socketio.start_background_task(handle_raspy)
                temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

@socketio.on('disconnect')
def handle_disconnect():
    global t_raspy
    addr = request.environ['REMOTE_ADDR']
    if addr == raspy_addr:
        print("Raspberry Pi has disconnected", file=sys.stdout)
        t_raspy['event'].clear()
        with t_raspy['lock']:
            if t_raspy['thread'] is not None:
                t_raspy['thread'].join()
                t_raspy['thread'] = None

@socketio.on('update_temp')
def handle_temp(data):
    global temp, pid_prev_error, power
    received_temp = data['temp']
    power, pid_prev_error = calc_power(received_temp, pid_prev_error)
    temp.pop(0)
    temp.append(received_temp)
    mqtt_client.publish('POWER', power)
    # print(mqtt_client.publish(topic, power))
