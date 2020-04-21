from flask import url_for, redirect, render_template, request, flash
from app import app, bcrypt, db
from app.forms import RegistrationForm, LoginForm
from app.models import User
from sqlalchemy import or_
from flask_login import current_user, login_user, login_required, logout_user
from datetime import timedelta

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about',methods=['GET'])
@login_required
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if(request.method == 'POST' and form.validate_on_submit()):
        
        # Hashing the password and decoding is part of syntax for python-3.
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
        password=hashed_pwd,roles=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash("Your registration is complete and has been sent to the Librarian for approval. You'll be receiving an approval mail shortly!", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if(request.method == "POST" and form.validate_on_submit()):
        user = User.query.filter(or_(User.username==form.login_field.data,
        User.email==form.login_field.data)).first()
        
        if(user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember.data, duration=timedelta(seconds=5))
            if current_user.roles =='Student' or current_user.roles =='Faculty':
                return redirect(url_for('index'))
            else:
                return redirect(url_for('about'))
        
        else:
            flash('Login Unsuccessful. Please check your credentials.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', title='Login Page', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/add_user")
@login_required
def manage_accounts_add():
    users = User.query.filter_by(account_state='disabled')
    return render_template('add_users.html', users=users)