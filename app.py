from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from datetime import date

app = Flask(__name__)

a_user = {'name': 'Taylor Sasser', 'email': 'jsasser4@uncc.edu'}
notes = {
    1: {'title': 'First Note', 'text': 'This is my first note', 'date': '10/18/2022'},
    2: {'title': 'Second Note', 'text': 'This is my second note', 'date': '10/18/2022'},
    3: {'title': 'Third Note', 'text': 'This is my third note', 'date': '10/18/2022'}
}


@app.route('/')
@app.route('/index')
def index():
    return render_template('notes.html', user=a_user)


@app.route('/notes')
def get_notes():
    return render_template('notes.html', user=a_user, notes=notes)


if __name__ == '__main__':
    app.run()
