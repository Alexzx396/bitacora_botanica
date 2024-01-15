document.getElementById('imagenes').addEventListener('change', function(event) {
    var imagePreview = document.getElementById('imagePreview');
    imagePreview.innerHTML = '';
    for (var i = 0; i < event.target.files.length; i++) {
        var file = event.target.files[i];
        var img = document.createElement('img');
        img.src = URL.createObjectURL(file);
        img.height = 100;  
        img.onload = function() {
            URL.revokeObjectURL(this.src);  
        };
        imagePreview.appendChild(img);
    }
});