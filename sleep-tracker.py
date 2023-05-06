from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/sleep-tracker', methods=['GET'])
def sleep_tracker():
    return render_template('sleep-tracker.html')

@app.route('/api/sleep-tracker/log-sleep', methods=['POST'])
def log_sleep():
    # to do - write to db
    # to do - consolidate with app.py?
    return request.get_json()


