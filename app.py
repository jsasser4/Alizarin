from datetime import datetime
from flask import Flask, url_for, request, session, redirect
from flask import render_template
from bcrypt import hashpw, gensalt, checkpw

from src.form import RegisterForm, LoginForm, ProjectForm, SprintForm, TaskForm
from src import db
from src.model.user import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_mapping(
    SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        h_password = hashpw(
            request.form['password'].encode('utf-8'), gensalt())
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        new_user = User(first_name=first_name,
                        last_name=last_name,
                        email=request.form['email'],
                        password_hash=h_password)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = first_name
        session['user_id'] = new_user.id
        return redirect(url_for('get_projects'))
    return render_template('app/register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        if checkpw(request.form['password'].encode('utf-8'), the_user.password_hash):
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            return redirect(url_for('get_projects'))
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("app/login.html", form=login_form)
    else:
        return render_template("app/login.html", form=login_form)


@app.route('/logout')
def logout():
    if session.get('user'):
        session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
