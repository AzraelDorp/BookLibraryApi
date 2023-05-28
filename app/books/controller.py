from flask_restx import Namespace, Resource
from flask import request
from flask_accepts import accepts, responds
from .schema import BookSchema, BookSchemaResponse
api = Namespace(name="books", description="")

from .model import BookModel

# plural for many

@api.route("")
class BookAPI(Resource):
    @responds(schema=BookSchemaResponse, api=api)
    @api.doc(responses={"200": "OK"})
    def get(self):
        '''Returns all Books with filters'''
        # books = DatabaseModel().getAllItems("Books")
        books = BookModel().getAllItems("Books")
        print(books)
        return  {"books": books}
    
    # build a post functions for the the book route
    @api.doc(responses={"201": "Created"})
    @accepts(schema=BookSchema, api=api)
    
    def post(self):
        '''Creates a new Book'''
        book_data = []
            
        for key, value in request.get_json().items():
            book_data.append({key: value})


        return {"success", 201}


# singular for one
@api.route("/<id>")
@api.param("id", "Book identifier")
@api.response(404, "Book not found")
class Book(Resource):
    @responds(schema=BookSchema, api=api)

    @api.doc(responses={"200": "OK"})
    def get(self, id):
        '''Returns a Book with id'''
        book = BookModel().getBookByID(BookSchema,id)
        return book
    

