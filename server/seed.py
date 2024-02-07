# Standard library imports
from random import randint

# Remote library imports
from faker import Faker
import requests
# Local imports
from app import app, db
from models import Bookclubs, Book, Library, Review, User



def seed_book_data():
    api_url = 'https://openlibrary.org/search.json?q=python'  
    response = requests.get(api_url)

    if response.status_code == 200:  
        book_data = response.json()
        print(book_data)
        for book_info in book_data.get('docs', []):  
            title = book_info.get('title', 'Unknown Title')
            author = ', '.join(book_info.get('author', []))
            genre = ', '.join(book_info.get('genre', []))
            print(book_info)
            new_book = Book(title=title, author=author, genre=genre)
            db.session.add(new_book)
            db.session.commit()

        print('Book data seeded successfully.')
    else:
        print('Failed to fetch Book data')

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        seed_book_data()
        

