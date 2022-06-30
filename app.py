from flask import Flask, jsonify, make_response, abort, request
from models import books

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/api/v1/books/", methods=["GET"])
def books_list_api_v1():
    return jsonify(books.all())

@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    return jsonify({"book": book})    

@app.route("/api/v1/books/", methods=["POST"])
def create_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    book = {
        'id': books.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description'),
        'author' : request.json.get('author')
    }
    books.create(book)
    return jsonify({'book': book}), 201    

@app.route("/api/v1/books/<int:book_id>", methods=['DELETE'])
def delete_book(book_id):
    result = books.delete(book_id)
    if not result:
        abort(404)
    return jsonify({'result': result})  

@app.route("/api/v1/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    todo = books.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'author' in data and not isinstance(data.get('author'), bool)
    ]):
        abort(400)
    book = {
        'title': data.get('title', book['title']),
        'description': data.get('description', book['description']),
        'author': data.get('author', book['author'])
    }
    books.update(book_id, book)
    return jsonify({'book': book})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found, the server could not find the requested website' , 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request, The browser (or proxy) sent a request that this server could not understand.', 'status_code': 400}), 400)


if __name__ == "__main__":
    app.run(debug=True)