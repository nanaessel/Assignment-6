from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from services import database


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmarks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Register the book service Blueprint
from book_service import book_service_bp
app.register_blueprint(book_service_bp, url_prefix='/books')

# Initialize the BookService
from book_service import BookService
book_service = BookService(db)

# Define some routes for testing
@app.route('/')
def hello_world():
    return 'Hello, world!'

@app.route('/books')
def get_all_books():
    books = book_service.get_all_books()
    return jsonify([book.__dict__ for book in books])

@app.route('/books/<id>')
def get_book_by_id(id):
    book = book_service.get_book_by_id(id)
    if book is None:
        abort(404)
    return jsonify(book.__dict__)

@app.route('/books', methods=['POST'])
def create_book():
    book = request.json
    new_book = book_service.create_book(book)
    return jsonify(new_book.__dict__)

if __name__ == '__main__':
    app.run(debug=True)
