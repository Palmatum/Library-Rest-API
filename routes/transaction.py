from flask import Blueprint

from controllers.TransactionController import (
    issue_book,
    return_book,
    get_all_borrowers,
    rent_generated,
    borrowers_book,
    issues_between_dates
)

transaction = Blueprint('transaction', __name__)

transaction.route('/issue', methods=["POST"])(issue_book)
transaction.route('/return', methods=["POST"])(return_book)
transaction.route('/get-all-borrowers', methods=["GET"])(get_all_borrowers)
transaction.route('/rent-generated', methods=["GET"])(rent_generated)
transaction.route('/borrowers-book', methods=["GET"])(borrowers_book)
transaction.route('/issues-between-ates', methods=["GET"])(issues_between_dates)
