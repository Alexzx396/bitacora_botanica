function confirmDelete(id) {
    if(confirm("¿Seguro que quieres borrar esta Carta Especie")) {
        window.location.href = `/destroy/bitacora_botanica/${id}`;
    }
}