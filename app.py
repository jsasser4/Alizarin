from datetime import datetime
from flask import Flask, url_for, request, session, redirect
from flask import render_template
from bcrypt import hashpw, gensalt, checkpw

from src.form import RegisterForm, LoginForm, ProjectForm, SprintForm, TaskForm
from src import db
from src.model.project import Project
from src.model.sprint import Sprint
from src.model.task import Task
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
    if session.get('user'):
        return redirect(url_for('projects'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        if checkpw(request.form['password'].encode('utf-8'), the_user.password_hash):
            session['user'] = the_user.first_name
            session['user_id'] = the_user.user_id
            return redirect(url_for('projects'))
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("app/login.html", form=login_form)
    else:
        return render_template("app/login.html", form=login_form)

@app.route('/project', methods=['POST', 'GET'])
@app.route('/project/<project_id>', methods=['POST', 'GET'])
def project(project_id=None):
    user = db.session.query(User).filter_by(user_id=session.get('user_id')).one()

    active_project = None
    if project_id is not None:
        active_project = db.session.query(Project).filter_by(project_id=project_id).one()
    elif len(user.projects) != 0:
        active_project = user.projects[0]

    project_form = ProjectForm()
    sprint_form = SprintForm()
    task_form = TaskForm()
    return render_template("app/projects.html",
                           project_form=project_form,
                           sprint_form=sprint_form,
                           task_form=task_form,
                           projects=user.projects,
                           active_projects=active_project)


@app.route('/project/add', methods=['POST', 'GET'])
def project_add():
    project_form = ProjectForm()
    if project_form.validate_on_submit():
        user = db.session.query(User).filter_by(user_id=session.get('user_id')).one()
        new_project = Project(name=request.form['name'])
        new_project.users.append(user)

        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('projects'))
    return redirect(url_for('projects'))


@app.route('/sprint/add/<project_id>', methods=['POST', 'GET'])
def sprint_add(project_id: int):
    sprint_form = SprintForm()
    if sprint_form.validate_on_submit():
        project: Project = db.session.query(Project).filter_by(project_id=project_id).one()
        sprint: Sprint = Sprint(name=sprint_form.name, project=project)
        db.session.add(sprint)
        db.session.commit()
        return redirect(url_for('projects'))
    return redirect(url_for('projects'))

@app.route('/task/add/<project_id>/<sprint_id>', methods=['POST', 'GET'])
def task_add(project_id, sprint_id):
    task_form = TaskForm()
    if task_form.validate_on_submit():
        project = db.session.query(Project).filter_by(project_id=project_id).one()
        sprint = db.session.query(Sprint).filter_by(sprint_id=sprint_id).one()
        task = Task(name=task_form.name, description=task_form.description, project=project, sprint=sprint)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('projects'))
    return redirect(url_for('projects'))


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
        session['user_id'] = new_user.user_id
        return redirect(url_for('projects'))
    return render_template('app/register.html', form=form)


@app.route('/logout')
def logout():
    if session.get('user'):
        session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)