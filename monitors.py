import subprocess
from statistics import median
from random import randint
from time import sleep


def loop_average(func):
    def wrapper_loop_average():
        results = []
        for i in range(1, 10):
            # TODO: Handle nones. also, do we want to handle 2 returns on t/h?
            results.append(func())
            sleep(1)
        return median(results)
    return wrapper_loop_average


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


if __name__ == "__main__":
    print(str(stub()))
