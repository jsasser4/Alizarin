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
    app.run(debug=True)
