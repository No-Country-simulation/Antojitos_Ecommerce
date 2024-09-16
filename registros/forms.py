

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation

from registros.models import CustomUser, BuyerUser, SellerUser, Categoria_Proveedor

# Definir los roles como opciones
ROLE_CHOICES = [
    ('buyer', 'Comprador'),
    ('seller', 'Vendedor'),
]

# Definir las 24 provincias como opciones
PROVINCIAS_CHOICES = [
    ('SELECCIONAR', 'Seleccionar Provincia'),
    ('BUENOS_AIRES', 'Buenos Aires'),
    ('CABA', 'CABA'),
    ('CATAMARCA', 'Catamarca'),
    ('CHACO', 'Chaco'),
    ('CHUBUT', 'Chubut'),
    ('CORDOBA', 'Córdoba'),
    ('CORRIENTES', 'Corrientes'),
    ('ENTRE_RIOS', 'Entre Ríos'),
    ('FORMOSA', 'Formosa'),
    ('JUJUY', 'Jujuy'),
    ('LA_PAMPA', 'La Pampa'),
    ('LA_RIOJA', 'La Rioja'),
    ('MENDOZA', 'Mendoza'),
    ('MISIONES', 'Misiones'),
    ('NEUQUEN', 'Neuquén'),
    ('RIO_NEGRO', 'Río Negro'),
    ('SALTA', 'Salta'),
    ('SAN_JUAN', 'San Juan'),
    ('SAN_LUIS', 'San Luis'),
    ('SANTA_CRUZ', 'Santa Cruz'),
    ('SANTA_FE', 'Santa Fe'),
    ('SANTIAGO_DEL_ESTERO', 'Santiago del Estero'),
    ('TIERRA_DEL_FUEGO', 'Tierra del Fuego'),
    ('TUCUMAN', 'Tucumán'),
]


class LoginForm(forms.Form):
    """
        Este es el formulario para logearse con una cuenta ya creada en el widget_registro
        
        Además se utiliza en la funcion de views.py " "
    """
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico', 'required': True}),
        error_messages={'invalid': 'La dirección de correo electrónico no es válida.'}
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'required': True}),
    )
    
    
class BuyerRegistrationForm(UserCreationForm):
    """
        Esto es parte del formulario para registrarse con una nueva cuenta en la hoja "Registro"
        
        Para el caso de los compradores
    """
    # le damos algunos formatos posibles
    email = forms.CharField(max_length=50, error_messages={
        'invalid': 'Ingrese una dirección de correo electrónico válida.'
    })
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    # Campo opcionales
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    cellphone = forms.CharField(max_length=25, required=False)
    province = forms.ChoiceField(choices=PROVINCIAS_CHOICES, required=False)  
    address = forms.CharField(max_length=250, required=False)  
    
    class Meta:
        # declaramos nuestro .models CustomUser y le pasamos los campos a completar que recuperamos
        model = BuyerUser
        # model = CustomUser
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'cellphone', 
                  'province', 'address')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # les asignamos un tipo de clase a todos nuestros widgets p/ trabajar con css
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # Asigna el rol de "buyer" directamente aquí
        user.role = 'buyer'
        if commit:
            user.save()
        return user

    def clean_password1(self):
        # Metodo necesario para poder eliminar la validacion doble del password2
        password1 = self.cleaned_data.get('password1')
        if password1:
            try:
                password_validation.validate_password(password1, self.instance)
            except forms.ValidationError as error:
                self.add_error('password1', error)
        return password1

    def clean_email(self):
        # metodo necesario para poder autenticar el email
        email = self.cleaned_data.get('email')
        # if CustomUser.objects.filter(email=email).exists():
        
        # Verificar si ya existe un usuario con el mismo correo electrónico en la base de datos,
        # excluyendo el usuario actual si se está editando (es decir, si 'self.instance.id' no es None).
        # La función 'exclude(id=self.instance.id)' asegura que si estamos editando un usuario existente,
        # no se considere el usuario que estamos editando en la búsqueda de correos electrónicos duplicados.
        if CustomUser.objects.filter(email=email).exclude(id=self.instance.id).exists():
            # Si se encuentra un usuario con el mismo correo electrónico (y no es el mismo usuario que se está editando),
            # se lanza una excepción de validación para indicar que el correo electrónico ya está en uso.
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email

class SellerRegistrationForm(UserCreationForm):
    """
        Esto es parte del formulario para registrarse con una nueva cuenta en la hoja "Registro"
        
        Para el caso de los Vendedores
    """
    # le damos algunos formatos posibles
    email = forms.CharField(max_length=50, error_messages={
        'invalid': 'Ingrese una dirección de correo electrónico válida.'
    })
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    name_store = forms.CharField(max_length=250, required=True)
    cellphone = forms.CharField(max_length=25, required=False)
    province = forms.ChoiceField(choices=PROVINCIAS_CHOICES, required=False)  # Campo opcional
    address = forms.CharField(max_length=250, required=False)  # Campo opcional
    
    # Campo para seleccionar la categoría del proveedor
    category = forms.ModelChoiceField(
        queryset=Categoria_Proveedor.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione una categoría"
    )
    
    class Meta:
        # declaramos nuestro .models CustomUser y le pasamos los campos a completar que recuperamos
        model = SellerUser
        fields = ('email', 'password1', 'password2', 'name_store', 'cellphone', 
                  'province', 'address', 'category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # les asignamos un tipo de clase a todos nuestros widgets p/ trabajar con css
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # Asigna el rol de "buyer" directamente aquí
        user.role = 'seller'
        
        # Asigna la categoría seleccionada
        user.category = self.cleaned_data.get('category')
        
        if commit:
            user.save()
        return user

    def clean_password1(self):
        # Metodo necesario para poder eliminar la validacion doble del password2
        password1 = self.cleaned_data.get('password1')
        if password1:
            try:
                password_validation.validate_password(password1, self.instance)
            except forms.ValidationError as error:
                self.add_error('password1', error)
        return password1

    def clean_email(self):
        # metodo necesario para poder autenticar el email
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email
    