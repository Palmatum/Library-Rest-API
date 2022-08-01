from flask import Flask

from routes.book import book
from routes.transaction import transaction

app = Flask(__name__)

app.register_blueprint(book, url_prefix='/book')
app.register_blueprint(transaction, url_prefix='/transaction')

if __name__ == '__main__':
    app.run(port=5000, debug=True)

