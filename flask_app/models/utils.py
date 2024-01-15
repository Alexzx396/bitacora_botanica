
def allowed_file(filename):
    # Verificar si la extensión del archivo está permitida
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions