from flask import Flask, jsonify, request, Response
from BookModel import *
from UserModel import *
from settings import *
import json
import jwt, datetime
from functools import wraps

app.config['SECRET_KEY'] = 'massive'

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')

        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Need a valid token to view this page'})

    return wrapper


@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])

    match = User.username_password_match(username, password)

    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', 401, mimetype='application/json')

def validate_book(book):
    if ("name" in book and "price" in book and "code" in book):
        return True
    else:
        return False

# PUT /books/323242
@app.route('/books/<int:code>', methods=['PUT'])
def put_book(code):
    request_data = request.get_json()
    update_book(code, request_data["price"], request_data["name"])
    response = Response("", status=204)
    return response

# PATCH /books/32312
@app.route('/books/<int:code>', methods=['PATCH'])
def updated_book(code):
    request_data = request.get_json()
    updated_book = {}

    if "name" in request_data:
        Book.update_book_name(code, request_data["name"])
    if "price" in request_data:
        Book.update_book_price(code, request_data["price"])

    response = Response("", status=204)
    response.headers["location"] = "/books/" + str(code)

    return response
# POST /books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if validate_book(request_data):
        Book.add_book(request_data["name"], request_data["price"], request_data["code"])
        response = Response("", 201, mimetype='application/json')
        response.headers["location"] = "/books/" + str(request_data["code"])
        return response
    else:
        error_message = {
            "error": "Invalid object passed in request",
            "help": "Make sure to match the following object structure: {'name': 'Harry Potter', 'price': 15.00, 'code': 3255343}"
        }

        response = Response(json.dumps(error_message), status=400, mimetype='application/json')
        return response

# GET /books/code
@app.route('/books/<int:code>')
def get_book_by_code(code):
    selected_book = Book.get_book(code)
    return jsonify(selected_book)

# DELETE /books/code
@app.route('/books/<int:code>', methods=['DELETE'])
def delete_book(code):
    Book.delete_book(code)
    return Response("", status=204)

# GET /books
@app.route('/books')
@token_required
def get_books():
    token = request.args.get('token')
    return jsonify({'books': Book.get_all_books()})

@app.route('/')
def hello_world():
    return 'Hello world!'

app.run(port=5000)
