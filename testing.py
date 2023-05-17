from main import db

if db:
    print("db connection working")

# weather tests


import unittest
from weather import return_url

class TestReturnUrl(unittest.TestCase):
    def test_return_url(self):
        # testing if sunny url is returned
        sunny_codes = [0, 1]
        expected_sunny_url = "https://source.unsplash.com/LD_phgnVdOA"
        actual_sunny_url = return_url(sunny_codes)
        self.assertEqual(actual_sunny_url, expected_sunny_url)
#         test for cloud
        cloudy_codes = [2, 3]
        expected_cloudy_url = "https://source.unsplash.com/uftVkZ1ikn4"
        actual_cloudy_url = return_url(cloudy_codes)
        self.assertEqual(actual_cloudy_url, expected_cloudy_url)
#         test for fog
        foggy_codes = [45, 48]
        expected_foggy_url = "https://source.unsplash.com/e2uTOpgW5Ec"
        actual_foggy_url = return_url(foggy_codes)
        self.assertEqual(actual_foggy_url, expected_foggy_url)
#         test for drizzle or rain
        rain_or_drizzle_codes = [51, 53, 55, 56, 57] + [61, 63, 65, 80, 81, 82]
        expected_rain_or_drizzle_url = "https://source.unsplash.com/8yt8kBuEqok"
        actual_rain_or_drizzle_url = return_url(rain_or_drizzle_codes)
        self.assertEqual(actual_rain_or_drizzle_url, expected_rain_or_drizzle_url)
#         test for snow
        snow_codes = [71, 73, 75, 77, 85, 86]
        expected_snow_url = "https://source.unsplash.com/efuwb5eBDrI"
        actual_snow_url = return_url(snow_codes)
        self.assertEqual(actual_snow_url, expected_snow_url)
#         test for else
        other_codes = [""]
        expected_other_url = "https://source.unsplash.com/lVDnLUACI18"
        actual_other_url = return_url(other_codes)
        self.assertEqual(actual_other_url, expected_other_url)
if __name__ == '__main__':
    unittest.main()

