import requests

# WMO Weather interpretation codes (WW)
sunny = [0, 1]
cloudy = [2, 3]
fog = [45, 48]
drizzle = [51, 53, 55, 56, 57]
rain = [61, 63, 65, 80, 81, 82]
snow = [71, 73, 75, 77, 85, 86]
storm = [95, 96, 99]


def return_url(code):
    if code in sunny:
        img_url = "https://source.unsplash.com/Fpqx6GGXfXs"
    elif code in cloudy:
        img_url = "https://source.unsplash.com/0juC5JIhPks"
    elif code in fog:
        img_url = "https://source.unsplash.com/TFyi0QOx08c"
    elif code in drizzle or code in rain:
        img_url = "https://source.unsplash.com/8lQyd8wEAzI"
    elif code in snow:
        img_url = "https://source.unsplash.com/OoQKL4cLZuc"
    else:
        img_url = "https://source.unsplash.com/lVDnLUACI18"

    return img_url


# using the weather API
def find_weather():
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
        # print(weather_dict[weathercode])

        # get image URL based on weathercode
        image_url = return_url(weathercode)
        # print(image_url)
        return image_url

    else:
        # showing the error message
        print("Error in the HTTP request")


find_weather()
