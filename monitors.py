import subprocess

def get_stub_value():
  return(12.1)

def get_cpu_temp():
  bashCommand = "/opt/vc/bin/vcgencmd measure_temp"
  process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()

  resp = str(output).replace('b"temp=','').replace("'C\\n\"",'')
  resp = float(resp)
  return(resp)  # Units are Degrees C

if __name__=="__main__":
  print(get_stub_value())
