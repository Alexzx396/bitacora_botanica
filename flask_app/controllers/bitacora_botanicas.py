from flask import render_template, redirect, session, request, flash, url_for
from flask_app import app
from flask_app.models.bitacora_botanica import Bitacora_botanica
from flask_app.models.user import User
from werkzeug.utils import secure_filename
from datetime import datetime
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

    # Obtener los datos de la bitácora botánica a editar
    bitacora_data = Bitacora_botanica.get_one({"id": id})

    # Verificar si se encontró la entrada de la bitácora botánica
    if not bitacora_data:
        flash("Bitácora botánica no encontrada.", "error")
        return redirect(url_for('dashboard'))
    
    # Formatear la fecha para mostrar en el formulario
    if bitacora_data.date_made and isinstance(bitacora_data.date_made, str):
        try:
            bitacora_data.date_made = datetime.strptime(bitacora_data.date_made, '%d-%m-%Y').strftime('%Y-%m-%d')
        except ValueError:
            flash("Formato de fecha no válido.", "error")

    # Obtener los datos del usuario actual para mostrar en la interfaz
    user_data = User.get_by_id(get_user_data())

    return render_template("edit_bitacora_botanica.html", edit=bitacora_data, user=user_data)


@app.route('/update/bitacora_botanica', methods=['POST'])
def update_bitacora_botanica():
    if not is_logged_in():
        return redirect('/logout')

    # Obtener los datos actuales
    current_data = Bitacora_botanica.get_one({'id': request.form['id']})

    # Procesar las imágenes cargadas
    new_filenames = process_uploaded_images(request.files.getlist('imagenes[]'))
    if new_filenames:
        image_urls = ','.join(new_filenames)
    else:
        # Mantener las imágenes existentes si no se cargan nuevas
        image_urls = request.form.get('image_url_existing', '')

   # Procesar la fecha
    new_date = request.form['date_made'] or current_data.date_made

    # Actualizar los datos
    data = {
        'id': request.form['id'],
        'name': request.form['name'],
        'Familia': request.form['Familia'],
        'Variedad': request.form['Variedad'],
        'date_made': new_date,
        'lugarobservado': request.form['lugarobservado'],
        'cultivo': request.form['cultivo'],
        'bibliografia': request.form['bibliografia'],
        'description': request.form['description'],
        'image_url': image_urls,
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











