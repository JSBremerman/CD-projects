from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models.ninja import Ninja


class Dojo:
    DB = "dojos_and_ninjas"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ninjas = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL(cls.DB).query_db(query)
        dojos = []
        for dojo in results:
            dojos.append( cls(dojo) )
        return dojos
    
    @classmethod
    def save(cls, data):
        query = """
            INSERT into dojos (name)
            VALUES (%(name)s);
        """
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def ninjas_at_dojo(cls, data):
        query = """
            SELECT * FROM dojos
            LEFT JOIN ninjas on dojos.id = ninjas.dojo_id
            WHERE dojos.id = %(id)s;
        """
        dojo_id = connectToMySQL(cls.DB).query_db(query,data)
        dojo = cls(dojo_id[0])
        for ninja in dojo_id:
            dojos_ninja = {
                'id': ninja['ninjas.id'],
                'first_name': ninja['first_name'],
                'last_name': ninja['last_name'],
                'age': ninja['age'],
                'created_at': ninja['ninjas.created_at'],
                'updated_at': ninja['ninjas.updated_at'],
                'dojo_id': ninja['dojo_id']
            }
            dojo.ninjas.append( Ninja(dojos_ninja))
        print(ninja)
        return dojo
    