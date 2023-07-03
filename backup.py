from app.books.model import BookModel as bookmodel

allbooks = bookmodel().getAllBooks()

# # export all books to a json file
import json
with open('books.json', 'w') as f:
    json.dump(allbooks, f)

        