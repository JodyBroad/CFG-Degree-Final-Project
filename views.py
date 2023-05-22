from flask import request, flash, render_template, session, redirect, url_for
from models import UserInfo, DailyRecord, SleepDuration, SleepQuality, MoodStatus
from forms import *
from app import app
from extensions import db
from datetime import datetime
from weather import find_weather


@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    error = ""
    form = LogInForm()

    if request.method == 'POST':
        # pop previous session in case someone was already logged in
        session.pop('logged_in', default=None)
        session.pop('id_number', default=None)
        session.pop('logged_in_username', default=None)

        # # taking the username and password from the form so that we can compare to the db
        form_username = request.form['email']
        form_password = request.form['password']

        # just to check query works
        # db_query_all = UserInfo.query.all()
        # print(db_query_all)

        # this is the refined query - will only return something if it matches both username and password
        db_username_password = UserInfo.query.filter_by(email=form_username, password=form_password).all()
        print(db_username_password)
        for user_id in db_username_password:
            user_id_for_session_variable = user_id.user_id

        # setting initial value of password_check to false:
        password_check = False

        if db_username_password:
            password_check = True
        else:
            password_check = False

        if password_check:

            # if validation has passed, save the username to the session object
            session['logged_in_username'] = form_username
            session['logged_in'] = True
            session['id_number'] = user_id_for_session_variable

            # gives you a message if it works
            flash(f'Success! {form.email.data} is now logged in', 'success')
            return render_template('home.html', form=form, message=error, title='home', weather_img=find_weather())
        else:
            flash(f' Login failed, please try again', 'danger')
            return render_template('home.html', form=form, message=error, title='home', weather_img=find_weather())
    return render_template('home.html', form=form, message=error, title='home', weather_img=find_weather())


@app.route('/logout')
def logout():
    error = ""

    # Clear the username stored in the session object
    session.pop('logged_in_username', default=None)
    session.pop('logged_in', default=None)
    session.pop('id_number', default=None)

    flash(f' You have logged out!', 'success')
    return render_template('logout.html', title='Logout', message=error, weather_img=find_weather())


@app.route('/register', methods=['GET', 'POST'])
def register():
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
            return render_template('register.html', form=form, message=error, title='register',
                                   weather_img=find_weather())
    return render_template('register.html', form=form, message=error, title='register', weather_img=find_weather())


@app.route('/tracking', methods=['GET', 'POST'])
def tracking():
    error = ""
    form = TrackingForm()
    if request.method == 'POST':
        # if user is logged in:
        if 'logged_in' in session:
            # date is defaulting to today's date for now - can get this pulling through the date entered on the home
            # screen later
            record_date = datetime.today().strftime('%Y-%m-%d')
            user_id = session['id_number']
            mood_id = form.mood_id.data
            mood_diary = form.mood_diary.data
            sleep_duration_id = form.sleep_duration_id.data
            sleep_quality_id = form.sleep_quality_id.data
            water_intake = form.water_intake.data
            steps_taken = form.steps_taken.data
            new_daily_record = DailyRecord(user_id=user_id, record_date=record_date, mood_id=mood_id,
                                           mood_diary=mood_diary, sleep_duration_id=sleep_duration_id,
                                           sleep_quality_id=sleep_quality_id, water_intake=water_intake,
                                           steps_taken=steps_taken)
            db.session.add(new_daily_record)
            db.session.commit()
            flash(f'Success! Your entry was added', 'success')
            # if successful, return to the homepage
            return render_template('tracking.html', form=form, message=error, title='tracking',
                                   weather_img=find_weather())
        else:
            flash(f'Please log in to make an entry', 'danger')
            return redirect(url_for('home'))
    return render_template('tracking.html', form=form, message=error, title='tracking', weather_img=find_weather())


# getting list of current users
@app.route('/user_list', methods=['GET'])
def user_list():
    error = ""
    users = UserInfo.query
    return render_template('user_list.html', users=users, message=error, weather_img=find_weather())


# getting a list of all users daily records
@app.route('/user_data', methods=['GET'])
def user_data():
    error = ""
    user_data = db.session.query(UserInfo, DailyRecord, MoodStatus, SleepDuration, SleepQuality).select_from(UserInfo)\
        .join(DailyRecord).join(MoodStatus).join(SleepDuration).join(SleepQuality).order_by(DailyRecord.record_date).all()
    headings = ('First Name', 'Last Name', 'Email', 'Date of Record', 'Mood', 'Diary', 'Sleep Duration',
                'Sleep Quality', 'Water intake', 'Steps taken')
    return render_template('user_data.html', user_data=user_data, headings=headings, message=error,
                           weather_img=find_weather())

@app.route('/calendar', methods=['GET'])
def calendar():
    users = [user_info.serialize() for user_info in db.session.query(UserInfo).all()]

    user_data = db.session.query(UserInfo, DailyRecord, MoodStatus, SleepDuration, SleepQuality)\
        .select_from(UserInfo)\
        .join(DailyRecord)\
        .join(MoodStatus)\
        .join(SleepDuration)\
        .order_by(UserInfo.user_id)\
        .order_by(DailyRecord.record_date)\
        .all()

    return render_template('calendar.html', user_data=user_data, users=users)

# getting a list of logged in users daily records
@app.route('/my_user_data', methods=['GET'])
def my_user_data():
    error = ""
    if 'logged_in' in session:
        user_id = session['id_number']
        user_data = db.session.query(UserInfo, DailyRecord, MoodStatus, SleepDuration, SleepQuality).select_from\
            (UserInfo).filter_by(user_id=user_id).join(DailyRecord).join(MoodStatus).join(SleepDuration).\
            join(SleepQuality).order_by(DailyRecord.record_date).all()
        headings = ('First Name', 'Last Name', 'Email', 'Date of Record', 'Mood', 'Diary', 'Sleep Duration',
                    'Sleep Quality', 'Water intake', 'Steps taken')
        return render_template('my_user_data.html', user_data=user_data, headings=headings, message=error,
                               weather_img=find_weather())
    else:
        flash(f'Please log in to view your entries', 'danger')
        return redirect(url_for('home'))
