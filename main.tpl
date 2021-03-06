<!DOCTYPE html>
<html lang="en">
<head>
    <title>Tempetature and Humidity</title>
    <!-- CSS only -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous">
</head>
<body>
    <h1>Raspberry Pi DHT22 Webserver Demo</h1>
    <p>The values below show the date, time, temperature and humidity readings from a DHT22 sensor</p>
    <p><img src="{{ get_url('static', filename='test.png') }}"></p>

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