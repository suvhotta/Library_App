from flask import url_for, redirect, render_template, request, flash
from app import app, bcrypt, db
from app.forms import RegistrationForm, LoginForm, AccountUpdation, UpdateProfile
from app.models import User
from sqlalchemy import or_, and_
from flask_login import current_user, login_user, login_required, logout_user
from datetime import timedelta
import smtplib, inspect, os
from PIL import Image

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
        
        if(user and user.account_state == "enabled" and bcrypt.check_password_hash(user.password, form.password.data)):
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
            if(form.account_state.data == "enabled"):
                user = User.query.filter_by(username=form.username.data).first()
                user.role = form.role.data
                user.fine = form.fine.data
                user.account_state = form.account_state.data
                db.session.commit()
                sendmail(form.email.data)
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
@login_required
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
                image_file = url_for("static", filename = "profile_pics/"+user.image_file)
                return render_template('delete_user_from_library.html',image_file=image_file, form=form)
            else:
                return redirect(url_for("manage_accounts_delete", username=None))
        else:
            user = User.query.filter_by(username=form.username.data).first()
            db.session.delete(user)
            db.session.commit()
            sendmail(form.email.data)
            flash(f'Account for User : <{form.username.data}> has been removed.', "success")
            return redirect(url_for("manage_accounts_delete", username=None))


#Function to send mails to users once their account has been created or has been removed from Library.
def sendmail(receiver_mail):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        email_address = 'madrid1902fan@gmail.com'
        email_password = 'madrid1902'
        smtp.login(email_address, email_password)

    #The inspect.stack here checks which is the caller function for this sendmail method, 
    # and accordingly changes the subject and body of the mail.
        if(inspect.stack()[1][3] == "manage_accounts_add"):
            subject = 'Central Library - Account Created'
            body = 'Congrats your Library account has been created. Please login using your credentials.'

        elif(inspect.stack()[1][3] == "manage_accounts_delete"):
            subject = 'Central Library - Account Deleted'
            body = "Your account has been removed from Central Library. In case of any queries please reach out to the Librarian."

        msg = f'Subject:{subject}\n\n{body}'

        smtp.sendmail(email_address, receiver_mail, msg) 

def save_image_file(form_image_file):
    random_hex = os.urandom(16).hex()
    #we require only the file extension and not the path.
    #hence we are just ignoring one variable by placing an _ in its place and taking the other
    _, file_ext = os.path.splitext(form_image_file.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_image_file)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/profile', methods=["GET","POST"])
@login_required
def profile():
    form = UpdateProfile()
    if form.validate_on_submit():
        #if something has actually been changed then only will perform a db commit
        #and flash message, else simply redirects
        if(current_user.username != form.username.data or current_user.email != form.email.data or current_user.name != form.name.data or form.image_file.data):
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.name = form.name.data
            picture_file = save_image_file(form.image_file.data)
            current_user.image_file = picture_file
            db.session.commit()
            flash("You're account has been successfully updated!", "success")
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.role.data = current_user.role
        form.email.data = current_user.email
        form.fine.data = current_user.fine
    image_file = url_for("static", filename = "profile_pics/"+current_user.image_file)
    return render_template("profile.html", image_file=image_file, form=form)