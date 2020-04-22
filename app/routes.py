from flask import url_for, redirect, render_template, request, flash
from app import app, bcrypt, db
from app.forms import RegistrationForm, LoginForm, AccountUpdation
from app.models import User
from sqlalchemy import or_, and_
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
        password=hashed_pwd,role=form.role.data)
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
        user = User.query.filter(or_(User.username == form.login_field.data,
        User.email == form.login_field.data)).first()
        
        if(user.account_state == "enabled" and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember.data, duration=timedelta(seconds=5))
            if current_user.role =='Student' or current_user.role =='Faculty':
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


@app.route("/manage_accounts/add_user/<username>", methods=['GET', 'POST'])
@app.route("/manage_accounts/add_user/", defaults={"username":None} )
@login_required
def manage_accounts_add(username):
    if(not username):
        users = User.query.filter_by(account_state='disabled')
        return render_template('add_users.html', users=users)

    else:
        form = AccountUpdation()
        if(request.method == "GET"):
            user = User.query.filter_by(username=username).first()
            if(user and user.account_state == "disabled"):
                form.username.data = user.username
                form.name.data = user.name
                form.role.data = user.role
                form.email.data = user.email
                form.account_state.data = user.account_state
                form.fine.data = user.fine
                return render_template('add_user_to_library.html', form=form)
            else:
                return redirect(url_for("manage_accounts_add", username=None))
        else:
            user = User.query.filter_by(username=form.username.data).first()
            user.role = form.role.data
            user.fine = form.fine.data
            user.account_state = form.account_state.data
            db.session.commit()
            if(form.account_state.data == "enabled"):
                flash(f'Account for User : <{user.username}> has been activated.', "success")
            return redirect(url_for("manage_accounts_add", username=None))

# @app.route("/manage_accounts/add_user/<username>", methods=['GET', 'POST'])
# @login_required
# def add_user_to_library(username):
#     form = AccountUpdation()
#     if(request.method == "GET"):
#         user = User.query.filter_by(username=username).first()
#         if(user.account_state == "disabled"):
#             form.username.data = user.username
#             form.name.data = user.name
#             form.role.data = user.role
#             form.email.data = user.email
#             form.account_state.data = user.account_state
#             form.fine.data = user.fine
#             return render_template('add_user_to_library.html', form=form)
#     else:
#         user = User.query.filter_by(username=form.username.data).first()
#         user.role = form.role.data
#         user.fine = form.fine.data
#         user.account_state = form.account_state.data
#         db.session.commit()
#         if(form.account_state.data == "enabled"):
#             flash(f'Account for User : <{user.username}> has been activated.', "success")
#         return render_template(url_for("manage_accounts_add_user"))

@app.route('/manage_accounts/remove_user/<username>', methods=["GET","POST"])
@app.route('/manage_accounts/remove_user/', defaults={"username":None})
def manage_accounts_delete(username):
    if(not username):
        users = User.query.filter(and_(User.account_state =='enabled', User.role!='Librarian'))
        return render_template("delete_users.html", users=users)

    else:
        form = AccountUpdation()
        if(request.method == "GET"):
            user = User.query.filter_by(username=username).first()
            if(user and user.account_state == "enabled" and user.role !="Librarian"):
                form.username.data = user.username
                form.name.data = user.name
                form.role.data = user.role
                form.email.data = user.email
                form.account_state.data = user.account_state
                form.fine.data = user.fine
                form.submit.label.text = "Delete Account"
                return render_template('delete_user_from_library.html', form=form)
            else:
                return redirect(url_for("manage_accounts_delete", username=None))
        else:
            user = User.query.filter_by(username=form.username.data).first()
            db.session.delete(user)
            db.session.commit()
            flash(f'Account for User : <{form.username.data}> has been removed.', "success")
            return redirect(url_for("manage_accounts_delete", username=None))