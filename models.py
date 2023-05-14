from extensions import db


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
