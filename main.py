# This is a sample Python script.

from bottle import route, run, static_file, template
import time
import serial
from datetime import datetime
import rrdtool
#from multiprocessing import Process
import threading
import sys

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

@route('/')
def serve_homepage():
    humidity = '{0:0.1f}'.format(45)
    temperature = '{0:0.1f}'.format(80)
    airq = getportdata()
    time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    rrdtool.graph('test.png',
                  '--title', 'Weather'
                  '--imgformat', 'PNG',
                  '--vertical-label', 'Air quality',
                  'DEF:a=test.rrd:temp:AVERAGE')
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
    line = ser.readline().decode().strip()
    ser.close()
    return line

def update_rrd():
    threading.Timer(60.0, update_rrd).start()
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
        update_rrd()
        run(host='0.0.0.0', port=8080, debug=True, reloader=True)
    except KeyboardInterrupt:
        print('Closing')
        sys.stdout.write("Aborted by user.\n")
        sys.exit(1)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
