from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

import os
import uuid
from productos.models import Producto


# Define una categoría para los proveedores
class Categoria_Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    image = models.ImageField(upload_to='registro/categoria/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"

    def __str__(self):
        return self.nombre


# Función para generar un nombre de archivo único basado en un UUID
def custom_upload_to_registro(instance, filename):
    nombre_base, extension = os.path.splitext(filename)
    unique_id = uuid.uuid4().hex
    return f"registro/{unique_id}{extension.lower()}"


# Gestor personalizado para manejar la creación de usuarios
class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractUser):
    """
        Modelo para generar un nuevo usuario autenticado con distintos roles, este modelo
        "CustomUser" de momento lo voy a utilizar como una base clase padre para los dos roles
    """
    
    # Elimina el campo de nombre de usuario del modelo de usuario por defecto
    username = None  
    
    # Agrega un campo de correo electrónico único para la autenticación
    email = models.EmailField(unique=True)
    
    # Campo para definir el rol del usuario
    role = models.CharField(max_length=10, default='buyer')
    
    # Campos adicionales para el perfil del usuario
    # Numero de celular tanto para el comprador como vendedor
    cellphone = models.CharField(max_length=20, blank=True, null=True)
    
    # direccion para ambos
    address = models.CharField(max_length=255, blank=True, null=True)

    # Campo de provincia con opciones predefinidas
    province = models.CharField(max_length=50, blank=True, null=True)

    # Imagen perfil del proveedor/comprador
    image = models.ImageField(upload_to=custom_upload_to_registro, null=True, blank=True,
                              default="registro/profile_def.jpg")
    
    # Imagen banner del proveedor/comprador si necesitara
    banner_image = models.ImageField(upload_to=custom_upload_to_registro, null=True, blank=True,
                                     default="registro/banner_def.jpg")
    
    # Define el campo email como el nombre de usuario para la autenticación
    USERNAME_FIELD = "email"

    # No se requieren campos adicionales al crear un superusuario
    REQUIRED_FIELDS = []
    
    # Usa el gestor personalizado para este modelo, y lo heredaran sus clases
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    
    
# Modelo de usuario personalizado que extiende CustomUser
# Para definir nuestro usuario vendedor
class SellerUser(CustomUser):
    
    # Para definir su propio nombre de Comercio
    name_store = models.CharField(max_length=255, blank=True, null=True, default="Nombre Empresa")
    
    # Cantida de estrellas para el local
    stars = models.IntegerField(default=3)
    
    # Relación con una categoría de proveedor
    category = models.ForeignKey(
        Categoria_Proveedor, 
        on_delete=models.SET_DEFAULT,
        default=1,
        blank=True, 
        null=True
    )
    
    # Relación Many-to-Many con el modelo Producto
    products = models.ManyToManyField(Producto, related_name='sellers', blank=True)
    
    # Representación del objeto como una cadena, devuelve el correo electrónico
    def __str__(self):
        return self.email
    
    # Esto es para asegurarse de que se guarde correctamente el rol que estamos utilizando
    def save(self, *args, **kwargs):
        self.role = 'seller'
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"


# Para definir nuestro usuario comprador
class BuyerUser(CustomUser):
    
    # Los campos first_name y last_name están disponibles por defecto y son opcionales
    # =================================================================================
    # first_name = Nombre del comprador
    # last_name = Apellido del usuario
    # =================================================================================
    # Estos campos son heredados por defecto como blank=True y null=True a los campos heredados
    # ya que son opcionales por defecto
    
    # para productos que el usuario guarda como favoritos
    saved_products = models.ManyToManyField(Producto, related_name='buyers', blank=True)
    
    # Eventualmente se hara un apartado de pedidos/facturas cuando se cree la clase
    # pedidos
    
    # Representación del objeto como una cadena, devuelve el correo electrónico
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Comprador"
        verbose_name_plural = "Compradores"
        
        
"""
    El siguiente bloque de código se utiliza para definir las relaciones Many-to-Many 
    del modelo SellerUser con los modelos Group y Permission de Django. Estas relaciones 
    son esenciales para manejar el sistema de permisos y grupos de usuarios, especialmente 
    cuando creas un modelo de usuario personalizado basado en AbstractUser.
        
    Explicacion:
        ManyToManyField: Indica una relación de muchos a muchos entre el modelo SellerUser 
        y el modelo Group (definido en auth.Group). Esto significa que un usuario puede 
        pertenecer a varios grupos, y un grupo puede tener varios usuarios.

        related_name='selleruser_set': Este argumento define el nombre que se usará para 
        acceder a los SellerUser asociados desde un objeto Group. Por defecto, Django 
        utiliza el nombre del modelo en minúsculas seguido de _set (e.g., user_set para 
        el modelo User). Dado que ya existe una relación similar en el modelo User de Django, 
        es necesario definir un related_name personalizado para evitar conflictos de nombres.
    
    
    # Esto debe ser agregado para evitar conflictos con la base de datos ya creada ?
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='selleruser_set',  # Añadido related_name para evitar el conflicto
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=('groups'),
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='selleruser_set',  # Añadido related_name para evitar el conflicto
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )
    """