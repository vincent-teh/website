from config import raspy_addr
from extensions import socketio
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

temp = 0

def handle_raspy():
    global t_raspy
    try:
        while t_raspy['event'].is_set():
            socketio.emit('update_direction', {'direction': 1})
            socketio.sleep(4)
    finally:
        t_raspy['event'].clear()


@socketio.on('connect')
def handle_connect():
    global t_raspy
    addr = request.environ['REMOTE_ADDR']
    print(addr + " has connected", file=sys.stdout)
    # Case handling specific for raspy
    if addr == raspy_addr:
        print("Raspberry Pi has connected", file=sys.stdout)
        with t_raspy['lock']:
            if t_raspy['thread'] is None:
                t_raspy['event'].set()
                t_raspy['thread'] = socketio.start_background_task(handle_raspy)

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
    global temp
    temp = data['temp']

def get_temp():
    return temp
