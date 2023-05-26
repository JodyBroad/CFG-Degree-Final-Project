# from main import db
#
# if db:
#     print("db connection working")

import unittest
from flask import Flask
from weather import return_url
from forms import BasicRegistrationForm, LogInForm, TrackingForm

class TestReturnUrl(unittest.TestCase):
    def test_return_url(self):
        # Testing if sunny URL is returned
        sunny_codes = [0, 1]
        expected_sunny_url = "https://source.unsplash.com/lVDnLUACI18"
        actual_sunny_url = return_url(sunny_codes)
        self.assertEqual(actual_sunny_url, expected_sunny_url)

        # Testing for cloudy URL
        cloudy_codes = [2, 3]
        expected_cloudy_url = "https://source.unsplash.com/uftVkZ1ikn4"
        actual_cloudy_url = return_url(cloudy_codes)
        self.assertEqual(actual_cloudy_url, expected_cloudy_url)

        # Testing for foggy URL
        foggy_codes = [45, 48]
        expected_foggy_url = "https://source.unsplash.com/e2uTOpgW5Ec"
        actual_foggy_url = return_url(foggy_codes)
        self.assertEqual(actual_foggy_url, expected_foggy_url)

        # Testing for rain or drizzle URL
        rain_or_drizzle_codes = [51, 53, 55, 56, 57] + [61, 63, 65, 80, 81, 82]
        expected_rain_or_drizzle_url = "https://source.unsplash.com/8yt8kBuEqok"
        actual_rain_or_drizzle_url = return_url(rain_or_drizzle_codes)
        self.assertEqual(actual_rain_or_drizzle_url, expected_rain_or_drizzle_url)

        # Testing for snow URL
        snow_codes = [71, 73, 75, 77, 85, 86]
        expected_snow_url = "https://source.unsplash.com/efuwb5eBDrI"
        actual_snow_url = return_url(snow_codes)
        self.assertEqual(actual_snow_url, expected_snow_url)

        # Testing for "else" case URL
        other_codes = [""]
        expected_other_url = "https://source.unsplash.com/lVDnLUACI18"
        actual_other_url = return_url(other_codes)
        self.assertEqual(actual_other_url, expected_other_url)


class TestForms(unittest.TestCase):
    def test_basic_registration_form_valid_email(self):
        form = BasicRegistrationForm()
        form.email.data = 'test@example.com'
        self.assertTrue(form.validate())

    def test_login_form_valid_email(self):
        form = LogInForm()
        form.email.data = 'test@example.com'
        self.assertTrue(form.validate())

    def test_forms_empty_password(self):
        # Test BasicRegistrationForm
        form = BasicRegistrationForm()
        form.password.data = ''
        self.assertFalse(form.validate())
        self.assertIn('Field must be provided.', form.password.errors)

        # Test LogInForm
        form = LogInForm()
        form.password.data = ''
        self.assertFalse(form.validate())
        self.assertIn('Field must be provided.', form.password.errors)

    def test_login_form_valid_credentials(self):
        form = LogInForm()
        form.email.data = 'test@example.com'
        form.password.data = 'password123'
        self.assertTrue(form.validate())

    def test_tracking_form_valid_submission(self):
        form = TrackingForm()
        form.mood_id.data = 2
        form.mood_diary.data = 'Feeling great today!'
        form.sleep_duration_id.data = 3
        form.sleep_quality_id.data = 2
        form.water_intake.data = 1500
        form.steps_taken.data = 5000
        self.assertTrue(form.validate())

    def test_tracking_form_invalid_submission(self):
        # Test missing required fields
        form = TrackingForm()
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.mood_id.errors)
        self.assertIn('This field is required.', form.sleep_duration_id.errors)
        self.assertIn('This field is required.', form.sleep_quality_id.errors)

        # Test invalid data
        form = TrackingForm()
        form.mood_id.data = 8  # Invalid choice
        form.sleep_duration_id.data = 6  # Invalid choice
        form.sleep_quality_id.data = 4  # Invalid choice
        form.water_intake.data = 'abc'  # Invalid input
        form.steps_taken.data = 'xyz'  # Invalid input
        self.assertFalse(form.validate())
        self.assertIn('Invalid choice.', form.mood_id.errors)
        self.assertIn('Invalid choice.', form.sleep_duration_id.errors)
        self.assertIn('Invalid choice.', form.sleep_quality_id.errors)
        self.assertIn('Invalid integer value.', form.water_intake.errors)
        self.assertIn('Invalid integer value.', form.steps_taken.errors)


     # CHECK OVER THIS TEST PLEASE 25.05.2023
    def test_daily_record_submission(self):
        with self.app:
            # Log in a user
            self.app.post('/home', data=dict(email='test@example.com', password='password'), follow_redirects=True)

            # Test successful record submission
            response = self.app.post('/tracking', data=dict(mood_id=1, mood_diary='Feeling good',
                                                            sleep_duration_id=1, sleep_quality_id=1,
                                                            water_intake=8, steps_taken=5000),
                                     follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            record = DailyRecord.query.filter_by(user_id=session['id_number']).first()
            self.assertIsNotNone(record)
            self.assertEqual(record.mood_id, 1)
            self.assertEqual(record.mood_diary, 'Feeling good')

            # Test missing record fields
            response = self.app.post('/tracking', data=dict(mood_id='', mood_diary='',
                                                            sleep_duration_id='', sleep_quality_id='',
                                                            water_intake='', steps_taken=''),
                                     follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Please fill in all the required fields', response.data)
            self.assertIsNone(DailyRecord.query.filter_by(user_id=session['id_number']).first())


if __name__ == '__main__':
    app = Flask(__name__)

    with app.app_context():
        unittest.main()
