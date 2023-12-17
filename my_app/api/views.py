from flask import Blueprint, flash, redirect, render_template, request, jsonify, abort, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from datetime import datetime
from my_app import db
from my_app.api.models import User, Task, Download
from my_app.api.forms import RegisterForm, LoginForm, TodoForm, EditTodoform, AddownloadForm
from pytube import YouTube

tasks =Blueprint('tasks', __name__)

@tasks.route('/')
def defualt():
    return render_template('home.html')
@tasks.route('/home')
def home():
    return render_template('home.html')

@tasks.route('/register', methods = ['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    
    if request.method == 'POST':
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        return redirect ('/login')

@tasks.route('/login', methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit:
        user = User.query.filter_by(email = form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect('/todos')
        flash("Invalid details")

    return render_template("login.html", form=form)

@tasks.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect('/home')

@tasks.route('/add_todo', methods= ['POST','GET'])
def add_tasks():
    form = TodoForm()
    if request.method == 'GET':
        return render_template('add_todo.html', form=form)
    if request.method == "POST":
        user = current_user
        if form.validate_on_submit:
            todo = Task(task_name=form.task_name.data, status =form.status.data,
                        due_date=form.due_date.data, todo_owner = user.id)
            db.session.add(todo)
            db.session.commit()
            return redirect('/todos')
            
@tasks.route('/todos')
def todos():
    wasNow = datetime.now()
    todos= Task.query.filter_by(todo_owner = current_user.id)
    #profileimage = url_for('static', filename='image/' + current_user.image_file)
    return render_template('todos.html', todos = todos ,wasNow=wasNow)

@tasks.route('/edit_task/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    user = current_user
    form = EditTodoform()
    task = Task.query.filter_by(id=id, todo_owner=current_user.id).first()

    if request.method == 'POST':
        if form.validate_on_submit():
            #print("Form is valid!")
            form.populate_obj(task)
            #print("it about to go down")
            db.session.commit()
            #print("it has been committed")
            return redirect('/todos')
        else:
            print("Form is not valid. Errors:", form.errors)
    elif request.method == 'GET':
        form.task_name.data = task.task_name
        form.due_date.data = task.due_date 
        form.status.data = task.status

    return render_template('edit_todo.html', form=form)  

   

@tasks.route('/delete_task/<int:id>', methods=['GET', 'POST'])
def delete(id):
    task = Task.query.filter_by(id=id, todo_owner=current_user.id).first()
    if request.method == 'POST':
        if task:
            db.session.delete(task)
            db.session.commit()
            return redirect('/todos')
        abort(404)

    return render_template('delete_task.html', task=task)

@tasks.route('/download', methods=['GET', 'POST'])
def download():
    user = current_user
    form = AddownloadForm()
    url = form.url.data
    path = r"\Downloads"
    if form.validate_on_submit():
        yt =YouTube(url)
        mp4files = yt.streams
        dvideo = mp4files.filter(file_extension='mp4')
        select = dvideo.first()
        #print("it about to go download")
        try:
            select.download(path)
            #print(url)
        except:
            render_template('error.html')
        db.session.commit()
    
    
    return render_template("download.html", form=form )


@tasks.errorhandler(404)
def not_found_error(e):
    return render_template('error.html')