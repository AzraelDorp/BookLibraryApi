from bson import ObjectId
from datetime import datetime
from flask import request, render_template, make_response, url_for, flash, redirect
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
TODO: Need to update all books from request.get_json() to data = request.get_json() and then use data["key"] to get the value
"""
api = Namespace(name="books", description="")

# endpoints for all books


@api.route("/")
class BookAPI(Resource):
    @responds(schema=BookSchemaResponse, api=api, status_code=201)
    @api.doc(responses={"200": "OK"})
    def get(self):
        '''Returns all Books with filters'''
        books = BookModel().getAllBooks()
        return {"books": books}


    # build a post functions for the the book route
    @api.doc(responses={"201": "Created"})
    @accepts(schema=BookSchemaPost, api=api)
    @responds(schema=BookSchemaPost, api=api, status_code=201)
    def post(self):
        '''Creates a new Book'''

        books = request.get_json()

        # add book defaults
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
        '''Returns a single Book'''
        book = BookModel().getBookByID(id)
        return book

# this endpoint needs to be revisited and updated
# do i want it to create a book or just update it
# add a put function for the book route
    @api.doc(responses={"200": "OK"})
    @accepts(schema=BookSchemaPost, api=api)
    @responds(schema=BookSchemaPost, api=api, status_code=201)
    def put(self, id):
        '''Updates a Book with id if it exists, otherwise creates a new Book'''

        dbBook = BookModel().getBookByID(id)

        # if the book exists then update it
        if dbBook:
            print("book exists")
            book = dbBook
            book["updated_at"] = datetime.now() # type: ignore
            # loop through the request body and update the book
            for key in request.get_json().keys():
                book[key] = request.get_json()[key]
            # update the book
            book = BookModel().updateBookByID(id, book)
            return book
        else:
            '''if the book does not exist then create it'''
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
        book = BookModel().getBookByID(id)

        # if the book exists then delete it
        if book:
            BookModel().deleteBook(book['book_id']) # type: ignore
        else:
            return {"message": "Book does not exist"}, 404
        return None, 204


# endpoints for internal use only
# these endpoints are not exposed to the user
# these are used to test functionality

"""
@api.route("/")
class BookAPI(Resource):
    @responds( api=api)
    @api.doc(responses={"200": "OK"})
    def get(self):
        '''Returns all Books with filters'''
        # books = DatabaseModel().getAllItems("Books")
        books = BookModel().getAllBooks()
        #print(books)
        
        #return  {"books": books}
        headers = {'Content-Type': 'text/html'}
        return make_response( render_template('index.html', books=books),headers) 
    
    # # build a post functions for the the book route
    # @api.doc(responses={"201": "Created"})
    # @accepts(schema=BookSchemaPost, api=api)
    # @responds(schema=BookSchemaPost, api=api, status_code=201)
    # def post(self):
    #     '''Creates a new Book'''
        
    #     books = request.get_json()

    #     # add book defaults
    #     # add a book_id to the book
    #     books["book_id"] = ObjectId()
    #     # add a created_at and updated_at to the book
    #     books["created_at"] = datetime.now()
    #     books["updated_at"] = datetime.now()

    #     books = BookModel().createBook(books)
    #     return books

@api.route("/newbook/")
class BookCreate(Resource):
    @responds( api=api)
    @api.doc(responses={"200": "OK"})
    def get(self):
        '''Returns all Books with filters'''
        # books = DatabaseModel().getAllItems("Books")
        # books = BookModel().getAllBooks()
        #print(books)
        
        #return  {"books": books}
        headers = {'Content-Type': 'text/html'}
        return make_response( render_template('create.html'),headers)
    
    # build a post functions for the the book route
    @api.doc(responses={"201": "Created"})
    @accepts( api=api)
    @responds(schema=BookSchemaPost, api=api, status_code=201)
    def post(self):
        '''Creates a new Book'''
        headers = {'Content-Type': 'text/html'}

        books = {}
        form = request.form
        for i in form:
            authors = []
            if i == "authors":
                for author in form[i].split(","):
                    authors.append(author)
                books[i] = authors
            else:
                books[i] = form[i]

        #print(books)

        # add book defaults
        # add a book_id to the book
        books["book_id"] = str(ObjectId())
        # add a created_at and updated_at to the book
        books["created_at"] = str(datetime.now())
        books["updated_at"] = str(datetime.now())

        response = BookModel().createBook(books)
        if response.get("ResponseMetadata").get("HTTPStatusCode") == 200:
            return  make_response( render_template('success.html', books=books),headers)
        #print(books)

        return make_response( render_template('success.html', books=books),headers)
 """
