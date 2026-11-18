# Name: Abisola Sanni
# File: book_api.py
# Description: Book CRUD API using Flask and SQLite

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"

db = SQLAlchemy(app)


# Book Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)


# Create database
with app.app_context():
    db.create_all()


# Home Page
@app.route("/")
def home():
    return "Welcome to the Book API!"


# CREATE - Add a book
@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()

    new_book = Book(
        book_name=data["book_name"],
        author=data["author"],
        publisher=data["publisher"]
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({"message": "Book added successfully!"})


# READ - View all books
@app.route("/books", methods=["GET"])
def get_books():
    books = db.session.execute(db.select(Book)).scalars().all()

    book_list = []

    for book in books:
        book_list.append({
            "id": book.id,
            "book_name": book.book_name,
            "author": book.author,
            "publisher": book.publisher
        })

    return jsonify(book_list)


# UPDATE - Update book
@app.route("/books/<int:id>", methods=["PUT"])
def update_book(id):
    book = db.get_or_404(Book, id)
    data = request.get_json()

    book.book_name = data["book_name"]
    book.author = data["author"]
    book.publisher = data["publisher"]

    db.session.commit()

    return jsonify({"message": "Book updated successfully!"})


# DELETE - Delete book
@app.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    book = db.get_or_404(Book, id)

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted successfully!"})


# Run the application
if __name__ == "__main__":
    app.run(debug=True)