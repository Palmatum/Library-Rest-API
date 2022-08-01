from flask import request, jsonify
from pymongo import MongoClient

# client = MongoClient('localhost:27017')
client = MongoClient("mongodb+srv://dude:1234@cluster0.uwhf8.mongodb.net/Books")

db = client.Books

def add_book():
    try:
        book_name = request.json['book_name']
        book_category = request.json['book_category']
        book_rent = request.json['book_rent']

        db.books.insert_one({
            'book_name': book_name,
            'book_category': book_category,
            'book_rent': book_rent
        })

        return jsonify(
            status = 'success',
            message = 'Book added successfully',
            data = {
                'book_name': book_name,
                'book_category': book_category,
                'book_rent': book_rent
            }
        )

    except Exception as e:
        return jsonify(
            status = 'error',
            message = 'Error adding book',
            error = str(e)
        )

def get_all_books():
    try:
        books = db.books.find()
        books_list = []
        for book in books:
            books_list.append({
                'book_name': book['book_name'],
                'book_category': book['book_category'],
                'book_rent': book['book_rent']
            })

        return jsonify(
            status = 'success',
            message = 'Books fetched successfully',
            data = books_list
        )

    except Exception as e:
        return jsonify(
            status = 'error',
            message = 'Error fetching books',
            error = str(e)
        )

def get_book_by_name():
    try:
        search_term = request.json['search_term']
        books = db.books.find({'book_name': {'$regex': search_term, '$options': 'i'}})
        books_list = []
        for book in books:
            books_list.append({
                'book_name': book['book_name'],
                'book_category': book['book_category'],
                'book_rent': book['book_rent']
            })

        return jsonify(
            status = 'success',
            message = 'Books fetched successfully',
            data = books_list
        )
    except Exception as e:
        return jsonify(
            status = 'error',
            message = 'Error fetching books',
            error = str(e)
        )

def get_book_by_rent():
    try:
        rent_range = request.json['rent_range']
        books = db.books.find({'book_rent': {'$gte': rent_range[0], '$lte': rent_range[1]}})
        books_list = []
        for book in books:
            books_list.append({
                'book_name': book['book_name'],
                'book_category': book['book_category'],
                'book_rent': book['book_rent']
            })

        return jsonify(
            status = 'success',
            message = 'Books fetched successfully',
            data = books_list
        )
    except Exception as e:
        return jsonify(
            status = 'error',
            message = 'Error fetching books',
            error = str(e)
        )

def get_book_by_deepsearch():
    try:
        search_term = request.json['search_term']
        rent_range = request.json['rent_range']
        books = db.books.find({'book_name': {'$regex': search_term, '$options': 'i'}, 'book_category': {'$regex': search_term, '$options': 'i'}, 'book_rent': {'$gte': rent_range[0], '$lte': rent_range[1]}})
        books_list = []
        for book in books:
            books_list.append({
                'book_name': book['book_name'],
                'book_category': book['book_category'],
                'book_rent': book['book_rent']
            })

        return jsonify(
            status = 'success',
            message = 'Books fetched successfully',
            data = books_list
        )
    except Exception as e:
        return jsonify(
            status = 'error',
            message = 'Error fetching books',
            error = str(e)
        )