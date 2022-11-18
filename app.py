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


@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/')
@app.route('/index')
def index():
    return render_template('notes.html')


@app.route('/notes')
def get_notes():
    return render_template('notes.html', user=a_user, notes=notes)


@app.route('/register', methods=['POST', 'GET'])
def register():
    """
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name, last_name, request.form['email'], h_password)
        # add user to database.py and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('get_notes'))

    # something went wrong - display register view
    return render_template('register.html', form=form)"""


"""
@app.route('/login', methods=['POST', 'GET'])
def login()
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('get_notes'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)


@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('index'))
"""

if __name__ == '__main__':
    app.run()
