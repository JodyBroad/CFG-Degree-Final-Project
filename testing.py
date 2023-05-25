from app import db, app
from flask import Flask, session
from unittest import TestCase, mock
from flask_sqlalchemy import SQLAlchemy
from models import *
from views import *
from forms import *
from weather import *


class TestDBConnection(TestCase):

    # checks we have a valid instance of a SQLAlchemy database
    def test_db_connection(self):
        self.assertIsInstance(db, SQLAlchemy)


class TestFlaskApp(TestCase):

    # checks we have a valid instance of a Flask app
    def test_flask_app(self):
        self.assertIsInstance(app, Flask)


class TestViews(TestCase):

    # testing that user_list query is returning data
    def test_user_list(self):
        with app.app_context():
            users = UserInfo.query
            # would be good to get this testing something more detailed than just if it is bringing stuff back
            self.assertIsNotNone(users)

    # testing that user_data query is returning data
    def test_user_data(self):
        with app.app_context():
            user_data = db.session.query(UserInfo, DailyRecord, MoodStatus, SleepDuration, SleepQuality).\
                select_from(UserInfo).join(DailyRecord).join(MoodStatus).join(SleepDuration).join(SleepQuality).\
                order_by(DailyRecord.record_date).all()
            # would be good to get this testing something more detailed than just if it is bringing stuff back
            self.assertIsNotNone(user_data)


    # test a query that should fail and make sure it raises an error if table name doesn't exist
    def test_not_user_list(self):
        with app.app_context():
            # would be good to get this testing something more detailed than just if it is bringing stuff back
            # not sure this is a valid test, was just trying to get it to make sure to raise an error if invalid table
            # name, but python picks this up before it is an issue, so not sure it is valid!
            with self.assertRaises(NameError):
                users = UserNotInfo.query


class TestReturnUrl(TestCase):

    def test_return_url_sunny(self):
        # # Testing if sunny URL is returned
        sunny_codes = [0, 1]
        expected_sunny_url = "https://source.unsplash.com/LD_phgnVdOA"
        actual_sunny_url_0 = return_url(0)
        actual_sunny_url_1 = return_url(1)
        self.assertEqual(actual_sunny_url_0, expected_sunny_url)
        self.assertEqual(actual_sunny_url_1, expected_sunny_url)

    def test_return_url_cloudy(self):
        # Testing for cloudy URL
        cloudy_codes = [2, 3]
        expected_cloudy_url = "https://source.unsplash.com/uftVkZ1ikn4"
        actual_cloudy_url_2 = return_url(cloudy_codes[0])
        actual_cloudy_url_3 = return_url(cloudy_codes[1])
        self.assertEqual(actual_cloudy_url_2, expected_cloudy_url)
        self.assertEqual(actual_cloudy_url_3, expected_cloudy_url)

    def test_return_url_foggy(self):
        # Testing for foggy URL
        foggy_codes = [45, 48]
        expected_foggy_url = "https://source.unsplash.com/e2uTOpgW5Ec"
        actual_foggy_url_45 = return_url(foggy_codes[0])
        actual_foggy_url_48 = return_url(foggy_codes[1])
        self.assertEqual(actual_foggy_url_45, expected_foggy_url)
        self.assertEqual(actual_foggy_url_48, expected_foggy_url)

    # not yet working, just needs reformatting as per the above
    # def test_return_url_rain_or_drizzle(self):
    #     # # Testing for rain or drizzle URL
    #     rain_or_drizzle_codes = [51, 53, 55, 56, 57] + [61, 63, 65, 80, 81, 82]
    #     expected_rain_or_drizzle_url = "https://source.unsplash.com/8yt8kBuEqok"
    #     actual_rain_or_drizzle_url = return_url(rain_or_drizzle_codes)
    #     self.assertEqual(actual_rain_or_drizzle_url, expected_rain_or_drizzle_url)

    # not yet working, just needs reformatting as per the above
    # # Testing for snow URL
    # snow_codes = [71, 73, 75, 77, 85, 86]
    # expected_snow_url = "https://source.unsplash.com/efuwb5eBDrI"
    # actual_snow_url = return_url(snow_codes)
    # self.assertEqual(actual_snow_url, expected_snow_url)

        # Testing for "else" case URL
    def test_return_url_else(self):
        other_codes = [""]
        expected_other_url = "https://source.unsplash.com/lVDnLUACI18"
        actual_other_url = return_url(other_codes)
        self.assertEqual(actual_other_url, expected_other_url)

class TestFindWeather(TestCase):

    # testing that find weather() returns string
    def test_find_weather(self):
        weather = find_weather()
        self.assertIsInstance(weather, str)

    # not working, need to mock the output not the input
    # @mock.patch('builtins.input', side_effect=["404"])
    # def test_find_weather_failure(self, param):
    #     with self.assertRaises(Exception):
    #         find_weather()

# tests we would like

# test the find_weather() - Rada to try
# test calendar()
# test session_variables()