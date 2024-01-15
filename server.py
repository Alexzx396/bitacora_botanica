# Importa la instancia de la aplicación Flask desde flask_app
from flask_app import app

# Importa los controladores (rutas) que deseas utilizar
from flask_app.controllers import bitacora_botanicas, users

# Verifica si este archivo se ejecuta directamente
if __name__ == "__main__":
    # Ejecuta la aplicación Flask en modo debug
    app.run(debug=True)