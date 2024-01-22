from flask_app.config.mysqlconnection import connectToMySQL
from flask import app, flash, render_template
from datetime import datetime
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
    def process_images(cls, images):
        """Procesa una lista de imágenes y devuelve sus URLs."""
        image_urls = []
        for image in images:
            if image and cls.allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                try:
                    image.save(image_path)
                    image_urls.append(filename)
                except Exception as e:
                    print(f"Error al guardar la imagen: {e}")
            else:
                print(f"Archivo no permitido o no válido: {image.filename}")
        return image_urls
    
    @classmethod
    def save(cls, data, images=None):
        """Guarda una nueva entrada de bitácora en la base de datos."""
        if images:
            image_urls = cls.process_images(images)
            data['image_url'] = ','.join(image_urls) if image_urls else None

        query = """
        INSERT INTO bitacora_botanica 
        (name, description, lugarobservado, cultivo, bibliografia, Familia, Variedad, date_made, user_id, image_url) 
        VALUES (%(name)s, %(description)s, %(lugarobservado)s, %(cultivo)s, %(bibliografia)s, %(Familia)s, %(Variedad)s, %(date_made)s, %(user_id)s, %(image_url)s);
        """
        try:
            return connectToMySQL(cls.db_name).query_db(query, data)
        except Exception as e:
            print(f"Error al insertar en la base de datos: {e}")
            return None



    @classmethod
    def format_date(cls, date):
        if isinstance(date, datetime):
            # Si date ya es un objeto datetime, solo formatearlo
            return date.strftime('%d-%m-%Y')
        elif isinstance(date, str):
            # Si date es una cadena, convertirla a datetime y luego formatearla
            try:
                return datetime.strptime(date, '%d-%m-%Y').strftime('%d-%m-%Y')
            except ValueError:
                # Manejar el error si la fecha no está en el formato esperado
                return None
        else:
            # Si date no es ni datetime ni cadena, devolver None o manejar de otra manera
            return None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM bitacora_botanica;"
        results = connectToMySQL(cls.db_name).query_db(query)
        bitacoras = []
        for row in results:
            bitacora = cls(row)
            if isinstance(bitacora.date_made, str):
                try:
                    bitacora.date_made = datetime.strptime(bitacora.date_made, '%d-%m--%Y')
                except ValueError:
                    bitacora.date_made = None 
            bitacoras.append(bitacora)
        return bitacoras


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM bitacora_botanica WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            bitacora = cls(results[0])
            bitacora.date_made = cls.format_date(bitacora.date_made)
            return bitacora
        return None
    

    
    @classmethod
    def get_search(cls, filter):
        query = "SELECT * FROM bitacora_botanica WHERE (name LIKE %%(filter)s) OR (Familia LIKE %%(filter)s) OR (Variedad LIKE %%(filter)s) OR (lugarobservado LIKE %%(filter)s);"
        results = connectToMySQL(cls.db_name).query_db(query, {'filter': f"%{filter['id']}%"})
        all_bitacora_botanica = []
        for row in results:
            all_bitacora_botanica.append(cls(row))
        return all_bitacora_botanica


    @classmethod
    def update(cls, data):
        query = """
        UPDATE bitacora_botanica 
        SET name = %(name)s, 
            description = %(description)s, 
            lugarobservado = %(lugarobservado)s, 
            cultivo = %(cultivo)s, 
            bibliografia = %(bibliografia)s, 
            Familia = %(Familia)s, 
            Variedad = %(Variedad)s, 
            date_made = %(date_made)s, 
            image_url = %(image_url)s, 
            updated_at = NOW() 
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def process_images(cls, images):
        image_urls = []
        for image in images:
            if image and cls.allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  
                image.save(image_path)
                image_urls.append(filename)
        return image_urls


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