from ..shared.models import DatabaseModel

class BookModel(DatabaseModel):
    def __init__(self):
        super().__init__()

    # create a book
    def createBook(self, book):
        self.addItem("Books", book)
        return True
    
    def getBookByID(self, tableSchema, book_id):
        book_key = {"isbn":{"S":book_id}}
        book = self.getItemsWithKey("Books", tableSchema, book_key)
        return book
