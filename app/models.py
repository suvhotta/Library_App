from app import app, db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime 
from marshmallow_sqlalchemy import ModelSchema

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    isbn = db.Column(db.BigInteger, nullable=False)
    description = db.Column(db.String(300), default="New Book added")
    pages = db.Column(db.Integer, nullable=False)
    #pickletype object stores python datatypes likes list using dumps and loads methods
    #the objects are stored as binary objects in db, and while retrieving data, gives back list object
    author = db.Column(db.PickleType, nullable=False)
    category = db.Column(db.PickleType, nullable=False)
    language = db.Column(db.String(20), nullable=False)
    num_copies = db.Column(db.Integer, default=1)
    copies = db.relationship('BookCopies', backref="book", cascade="all,delete-orphan", lazy="dynamic")
    def __repr__(self):
        return f'<Book-title: {self.title} , ISBN:{self.isbn}>'



class BookCopies(db.Model):
    book_copy_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    added_date = db.Column(db.DateTime,default=datetime.utcnow)
    #Defining the foreign key to connect the copies to the parent book table
    book_id = db.Column(db.Integer,db.ForeignKey('books.id'))
    

class BooksSchema(ModelSchema):
    class Meta:
        model = Books
        
class BookCopiesSchema(ModelSchema):
    class Meta:
        model = BookCopies


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default="default.jpg")
    fine = db.Column(db.Integer, default=0, nullable=False)
    account_state = db.Column(db.String(10),default='disabled', nullable=False)
    def __repr__(self):
        return f'<User: {self.username}, {self.email}>'

    def get_reset_token(self):
        s = Serializer(app.config["SECRET_KEY"])
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token,expires_sec=300):
        s = Serializer(app.config["SECRET_KEY"],expires_sec)
        try:
            user_id = s.loads(token)['user_id']

        except:
            return None

        return User.query.get(user_id)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))