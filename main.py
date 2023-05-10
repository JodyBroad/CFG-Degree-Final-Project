from flask import Flask, request, flash, url_for, redirect, render_template
# SQLAlchemy is how we link to the db
from flask_sqlalchemy import SQLAlchemy
# this is what we will use to capture data entered on the website
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField, IntegerField
# validators will be useful for making sure valid input coming from the website
from wtforms.validators import Email, DataRequired
# for date info
from datetime import datetime

# creating an instance of the app
app = Flask(__name__)
# You will need to change the password here if your MySQL password is different
# the very first time you use this, make sure that you have gone into MySQL and just created a DB called
# "CFGFinalProject" - you only need to do this once, don't need to do anything else in MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:IncorrectPaiPolca25@localhost/CFGFinalProject"
app.config['SECRET_KEY'] = "random string"
# creating a db accessible via the app
db = SQLAlchemy(app)


# This should ideally be in separate models.py file but is ok here for now

# Models - table structure for the db

# UserInfo table
class UserInfo(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(15), nullable=False)
    # not field in table but relationship between userInfo and DailyRecord
    user_info = db.relationship('DailyRecord', backref='user_info')


class MoodStatus(db.Model):
    mood_id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(50), nullable=False)
    # not field in table but relationship between MoodStatus and DailyRecord
    mood_status = db.relationship('DailyRecord', backref='mood_status')


class SleepDuration(db.Model):
    sleep_duration_id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.String(50), nullable=False)
    # not field in table but relationship between SleepDuration and DailyRecord
    sleep_duration = db.relationship('DailyRecord', backref='sleep_duration')


class SleepQuality(db.Model):
    sleep_quality_id = db.Column(db.Integer, primary_key=True)
    quality = db.Column(db.String(50), nullable=False)
    # not field in table but relationship between SleepQuality and DailyRecord
    sleep_quality = db.relationship('DailyRecord', backref='sleep_quality')


class DailyRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id is the Foreign Key linking to the UserInfo table
    user_id = db.Column(db.Integer, db.ForeignKey('user_info'), nullable=False)
    record_date = db.Column(db.Date, nullable=False)
    # mood_id is the Foreign Key linking to the MoodStatus table
    mood_id = db.Column(db.Integer, db.ForeignKey('mood_status'))
    # save the mood diary free text entry to the daily record
    mood_diary = db.Column(db.String(250), nullable=True)
    # sleep_duration_id is the Foreign Key linking to the SleepDuration table (will be one of a choice of categories)
    sleep_duration_id = db.Column(db.Integer, db.ForeignKey('sleep_duration'))
    # sleep_quality_id is the Foreign Key linking to the SleepQuality table (will be one of a choice of categories)
    sleep_quality_id = db.Column(db.Integer, db.ForeignKey('sleep_quality'))
    water_intake = db.Column(db.Integer, nullable=True)
    steps_taken = db.Column(db.Integer, nullable=True)


# This should ideally be in separate create.py file but ok here for now

# Values for the table to be inserted

# UserInfo table
# each row of the table
user_1 = UserInfo(forename='Jody', surname='Broad', email='Jody@email.com', password='password1')
user_2 = UserInfo(forename='Melissa', surname='Long', email='Melissa@email.com', password='password2')
user_3 = UserInfo(forename='Rada', surname='Kanchananupradit', email='Rada@email.com', password='password3')
user_4 = UserInfo(forename='Khadija', surname='Warsama', email='Khadija@email.com', password='password4')
user_5 = UserInfo(forename='Georgie', surname='Annett', email='Georgie@email.com', password='password5')
# save the rows to a list
users = [user_1, user_2, user_3, user_4, user_5]

# MoodStatus
mood_1 = MoodStatus(mood='No data')
mood_2 = MoodStatus(mood='Happy')
mood_3 = MoodStatus(mood='Sad')
mood_4 = MoodStatus(mood='Angry')
mood_5 = MoodStatus(mood='Sleepy')
mood_6 = MoodStatus(mood='Sick')
mood_7 = MoodStatus(mood='Anxious')

# save the rows to a list
moods = [mood_1, mood_2, mood_3, mood_4, mood_5, mood_6, mood_7]

# Sleep duration
sleep_1 = SleepDuration(duration='No data')
sleep_2 = SleepDuration(duration='1-5 hours')
sleep_3 = SleepDuration(duration='5-8 hours')
sleep_4 = SleepDuration(duration='8-10 hours')
sleep_5 = SleepDuration(duration='10+ hours')

# save the rows to a list
sleeps = [sleep_1, sleep_2, sleep_3, sleep_4, sleep_5]

# Sleep Quality
quality_1 = SleepQuality(quality="No data")
quality_2 = SleepQuality(quality="Good")
quality_3 = SleepQuality(quality="Bad")

# save the rows to a list
qualities = [quality_1, quality_2, quality_3]

# Daily Record
daily_record_1 = DailyRecord(user_id=1, record_date='2023-05-08', mood_id=2, mood_diary='Fine',
                             sleep_duration_id=3, sleep_quality_id=2, water_intake=1500, steps_taken=8500)
daily_record_2 = DailyRecord(user_id=2, record_date='2023-05-07', mood_id=3,
                             sleep_duration_id=3, sleep_quality_id=3, water_intake=1800, steps_taken=12000)
