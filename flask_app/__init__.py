from flask import Flask, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'flask_app/static/uploads'
app.secret_key = 'hadoken'

# Crear la carpeta de subidas si no existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/uploads/<filename>')
def uploads(filename):
    print("Solicited file:", filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

