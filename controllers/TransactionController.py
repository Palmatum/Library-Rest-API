from datetime import datetime
from flask import request, jsonify
from pymongo import MongoClient

# client = MongoClient('localhost:27017')
client = MongoClient("mongodb+srv://dude:1234@cluster0.uwhf8.mongodb.net/Transactions")

db = client.Transactions

def issue_book():
    try:
        book_name = request.json['book_name']
        book_category = request.json['book_category']
        book_rent = request.json['book_rent']
        borrower_name = request.json['borrower_name']
        issue_date = request.json['issue_date']


        issue_date = datetime.strptime(issue_date, '%d-%m-%Y')
        borrower_flag = False
        book = db.books.find_one({'book_name': book_name})

        if book:
            for i in book['current_borrowers']:
                if i['borrower_name'] == borrower_name:
                    borrower_flag = True
                    break
            if borrower_flag is False:
                db.books.update_one(
                    {'book_name': book_name},
                    {'$push': {'current_borrowers': {'borrower_name': borrower_name, 'issue_date': issue_date}}}
                )
            else:
                return jsonify(
                    status = 'error',
                    message = 'Borrower already has this book',
                    error = 'Borrower already has this book'
                )
        else:
            db.books.insert_one({
                'book_name': book_name,
                'book_category': book_category,
                'book_rent': book_rent,
                'current_borrowers': [{'borrower_name': borrower_name, 'issue_date': issue_date}],
                'previous_borrowers': [],
                'rent_generated': 0
            })

        return jsonify(
            status = 'success',
            message = 'Book issued successfully',
            data = {
                'book_name': book_name,
                'book_category': book_category,
                'book_rent': book_rent,
                'borrower_name': borrower_name,
                'issue_date': issue_date,
                'rent_generated': 0
            }
        )

    except Exception as e:
        return jsonify(
            status = 'error',
            message = 'Error adding book',
            error = str(e)
        )

def return_book():
    try:
        book_name = request.json['book_name']
        borrower_name = request.json['borrower_name']
        return_date = request.json['return_date']

        return_date = datetime.strptime(return_date, '%d-%m-%Y')
        book = db.books.find_one({'book_name': book_name})

        if not book:
            return jsonify(
                status = 'error',
                message = 'Book not found',
                error = 'Book not found',
            )
        
        borrower_flag = False

        for i in book['current_borrowers']:
            if i['borrower_name'] == borrower_name:
                borrower_flag = True
                break
        
        if borrower_flag is False:
            return jsonify(
                status = 'error',
                message = 'Borrower not found',
                error = 'Borrower not found',
            )

        issue_date = book['current_borrowers'][0]['issue_date']

        if issue_date > return_date:
            return jsonify(
                status = 'error',
                message = 'Return date is before issue date',
                error = 'Return date is before issue date',
            )
        
        db.books.update_one(
            {'book_name': book_name},
            {'$pull': {'current_borrowers': {'borrower_name': borrower_name}}}
        )

        db.books.update_one(
            {'book_name': book_name},
            {'$push': {'previous_borrowers': {'borrower_name': borrower_name, 'issue_date': issue_date, 'return_date': return_date}}}
        )

        days_between = (return_date - issue_date).days
        rent = days_between * book['book_rent']

        db.books.update_one(
            {'book_name': book_name},
            {'$inc': {'rent_generated': rent}}
        )

        return jsonify(
            status = 'success',
            message = 'Book returned successfully',
            data = {
                'book_name': book_name,
                'borrower_name': borrower_name,
                'issue_date': issue_date.strftime('%d-%m-%Y'),
                'return_date': return_date.strftime('%d-%m-%Y'),
                'days_between': days_between,
                'rent': rent
            }
        )

    except Exception as e:
        return jsonify(
            status = 'error',
            message = 'Error adding book',
            error = str(e)
        )

def get_all_borrowers():
    try:
        book_name = request.json['book_name']

        book = db.books.find_one({'book_name': book_name})
        
        res = []

        if not book:
            return jsonify(
                status = 'error',
                message = 'Book not found',
                error = 'Book not found',
            )
        
        for i in book['current_borrowers']:
            res.append(i['borrower_name'])

        for i in book['previous_borrowers']:
            res.append(i['borrower_name'])

        res = list(set(res))

        return jsonify(
            status = 'success',
            message = 'All borrowers found',
            data = res
        )

    except Exception as e:
        return jsonify(
            status = 'error',
            message = 'Error fetching borrowers',
            error = str(e)
        )

def rent_generated():
    try:
        book_name = request.json['book_name']

        book = db.books.find_one({'book_name': book_name})
        
        if not book:
            return jsonify(
                status = 'error',
                message = 'Book not found',
                error = 'Book not found',
            )

        return jsonify(
            status = 'success',
            message = 'Rent generated successfully',
            data = book['rent_generated']
        )
    except Exception as e:
        return jsonify(
            status = 'error',
            message = 'Error fetching rent',
            error = str(e)
        )

def borrowers_book():
    try:
        borrower_name = request.json['borrower_name']
        
        books = db.books.find()
        res = []

        for i in books:
            for j in i['current_borrowers']:
                if j['borrower_name'] == borrower_name:
                    res.append(i['book_name'])
                    break

        if len(res) == 0:
            return jsonify(
                status = 'error',
                message = 'Borrower has no books',
                error = 'Borrower has no books'
            )

        return jsonify(
            status = 'success',
            message = 'Borrower has books',
            data = res
        )

    except Exception as e:
        return jsonify(
            status = 'error',
            message = 'Error fetching borrowers',
            error = str(e)
        )

def issues_between_dates():
    try:
        start_date = request.json['start_date']
        end_date = request.json['end_date']

        start_date = datetime.strptime(start_date, '%d-%m-%Y')
        end_date = datetime.strptime(end_date, '%d-%m-%Y')

        books = db.books.find()
        res = []

        for i in books:
            for j in i['previous_borrowers']:
                if j['issue_date'] >= start_date and j['issue_date'] <= end_date:
                    res.append(i['book_name'])
                    break

        if len(res) == 0:
            return jsonify(
                status = 'error',
                message = 'No books issued between the dates',
                error = 'No books issued between the dates'
            )

        return jsonify(
            status = 'success',
            message = 'Books issued between the dates',
            data = res
        )

    except Exception as e:
        return jsonify(
            status = 'error',
            message = 'Error fetching issues',
            error = str(e)
        )


# books {
#   book_name: '',
#   book_rent: ''
#   current_borrowers: [{
#       name: '',
#       issue_date: '',
#   }],
#   previous_borrowers: [{
#       name: '',
#       issue_date: '',
#       return_date: '',
#    }]
# }

