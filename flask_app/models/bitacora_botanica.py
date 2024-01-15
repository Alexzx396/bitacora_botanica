from flask_app.config.mysqlconnection import connectToMySQL
from flask import app, flash
from werkzeug.utils import secure_filename
import os

class Bitacora_botanica:
    db_name = 'biitacora_botanica'
    
    def __init__(self, db_data):
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
        self.image_url = db_data['image_url']  

    @staticmethod
    def allowed_file(filename):
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @classmethod
    def save(cls, data, images=None):
        image_urls = []

        if images:

            for image in images:
                print("Procesando imagen:", image.filename)  # Depuración

                if image and cls.allowed_file(image.filename):
                    print("Imagen permitida:", image.filename)  # Depuración
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                    try:
                        image.save(image_path)
                        image_urls.append(filename)
                        print("Imagen guardada y añadida a la lista:", filename)  # Depuración
                    except Exception as e:
                        print("Error al guardar la imagen:", e)  # Manejo de errores
                else:
                    print(f"Archivo no permitido o no válido: {image.filename}")  # Depuración
                # Concatena los nombres de archivo en una cadena separada por comas
                print("Filenames antes de unir:", image_urls)
                data['image_url'] = ','.join(image_urls) if image_urls else None
                print("Image URLs:", data['image_url'])  # Depuración


        # Consulta SQL para insertar los datos
        query = """
        INSERT INTO bitacora_botanica 
        (name, description, lugarobservado, cultivo, bibliografia, Familia, Variedad, date_made, user_id, image_url) 
        VALUES (%(name)s, %(description)s, %(lugarobservado)s, %(cultivo)s, %(bibliografia)s, %(Familia)s, %(Variedad)s, %(date_made)s, %(user_id)s, %(image_url)s);
        """
        # Intenta ejecutar la consulta SQL y maneja excepciones
        try:
            return connectToMySQL(cls.db_name).query_db(query, data)
        except Exception as e:
            print(f"Error al insertar en la base de datos: {e}")
            return None


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM bitacora_botanica;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_bitacora_botanica = []
        for row in results:
            all_bitacora_botanica.append(cls(row))
        return all_bitacora_botanica
    
    #  buscador de imagenes 
    @classmethod
    def get_search(cls, filter):
        query = "SELECT * FROM bitacora_botanica WHERE (name LIKE %%(filter)s) OR (Familia LIKE %%(filter)s) OR (Variedad LIKE %%(filter)s) OR (lugarobservado LIKE %%(filter)s);"
        results = connectToMySQL(cls.db_name).query_db(query, {'filter': f"%{filter['id']}%"})
        all_bitacora_botanica = []
        for row in results:
            all_bitacora_botanica.append(cls(row))
        return all_bitacora_botanica

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM bitacora_botanica WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return cls(results[0])
        return None

    @classmethod
    def update(cls, data, new_images=None):
        image_urls = data['image_url'].split(',') if data['image_url'] else []
        print("URLs de imagen existentes:", image_urls)  # Depuración

        if new_images:
            for new_image in new_images:
                if new_image and cls.allowed_file(new_image.filename):
                    filename = secure_filename(new_image.filename)
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    try:
                        new_image.save(image_path)
                        image_urls.append(filename)
                        print("Imagen guardada:", filename)  # Depuración
                    except Exception as e:
                        print("Error al guardar la imagen:", e)  # Manejo de errores
                else:
                    if new_image:
                        print("Archivo no permitido o no válido:", new_image.filename)  # Depuración

        data['image_url'] = ','.join(image_urls)
        print("URLs de imagen actualizadas:", data['image_url'])  # Depuración

        query = "UPDATE bitacora_botanica SET name = %(name)s, description = %(description)s, lugarobservado = %(lugarobservado)s, cultivo = %(cultivo)s, bibliografia = %(bibliografia)s, Familia = %(Familia)s, Variedad = %(Variedad)s, date_made = %(date_made)s, image_url = %(image_url)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


    
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM bitacora_botanica WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

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