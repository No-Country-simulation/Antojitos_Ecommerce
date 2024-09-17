from django.db import models

# PAra trabajar con zonas horarias
from django.utils import timezone
from datetime import timedelta

# Para generar Archivos Unicos como imagenes
import os
import uuid
from registros.models import SellerUser
# Create your models here.


def custom_upload_to_producto(instance, filename):
    """
        Genera un nombre de archivo único basado en un UUID.
    """
    nombre_base, extension = os.path.splitext(filename)
    unique_id = uuid.uuid4().hex
    return f"producto/{unique_id}{extension.lower()}"


# Modelo de la Categoría
class Categoria(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='producto/categoria/', null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Esto se visualiza en el panel de admin
    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"

    def __str__(self):
        return self.name
    
    
# Modelo de Subcategoria, con relación a la Categoría
class Subcategoria(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="subcategorias")
    image_url = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Subcategoría de Producto"
        verbose_name_plural = "Subcategorías de Productos"

    def __str__(self):
        return f"{self.name} (Categoría: {self.category.name})"


class Producto(models.Model):
    name = models.CharField(max_length=200)

    # Relación con la categoría
    category = models.ForeignKey(Categoria, on_delete=models.SET_DEFAULT, default=1)
    
    # Relación con la subcategoría (opcional)
    sub_category = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    
    # Descripcion del producto como campo de texto, ya que no sabemos su extension
    description = models.TextField(null=True, blank=True)
    
    # Imagen principal del producto, por ahora será unica
    image = models.ImageField(upload_to=custom_upload_to_producto, null=True, blank=True)
    
    # Por ahora solucion viable carga por pinterest
    image_url = models.TextField(null=True, blank=True, 
                                 default="https://i.pinimg.com/736x/32/fd/c3/32fdc305ad5fc48a75e527d0040e51d0.jpg")
    
    price = models.FloatField()
    discount = models.IntegerField(null=True, blank=True)
    # Eventualmente se calculara y mostrara para cada producto
    # precio_descuento = precio - descuento
    
    stock = models.IntegerField(default=1)
    available = models.BooleanField(default=True)
    
    # Relación con el vendedor
    seller = models.ForeignKey(SellerUser, on_delete=models.CASCADE, 
                               related_name='products', null=True, blank=True)

    # Para crear las fechas en general de cuando se crea y/o actualiza
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        # Esto se visualiza en el panel de admin
        return self.name

    class Meta:
        # Esto se visualiza en el panel de admin
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        
        
