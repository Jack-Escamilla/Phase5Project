#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource
from flask import request, session
from sqlalchemy.exc import IntegrityError
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from config import app, db, api
import os


# Local imports
from config import app, db, api
# Add your model imports
from models import User, Bookclubs, Library, Review, Book

# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


@app.route('/')
def home():
    return ''


@app.before_request
def route_filter():
    bypass_routes = ["signup","login"]
    if request.endpoint not in bypass_routes and not session.get("user_id"):
        return {"Error": "Unauthorized"},401
    
@app.route('/signup',methods=['POST'])
def signup():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print(data)
            new_user = User(
                username = data["username"],
                 _password_hash = data["password"]
                
            )
            new_user.password_hash = data["password"]
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return new_user.to_dict(rules = ('-password_hash')),201
        except Exception as e:
            print(e)
            return {"Error": "Could not make user"},422
        
@app.route('/checksession',methods=['GET'])
def check_session():
    if request.method == 'GET':
        user = User.query.filter(User.id == session["user_id"]).first()
        return user.to_dict(rules = ('-password_hash')),200
    
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter(User.username == data["username"]).first()
        if user and user.authenticate(data['password']):
            session['user_id'] = user.id
            print(session)
            return user.to_dict(rules = ('-password_hash')),200
        else:
            return {"Error": "Not valid user name or password"}, 401
        

@app.route('/logout', methods=['DELETE'])
def logout():
    if request.method == 'DELETE':
        session['user_id'] = None
        return {},204
    
@app.route('/bookclubs', methods = ['GET','POST'])
def bookclubs_route():
    if request.method == "GET":
        all_clubs = Bookclubs.query.all()
        dict_teams = []
        for bookclub in all_clubs:
            dict_teams.append(bookclub.to_dict())
        return make_response(dict_teams,200)
    elif request.method == "POST":
        try:
            data = request.get.json()
            new_club = Bookclubs(
                name = data['name'])
            db.session.add(new_club)
            db.session.commit()
            return make_response(new_club.to_dict())
        except:
            return make_response({"errors": ["validation errors"]},400)
        
@app.route('/bookclubs/<int:id>', methods = ['GET', 'PATCH','DELETE'])
def single_bookclubs_route(id):
    found_club = Bookclubs.query.filter(Bookclubs.id==id).first()
    if found_club:
        if request.method == "GET":
            return make_response(found_club.to_dict(),200)
        elif request.method == "PATCH":
            try:
                data = request.get_json()
                for attr in data:
                    setattr(found_club,attr,data[attr])
                db.session.add(found_club)
                db.session.commit()
                return make_response(found_club.to_dict(),202)
            except:
                return make_response({"errors": ["validation errors"]},400)
        elif request.method == "DELETE":
            db.session.delete(found_club)
            db.session.commit()
            return make_response({},204)
    else:
        return make_response({"error": "Team not found"},404)
    
@app.route('/librarys', methods = ['GET','POST'])
def library_route():
    if request.method == "GET":
        all_librarys = Library.query.all()
        dict_teams = []
        for library in all_librarys:
            dict_teams.append(library.to_dict())
        return make_response(dict_teams,200)
    elif request.method == "POST":
        try:
            data = request.get.json()
            new_library = Library(
                name = data['name'])
            db.session.add(new_library)
            db.session.commit()
            return make_response(new_library.to_dict())
        except:
            return make_response({"errors": ["validation errors"]},400)
        
@app.route('/library/<int:id>', methods=['POST', 'DELETE'])
def manage_library_books(id):
    data = request.get_json()

    library_id = id
    book_id = data.get('book_id')

    try:
        library = Library.query.get(library_id)

        if library:
            book = Book.query.get(book_id)

            if request.method == 'POST':
                
                if book not in library.books:
                    library.books.append(book)
                    db.session.commit()
                    return jsonify({'message': 'Book added to library successfully'}), 201
                else:
                    return jsonify({'message': 'Book already in library'}), 400
            elif request.method == 'DELETE':
                
                if book in library.books:
                    library.books.remove(book)
                    db.session.commit()
                    return jsonify({'message': 'Book removed from library successfully'}), 200
                else:
                    return jsonify({'message': 'Book not found in library'}), 404
        else:
            return jsonify({'message': 'Library not found'}), 404
    except Exception as e:
        db.session.rollback()
        return(f"An error occurred: {e}"), 500
    finally:
        db.session.close()

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = [{'id': book.id, 'title': book.title, 'author': book.author, 'review': book.review} for book in books]
    return jsonify({'books': book_list})

@app.route('/review', methods=['POST'])
def add_review():
    data = request.get_json()

    new_book = Book(title=data['title'], author=data['author'], review=data['review'])

    try:
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'message': 'Review added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return(f"An error occurred: {e}"), 500
    finally:
        db.session.close()

@app.route('/review/<int:book_id>', methods=['DELETE'])
def delete_review(book_id):
    try:
        book = Book.query.get(book_id)

        if book:
            db.session.delete(book)
            db.session.commit()
            return jsonify({'message': 'Review deleted successfully'}), 200
        else:
            return jsonify({'message': 'Review not found'}), 404
    except Exception as e:
        db.session.rollback()
        return(f"An error occurred: {e}"), 500
    finally:
        db.session.close()

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
