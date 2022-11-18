from flask import Flask
from flask import render_template
from src import db
from src.model import login_attempt, project, sprint, story, task, user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

a_user = {'name': 'Taylor Sasser', 'email': 'jsasser4@uncc.edu'}
notes = {
    1: {'title': 'First Note', 'text': 'This is my first note', 'date': '10/18/2022'},
    2: {'title': 'Second Note', 'text': 'This is my second note', 'date': '10/18/2022'},
    3: {'title': 'Third Note', 'text': 'This is my third note', 'date': '10/18/2022'}
}


@app.route('/register')
def home():
    return render_template('app/register.html')


@app.route('/')
@app.route('/index')
def index():
    return render_template('app/home.html')


@app.route('/projects')
def get_projects():
    return render_template('app/projects.html')


@app.route('/login')
def get_login():
    return render_template('app/login.html')


if __name__ == '__main__':
    app.run()
