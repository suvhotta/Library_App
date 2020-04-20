from app import db

class Books(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    isbn = db.Column(db.BigInteger, nullable=False)
    description = db.Column(db.String(300), default="New Book added")
    author = db.Column(db.PickleType, nullable=False)
    category = db.Column(db.PickleType, nullable=False)
    language = db.Column(db.String(20), nullable=False)
    copies = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<Book-title: {self.title} , ISBN:{self.isbn}>'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default="default.jpg")
    fine = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f'<User: {self.username}, {self.email}>'
