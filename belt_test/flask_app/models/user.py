from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import sighting
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = 'sasquatch_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_registration(user):
        is_valid = True
        if User.check_email(user['email']) != None:
            is_valid = False
            flash('Email not available', 'registration')
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash('Invalid email address', 'registration')
        if len(user['first_name']) < 2:
            is_valid = False
            flash('First name must be at least 2 characters', 'registration')
        if len(user['last_name']) < 2:
            is_valid = False
            flash('Last name must be at least 2 characters', 'registration')
        if len(user['password']) < 8:
            is_valid = False
            flash('Password must be at least 8 characters', 'registration')
        if user['password'] != user['confirm_password']:
            is_valid = False
            flash('Passwords must match', 'registration')
        if not re.search('[0-9]', user['password']):
            is_valid = False
            flash('Password must include a number', 'registration')
        if not re.search('[A-Z]', user['password']):
            is_valid = False
            flash('Password must include a capital letter', 'registration')
        if not re.search('[$#@!%^&*]', user['password']):
            is_valid = False
            flash('Password must include a special character', 'registration')
        return is_valid
    
    @classmethod
    def check_email(cls, email):
        query = """
            SELECT * FROM users
            WHERE email = %(email)s
        """
        results = connectToMySQL(cls.DB).query_db(query, {'email': email})
        if results:
            return cls(results[0])
        else:
            return None
        
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_user(cls, data):
        query = """
            SELECT * FROM users
            WHERE id = %(id)s
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    