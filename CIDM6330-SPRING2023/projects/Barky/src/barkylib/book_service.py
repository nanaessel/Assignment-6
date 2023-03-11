from flask import Blueprint
from bson.objectid import ObjectId


book_service_bp = Blueprint('book_service', __name__)

class BookService:
    def __init__(self, book_dao):
        self.book_dao = book_dao

    def get_all_books(self):
        return self.book_dao.get_all_books()

    def get_book_by_id(self, id):
        return self.book_dao.get_book_by_id(id)

    def create_book(self, book):
        return self.book_dao.create_book(book)

    def update_book(self, id, book):
        return self.book_dao.update_book(id, book)

    def delete_book(self, id):
        return self.book_dao.delete_book(id)

class BookDao:
    def __init__(self, db):
        self.db = db

    def get_all_books(self):
        return self.db.books.find()

    def get_book_by_id(self, id):
        return self.db.books.find_one({'_id': ObjectId(id)})

    def create_book(self, book):
        result = self.db.books.insert_one(book)
        return self.db.books.find_one({'_id': result.inserted_id})

    def update_book(self, id, book):
        self.db.books.replace_one({'_id': ObjectId(id)}, book)
        return self.get_book_by_id(id)

    def delete_book(self, id):
        self.db.books.delete_one({'_id': ObjectId(id)})
