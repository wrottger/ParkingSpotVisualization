import json
from time import sleep
import collections
import config
import serial
from serial import SerialException
from serial.tools import list_ports


def append_outputs(datapoints, outputs, bufferlen):
    current_sensor = 0
    while len(outputs) != 0:
        minimum = min(outputs, key=lambda element: element['ID'])
        for sensor_value in minimum['data']:
            if len(datapoints) <= current_sensor:
                datapoints.append(collections.deque(maxlen=config.BUFFER_SIZE))
            datapoints[current_sensor].append(sensor_value)
            current_sensor += 1
        outputs.remove(minimum)
    return datapoints


def get_com_ports():
    return ["/dev/ttyACM0", "/dev/ttyACM1"]


def get_line(port):
    for attempt in range(3):
        try:
            with serial.Serial(port, 9600, timeout=1) as ser:
                return ser.readline().decode('utf-8')
        except SerialException:
            sleep(0.2)
    return None


def get_full_line(port):
    for attempt in range(3):
        line = get_line(port)
        try:
            json.loads(line)
            return line
        except json.decoder.JSONDecodeError:
            continue
    return None
