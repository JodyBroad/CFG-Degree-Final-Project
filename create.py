from models import UserInfo, MoodStatus, SleepDuration, SleepQuality, DailyRecord
from extensions import db
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

def seed():
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
