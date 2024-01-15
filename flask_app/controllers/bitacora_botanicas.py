from flask import render_template, redirect, session, request, flash, url_for
from flask_app import app
from flask_app.models.bitacora_botanica import Bitacora_botanica
from flask_app.models.utils import allowed_file
from flask_app.models.user import User
from werkzeug.utils import secure_filename
import os


@app.route('/new/bitacora_botanica')
def new_bitacora_botanica():
     # Redirige a '/logout' si el usuario no está en sesión.
    #  - Utiliza el modelo 'User' para obtener los datos del usuario actual.
    if 'user_id' not in session:
        return redirect('/logout')
    data = {"id": session['user_id']}
    return render_template('new_bitacora_botanica.html', user=User.get_by_id(data))

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
    # Redirige a 'logout' si el usuario no está en sesión o a 'new_bitacora_botanica' si la validación falla.
    if 'user_id' not in session:
        return redirect('logout')
    if not Bitacora_botanica.validate_bitacora_botanica(request.form):
        return redirect(url_for('new_bitacora_botanica'))
    
    filenames = [] # Lista para almacen
    
    # Obtén la lista de objetos 'FileStorage' del campo de archivos 'imagenes'
    images = request.files.getlist('imagenes[]') 
    
    for image in images:
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            filenames.append(filename)
        else:
           if image:
                flash(f"Archivo no permitido: {image.filename}. Solo se permiten las extensiones: png, jpg, jpeg, gif.", 'error')
            
    image_urls = ','.join(filenames)

    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "lugarobservado": request.form["lugarobservado"],
        "cultivo": request.form["cultivo"],
        "bibliografia": request.form["bibliografia"],
        "Familia": request.form["Familia"],
        "Variedad": request.form["Variedad"],
        "date_made": request.form["date_made"],
        "image_url": image_urls,
        "user_id": session["user_id"]
    }
    Bitacora_botanica.save(data)
    return redirect(url_for('dashboard'))

@app.route('/edit/bitacora_botanica/<int:id>')
def edit_bitacora_botanica(id):

    if 'user_id' not in session:
        return redirect('/logout')
    data = {"id": id}
    user_data = {"id": session['user_id']}
    return render_template("edit_bitacora_botanica.html", edit=Bitacora_botanica.get_one(data), user=User.get_by_id(user_data))

@app.route('/update/bitacora_botanica', methods=['POST'])
def update_bitacora_botanica():
    # Actualiza una entrada existente en la bitácora botánica con la información proporcionada en el formulario.
    if 'user_id' not in session:
        return redirect('/logout')
    if not Bitacora_botanica.validate_bitacora_botanica(request.form):
        return redirect('/edit/bitacora_botanica/' + request.form['id'])

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
    return redirect('/dashboard')

@app.route('/bitacora_botanica/<int:id>')
def show_bitacora_botanica(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {"id": id}
    user_data = {"id": session['user_id']}
    return render_template("show_bitacora_botanica.html", bitacora_botanica=Bitacora_botanica.get_one(data), user=User.get_by_id(user_data))

@app.route('/destroy/bitacora_botanica/<int:id>')
def destroy_bitacora_botanica(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {"id": id}
    Bitacora_botanica.destroy(data)
    return redirect('/dashboard')


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Verificar si el componente 'file' está en la solicitud
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # Si el usuario no selecciona un archivo, el navegador
        # podría enviar una parte vacía sin nombre de archivo
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(file_path)
                flash('File successfully uploaded')
            except Exception as e:
                flash('An error occurred: ' + str(e))
                return redirect(request.url)
    





