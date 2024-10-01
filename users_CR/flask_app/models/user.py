from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt

import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "users_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) <= 0:
            flash('Required Field - First Name')
            is_valid = False
        if len(data['last_name']) <= 0:
            flash('Required Field - Last Name')
            is_valid = False
        if len(data['email']) <= 0:
            flash('Required Field - Email')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users
    
    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM users
                WHERE id = %(id)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def save(cls, data):
        query = """
                INSERT into users (first_name, last_name, email)
                VALUES (%(first_name)s,%(last_name)s,%(email)s);
            """
        return connectToMySQL(cls.DB).query_db(query,data)

    
    @classmethod
    def update(cls, data):
        query = """
                UPDATE users
                SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at=NOW()
                WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query,data)
        
    
    @classmethod
    def delete(cls, id):
        query = """
                DELETE FROM users 
                WHERE id = %(id)s;
        """
        data = {'id': id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
    
    @classmethod
    def register(cls, data):
        query = """
            INSERT INTO users (username, password)
            VALUES (%(username)s, %(password)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)
