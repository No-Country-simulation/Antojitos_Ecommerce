from django.db import models

# Import Django's built-in AbstractUser to extend the User model
from django.contrib.auth.models import AbstractUser

# Import BaseUserManager to create a custom user manager
from django.contrib.auth.models import BaseUserManager

# Para generar Archivos Unicos como imagenes
import os
import uuid

from productos.models import Producto


# Create your models here.
class Categoria_Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    image = models.ImageField(upload_to='registro/categoria/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Esto se visualiza en el panel de admin
    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"

    def __str__(self):
        return self.nombre
    

def custom_upload_to_registro(instance, filename):
    """
        Genera un nombre de archivo único basado en un UUID.
    """
    nombre_base, extension = os.path.splitext(filename)
    unique_id = uuid.uuid4().hex
    return f"producto/{unique_id}{extension.lower()}"


# Custom manager for handling user creation
class CustomUserManager(BaseUserManager):
    
    # Method to create a regular user
    def create_user(self, email, password=None, **extra_fields):
        # Check if the email is provided
        if not email:
            raise ValueError('The Email field must be set')
        
        # Normalize the email by lowercasing the domain part
        email = self.normalize_email(email)
        
        # Create a user instance with the provided email and extra fields
        user = self.model(email=email, **extra_fields)
        
        # Set the user's password
        user.set_password(password)
        
        # Save the user to the database
        user.save(using=self._db)
        return user

    # Method to create a superuser (admin)
    def create_superuser(self, email, password=None, **extra_fields):
        # Set default fields for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Ensure is_staff is True for superusers
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        # Ensure is_superuser is True for superusers
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Create the superuser with the provided email and extra fields
        return self.create_user(email, password, **extra_fields)


# Custom User model extending AbstractUser
class CustomUser(AbstractUser):
    
    # Definir las 24 provincias como opciones
    PROVINCIAS_CHOICES = [
        ('BUENOS_AIRES', 'Buenos Aires'),
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
        ('CIUDAD_DE_BUENOS_AIRES', 'Ciudad Autónoma de Buenos Aires'),
    ]

    # Remove the username field from the default User model
    username = None  
    
    # Add a unique email field for authentication
    email = models.EmailField(unique=True)
    
    # Additional fields for user profile
    name = models.CharField(max_length=255, blank=True, null=True)
    cellphone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    stars = models.IntegerField(default=3)
    
    # Si se eliminase la categoría setea por defecto el valor de categoria 1
    category = models.ForeignKey(Categoria_Proveedor, on_delete=models.SET_DEFAULT, default=1,
                                 blank=True, null=True)
    
    # Relación Many-to-Many con el modelo Product
    products = models.ManyToManyField(Producto, related_name='users', blank=True, null=True)

    # Campo de provincia con opciones predefinidas
    province = models.CharField(max_length=50, choices=PROVINCIAS_CHOICES, blank=True, null=True)
    
    # Imagen unica del proveedor
    image = models.ImageField(upload_to=custom_upload_to_registro, null=True, blank=True)

    # Set email as the username field for authentication
    USERNAME_FIELD = "email"

    # Remove the requirement for additional fields when creating a superuser
    REQUIRED_FIELDS = []

    # Specify that this model should use the custom user manager
    objects = CustomUserManager()

    # String representation of the user, returning the email
    def __str__(self):
        return self.email