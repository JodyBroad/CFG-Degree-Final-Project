from flask import Flask
from extensions import db
from create import seed


def register_extensions(app):
    db.init_app(app)


def create_app():
    app = Flask(__name__)

    # You will need to change the password here if your MySQL password is different
    # the very first time you use this, make sure that you have gone into MySQL and just created a DB called
    # "CFGFinalProject" - you only need to do this once, don't need to do anything else in MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:ROOKwood1230@localhost/CFGFinalProject"
    app.config['SECRET_KEY'] = "random string"

    register_extensions(app)
    return app


app = create_app()

if __name__ == '__main__':
    with app.app_context():
        seed()
        # this import needs to be made here to avoid circular imports:
        # https://stackoverflow.com/questions/42909816/can-i-avoid-circular-imports-in-flask-and-sqlalchemy
        from views import *
    app.run(debug=True)

