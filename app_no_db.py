from flask import Flask, jsonify, request, Response
import json

app = Flask(__name__)
print(__name__)

books = [
    {
        'name': 'Harry Potter',
        'price': 15.00,
        'code': 3255343
    },
    {
        'name': 'Game of Thrones',
        'price': 13.00,
        'code': 2445332
    }
]

def validate_book(book):
    if ("name" in book and "price" in book and "code" in book):
        return True
    else:
        return False

# PUT /books/323242
@app.route('/books/<int:code>', methods=['PUT'])
def put_book(code):
    request_data = request.get_json()

    for book in books:
        if book["code"] == code:
            book["name"] = request_data["name"]
            book["price"] = request_data["price"]

    response = Response("", status=204)
    return response

# PATCH /books/32312
@app.route('/books/<int:code>', methods=['PATCH'])
def updated_book(code):
    request_data = request.get_json()
    updated_book = {}

    if "name" in request_data:
        updated_book["name"] = request_data["name"]
    if "price" in request_data:
        updated_book["price"] = request_data["price"]

    for book in books:
        if book["code"] == code:
            book.update(updated_book)

    response = Response("", status=204)
    response.headers["location"] = "/books/" + str(code)

    return response
# POST /books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if validate_book(request_data):
        new_book = {
            'name': request_data["name"],
            'price': request_data["price"],
            'code': request_data["code"]
        }
        books.insert(0, new_book)

        response = Response("", 201, mimetype='application/json')
        response.headers["location"] = "/books/" + str(new_book["code"])
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
    selected_book = {}

    for book in books:
        if book["code"] == code:
            selected_book = {
                'name': book["name"],
                'price': book["price"],
                'code': book["code"]
            }

    return jsonify(selected_book)

# DELETE /books/code
@app.route('/books/<int:code>', methods=['DELETE'])
def delete_book(code):
    for idx, book in enumerate(books):
        if book["code"] == code:
            books.pop(idx)

    return Response("", status=204)

# GET /books
@app.route('/books')
def get_books():
    return jsonify({'books': books})

@app.route('/')
def hello_world():
    return 'Hello world!'

app.run(port=5000)
