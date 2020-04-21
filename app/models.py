from app import db, login_manager
from flask_login import UserMixin

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    isbn = db.Column(db.BigInteger, nullable=False)
    description = db.Column(db.String(300), default="New Book added")
    author = db.Column(db.PickleType, nullable=False)
    category = db.Column(db.PickleType, nullable=False)
    language = db.Column(db.String(20), nullable=False)
    copies = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<Book-title: {self.title} , ISBN:{self.isbn}>'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    roles = db.Column(db.String(10), nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default="default.jpg")
    fine = db.Column(db.Integer, default=0, nullable=False)
    account_state = db.Column(db.String(10),default='disabled', nullable=False)
    def __repr__(self):
        return f'<User: {self.username}, {self.email}>'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))