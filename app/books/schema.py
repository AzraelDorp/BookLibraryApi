from marshmallow import Schema, fields
# write a schema for the book model
class BookSchema(Schema):
    book_id = fields.String()
    title = fields.String(required=True)
    authors = fields.List(fields.String())
    description = fields.String()
    isbn = fields.String()
    year_published = fields.Integer()
    created_at = fields.String() # look into ways to convert to datetime
    updated_at = fields.String()
    genre = fields.String()
    image = fields.String()
    publisher = fields.String()
    pages = fields.Integer()
    type_of_book = fields.String()
    progress = fields.String()
    language = fields.String()
    country = fields.String()
    links = fields.List(fields.String())
    quantity = fields.Integer()
    deleted = fields.Boolean()

class BookSchemaResponse(Schema):
    books = fields.List(fields.Nested(BookSchema))


class BookSchemaPost(BookSchema):
    pass


    # # class Meta:
    # #     ordered = True
    # #     fields = ('id', 'title', 'author', 'description', 'year', 'created_at', 'updated_at', 'genre', 'isbn', 'image', 'publisher', 'pages', 'language', 'country', 'link', 'quantity')