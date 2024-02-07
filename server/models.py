from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import ForeignKey, Column, Integer, String, create_engine, MetaData
from sqlalchemy.orm import Session, declarative_base, relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import SQLAlchemy

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    _password_hash = db.Column(db.String)
    #relationship column:
    book_clubs = db.relationship('Bookclubs', back_populates = "user")
    library = db.relationship('Library', back_populates = "user")
    review = db.relationship('Review', back_populates = "user")
    book = db.relationship('Book', back_populates = "user")
    #serialzier:
    serialize_rules = ('-book_clubs.users', '-library.users', '-review.users', '-book.users')

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Can't access this")
        # return self._password_hash
    
    #This is boiler plate code:
    @password_hash.setter
    def password_hash(self, password):
        hashed_password = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = hashed_password.decode('utf-8')

    def authenticate(self,password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
    
    #Validation: Must have user
    @validates('user')
    def validate_user(self,key,value):
        if value:
            return value
        else:
            raise ValueError("Not valid User")
        
class Bookclubs(db.Model,SerializerMixin):
    __tablename__= "book_clubs"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    #relationship columns:
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates=("book_clubs"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    book = db.relationship("Book", back_populates=("book_clubs"))
    #serializer:
    serialize_rules=('-book.book_clubs','-user.book_clubs')

    def __repr__(self):
        return repr(f"{self.name}")

class Library(db.Model,SerializerMixin):
    __tablename__= "library"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    #relationship columns:
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="library")
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    book = db.relationship("Book", back_populates=("library"))
    
    #serializer:
    serialize_rules=('-book.library','-user.library')

    def __repr__(self):
        return repr(f"{self.book}")

class Review(db.Model,SerializerMixin):
    __tablename__= "review"
    id = db.Column(db.Integer, primary_key = True)
    review = db.Column(db.String)
    #relationship columns:
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="review")
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    book = db.relationship("Book", back_populates=("review"))
    #serializer:
    serialize_rules=('-book.review','-user.review')

    def __repr__(self):
        return repr(f"{self.book}")

class Book(db.Model,SerializerMixin):
    __tablename__= "book"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    genre = db.Column(db.String)
    #relationship columns:
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="book")
    book_clubs = db.relationship('Bookclubs', back_populates = "book")
    library = db.relationship('Library', back_populates = "book")
    review = db.relationship('Review', back_populates = "book")
    #serializer:
    serialize_rules=('-book_clubs.book','-user.book','-library.book', '-review.book')

    def __repr__(self):
        return repr(f"{self.title}, {self.author}, {self.genre}")

