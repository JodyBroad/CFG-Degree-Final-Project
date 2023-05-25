import requests

# WMO Weather interpretation codes (WW)
sunny = [0, 1]
cloudy = [2, 3]
fog = [45, 48]
drizzle = [51, 53, 55, 56, 57]
rain = [61, 63, 65, 80, 81, 82]
snow = [71, 73, 75, 77, 85, 86]
storm = [95, 96, 99]


# function that returns an image url based on a weather code
def return_url(code):
    if code in sunny:
        img_url = "https://source.unsplash.com/LD_phgnVdOA"
    elif code in cloudy:
        img_url = "https://source.unsplash.com/uftVkZ1ikn4"
    elif code in fog:
        img_url = "https://source.unsplash.com/e2uTOpgW5Ec"
    elif code in drizzle or code in rain:
        img_url = "https://source.unsplash.com/8yt8kBuEqok"
    elif code in snow:
        img_url = "https://source.unsplash.com/efuwb5eBDrI"
    else:
        img_url = "https://source.unsplash.com/lVDnLUACI18"

    return img_url


# function that checks response code from the request
def response_code(json_response, code):
    # checking the status code of the request
    if code == 200:
        # getting data in the json format
        data = json_response.json()

        # getting all the daily data
        daily = data['daily']

        # getting the weather-code to tell us the weather condition on that day
        weathercode = daily['weathercode'][0]

        # get image URL based on weathercode
        image_url = return_url(weathercode)
        return image_url

    else:
        # showing the error message
        raise Exception("Error in the HTTP request")


# using the weather API to return a weather background image
def find_weather():
    # HTTP request
    response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=51.51&longitude=-0.13&forecast_days=1"
                            "&timezone=GMT&daily=weathercode")

    # check the request response
    background_url = response_code(response, response.status_code)

    return background_url
