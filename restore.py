import json
from app.books.model import BookModel as bookmodel

#import all books from a json file
with open('books.json') as f:
    data = json.load(f)
    for book in data:
        bookmodel().createBook(book)
        