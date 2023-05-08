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
    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)


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

# need to create all the other tables!



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
        db.session.commit()
    app.run(debug=True)