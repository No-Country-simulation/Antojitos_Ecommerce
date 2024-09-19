function showForm(role) {
    // Ocultar ambos formularios
    document.getElementById('form-comprador').classList.remove('active');
    document.getElementById('form-vendedor').classList.remove('active');

    let tituloRegistro = document.getElementById('titulo-registro');
    let buttonContainer = document.getElementById('button-container');
    let backButton = document.getElementById('back-button');
    
    // Mostrar el formulario seleccionado y cambiar el título
    if (role === 'comprador') {
        document.getElementById('form-comprador').classList.add('active');
        tituloRegistro.textContent = "Registro de Cliente";
    } else if (role === 'vendedor') {
        document.getElementById('form-vendedor').classList.add('active');
        tituloRegistro.textContent = "Registro de Empresa";
    }
    
    // Ocultar el contenedor de botones y mostrar la flecha
    buttonContainer.style.display = 'none';
    backButton.style.display = 'inline-block';
}

function goBack() {
    let tituloRegistro = document.getElementById('titulo-registro');
    let buttonContainer = document.getElementById('button-container');
    let backButton = document.getElementById('back-button');
    
    // Restaurar el título original y mostrar el contenedor de botones
    tituloRegistro.textContent = "Registro de Usuarios";
    buttonContainer.style.display = 'block';
    
    // Ocultar la flecha y los formularios
    backButton.style.display = 'none';
    document.getElementById('form-comprador').classList.remove('active');
    document.getElementById('form-vendedor').classList.remove('active');
}

// se supone que esto deberia de funcionar a forzar a entrar a algun boton en los post
document.addEventListener('DOMContentLoaded', function() {
    // Recuperar el valor de 'form_user_type' desde el HTML
    const userTypeElement = document.getElementById('user-type');
    const formUserType = userTypeElement.getAttribute('data-form-user-type');

    if (formUserType === 'comprador') {
        showForm(formUserType);
    } else if (formUserType === 'vendedor') {
        showForm(formUserType);
    }
});