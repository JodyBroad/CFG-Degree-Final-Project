from flask import Flask, request, flash, url_for, redirect, render_template
# SQLAlchemy is how we link to the db
from flask_sqlalchemy import SQLAlchemy
# this is what we will use to capture data entered on the website
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
# validators will be useful for making sure valid input coming from the website
from wtforms.validators import Email, DataRequired

# creating an instance of the app
app = Flask(__name__)
# You will need to change the password here if your MySQL password is different
# the very first time you use this, make sure that you have gone into MySQL and just created a DB called
# "CFGFinalProject" - you only need to do this once, don't need to do anything else in MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password@localhost/CFGFinalProject"
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
#
# UserInfo table
# each row of the table
user_1 = UserInfo(forename='Jody', surname='Broad', email='Jody@email.com')
user_2 = UserInfo(forename='Melissa', surname='Long', email='Melissa@email.com')
user_3 = UserInfo(forename='Rada', surname='Kanchananupradit', email='Rada@email.com')
user_4 = UserInfo(forename='Khadija', surname='Warsama', email='Khadija@email.com')
user_5 = UserInfo(forename='Georgie', surname='Annett', email='Georgie@email.com')
# save the rows to a list
users = [user_1, user_2, user_3, user_4, user_5]

# MoodStatus
mood_1 = MoodStatus(mood='Happy')
mood_2 = MoodStatus(mood='Sad')
mood_3 = MoodStatus(mood='Angry')
mood_4 = MoodStatus(mood='Sleepy')
mood_5 = MoodStatus(mood='Sick')
mood_6 = MoodStatus(mood='Anxious')

# save the rows to a list
moods = [mood_1, mood_2, mood_3, mood_4, mood_5, mood_6]

# Sleep duration
sleep_1 = SleepDuration(duration='1-5 hours')
sleep_2 = SleepDuration(duration='5-8 hours')
sleep_3 = SleepDuration(duration='8-10 hours')
sleep_4 = SleepDuration(duration='11+ hours')

# save the rows to a list
sleeps = [sleep_1, sleep_2, sleep_3, sleep_4]

# Sleep Quality
quality_1 = SleepQuality(quality="Good")
quality_2 = SleepQuality(quality="Bad")

# save the rows to a list
qualities = [quality_1, quality_2]

# Daily Record
daily_record_1 = DailyRecord(user_id=1, record_date='2023-05-08', mood_id=1, mood_diary='Fine',
                             sleep_duration_id=3, sleep_quality_id=1, water_intake=1500, steps_taken=8500)
daily_record_2 = DailyRecord(user_id=2, record_date='2023-05-07', mood_id=2,
                             sleep_duration_id=2, sleep_quality_id=2, water_intake=1800, steps_taken=12000)
daily_record_3 = DailyRecord(user_id=3, record_date='2023-05-08', mood_id=4, mood_diary='So very tired',
                             sleep_duration_id=1, sleep_quality_id=2, water_intake=2500, steps_taken=11500)

# save the rows to a list
records = [daily_record_1, daily_record_2, daily_record_3]

# This should be in separate forms.py file but ok here for now

# forms

# example of how these work
class BasicRegistrationForm(FlaskForm):
    forename = StringField('First Name')
    surname = StringField('Last Name')
    email = StringField('Email', validators=[DataRequired(), Email(message="Please supply a valid email")])
    submit = SubmitField('Register')


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
        if len(email) == 0:
            error = "Please supply email address"
        else:
            user = UserInfo(forename=forename, surname=surname, email=email)
            db.session.add(user)
            db.session.commit()
            # gives you a message if it works
            flash(f'Success! {form.email.data} is now signed up for an account', 'success')
            return render_template('home.html', form=form, message=error, title='home')
    return render_template('home.html', form=form, message=error, title='home')


# getting list of current users
@app.route('/user_list', methods=['GET'])
def user_list():
    error = ""
    users = UserInfo.query
    return render_template('user_list.html', users=users, message=error)


if __name__ == '__main__':
    with app.app_context():
        # just drops any existing data
        db.drop_all()
        # creates all the tables
        db.create_all()
        # use this to add the list of users all at once (will add more for other tables)
        db.session.add_all(users)
        db.session.add_all(moods)
        db.session.add_all(sleeps)
        db.session.add_all(qualities)
        db.session.add_all(records)
        db.session.commit()
    app.run(debug=True)