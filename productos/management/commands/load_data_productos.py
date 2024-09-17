

# load_producto_data.py
import pandas as pd
from django.core.management.base import BaseCommand
from productos.models import Producto, Categoria, Subcategoria
from registros.models import SellerUser


"""
    path/to/poject>   .\venv\Scripts\Activate.ps1
    Only you can use this with 
    pandas      - pip install pandas
    openpyxl    - pip install openpyxl
"""


class Command(BaseCommand):
    help = 'Carga productos desde un archivo Excel'

    def handle(self, *args, **kwargs):
        # Cargar el archivo Excel
        file_path = 'productos/data/info_productos.xlsx'
        df = pd.read_excel(file_path)

        # itera por las filas a razon de una linea por vuelta de ciclo
        for index, row in df.iterrows():
            
            # Obtener o crear la categoría
            categoria, _ = Categoria.objects.get_or_create(name=row['category'])

            # Obtener o crear la subcategoría (si existe en el Excel)
            subcategoria = None
            if pd.notna(row['sub_category']):
                subcategoria, _ = Subcategoria.objects.get_or_create(
                    name=row['sub_category'],
                    category=categoria  # Relacionar la subcategoría con la categoría correspondiente
                )
            
            # Verificar si el producto ya existe para el vendedor
            seller = SellerUser.objects.filter(id=row['seller_id']).first()

            if seller:
                # Filtrar por nombre del producto y vendedor
                prod_exist = Producto.objects.filter(name=row['name'], seller=seller).first()
                
            else:
                self.stdout.write(self.style.ERROR(f'No se encontró el vendedor con ID {row["seller_id"]}'))
                continue

            if prod_exist:
                # Actualizar campos si el producto ya existiera
                prod_exist.price = row['price'] if pd.notna(row['price']) else prod_exist.price
                prod_exist.stock = row['stock'] if pd.notna(row['stock']) else prod_exist.stock
                prod_exist.image = row['image'] if pd.notna(row['image']) else prod_exist.image
                prod_exist.image_url = row['image_url'] if pd.notna(row['image_url']) else prod_exist.image_url
                
                prod_exist.category = categoria
                prod_exist.seller = seller
                
                # Si hay una subcategoría en el archivo, actualizarla
                if subcategoria:
                    prod_exist.sub_category = subcategoria
                      
                # Guardar los cambios en la base de datos
                prod_exist.save()

                self.stdout.write(self.style.SUCCESS(f'Producto "{prod_exist.name}" actualizado.'))

            else:
                # Crear el nuevo producto
                producto = Producto.objects.create(
                    name=row['name'],
                    category=categoria,
                    seller=seller,
                    sub_category=subcategoria,
                    price=row['price'] if pd.notna(row['price']) else None,
                    discount=row['discount'] if pd.notna(row['discount']) else 0,
                    stock=row['stock'] if pd.notna(row['stock']) else 1,
                    image_url=row['image_url'] if pd.notna(row['image_url']) else None, # con None usa el valor por defecto
                ) 

                # mensaje para saber si se creo por consola
                self.stdout.write(self.style.SUCCESS(f'Producto "{producto.name}" creado.'))