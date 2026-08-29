import requests

url = "https://api.open-meteo.com/v1/forecast?" \
"latitude=23.81&longitude=90.41&current_weather=true"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data)
    current_weather = data.get("current_weather", {})
    temperature = current_weather.get("temperature")
    windspeed = current_weather.get("windspeed")
    winddirection = current_weather.get("winddirection")
    weathercode = current_weather.get("weathercode")

    print(f"Current Temperature: {temperature}°C")
    print(f"Wind Speed: {windspeed} m/s")
    print(f"Wind Direction: {winddirection}°")
    print(f"Weather Code: {weathercode}")

else:
    print(f"Failed to retrieve weather data. Status code: {response.status_code} response: {response.text}")