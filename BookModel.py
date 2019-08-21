from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)

class Book(db.Model):
    # sql table name
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    code = db.Column(db.Integer)

    def json(self):
        return {'name': self.name, 'price': self.price, 'code': self.code}

    def add_book(_name, _price, _code):
        new_book = Book(name=_name, price=_price, code=_code)
        db.session.add(new_book)
        db.session.commit()

    def get_all_books():
        return [Book.json(book) for book in Book.query.all()]

    def get_book(_code):
        return Book.json(Book.query.filter_by(code=_code).first())

    def update_book_price(_code, _price):
        book_to_update = Book.query.filter_by(code=_code).first()
        book_to_update.price = _price
        db.session.commit()

    def update_book_name(_code, _name):
        book_to_update = Book.query.filter_by(code=_code).first()
        book_to_update.name = _name
        db.session.commit()

    def update_book(_code, _price, _name):
        book_to_update = Book.query.filter_by(code=_code).first()
        book_to_update.name = _name
        book_to_update.price = _price
        db.session.commit()

    def delete_book(_code):
        Book.query.filter_by(code=_code).delete()
        db.session.commit()

    def __repr__(self):
        book_object = {
            'name': self.name,
            'price': self.price,
            'code': self.code
        }
        return json.dumps(book_object)
