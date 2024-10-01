from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Sighting:
    DB = 'sasquatch_schema'
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.info = data['info']
        self.date = data['date']
        self.num_of_squatches = data['num_of_squatches']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None

    @staticmethod
    def validate_sighting(data):
        valid = True
        if len(data['location']) == 0:
            flash("Please input a location")
            valid = False
        if len(data['info']) == 0:
            flash("Please include a desciption of the sighting")
            valid = False
        if data['date'] == '':
            flash('Please select the date of your sighting')
            valid = False
        if data['num_of_squatches'] == '0':
            flash('Squatches exist. Perhaps you made a mistake in selecting the number you saw. Select a value greater than 0')
            valid = False
        return valid

    @classmethod
    def get_one_sighting(cls, data):
        query = """
            SELECT * FROM sightings
            JOIN users on sightings.user_id = users.id
            WHERE sightings.id = %(id)s
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        sighting = []
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
            sighting.append(temp)
        return sighting

    @classmethod
    def get_all_sightings(cls):
        query = """
            SELECT * FROM sightings
            JOIN users on sightings.user_id = users.id;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        sightings = []
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
            sightings.append(temp)
        return sightings
    
    @classmethod
    def save_sighting(cls, data):
        query = """
            INSERT INTO sightings (location, info, date, num_of_squatches, user_id)
            VALUES (%(location)s, %(info)s, %(date)s, %(num_of_squatches)s, %(user_id)s) 
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        print('Here are the saved results:', results)
        return results

    @classmethod
    def delete(cls, data):
        query = """
                DELETE from sightings WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def edit_this_sighting(cls, data):
        query = """
                SELECT * FROM sightings
                JOIN users on sightings.user_id = users.id
                WHERE sightings.id = %(id)s;
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
        return temp
    
    @classmethod
    def update(cls, data):
        query = """
            UPDATE sightings
            SET location = %(location)s,
            info = %(info)s,
            date = %(date)s,
            num_of_squatches = %(num_of_squatches)s
            WHERE id = %(id)s
        """
        return connectToMySQL(cls.DB).query_db(query, data)