import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from datetime import date
from database import db

from models import Note as Note
from models import User as User
from models import Project as Project



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_testfile.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)
# Setup models
with app.app_context():
    db.create_all()   # run under the app context


@app.route('/projects')
def get_projects():
    #retrieve user from database
    a_user = db.session.query(User).filter_by(email='lfrazee1@uncc.edu').one()
    #retieve notes from database
    my_projects = db.session.query(Project).all()
    
    return render_template('projects.html' , projects = my_projects, user = a_user)

@app.route('/projects/<project_id>')
def get_project(project_id):
    #retrieve user from database
    a_user = db.session.query(User).filter_by(email='lfrazee1@uncc.edu').one()
    #retrieve note
    my_project = db.session.query(Project).filter_by(id = project_id).one()
    return render_template('project.html' , project=my_project, user = a_user)

@app.route('/projects/new', methods = ['GET', 'POST'])
def new_project():

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['noteText']
        #create a stamp date
        from datetime import date
        today = date.today()
        today= today.strftime("%m-%d-%Y")
        new_record = Project(title, text, today)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('get_projects'))
    else:
        a_user = db.session.query(User).filter_by(email='lfrazee1@uncc.edu').one()
        return render_template('new_project.html', user = a_user)

@app.route('/projects/edit/<project_id>', methods = ['GET', 'POST'])
def update_project(project_id):
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['noteText']

        project = db.session.query(Project).filter_by(id = project_id).one()
        project.title = title
        project.text=text
        db.session.add(project)
        db.session.commit()

        return redirect(url_for('get_projects'))
    else:
        #retrieve user from database
        a_user = db.session.query(User).filter_by(email='lfrazee1@uncc.edu').one()
        #retrieve project
        my_project = db.session.query(Project).filter_by(id =project_id).one()

        return render_template('new_project.html', project=my_project, user = a_user)

@app.route('/projects/delete/<project_id>', methods = ['POST'])
def delete_project(project_id):
   
    my_project = db.session.query(Project).filter_by(id =project_id).one()
    db.session.delete(my_project)
    db.session.commit()

    return redirect(url_for('get_projects'))

@app.route('/testHTML')
def testUI():
  
    return render_template("testHTML.html")


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
