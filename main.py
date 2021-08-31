# This is a sample Python script.

from bottle import route, run, static_file, template, BaseTemplate
import bottle
import time
import serial
from datetime import datetime
import rrdtool
#from multiprocessing import Process
import threading
import sys

currentAirQ = 0
currentTemp = 25
currentHumid = 45

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def tprint(var):
    print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+" :: "+str(var))

@route('/')
def serve_homepage():
    humidity = '{0:0.1f}'.format(newtemp)
    temperature = '{0:0.1f}'.format(newhumid)
    time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    rrdtool.graph('static/test.png',
                  '--title', 'Weather',
                  '--imgformat', 'PNG',
                  '--vertical-label', 'Air quality',
                  'DEF:a=test.rrd:airq:AVERAGE',
                  'AREA:a#00FF00:Air')

    myData = {
      'tempVal' : temperature,
      'humidVal' : humidity,
      'airtempVal': currentAirQ,
      'myTime' : time
     }
    return template('main.tpl', **myData)

@route('/static/<filename:path>', name='static')
def serve_static(filename):
    return static_file(filename, root='static')

def getportdata():
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=30)  # ttyACM1 for Arduino board
    if not ser.isOpen():
        ser.open()
    line = ser.readline().decode().strip()
    ser.close()
    return line

def update_rrd():
    global currentAirQ
    global currentTemp
    global currentHumid
    threading.Timer(60.0, update_rrd).start()
    newtemp = 25
    newhum = 43
    newairq = getportdata()
    rrdtool.update("test.rrd", "N:{}:{}:{}".format(newtemp,newhum,newairq))
    tprint("Update RRD db {}".format(newairq))
    currentAirQ = newairq
    currentTemp = newtemp
    currentHumid = newhum
 
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    serport = 'COM3'
    rrdtool.create(
        "test.rrd",
        "--start", "now",
        "--step", "60",
        "RRA:AVERAGE:0.5:1m:24h",
        "RRA:AVERAGE:0.5:5m:14d",
        "RRA:AVERAGE:0.5:5h:90d",
        "DS:temp:GAUGE:600:-273:5000",
        "DS:humid:GAUGE:600:0:1000",
        "DS:airq:GAUGE:600:0:2000"
    )
    app = bottle.default_app()
    BaseTemplate.defaults['get_url'] = app.get_url  # reference to function
    try:
        update_rrd()
        run(host='0.0.0.0', port=8080, debug=True, reloader=True)
    except KeyboardInterrupt:
        tprint('Closing')
        sys.stdout.write("Aborted by user.\n")
        sys.exit(1)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
