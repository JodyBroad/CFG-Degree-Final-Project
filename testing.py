from app import db, app
from flask import Flask, session
from unittest import TestCase, main, mock
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
    
    def test_calendar_returns_data_for_get_request(self):
        with app.app_context():
            users = db.session.query(UserInfo).all()
            self.assertIsNotNone(users)

        with app.test_client() as test_client:
            # Request the calendar page
            response = test_client.get('/calendar')

            # Check the response is successful
            self.assertEqual(response.status_code, 200)

            # Check the select dropdowns exist
            self.assertIn(b'id="selected-user"', response.data)
            self.assertIn(b'id="selected-metric"', response.data)

            # Check each user name is in the response HTML (select drop-down option should have these)
            for user in users:
                self.assertIn(user.get_full_name().encode(), response.data)

            # Check each metric option is in the response HTML (select drop-down option should have these)
            for option in ['Mood', 'Sleep Quality', 'Sleep Duration', 'Water Consumption', 'Steps Taken']:
                self.assertIn(option.encode(), response.data)

            # Check that the calendar element exists
            self.assertIn(b'id="calendar"', response.data)
            
            # Check that the navbar has all the correct links
            self.assert_navbar_contains_links(response.data)

    def test_calendar_returns_405_for_post_post(self):
        with app.test_client() as test_client:
            response = test_client.post('/calendar')
            self.assertEqual(response.status_code, 405)

    def test_not_found(self):
        with app.test_client() as test_client:
            response = test_client.get('/not-existent-route')
            self.assertEqual(response.status_code, 404)
            self.assertIn(b'Not Found', response.data)

    def assert_navbar_contains_links(self, response_data):
        links = [
            '<a class="nav-link" href="/">Home</a>',
            '<a class="nav-link" href="/calendar">Calendar</a>',
            '<a class="nav-link" href="/tracking">Tracking</a>',
            '<a class="nav-link" href="/my_user_data">My Daily Records</a>',
            '<a class="nav-link" href="/user_data">All User Data</a>',
            '<a class="nav-link" href="/user_list">User List</a>',
        ]

        for link in links:
            self.assertIn(link.encode(), response_data)

    # test a query that should fail and make sure it raises an error if table name doesn't exist
    # def test_not_user_list(self):
    #     with app.app_context():
    #         # would be good to get this testing something more detailed than just if it is bringing stuff back
    #         # not sure this is a valid test, was just trying to get it to make sure to raise an error if invalid table
    #         # name, but python picks this up before it is an issue, so not sure it is valid!
    #         with self.assertRaises(NameError):
    #             users = UserNotInfo.query


class TestReturnUrl(TestCase):

    def test_return_url_sunny(self):
        # # Testing if sunny URL is returned
        sunny_codes = [0, 1]
        expected_sunny_url = "https://source.unsplash.com/LD_phgnVdOA"
        actual_sunny_url_0 = return_url(sunny_codes[0])
        actual_sunny_url_1 = return_url(sunny_codes[1])
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

    def test_return_url_rain_or_drizzle(self):
        # # Testing for rain or drizzle URL
        rain_or_drizzle_codes = [51, 53, 55, 56, 57, 61, 63, 65, 80, 81, 82]
        expected_rain_or_drizzle_url = "https://source.unsplash.com/8yt8kBuEqok"
        actual_rain_or_drizzle_url_51 = return_url(rain_or_drizzle_codes[0])
        actual_rain_or_drizzle_url_53 = return_url(rain_or_drizzle_codes[1])
        actual_rain_or_drizzle_url_55 = return_url(rain_or_drizzle_codes[2])
        actual_rain_or_drizzle_url_56 = return_url(rain_or_drizzle_codes[3])
        actual_rain_or_drizzle_url_57 = return_url(rain_or_drizzle_codes[4])
        actual_rain_or_drizzle_url_61 = return_url(rain_or_drizzle_codes[5])
        actual_rain_or_drizzle_url_63 = return_url(rain_or_drizzle_codes[6])
        actual_rain_or_drizzle_url_65 = return_url(rain_or_drizzle_codes[7])
        actual_rain_or_drizzle_url_80 = return_url(rain_or_drizzle_codes[8])
        actual_rain_or_drizzle_url_81 = return_url(rain_or_drizzle_codes[9])
        actual_rain_or_drizzle_url_82 = return_url(rain_or_drizzle_codes[10])
        self.assertEqual(actual_rain_or_drizzle_url_51, expected_rain_or_drizzle_url)
        self.assertEqual(actual_rain_or_drizzle_url_53, expected_rain_or_drizzle_url)
        self.assertEqual(actual_rain_or_drizzle_url_55, expected_rain_or_drizzle_url)
        self.assertEqual(actual_rain_or_drizzle_url_56, expected_rain_or_drizzle_url)
        self.assertEqual(actual_rain_or_drizzle_url_57, expected_rain_or_drizzle_url)
        self.assertEqual(actual_rain_or_drizzle_url_61, expected_rain_or_drizzle_url)
        self.assertEqual(actual_rain_or_drizzle_url_63, expected_rain_or_drizzle_url)
        self.assertEqual(actual_rain_or_drizzle_url_65, expected_rain_or_drizzle_url)
        self.assertEqual(actual_rain_or_drizzle_url_80, expected_rain_or_drizzle_url)
        self.assertEqual(actual_rain_or_drizzle_url_81, expected_rain_or_drizzle_url)
        self.assertEqual(actual_rain_or_drizzle_url_82, expected_rain_or_drizzle_url)

    # not yet working, just needs reformatting as per the above
    # Testing for snow URL
    def test_return_url_snow(self):
        snow_codes = [71, 73, 75, 77, 85, 86]
        expected_snow_url = "https://source.unsplash.com/efuwb5eBDrI"
        actual_snow_url_71 = return_url(snow_codes[0])
        actual_snow_url_73 = return_url(snow_codes[1])
        actual_snow_url_75 = return_url(snow_codes[2])
        actual_snow_url_77 = return_url(snow_codes[3])
        actual_snow_url_85 = return_url(snow_codes[4])
        actual_snow_url_86 = return_url(snow_codes[5])
        self.assertEqual(actual_snow_url_71, expected_snow_url)
        self.assertEqual(actual_snow_url_73, expected_snow_url)
        self.assertEqual(actual_snow_url_75, expected_snow_url)
        self.assertEqual(actual_snow_url_77, expected_snow_url)
        self.assertEqual(actual_snow_url_85, expected_snow_url)
        self.assertEqual(actual_snow_url_86, expected_snow_url)

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
