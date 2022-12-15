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
from src.model.story import Story
from src.model.login_attempt import LoginAttempt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_mapping(SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')
db.init_app(app)


@app.template_filter()
def strftime(value, fmt="%H:%M %d-%m-%y"):
    return value.strftime(fmt)

with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/index')
def index():
    if session.get('user'):
        return redirect(url_for('project'))
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
            return redirect(url_for('project'))
        login_form.password.errors = ["Incorrect username or password."]
        new_login_attempt = LoginAttempt(email=request.form['email'], password=request.form['password'].encode('utf-8'))
        db.session.add(new_login_attempt)
        db.session.commit()
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
        return redirect(url_for('project', project_id=user.projects[0].project_id))

    project_form = ProjectForm()
    sprint_form = SprintForm()
    task_form = TaskForm()
    return render_template("app/project.html", project_form=project_form, sprint_form=sprint_form, task_form=task_form,
                           projects=user.projects, active_project=active_project)


@app.route('/project/add', methods=['POST', 'GET'])
def project_add():
    project_form = ProjectForm()
    if project_form.validate_on_submit():
        user = db.session.query(User).filter_by(user_id=session.get('user_id')).one()
        new_project = Project(name=request.form['name'], created_by=user)
        new_project.users.append(user)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('project', project_id=new_project.project_id))
    return redirect(url_for('project'))


@app.route('/sprint/add/<project_id>', methods=['POST', 'GET'])
def sprint_add(project_id: int):
    sprint_form = SprintForm()
    if sprint_form.validate_on_submit():
        p: Project = db.session.query(Project).filter_by(project_id=project_id).one()
        sprint: Sprint = Sprint(name=request.form['name'], project=p)
        db.session.add(sprint)
        db.session.commit()
        return redirect(url_for('project', project_id=project_id))
    return redirect(url_for('project'))


@app.route('/task/add/<project_id>/<sprint_id>', methods=['POST', 'GET'])
def task_add(project_id, sprint_id):
    task_form = TaskForm()
    if task_form.validate_on_submit():
        p = db.session.query(Project).filter_by(project_id=project_id).one()
        s = db.session.query(Sprint).filter_by(sprint_id=sprint_id).one()
        task = Task(name=task_form.name, description=task_form.description, project=p, sprint=s)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('project'))
    return redirect(url_for('project'))


@app.route('/story/<project_id>', methods=['POST', 'GET'])
def story(project_id):
    user = db.session.query(User).filter_by(user_id=session.get('user_id')).one()
    stories = db.session.query(Story).filter_by(project_id=project_id).all()

    project_form = ProjectForm()
    return render_template("app/story.html", stories=stories, project_form=project_form, projects=user.projects)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        h_password = hashpw(request.form['password'].encode('utf-8'), gensalt())
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        new_user = User(first_name=first_name, last_name=last_name, email=request.form['email'],
                        password_hash=h_password)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = first_name
        session['user_id'] = new_user.user_id
        return redirect(url_for('project'))
    return render_template('app/register.html', form=form)


@app.route('/logout')
def logout():
    if session.get('user'):
        session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
