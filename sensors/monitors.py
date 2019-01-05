import subprocess
from statistics import median
from random import randint
from time import sleep
import Adafruit_DHT


def loop_average(func):
    def wrapper_loop_average():
        results = []
        for i in range(0, 5):
            # TODO: Handle nones.
            results.append(func())
            sleep(1)
        results = [x for x in results if x is not None]
        if len(results) < 3:
            raise IOError('Sensor returned more than 2 errors')
        print(results)
        return median(results)
    return wrapper_loop_average


def _read_temp_humidity_sensor():
    temp = None
    humid = None
    tries = 0
    while temp is None or humid is None:
        tries += 1
        if tries > 5:
            raise OSError("Can't communicate with sensor")
        humid, temp = Adafruit_DHT.read_retry(11, 4)

    return float(humid), float(temp)


@loop_average
def stub():
    val = randint(11, 40)
    return val


@loop_average
def cpu_temp():
    bash_command = "/opt/vc/bin/vcgencmd measure_temp"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    resp = str(output).replace('b"temp=', '').replace("'C\\n\"", '')
    resp = float(resp)
    return resp  # Units are Degrees C


@loop_average
def room_temp():
    _, temp = _read_temp_humidity_sensor()
    return temp


@loop_average
def room_humidity():
    humid, _ = _read_temp_humidity_sensor()
    return humid


if __name__ == "__main__":
    print(str(stub()))
    print(str(room_temp()))
    print(str(room_humidity()))
