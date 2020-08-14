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
for refresh (update weather data) use method class: 
```weather.refresh(request.form["city"])```
#### Options
```method weather.content()``` support any format date \
Example: 
```weather.content("%d.%m.%Y %H:%M:%S")```
Default:
```%Y-%m-%d %H:%M:%S```
## Error:
Error connect - wrong internet connection \
Error content - wrong API key or wrong request
# Log change
check spelling PEP8
Add code error display \
401 - api key not correct

