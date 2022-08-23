from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.bitacora_botanica import Bitacora_botanica
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')



#CREAR.........
@app.route('/registro')
def registro():
    return render_template('registro.html')


@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/registro')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')



#INICIAR SESION
@app.route('/login')
def iniciar_sesion():
    return render_template('login.html')


@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Email incorrecto","login")
        return redirect('/login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Contraseña incorrecta","login")
        return redirect('/login')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html",user=User.get_by_id(data),bitacora_botanica=Bitacora_botanica.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



