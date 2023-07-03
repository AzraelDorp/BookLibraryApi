from app.books.model import BookModel as bookmodel


allbooks = bookmodel().getAllBooks()

for book in allbooks:
    bookmodel().deleteBook(book["book_id"])