import json

from pandas import read_csv

import config
from statistics import mean
from serial_utils import get_com_ports, get_line, append_outputs, get_full_line


def import_calibrated_mean():
    with open(config.CALIBRATION_FILE, "r") as f:
        string_values = f.readline().split(sep=", ")
    return list(map(float, string_values))


def process_outputs(sensor_outputs):
    normal_mean = import_calibrated_mean()
    statuses = list()
    for idx, sensor in enumerate(sensor_outputs):
        # print(f'm= {mean(sensor)}, {normal_mean[idx]}', end="")
        if abs(mean(sensor) - normal_mean[idx]) > config.ALLOWED_DEVIATION:
            statuses.append("1")
        else:
            statuses.append("0")
    return statuses


def main():
    datapoints = list()
    while True:
        hall_effect_outputs = list()
        ports = get_com_ports()

        for port in ports:
            hall_effect_outputs.append(json.loads(get_full_line(port)))
        append_outputs(datapoints, hall_effect_outputs, config.BUFFER_SIZE)
        statuses = process_outputs(datapoints)
        print(statuses)
        with open(config.STATUS_FILE, 'w') as f:
            f.write(", ".join(statuses))


if __name__ == '__main__':
    main()
