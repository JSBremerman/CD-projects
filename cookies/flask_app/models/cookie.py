from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


class Cookie:
    DB = "cookies_schema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.cookie_type = data['cookie_type']
        self.num_of_boxes = data['num_of_boxes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @staticmethod
    def is_valid(user):
        valid = True
        if re.search('select_cookie', user['cookie_type']):
            valid = False
            flash('Please choose a Cookie Type')
        if re.search('choose', user['num_of_boxes']):
            valid = False
            flash('Please choose Number of Boxes')
        return valid
        
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (name, cookie_type, num_of_boxes)
            VALUES(%(name)s, %(cookie_type)s, %(num_of_boxes)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM users;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users
    
    @classmethod
    def update_cookies(cls, data):
        query = """
            UPDATE users
            SET name = %(name)s, cookie_type = %(cookie_type)s, num_of_boxes = %(num_of_boxes)s
            WHERE id = %(id)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        print (result)
        return result

    @classmethod
    def get_user(cls, data):
        query = """
            SELECT * FROM users
            WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
