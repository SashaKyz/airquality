# This is a sample Python script.

from bottle import route, run, static_file, template
import time
import serial
from datetime import datetime
import rrdtool


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
    ser = serial.Serial('COM3', 115200, timeout=30)  # ttyACM1 for Arduino board
    if not ser.isOpen():
        ser.open()
    print('com3 is open', ser.isOpen())
    line = ser.readline()
    print(line)
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
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)
    print('Closing')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
