from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author


class Book:
    DB = "books_schema"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.author_favorite = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL(cls.DB).query_db(query)
        books = []
        for book in results:
            books.append( cls(book) )
        return books

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO books (title, num_of_pages)
            VALUES (%(title)s, %(num_of_pages)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def author_fav(cls, data):
        query = """
            SELECT * from books
            LEFT JOIN favorites on books.id = favorites.book_id
            LEFT JOIN authors on authors.id = favorites.author_id
            WHERE books.id = %(id)s;
        """
        result = connectToMySQL(cls.DB).query_db(query,data)
        book = cls(result[0])
        for row in result:
            if row['authors.id'] == None:
                break
            data = {
                'id': row['authors.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'created_at': row['authors.created_at'],
                'updated_at': row['authors.updated_at']
            }
            book.author_favorite.append(author.Author(data))
        return book
    
    @classmethod
    def book_id(cls, data):
        query = """
            SELECT * FROM books WHERE books.id
            NOT IN (SELECT book_id FROM favorites WHERE author_id = %(id)s);
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        books =[]
        for result in results:
            books.append(cls(result))
        print("These are the books:", books)
        return books

        