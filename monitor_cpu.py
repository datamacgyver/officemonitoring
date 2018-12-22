import subprocess


def get_value():
  bashCommand = "/opt/vc/bin/vcgencmd measure_temp"
  process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()

  resp = str(output).replace('b"temp=','').replace("'C\\n\"",'')
  resp = float(resp)
  return(resp)  # Units are Degrees C

if __name__=="__main__":
  print(get_value())
