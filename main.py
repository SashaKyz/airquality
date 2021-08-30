# This is a sample Python script.

from bottle import route, run, static_file, template
import time
import serial
from datetime import datetime
import rrdtool
from multiprocessing import Process


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

@route('/')
def serve_homepage():
    humidity = '{0:0.1f}'.format(45)
    temperature = '{0:0.1f}'.format(80)
    airq = getportdata()
    time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    myData = {
      'tempVal' : temperature,
      'humidVal' : humidity,
      'airtempVal': airq,
      'myTime' : time
     }
    return template('main.tpl', **myData)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print('Hi, {}'.format(name))  # Press Ctrl+F8 to toggle the breakpoint.

def getportdata():
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=30)  # ttyACM1 for Arduino board
    if not ser.isOpen():
        ser.open()
    print('com3 is open', ser.isOpen())
    line = ser.readline().decode().strip()
    ser.close()
    return line

def update_rrd():
    newairq = getportdata()
    rrdtool.update("test.rrd", "N:{}".format(newairq))
    print("Update RRD db {}".format(newairq))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    serport = 'COM3'
    rrdtool.create(
        "test.rrd",
        "--start", "now",
        "--step", "300",
        "RRA:AVERAGE:0.5:1:1200",
        "DS:temp:GAUGE:600:-273:5000")
    try:
        t = Process(target=run(host='0.0.0.0', port=8080))
        t.daemon = True
        t.start()
        t.join()
        h = Process(target=update_rrd())
        h.daemon = True
        h.start()
        h.join()

    except KeyboardInterrupt:
        print('Closing')
        sys.stdout.write("Aborted by user.\n")
        sys.exit(1)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
