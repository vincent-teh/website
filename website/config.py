from threading import Lock
import sys

live_video_url = "slide7.mp4"
graph_url = 0
raspy_addr = "192.168.137.11"
topic = 'POWER'
broker_url = '192.168.137.1'


direction = 0
l_direction = Lock()

def update_direction(_direction):
    global direction, l_direction
    with l_direction:
        direction = _direction

def get_direction():
    global direction, l_direction
    with l_direction:
        return direction
