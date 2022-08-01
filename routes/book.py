from flask import Blueprint

from controllers.BookController import (
    add_book,
    get_all_books,
    get_book_by_name,
    get_book_by_rent,
    get_book_by_deepsearch
)

book = Blueprint('book', __name__)

book.route('/', methods=["POST"])(add_book)
book.route('/', methods=["GET"])(get_all_books)
book.route('/search/search-by-term', methods=["GET"])(get_book_by_name)
book.route('/search/rent', methods=["GET"])(get_book_by_rent)
book.route('/search/deepsearch', methods=["GET"])(get_book_by_deepsearch)