from app import db, app
from flask import Flask, session
from unittest import TestCase, mock
from flask_sqlalchemy import SQLAlchemy
from models import *
from views import *
from forms import *


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


