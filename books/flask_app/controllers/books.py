from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.book import Book
from flask_app.models.author import Author


@app.route('/books')
def books():
    return render_template('books.html', books=Book.get_all())

@app.route('/books/add_book', methods=['POST'])
def add_book():
    data = {
        'title': request.form['title'],
        'num_of_pages': request.form['num_of_pages']
    }
    id = Book.save(data)
    return redirect(f'/books/{ id }')

@app.route('/books/<int:id>')
def book_show(id):
    data = {'id': id}
    return render_template('book_show.html', book = Book.author_fav(data), author_id = Author.author_id(data))


