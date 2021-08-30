<!DOCTYPE html>
<html lang="en">
<head>
    <title>Tempetature and Humidity</title>
    <link rel="stylesheet" type="text/css" href="http://twitter.github.com/bootstrap/assets/css/bootstrap.css">
</head>
<body>
    <h1>Raspberry Pi DHT22 Webserver Demo</h1>
    <p>The values below show the date, time, temperature and humidity readings from a DHT22 sensor</p>
    <p><img src="test.png"></p>

    <br /><br />
    <h3> Temperature ==> {{tempVal}} <sup>o</sup>C</h3>
    <h3> Humidity    ==> {{humidVal}} %</h3>
    <h3> AirQuality  ==> {{airtempVal}} </h3>
    <hr>
    <h3> Last Sensor Reading: {{myTime}} <a
href="/"class="button">Refresh</a></h3>
    <hr>
</body>
</html>