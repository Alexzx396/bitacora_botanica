from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.bitacora_botanica import Bitacora_botanica
from flask_app.models.user import User


@app.route('/new/bitacora_botanica')
def new_bitacora_botanica():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_bitacora_botanica.html',user=User.get_by_id(data))

# Prueba buscador
#@app.route('/search/bitacora_filter/<id>')
@app.route('/search/bitacora_filter/<string:planta>')
def search_bitacora_filter(planta):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    filter = {
        "id": planta
    }
    return render_template("dashboard.html",user=User.get_by_id(data),bitacora_botanica=Bitacora_botanica.get_search(filter))
# Prueba buscador

@app.route('/create/bitacora_botanica',methods=['POST'])
def create_bitacora_botanica():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Bitacora_botanica.validate_bitacora_botanica(request.form):
        return redirect('/new/bitacora_botanica')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "lugarobservado": request.form["lugarobservado"],
        "cultivo": request.form["cultivo"],
        "bibliografia": request.form["bibliografia"],
        "Familia": request.form["Familia"],
        "Variedad": request.form["Variedad"],
        "date_made": request.form["date_made"],
        "user_id": session["user_id"]
    }
    Bitacora_botanica.save(data)
    return redirect('/dashboard')

@app.route('/edit/bitacora_botanica/<int:id>')
def edit_bitacora_botanica(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_bitacora_botanica.html",edit=Bitacora_botanica.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/bitacora_botanica',methods=['POST'])
def update_bitacora_botanica():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Bitacora_botanica.validate_bitacora_botanica(request.form):
        return redirect('/new/bitacora_botanica')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "lugarobservado": request.form["lugarobservado"],
        "cultivo": request.form["cultivo"],
        "bibliografia": request.form["bibliografia"],
        "Familia": request.form["Familia"],
        "Variedad": request.form["Variedad"],
        "date_made": request.form["date_made"],
        "id": request.form['id']
    }
    Bitacora_botanica.update(data)
    return redirect('/dashboard')

@app.route('/bitacora_botanica/<int:id>')
def show_bitacora_botanica(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_bitacora_botanica.html", bitacora_botanica= Bitacora_botanica.get_one(data),user=User.get_by_id(user_data))

@app.route('/destroy/bitacora_botanica/<int:id>')



def destroy_bitacora_botanica(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Bitacora_botanica.destroy(data)
    return redirect('/dashboard')

#Paul prueba
@app.route('/search/bitacora_botanica/<int:id>')
def search(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("search.html", bitacora_botanica= Bitacora_botanica.get_one(data),user=User.get_by_id(user_data))
#Paul prueba




