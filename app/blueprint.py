from flask import Blueprint
from flask_restx import Api
from app.books.endpoint import api as books

blueprint = Blueprint('api', __name__,'/')

api = Api(
    blueprint,
    title='Library Rest API',
    version='1.0',
    description='Rest API to interact with a Personal Library.',
    doc='/doc'
    # All API metadatas
)

api.add_namespace(books, path='/books')
