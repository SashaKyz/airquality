# This is a sample Python script.

from bottle import route, run, static_file, template, BaseTemplate
import bottle
import time
import serial
from datetime import datetime
import rrdtool
import threading
import sys
import os.path
from sys import platform

class currentStatus:
    AirQ = 0
    Temp = 25
    Temp1 = 25
    Humid = 45
    Pressure = 1015.5
    Altitude = 45.8

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def tprint(var):
    print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+" :: "+str(var))

@route('/')
def serve_homepage():
    time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    rrdtool.graph('static/main1.png',
                  '--title', 'AirQuality',
                  '--imgformat', 'PNG',
                  'DEF:a=test.rrd:airq:AVERAGE',
                  'DEF:c=test.rrd:temp:AVERAGE',
                  'DEF:b=test.rrd:pressure:AVERAGE',
                  'DEF:d=test.rrd:altitude:AVERAGE',
                  'DEF:f=test.rrd:humid:AVERAGE',
                  'DEF:e=test.rrd:temp1:AVERAGE',
                  'LINE1:a#00FF00:AirQuality(MQ3)',
                  'AREA:d#00FFFF:AirQuality(MQ135)'
                  )
    rrdtool.graph('static/main2.png',
                  '--title', 'Weather',
                  '--imgformat', 'PNG',
                  '--lower-limit', '0',
                  '--upper-limit', '100',
                  '--rigid',
                  'DEF:a=test.rrd:airq:AVERAGE',
                  'DEF:c=test.rrd:temp:AVERAGE',
                  'DEF:b=test.rrd:pressure:AVERAGE',
                  'DEF:d=test.rrd:altitude:AVERAGE',
                  'DEF:f=test.rrd:humid:AVERAGE',
                  'DEF:e=test.rrd:temp1:AVERAGE',
                  'LINE1:c#FF0000:Temperature',
                  'AREA:e#00FF00:Temperature1',

                  'LINE1:f#0000FF:Humid'
                  )
    rrdtool.graph('static/main3.png',
                  '--title', 'Pressure',
                  '--imgformat', 'PNG',
                  '--slope-mode',
                  '--alt-autoscale',
                  '--alt-autoscale-min',
                  '--alt-autoscale-max',
                  '--rigid',
                  'DEF:a=test.rrd:airq:AVERAGE',
                  'DEF:c=test.rrd:temp:AVERAGE',
                  'DEF:b=test.rrd:pressure:AVERAGE',
                  'DEF:d=test.rrd:altitude:AVERAGE',
                  'DEF:f=test.rrd:humid:AVERAGE',
                  'DEF:e=test.rrd:temp1:AVERAGE',
                  'LINE1:b#00FFFF:Pressure',
                  )
    myData = {
      'tempVal' : currentParam.Temp,
      'temp1Val': currentParam.Temp1,
      'humidVal' : currentParam.Humid,
      'airtempVal': currentParam.AirQ,
      'pressureVal': currentParam.Pressure,
      'altitudeVal': currentParam.Altitude,
      'myTime' : time
     }
    return template('main.tpl', **myData)

@route('/static/<filename:path>', name='static')
def serve_static(filename):
    return static_file(filename, root='static')

def getportdata():
    line = ser.readline().decode().strip()
    return line


#smoke:temperature:pressure:smoke1:humidity:temperature

def update_rrd():
    global currentParam
    threading.Timer(60.0, update_rrd).start()
    newmetric = getportdata().split(':')
    if len(newmetric) >= 4:
        currentParam.AirQ = newmetric[0]
        currentParam.Temp = newmetric[1]
        currentParam.Pressure = newmetric[2]
        currentParam.Altitude = newmetric[3]
        if len(newmetric) == 6:
            currentParam.Humid = newmetric[4]
            currentParam.Temp1 = newmetric[5]
    elif len(newmetric) == 3:
        currentParam.AirQ = newmetric[0]
        currentParam.Humid = newmetric[1]
        currentParam.Temp1 = newmetric[2]
    else:
        currentParam.AirQ = newmetric[0]

    rrdtool.update("test.rrd", "N:{}:{}:{}:{}:{}:{}".format(currentParam.AirQ,currentParam.Temp,currentParam.Pressure,
                                                            currentParam.Altitude,currentParam.Humid,currentParam.Temp1))
    tprint("Update RRD db {}".format(newmetric))
 
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    currentParam = currentStatus()
    if platform == "linux":
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=30)  # ttyACM0 on my raspberry pi for Arduino board
    elif platform == "win32":
        ser = serial.Serial('COM3', 115200, timeout=30)  # COM3 on windows
    else:
        tprint("Error - unknown system ")
        exit(1)
    if not ser.isOpen():
        ser.open()
    if not os.path.isfile("test.rrd"):
      rrdtool.create(
        "test.rrd",
        "--start", "now",
        "--step", "60",
        "RRA:AVERAGE:0.5:1m:24h",
        "RRA:AVERAGE:0.5:5m:14d",
        "RRA:AVERAGE:0.5:5h:90d",
        "DS:airq:GAUGE:600:0:2000",
        "DS:temp:GAUGE:600:-273:5000",
        "DS:pressure:GAUGE:600:0:2000",
        "DS:altitude:GAUGE:600:0:2000",
        "DS:humid:GAUGE:600:0:1000",
        "DS:temp1:GAUGE:600:-273:5000"
      )
    app = bottle.default_app()
    BaseTemplate.defaults['get_url'] = app.get_url  # reference to function
    try:
        update_rrd()
        run(host='0.0.0.0', port=8080, debug=True, reloader=True)
    except KeyboardInterrupt:
        tprint('Closing')
        ser.close()
        sys.stdout.write("Aborted by user.\n")
        sys.exit(1)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
