campo = document.getElementById('buscarInput');
boton = document.getElementById('buscarBtn');

campo.addEventListener('input', function(evento){
    let contenido = evento.target.value;
    boton.setAttribute('href', `/search/bitacora_filter/${contenido}`);
});