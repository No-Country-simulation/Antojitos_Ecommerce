from django.contrib import admin

# Register your models here.

# Pasos para agregar un show en Admin
# 1 - importar nuestro model producto
# 2 - crear una clase especial para dar mas funcionalidades de ser necesario

from productos.models import Producto


class ProductoAdmin(admin.ModelAdmin):
    
    # Establece estos campos solo como lectura
    readonly_fields = ('created', 'updated')

# Esto es para que se apliquen los cambios en nuestra vistas de admin
admin.site.register(Producto, ProductoAdmin)

