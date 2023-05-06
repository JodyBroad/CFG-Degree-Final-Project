from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
# this is what we will use to capture data entered on the website
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email, DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password@localhost/CFGFinalProject"
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

# Models - tables for the db

# UserInfo table
class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)


def __init__(self, forename, surname, email):
   self.forename = forename
   self.surname = surname
   self.email = email


# Values for the table
#
# UserInfo table
# each row of the table
user_1 = UserInfo(forename='Jody', surname='Broad', email='Jody@email.com')
user_2 = UserInfo(forename='Melissa', surname='Long', email='Melissa@email.com')
# save the rows to a list
users = [user_1, user_2]

# need to create all the other tables!




# forms


# example of how these work
class BasicRegistrationForm(FlaskForm):
    forename = StringField('First Name')
    surname = StringField('Last Name')
    email = StringField('Email', validators=[DataRequired(), Email(message="Please supply a valid email")])
    submit = SubmitField('Register')


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
            # this flash doesn't work yet as I haven't set up a navbar or anything
            flash(f'Success! {form.email.data} is now signed up for an account', 'success')
            return render_template('home.html', form=form, message=error, title='home')
    return render_template('home.html', form=form, message=error, title='home')






if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)