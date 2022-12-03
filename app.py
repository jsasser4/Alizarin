from datetime import datetime

from flask import Flask, url_for, request, session, redirect
from flask import render_template
from bcrypt import hashpw, gensalt, checkpw
from src.form import RegisterForm, LoginForm, ProjectForm, SprintForm, TaskForm

from src import db
from src.model.task import Task
from src.model.user import User
from src.model.story import Story
from src.model.sprint import Sprint
from src.model.project import Project
from src.model.login_attempt import LoginAttempt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_mapping(
    SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/test')
def test():
    return render_template('app/test.html')


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('login'))


"""
@app.route('/projects/<project_id>/<sprint_id>', methods=['POST', 'GET'])
def add_task(project_id, sprint_id):
    current_user = db.session.query(User).filter_by(id=session['user_id']).first_or_404()
    current_sprint = db.session.query(Sprint).filter_by(id=sprint_id, project_id=project_id)
    form = TaskForm()
    if request.method == "POST" and form.validate_on_submit():
        name = request.form['name']
        desc = request.form['desc']
        sprint = Task(name=name, description=desc, sprint=current_sprint)
        db.session.add(sprint)
        db.session.commit()
    return render_template('app/sprints.html', user=current_user, form=form)
"""


@app.route('/project/add', methods=['GET', 'POST'])
def add_project():
    current_user = db.session.query(User).filter_by(id=session['user_id']).one()
    form = ProjectForm()
    if request.method == "POST" and form.validate_on_submit():
        name = request.form['name']
        comment = request.form['comment']
        project = Project(name=name, comment=comment, created_by=current_user)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('get_projects'))
    return render_template('app/add.html', form=form)

@app.route('/project/edit/<project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    project = db.session.query(Project).filter_by(id=project_id).one()
    if project is None:
        return redirect(url_for('get_projects'))
    form = ProjectForm()
    form.name.data = project.name
    form.comment.data = project.comment

    if request.method == "POST" and form.validate_on_submit():
        project_name = request.form['name']
        comment = request.form['comment']
        project.name = project_name
        project.comment = comment
        db.session.commit()
        return redirect(url_for('get_projects'))

    return render_template('app/edit.html', form=form, project=project)

@app.route('/project/delete/<project_id>', methods=['POST'])
def delete_project(project_id):
    current_user = db.session.query(User).filter_by(id=session['user_id']).one()
    project = db.session.query(Project).filter_by(id=project_id).one()
    db.session.delete(project)
    db.session.commit()
    return render_template('app/projects.html')


@app.route('/project/<project_id>', methods=['GET'])
def view_project(project_id):
    current_user = db.session.query(User).filter_by(id=session['user_id']).one()
    current_project = db.session.query(Project).filter_by(id=project_id).first_or_404()
    return render_template('app/project.html', project=current_project)


@app.route('/projects', methods=['GET'])
def get_projects():
    current_user = db.session.query(User).filter_by(id=session['user_id']).one()
    user_projects = db.session.query(Project).filter_by(created_by=current_user).all()
    if len(user_projects) == 0:
        return redirect(url_for('add_project'))
    return render_template('app/projects.html', projects=user_projects)

@app.route('/sprints')
def get_sprints():
    return render_template('app/sprints.html')


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
