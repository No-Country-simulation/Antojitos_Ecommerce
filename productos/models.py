from django.db import models

# PAra trabajar con zonas horarias
from django.utils import timezone
from datetime import timedelta

# Para generar Archivos Unicos como imagenes
import os
import uuid


# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    image = models.ImageField(upload_to='producto/categoria/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Esto se visualiza en el panel de admin
    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"

    def __str__(self):
        return self.nombre


def custom_upload_to_producto(instance, filename):
    """
        Genera un nombre de archivo único basado en un UUID.
    """
    nombre_base, extension = os.path.splitext(filename)
    unique_id = uuid.uuid4().hex
    return f"producto/{unique_id}{extension.lower()}"


class Producto(models.Model):
    name = models.CharField(max_length=200)

    # Si se eliminase la categoría setea por defecto el valor de categoria 1
    category = models.ForeignKey(Categoria, on_delete=models.SET_DEFAULT, default=1)
    
    # Sub-Category del producto ? ver si es necesario
    # sub_category = models.ManyToManyField(Subcategoria, blank=True, related_name='productos')
    
    # Descripcion del producto como campo de texto, ya que no sabemos su extension
    description = models.TextField(null=True, blank=True)
    
    # Imagen principal del producto, por ahora será unica
    # imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    image = models.ImageField(upload_to=custom_upload_to_producto, null=True, blank=True)
    
    price = models.FloatField()
    discount = models.IntegerField(null=True, blank=True)
    # Eventualmente se calculara y mostrara para cada producto
    # precio_descuento = precio - descuento
    
    stock = models.IntegerField(default=1)
    available = models.BooleanField(default=True)
    
    # Para crear las fechas en general de cuando se crea y/o actualiza
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        # Esto se visualiza en el panel de admin
        return self.nombre


    class Meta:
        # Esto se visualiza en el panel de admin
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        

