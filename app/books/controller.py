from bson import ObjectId
from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource
from flask_accepts import accepts, responds
from .model import BookModel
from .schema import BookSchema, BookSchemaResponse, BookSchemaPost

"""
TODO: need to go through each of these endpoints and add the appropriate filters
TODO: Need to add the correct error handling for each of these endpoints
TODO: Need to add the correct response codes for each of these endpoints
TODO: Need to add the correct documentation for each of these endpoints
TODO: Need to add the correct authentication for each of these endpoints

"""
api = Namespace(name="books", description="")

# endpoints for all books

@api.route("")
class BookAPI(Resource):
    @responds(schema=BookSchemaResponse, api=api)
    @api.doc(responses={"200": "OK"})
    def get(self):
        '''Returns all Books with filters'''
        # books = DatabaseModel().getAllItems("Books")
        books = BookModel().getAllBooks()
        print(books)
        return  {"books": books}
    
    # build a post functions for the the book route
    @api.doc(responses={"201": "Created"})
    @accepts(schema=BookSchemaPost, api=api)
    @responds(schema=BookSchemaPost, api=api, status_code=201)
    def post(self):
        '''Creates a new Book'''
        
        books = request.get_json()

        # add book defaults
        # add a book_id to the book
        books["book_id"] = ObjectId()
        # add a created_at and updated_at to the book
        books["created_at"] = datetime.now()
        books["updated_at"] = datetime.now()

        books = BookModel().createBook(books)
        return books


# enpoints for a single book
@api.route("/<id>")
@api.param("id", "Book identifier")
@api.response(404, "Book not found")
class Book(Resource):
    @responds(schema=BookSchema, api=api)

    @api.doc(responses={"200": "OK"})
    def get(self, id):
        '''Returns a Book with id'''
        book = BookModel().getBookByID(id)
        return book

# add a put function for the book route
    @api.doc(responses={"200": "OK"})
    @accepts(schema=BookSchemaPost, api=api)
    @responds(schema=BookSchemaPost, api=api, status_code=201)
    def put(self, id):
        '''Updates a Book with id if it exists, otherwise creates a new Book'''

        dbBook = BookModel().getBookByID(id)
        # add a created_at and updated_at to the book
        if dbBook:
            print("book exists")
            book = dbBook
            book["updated_at"] = datetime.now()
            # loop through the request body and update the book
            for key in request.get_json().keys():
                book[key] = request.get_json()[key]
            # update the book
            book = BookModel().updateBookByID(id, book)
            return book
        else:
            print("book does not exist")
            book = request.get_json()
            book["book_id"] = id
            book["created_at"] = datetime.now()
            book["updated_at"] = datetime.now()
            book = BookModel().createBook(book)
            return book

    @api.doc(responses={"204": "No Content"})
    def delete(self, id):
        '''Deletes a Book with id'''
        BookModel().deleteBook(id)
        return None, 204
