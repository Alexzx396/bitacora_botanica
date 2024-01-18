from flask import render_template, redirect, session, request, flash, url_for
from flask_app import app
from flask_app.models.bitacora_botanica import Bitacora_botanica
from flask_app.models.user import User
from werkzeug.utils import secure_filename
import os

# Funciones Auxiliares
def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def is_logged_in():
    return 'user_id' in session

def get_user_data():
    return {"id": session['user_id']} if is_logged_in() else None

def process_uploaded_images(images):
    filenames = []
    for image in images:
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                image.save(image_path)
                filenames.append(filename)
            except Exception as e:
                flash(f"Error al guardar la imagen: {e}", 'error')
        else:
            flash(f"Archivo no permitido: {image.filename}", 'error')
    return filenames

# Rutas de la Aplicación
@app.route('/new/bitacora_botanica/')
def new_bitacora_botanica():
    if not is_logged_in():
        return redirect('/logout')
    return render_template('new_bitacora_botanica.html', user=User.get_by_id(get_user_data()))

@app.route('/search/bitacora_filter/<string:planta>')
def search_bitacora_filter(planta):  
    # Muestra los resultados en 'dashboard.html'.
    if 'user_id' not in session:
        return redirect('/logout')
    data = {"id": session['user_id']}
    filter = {"id": planta}
    return render_template("dashboard.html", user=User.get_by_id(data), bitacora_botanica=Bitacora_botanica.get_search(filter))



@app.route('/create/bitacora_botanica', methods=['POST'])
def create_bitacora_botanica():
    if not is_logged_in():
        return redirect('/logout')

    filenames = process_uploaded_images(request.files.getlist('imagenes[]'))

    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "lugarobservado": request.form["lugarobservado"],
        "cultivo": request.form["cultivo"],
        "bibliografia": request.form["bibliografia"],
        "Familia": request.form["Familia"],
        "Variedad": request.form["Variedad"],
        "date_made": request.form["date_made"],
        "image_url": ','.join(filenames),
        "user_id": session["user_id"]
    }
    Bitacora_botanica.save(data)
    return redirect(url_for('dashboard'))

@app.route('/edit/bitacora_botanica/<int:id>')
def edit_bitacora_botanica(id):
    if not is_logged_in():
        return redirect('/logout')
    data = {"id": id}
    return render_template("edit_bitacora_botanica.html", edit=Bitacora_botanica.get_one(data), user=User.get_by_id(get_user_data()))

@app.route('/update/bitacora_botanica', methods=['POST'])
def update_bitacora_botanica():
    if not is_logged_in():
        return redirect('/logout')
    if not Bitacora_botanica.validate_bitacora_botanica(request.form):
        return redirect(url_for('edit_bitacora_botanica', id=request.form['id']))

    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "lugarobservado": request.form["lugarobservado"],
        "cultivo": request.form["cultivo"],
        "bibliografia": request.form["bibliografia"],
        "Familia": request.form["Familia"],
        "Variedad": request.form["Variedad"],
        "date_made": request.form["date_made"],
        "id": request.form['id'],
        "image_url": request.form['image_url']
        
    }
    Bitacora_botanica.update(data)
    return redirect(url_for('dashboard'))

@app.route('/bitacora_botanica/<int:id>')
def show_bitacora_botanica(id):
    if not is_logged_in():
        return redirect('/logout')
    data = {"id": id}
    return render_template("show_bitacora_botanica.html", bitacora_botanica=Bitacora_botanica.get_one(data), user=User.get_by_id(get_user_data()))

@app.route('/destroy/bitacora_botanica/<int:id>')
def destroy_bitacora_botanica(id):
    if not is_logged_in():
        return redirect('/logout')
    data = {"id": id}
    Bitacora_botanica.destroy(data)
    return redirect(url_for('dashboard'))






