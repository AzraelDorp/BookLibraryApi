from ..shared.models import DatabaseModel
from .schema import BookSchema

class BookModel(DatabaseModel):
    def __init__(self):
        super().__init__()

    # create a book
    def createBook(self, book):
        book = self.addItem("Books", BookSchema(), book)
        return book
    
    def getBookByID(self, book_id):
        book_key = {"book_id":{"S":book_id}}
        book = self.getItemsWithKey("Books", BookSchema(), book_key)
        return book
    
    def updateBookByID(self, book_id, book):
        book_key = {"book_id":{"S":book_id}}
        book = self.updateItemByID("Books", BookSchema(), book_key, book)
        return book
    
    # need to add filters here
    def getAllBooks(self):
        books = self.getAllItems("Books", BookSchema())
        return books

     # delete a book
    def deleteBook(self, book_id):
        book_key = {"book_id":book_id}
        book = self.deleteItem("Books", book_key)
        return book
    