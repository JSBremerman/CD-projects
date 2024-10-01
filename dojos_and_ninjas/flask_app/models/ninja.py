from flask_app.config.mysqlconnection import connectToMySQL


class Ninja:
    DB = "dojos_and_ninjas"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.dojo_id = data['dojo_id']

    @classmethod
    def save(cls, data):
        query = """
            INSERT into ninjas (first_name, last_name, age, dojo_id)
            VALUES (%(first_name)s,%(last_name)s,%(age)s,%(dojo_id)s);
        """
        result = connectToMySQL(cls.DB).query_db(query,data)
        print(result)
        return result
    
    @classmethod
    def get_ninja(cls, data):
        query = """
                SELECT * FROM ninjas
                WHERE id = %(id)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        print("This is the", result)
        return cls(result[0])
    
    # @classmethod
    # def get_dojo(cls, id):
    #     query = """
    #             SELECT * FROM ninjas
    #             WHERE id = %(id)s;
    #     """
    #     data = {'id': id}
    #     result = connectToMySQL(cls.DB).query_db(query, data)
    #     print(result)
    #     return result
        
        
    
    @classmethod
    def update_ninja(cls, data):
        query = """
            UPDATE ninjas
            SET first_name = %(first_name)s, last_name = %(last_name)s, age = %(age)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete_ninja(cls, id):
        query = """
            DELETE FROM ninjas
            WHERE id = %(id)s;
        """
        data = {'id': id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        # print("This is the", result)
        return result