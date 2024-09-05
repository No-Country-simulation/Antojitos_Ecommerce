

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate


from registros.forms import LoginForm
from registros.forms import BuyerRegistrationForm, SellerRegistrationForm


from django.http import JsonResponse

# This is for edit form
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash



# Create your views here.


def registro(request):
    """ 
        Este formulario es el registro de usuarios nuevos dentro del proyecto 
    """

    if request.method == 'POST':
        form = BuyerRegistrationForm(request.POST)
        if form.is_valid():
            # Guardar el usuario y encriptar la contraseña usando el método `save` del formulario.
            form.save()

            # Autenticar al usuario usando el email
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email=email, password=password)

            # Iniciar sesión del usuario
            if user is not None:
                login(request, user)

            # Redirigir a la página principal.
            return redirect('Home')

        else:
            print(request.POST)  # Esto imprimirá los datos enviados en la solicitud POST.
            print("\n\n")
            print(form.errors)  # Imprime los errores del formulario en la consola para depurar.

        form_submitted = True

    else:
        form = BuyerRegistrationForm()
        form_submitted = False

    context = {'form': form, 'form_submitted': form_submitted}

    return render(request, 'registros/registro.html', context)


@login_required
def profile_page(request):
    """ 
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # Guarda los cambios en el usuario

            # Actualizar la sesión del usuario para reflejar los cambios
            update_session_auth_hash(request, request.user) # Proteccion de la contraseña
            messages.success(request, '¡Perfil actualizado con éxito!')
            return redirect('Profile_Page')  # Redirige a la página de perfil o a donde prefieras
    else:
        form = EditUserForm(instance=request.user)
        
    context= , {'form': form}
    """

    return render(request, 'registros/profile_page.html')



def registro_widget(request):
    """
        Esta funcion se llama en widget_registro para confirmar que el usuario se logee

    Returns:
        redirecciones al Home en caso de logearse jejej
    """

    if request.method == 'POST':
        # Initialize the form with the POST data
        form = LoginForm(request.POST)

        # Validate the form data
        if form.is_valid():
            # Extract email and password from cleaned form data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authenticate the user with the provided email and password
            user = authenticate(request, email=email, password=password)

            # If authentication is successful then Log the user in
            if user is not None:
                login(request, user)

                # Check the user's role and redirect accordingly
                if user.role == 'buyer':
                    return redirect('Home')
                elif user.role == 'seller':
                    return redirect('Home')

            # If authentication is NOT successful
            else:
                form.add_error(None, 'Correo electrónico o contraseña incorrectos')

    # Para otros metodos que no sean Post, generalmente GET
    else:
        form = LoginForm()

    # For non-AJAX requests or GET requests, render the login form template
    return render(request, 'Home', {'form': LoginForm()})


def close_session(request):
    """
    Logs out the user and redirects them to the homepage or another page after logging out.

    This view handles the logout process by calling the `logout` function to end
    the user's session. After logging out, the user is redirected to the homepage
    or any other specified page.

    :param request: The HTTP request object used to process the logout request.
    :return: A redirect response to the homepage or another specified page after logout.
    """
    logout(request)
    return redirect('Home')