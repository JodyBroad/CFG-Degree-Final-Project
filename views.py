from flask import request, flash, render_template
from models import UserInfo, DailyRecord, SleepDuration, SleepQuality, MoodStatus
from forms import *
from app import app
from extensions import db
from datetime import datetime

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