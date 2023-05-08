import jsonify, requests

# dictionary of WMO Weather interpretation codes (WW)
weather_dict = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    56: "freezing light drizzle",
    57: "freezing dense drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    71: "slight snow fall",
    73: "moderate now fall",
    75: "heavy snow fall",
    77: "snow grains",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    85: "slight snow showers",
    86: "heavy snow showers",
    95: "thunderstorm",  # (slight or moderate)
    96: "thunderstorm with slight hail",
    99: "thunderstorm with heavy hail"
}


# using the weather API

# BASE_URL = "https://api.open-meteo.com/v1/forecast?"
CITY = "LONDON"

# HTTP request
response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=51.51&longitude=-0.13&forecast_days=1"
                        "&timezone=GMT&daily=weathercode")

# checking the status code of the request
if response.status_code == 200:
    # getting data in the json format
    data = response.json()
    # print(data)
    # getting all the daily data
    daily = data['daily']
    # getting the weather-code to tell us the weather condition on that day
    weathercode = daily['weathercode'][0]
    # print(weathercode)
    print(weather_dict[weathercode])

else:
    # showing the error message
    print("Error in the HTTP request")



