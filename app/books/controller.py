from flask_restx import Namespace, Resource
from flask import request

api = Namespace("books", description="")

# plural for many
@api.route("")
class BookAPI(Resource):
    @api.doc(responses={"200": "OK"})
    def get(self):
        '''Returns all Book with filters'''
        return {"success", 200}
    
    # build a post functions for the the book route
    @api.doc(responses={"201": "Created"})
    def post(self):
        '''Creates a new Book'''
        book_data = []
            
        for key, value in request.get_json().items():
            book_data.append({key: value})


        return {"success", 201}


# singular for one
@api.route("/<int:id>")
@api.param("id", "Book identifier")
@api.response(404, "Book not found")
class Book(Resource):
    @api.doc(responses={"200": "OK"})
    def get(self, id):
        '''Returns a Book with id'''
        return {"success", 200}
    

