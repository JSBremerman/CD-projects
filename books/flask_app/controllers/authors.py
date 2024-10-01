from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.author import Author
from flask_app.models.book import Book


@app.route('/')
def home():
    return redirect('/authors')

@app.route('/authors')
def authors():
    return render_template('authors.html', authors= Author.get_all())

@app.route('/authors/add_author', methods=['POST'])
def add_author():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name']
    }
    id = Author.save(data)
    return redirect(f'/authors/{id}')

@app.route('/authors/<int:id>')
def author_show(id):
    data = {'id': id}
    return render_template('author_show.html', author = Author.fav_book(data), book_id = Book.book_id(data))

@app.route('/authors/add_fav_book', methods=['POST'])
def add_fav_book():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.add_fav(data)
    return redirect(f"/authors/{request.form['author_id']}")

