from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, EmailField, SubmitField,SelectField,DateField

class RegisterForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class TodoForm(FlaskForm):
    task_name = StringField('Name', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Complete','Complete'), ('Not Started', 'Not Started')])
    submit = SubmitField('Add Task')

class EditTodoform(FlaskForm):
    task_name = StringField('Name', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[('COMPLETED','COMPLETED'), ('NOTSTARTED', 'NOTSTARTED')])
    submit = SubmitField(' Edit Task')