daily_record_3 = DailyRecord(user_id=3, record_date='2023-05-08', mood_id=5, mood_diary='So very tired',
                             sleep_duration_id=2, sleep_quality_id=3, water_intake=2500, steps_taken=11500)
daily_record_4 = DailyRecord(user_id=3, record_date='2023-05-07', mood_id=4, mood_diary='This is fine',
                             sleep_duration_id=5, sleep_quality_id=2, water_intake=2000, steps_taken=11500)
daily_record_5 = DailyRecord(user_id=3, record_date='2023-05-06', mood_id=3, sleep_duration_id=4, sleep_quality_id=2,
                             water_intake=1500, steps_taken=1000)

# save the rows to a list
records = [daily_record_1, daily_record_2, daily_record_3, daily_record_4, daily_record_5]


# This should be in separate forms.py file but ok here for now

# forms

# example of how these work
class BasicRegistrationForm(FlaskForm):
    forename = StringField('First Name')
    surname = StringField('Last Name')
    email = StringField('Email', validators=[DataRequired(), Email(message="Please supply a valid email")])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class TrackingForm(FlaskForm):
    # date is defaulting to today's date for now - can get this pulling through the date entered on the home screen later
    # date = datetime.today().strftime('%Y-%m-%d')
    mood_id = RadioField('Select the emoji that most closely matches your mood', choices=[(1, 'No data'), (2, 'Happy'),
                                                                                          (3, 'Sad'), (4, 'Angry'),
                                                                                          (5, 'Sleepy'), (6, 'Sick'),
                                                                                          (7, 'Anxious')], default=1,
                                                                                            coerce=int)
    mood_diary = StringField('Add a short optional reflective diary entry')
    sleep_duration_id = SelectField('How many hours did you sleep?', choices=[(1, 'No data'), (2, '1-5 hours'),
                                                                              (3, '5-8 hours'), (4, '8-10 hours'),
                                                                              (5, '10+ hours')])
    sleep_quality_id = SelectField('How would you rate the quality of your sleep?', choices=[(1, 'No data'),
                                                                                             (2, 'Good'), (3, 'Bad')])
    water_intake = IntegerField('How many ml of water have you drunk today?')
    steps_taken = IntegerField('How many steps have you taken today?')
    submit = SubmitField('Submit tracking record')


# This should be in separate routes.py file but ok here for now
# routes

@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    error = ""
    form = BasicRegistrationForm()

    if request.method == 'POST':
        forename = form.forename.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data
        if len(email) == 0:
            error = "Please supply email address"
        else:
            user = UserInfo(forename=forename, surname=surname, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            # gives you a message if it works
            flash(f'Success! {form.email.data} is now signed up for an account', 'success')
            return render_template('home.html', form=form, message=error, title='home')
    return render_template('home.html', form=form, message=error, title='home')


@app.route('/tracking', methods=['GET', 'POST'])
def tracking():
    error = ""
    form = TrackingForm()
    if request.method == 'POST':
        # date is defaulting to today's date for now - can get this pulling through the date entered on the home screen
        # later
        record_date = datetime.today().strftime('%Y-%m-%d')
        # defaulting the user id until we have the log in working
        user_id = 1
        mood_id = form.mood_id.data
        mood_diary = form.mood_diary.data
        sleep_duration_id = form.sleep_duration_id.data
        sleep_quality_id = form.sleep_quality_id.data
        water_intake = form.water_intake.data
        steps_taken = form.steps_taken.data
        new_daily_record = DailyRecord(user_id=user_id, record_date=record_date, mood_id=mood_id, mood_diary=mood_diary,
                                       sleep_duration_id=sleep_duration_id, sleep_quality_id=sleep_quality_id,
                                       water_intake=water_intake, steps_taken=steps_taken)
        db.session.add(new_daily_record)
        db.session.commit()
        flash(f'Success! Your entry was added', 'success')
        # if successful, return to the homepage
        return render_template('tracking.html', form=form, message=error, title='tracking')
    return render_template('tracking.html', form=form, message=error, title='tracking')




# getting list of current users
@app.route('/user_list', methods=['GET'])
def user_list():
    error = ""
    users = UserInfo.query
    return render_template('user_list.html', users=users, message=error)


# getting a list of all users daily records
@app.route('/user_data', methods=['GET'])
def user_data():
    error = ""
    user_data = db.session.query(UserInfo, DailyRecord, MoodStatus, SleepDuration, SleepQuality).select_from(UserInfo)\
        .join(DailyRecord).join(MoodStatus).join(SleepDuration).join(SleepQuality).all()
    headings = ('First Name', 'Last Name', 'Email', 'Date of Record', 'Mood', 'Diary', 'Sleep Duration',
                'Sleep Quality', 'Water intake', 'Steps taken')
    return render_template('user_data.html', user_data=user_data, headings=headings, message=error)

if __name__ == '__main__':
    with app.app_context():
        # just drops any existing data
        db.drop_all()
        # creates all the tables
        db.create_all()
        # use this to populate the tables with all the data (will add more for other tables)
        db.session.add_all(users)
        db.session.add_all(moods)
        db.session.add_all(sleeps)
        db.session.add_all(qualities)
        db.session.add_all(records)
        db.session.commit()
    app.run(debug=True)
