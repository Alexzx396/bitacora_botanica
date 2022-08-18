from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Bitacora_botanica:
    db_name = 'biitacora_botanica'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.description = db_data['description']
        self.lugarobservado = db_data['lugarobservado']
        self.cultivo = db_data['cultivo']
        self.bibliografia = db_data['bibliografia']
        self.Familia = db_data['Familia']
        self.Variedad = db_data['Variedad']
        self.date_made = db_data['date_made']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO bitacora_botanica (name, description, Familia, Variedad,  lugarobservado, cultivo, bibliografia,  date_made, user_id) VALUES (%(name)s,%(description)s, %(lugarobservado)s, %(cultivo)s, %(bibliografia)s,%(Familia)s ,%(Variedad)s, %(date_made)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM bitacora_botanica;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_bitacora_botanica = []
        for row in results:
            print(row['date_made'])
            all_bitacora_botanica.append( cls(row) )
        return all_bitacora_botanica

# Prueba buscador
    @classmethod
    def get_search(cls,filter):
        print (filter)
        query = "SELECT * FROM bitacora_botanica where (name like'%"+filter['id']+"%') or (Familia like'%"+filter['id']+"%') or (Variedad like'%"+filter['id']+"%') or (lugarobservado like'%"+filter['id']+"%');"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_bitacora_botanica = []
        for row in results:
            print(row['date_made'])
            all_bitacora_botanica.append( cls(row) )
        return all_bitacora_botanica
# Prueba buscador
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM bitacora_botanica WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE bitacora_botanica SET name=%(name)s, description=%(description)s, lugarobservado=%(lugarobservado)s, cultivo=%(cultivo)s, bibliografia=%(bibliografia)s, Familia=%(Familia)s, Variedad=%(Variedad)s, date_made=%(date_made)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM bitacora_botanica WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_bitacora_botanica(bitacora_botanica):
        is_valid = True
        if len(bitacora_botanica['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters","bitacora_botanica")
        if len(bitacora_botanica['Familia']) < 3:
            is_valid = False
            flash("Familia must be at least 3 characters","bitacora_botanica")
        if len(bitacora_botanica['Variedad']) < 3:
            is_valid = False
            flash("Variedad must be at least 3 characters","bitacora_botanica")
        if len(bitacora_botanica['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","bitacora_botanica")
        if len(bitacora_botanica['lugarobservado']) < 3:
            is_valid = False
            flash("lugarobservado must be at least 3 characters","bitacora_botanica")
        if len(bitacora_botanica['cultivo']) < 3:
            is_valid = False
            flash("cultivo must be at least 3 characters","bitacora_botanica")
        if len(bitacora_botanica['bibliografia']) < 3:
            is_valid = False
            flash("bibliografia must be at least 3 characters","bitacora_botanica")
        if  bitacora_botanica['date_made'] == "":
            is_valid = False
            flash("Please enter a date","bitacora_botanica")
        return is_valid