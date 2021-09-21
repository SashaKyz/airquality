<!DOCTYPE html>
<html lang="en">
<head>
    <title>Tempetature and Humidity</title>
    <!-- CSS only -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous">
</head>
<body>
    <h1>Weather home station</h1>
    <p>The values below show the date, time, temperature and humidity readings from a DHT22 sensor</p>
    <p><img src="/weather/{{ get_url('static', filename='main1.png') }}"></p>
    <p><img src="/weather/{{ get_url('static', filename='main2.png') }}"></p>
    <p><img src="/weather/{{ get_url('static', filename='main3.png') }}"></p>
    <br /><br />
    <h3> Temperature(BMP280) ==> {{tempVal}} <sup>o</sup>C</h3>
    <h3> Temperature(DHT)    ==> {{temp1Val}} <sup>o</sup>C</h3>
    <h3> Humidity(DHT)       ==> {{humidVal}} %</h3>
    <h3> Pressure(BMP280)    ==> {{pressureVal}}</h3>
    <h3> AirQuality(MQ3)      ==> {{airtempVal}}</h3>
    <h3> AirQuality(MQ135)    ==> {{altitudeVal}} </h3>
    <hr>
    <h3> Last Sensor Reading: {{myTime}} <a
href="/weather/"class="button">Refresh</a></h3>
    <hr>
</body>
</html>
