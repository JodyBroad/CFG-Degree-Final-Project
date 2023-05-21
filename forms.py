# copied from Jody's main.py: 

# this is what we will use to capture data entered on the website
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField, IntegerField, PasswordField, EmailField
# validators will be useful for making sure valid input coming from the website
from wtforms.validators import Email, DataRequired


class BasicRegistrationForm(FlaskForm):
    forename = StringField('First Name')
    surname = StringField('Last Name')
    email = EmailField('Email', validators=[DataRequired(), Email(message="Please supply a valid email")])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register for a new account')


class LogInForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email(message="Please supply a valid email")])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In to Existing Account')


class TrackingForm(FlaskForm):
    # date is defaulting to today's date for now - can get this pulling through the date entered on the home screen
    # later
    # date = datetime.today().strftime('%Y-%m-%d')
    mood_id = RadioField('Select the emoji that most closely matches your mood ', choices=[(1, '\U0001F636 - No data'),
                                                                                        (2, '\U0001F600 - Happy'),
                                                                                        (3, '\U0001F622 - Sad'),
                                                                                        (4, '\U0001F92C - Angry'),
                                                                                        (5, '\U0001F634 - Sleepy'),
                                                                                        (6, '\U0001F912 - Sick'),
                                                                                        (7, '\U0001F61F - Anxious')],
                                                                                        default=1, coerce=int)
    mood_diary = StringField('Add a short optional reflective diary entry ')
    sleep_duration_id = SelectField('How many hours did you sleep? ', choices=[(1, 'No data'), (2, '1-5 hours'),
                                                                              (3, '5-8 hours'), (4, '8-10 hours'),
                                                                              (5, '10+ hours')])
    sleep_quality_id = SelectField('How would you rate the quality of your sleep? ', choices=[(1, 'No data'),
                                                                                             (2, 'Good'), (3, 'Bad')])
    water_intake = IntegerField('How many ml of water have you drunk today? ')
    steps_taken = IntegerField('How many steps have you taken today? ')
    submit = SubmitField('Submit tracking record ')
