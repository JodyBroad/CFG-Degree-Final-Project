from app import db, app
from flask import Flask
from unittest import TestCase
from flask_sqlalchemy import SQLAlchemy
from views import *
from weather import *


class TestDBConnection(TestCase):

    # checks we have a valid instance of a SQLAlchemy database
    def test_db_connection(self):
        self.assertIsInstance(db, SQLAlchemy)


class TestFlaskApp(TestCase):

    # checks we have a valid instance of a Flask app
    def test_flask_app(self):
        self.assertIsInstance(app, Flask)


# password must be correct on app.py

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

    # testing that Exception error is raised when request response is not 200
    def test_find_weather_failure(self):
        response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=51.51&longitude=-0.13&forecast_days=1"
                                "&timezone=GMT&daily=weathercode")
        with self.assertRaises(Exception):
            response_code(response, 404)


# Georgie tried really hard to get log in testing and db writing, but testing was too complicated - Youri said we'd
# need to know Selenium,which none of us do

    # def test_daily_record_submission(self):
    #     with self.app:
    #         # Log in a user
    #         self.app.post('/home', data=dict(email='test@example.com', password='password'), follow_redirects=True)
    #
    #         # Test successful record submission
    #         response = self.app.post('/tracking', data=dict(mood_id=1, mood_diary='Feeling good', sleep_duration_id=1,
    #                                     sleep_quality_id=1, water_intake=8, steps_taken=5000), follow_redirects=True)
    #         self.assertEqual(response.status_code, 200)
    #         record = DailyRecord.query.filter_by(user_id=session['id_number']).first()
    #         self.assertIsNotNone(record)
    #         self.assertEqual(record.mood_id, 1)
    #         self.assertEqual(record.mood_diary, 'Feeling good')
    #
    #         # Test missing record fields
    #         response = self.app.post('/tracking', data=dict(mood_id='', mood_diary='', sleep_duration_id='',
    #                                     sleep_quality_id='', water_intake='', steps_taken=''), follow_redirects=True)
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn(b'Please fill in all the required fields', response.data)
    #         self.assertIsNone(DailyRecord.query.filter_by(user_id=session['id_number']).first())


# These tests are really just trying to test the validation that is part of Flask forms, so not required

# class TestForms(TestCase):
#     def test_basic_registration_form_valid_email(self):
#         form = BasicRegistrationForm()
#         form.email.data = 'test@example.com'
#         self.assertTrue(form.validate())
#
#     def test_login_form_valid_email(self):
#         form = LogInForm()
#         form.email.data = 'test@example.com'
#         self.assertTrue(form.validate())
#
#     def test_forms_empty_password(self):
#         # Test BasicRegistrationForm
#         form = BasicRegistrationForm()
#         form.password.data = ''
#         self.assertFalse(form.validate())
#         self.assertIn('Field must be provided.', form.password.errors)
#
#         # Test LogInForm
#         form = LogInForm()
#         form.password.data = ''
#         self.assertFalse(form.validate())
#         self.assertIn('Field must be provided.', form.password.errors)
#
#     def test_login_form_valid_credentials(self):
#         form = LogInForm()
#         form.email.data = 'test@example.com'
#         form.password.data = 'password123'
#         self.assertTrue(form.validate())
#
#     def test_tracking_form_valid_submission(self):
#         form = TrackingForm()
#         form.mood_id.data = 2
#         form.mood_diary.data = 'Feeling great today!'
#         form.sleep_duration_id.data = 3
#         form.sleep_quality_id.data = 2
#         form.water_intake.data = 1500
#         form.steps_taken.data = 5000
#         self.assertTrue(form.validate())
#
#     def test_tracking_form_invalid_submission(self):
#         # Test missing required fields
#         form = TrackingForm()
#         self.assertFalse(form.validate())
#         self.assertIn('This field is required.', form.mood_id.errors)
#         self.assertIn('This field is required.', form.sleep_duration_id.errors)
#         self.assertIn('This field is required.', form.sleep_quality_id.errors)
#
#         # Test invalid data
#         form = TrackingForm()
#         form.mood_id.data = 8  # Invalid choice
#         form.sleep_duration_id.data = 6  # Invalid choice
#         form.sleep_quality_id.data = 4  # Invalid choice
#         form.water_intake.data = 'abc'  # Invalid input
#         form.steps_taken.data = 'xyz'  # Invalid input
#         self.assertFalse(form.validate())
#         self.assertIn('Invalid choice.', form.mood_id.errors)
#         self.assertIn('Invalid choice.', form.sleep_duration_id.errors)
#         self.assertIn('Invalid choice.', form.sleep_quality_id.errors)
#         self.assertIn('Invalid integer value.', form.water_intake.errors)
#         self.assertIn('Invalid integer value.', form.steps_taken.errors)


# other tests we would like

# test calendar()
# test session_variables()
