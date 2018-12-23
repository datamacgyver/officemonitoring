import subprocess


def stub(val):
    return val


def cpu_temp():
    bash_command = "/opt/vc/bin/vcgencmd measure_temp"
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    resp = str(output).replace('b"temp=', '').replace("'C\\n\"", '')
    resp = float(resp)
    return resp  # Units are Degrees C


if __name__ == "__main__":
    print(stub())
