from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Recipe:
    DB = 'recipe_schema'
    def __init__(self, data):
        self.id = data['id']
        self.dish_name = data['dish_name']
        self.description = data['description']
        self.under_thirty = data['under_thirty']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.date = data['date']
        self.user = None
        
    @classmethod
    def get_one(cls, data):
        query = """
            SELECT * FROM recipes
            JOIN users on recipes.user_id = users.id
            WHERE recipes.id = %(id)s
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        print('Here are the results', results)
        recipe = []
        for row in results:
            temp = cls(row)
            data ={
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            temp.user = user.User(data)
            recipe.append(temp)
        return recipe

    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM recipes
            JOIN users on recipes.user_id = users.id;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        print('Here are the results', results)
        recipe = []
        for row in results:
            temp = cls(row)
            data ={
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            temp.user = user.User(data)
            recipe.append(temp)
        return recipe
    
    @classmethod
    def cookbook(cls):
        query = """
            SELECT * FROM recipes
            LEFT JOIN cookbook on cookbook.recipe_id = recipes.id
            LEFT JOIN users on users.id = cookbook.user_id
        """
        results = connectToMySQL(cls.DB).query_db(query)
        recipes = []
        for row in results:
            temp = cls(row)
            data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
                
            }
            temp.user = user.User(data)
            recipes.append(temp)
        print(results)
        return recipes
    
    @classmethod
    def save_recipe(cls, data):
        query = """
            INSERT INTO recipes (dish_name, description, under_thirty, instructions, date, user_id)
            VALUES (%(dish_name)s, %(description)s, %(under_thirty)s, %(instructions)s, %(date)s, %(user_id)s) 
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        print('Here are the results:', results)
        return results
    
    @classmethod
    def get_one_recipe(cls, data):
        query = """
                SELECT * FROM recipes
                JOIN users on recipes.user_id = users.id
                WHERE recipes.id = %(id)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result:
            return False
        
        result = result[0]
        temp = cls(result)
        data = {
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at']                
        }
        temp.user = user.User(data)
        print('get one recipe results', result)
        return temp
    
    @classmethod
    def delete(cls, data):
        query = """
                DELETE from recipes WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    # @classmethod
    # def update(cls,form_data):
    #     query = """
    #             UPDATE recipes
    #             SET name = %(name)s,
    #             description = %(description)s,
    #             instructions = %(instructions)s ,
    #             date_made = %(date_made)s,
    #             under_30 = %(under_30)s
    #             WHERE id = %(id)s;
    #             """
    #     return connectToMySQL(db).query_db(query,form_data)
    
