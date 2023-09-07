from statistics import mean

from serial_utils import get_com_ports, get_line, append_outputs
import json
import config


def get_mean_value(sensor_outputs):
    mean_values = list()
    for sensor in sensor_outputs:
        mean_values.append(str(mean(sensor)))
    return mean_values


def main():
    datapoints = list()
    sensor_outputs = list()

    ports = get_com_ports()
    for i in range(config.CALIBRATION_SIZE):
        for port in ports:
            line = get_line(port)
            try:
                sensor_outputs.append(json.loads(line))
            except json.decoder.JSONDecodeError:
                continue
        datapoints = append_outputs(datapoints, sensor_outputs, config.CALIBRATION_SIZE)
    mean_values = get_mean_value(datapoints)
    with open(config.CALIBRATION_FILE, 'w') as f:
        f.write(", ".join(mean_values))


if __name__ == '__main__':
    main()
