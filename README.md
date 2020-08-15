# Weather Class - Web Service example
Data about temperature, pressure and wind speed obtained from the \
API are returned through the method, content() of the Weather class
## Install:
create api key: https://openweathermap.org/api \
install python and pip: \
Ubuntu 16 >=: \
sudo apt install python3 \
sudo apt install python3-pip \
pip3 install -r requitrments.txt
## Setting class:
```
app_name = 'Your company'
api_key = 'insert_api_key'
server = 'insert_api_server_openweathermap'
city_name = 'Krasnodar'
weather = Weather(app_name, api_key, server, city_name)
```
you can use no set city_map, default city Moscow
#### Refresh weather
for refresh (update weather data) use method class: \
```weather.refresh(request.form["city"])```
#### Options
```method weather.content()``` support any format date \
Example: \
```weather.content("%d.%m.%Y %H:%M:%S")```
Default: \
```%Y-%m-%d %H:%M:%S```
## Debug
```weather = Weather(app_name, api_key, server, city_name, debug=False)``` \
**True** - debuger more information problem connect for request \
Example: \
```
HTTPConnectionPool(host='api.opnweathermap.org', port=80): 
Max retries exceeded with url: 
/data/2.5/weather?q=%D1%81%D0%B0%D0%BD%D0%BA%D1%82-%D0%BF%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3&appid=a5f756f97a8cf1082787e8d36699c449&units=metric (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7fcd0e647460>: Failed to establish a new connection: [Errno -2] Name or service not known')) 
```
**False** - minimum information problem
## Error:
Error connect - wrong internet connection \
Error content - wrong API key or wrong request
# Log change
add show: Direction of the wind \
add debug variable \
add print error connect terminal \
check spelling PEP8
Add code error display \
401 - api key not correct

