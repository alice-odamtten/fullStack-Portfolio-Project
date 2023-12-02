from flask import Blueprint, flash, redirect, render_template, request, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from my_app import db
from my_app.api.models import User, Task
from my_app.api.forms import RegisterForm, LoginForm, TodoForm, EditTodoform

tasks =Blueprint('tasks', __name__)

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
                        due_data=form.due_date.data, todo_owner = user.id)
            db.session.add(todo)
            db.session.commit()
            return redirect('/todos')
            
@tasks.route('/todos')
def todos():
    todos= Task.query.filter_by(todo_owner = current_user.id)
    return render_template('todos.html', todos = todos)

@tasks.route('/edit_task/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    user = current_user
    form = EditTodoform()
    task = Task.query.filter_by(id=id, todo_owner=current_user.id).first()

    if form.validate_on_submit():
        task.task_name = form.task_name.data
        task.due_date =form.due_date.data
        task.status=form.status.data
        db.session.commit()
        return redirect('/todos')
    
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