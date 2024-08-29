

from django.core.management.base import BaseCommand
from productos.models import Categoria

# No es necesario agregar este comando a ningun lado
# Por el momento solo hay que poner en nuestra terminal
# python manage.py load_data


class Command(BaseCommand):
    help = 'Cargar categorías, subcategorías y marcas desde un diccionario'

    def handle(self, *args, **options):
        # Datos para cargar
        list_categories = [
            # Periféricos
            "Comida", "Bebida", "Frutas",

            # Discos SSD
            "Verduras", "Panificados"
        ]
        
        # Cargar categorías
        for i in list_categories:
            categoria, created = Categoria.objects.get_or_create(nombre=i)
        
            if created:
                self.stdout.write(self.style.SUCCESS(f'Categoría "{i}" creada.'))
            else:    
                self.stdout.write(self.style.SUCCESS(f'Categoría "{i}" ya estaba creada.'))

