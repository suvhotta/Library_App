from flask import url_for, redirect, render_template, request, flash
from app import app, bcrypt, db
from app.forms import RegistrationForm, LoginForm
from app.models import User
from sqlalchemy import or_

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if(request.method == 'POST' and form.validate_on_submit()):
        #Hashing the password and decoding is part of syntax for python-3.
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
        password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. Now you can login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if(request.method == "POST" and form.validate_on_submit()):
        user = User.query.filter(or_(User.username==form.login_field.data,
        User.email==form.login_field.data)).first()
        
        if(user and bcrypt.check_password_hash(user.password, form.password.data)):
            flash('Login Successful', 'success')
            return redirect(url_for('index'))
        
        else:
            flash('Login Unsuccessful. Please check your credentials.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', title='Login Page', form=form)