

# load_producto_data.py
import pandas as pd
from django.core.management.base import BaseCommand
from productos.models import Producto, Categoria


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
            categoria, _ = Categoria.objects.get_or_create(nombre=row['category'])

            # Verificar si el producto ya existe
            producto_existente = Producto.objects.filter(name=row['name']).first()

            if producto_existente:
                # Actualizar el precio
                producto_existente.price = row['price'] if pd.notna(row['price']
                                                                    ) else producto_existente.price
                # Actualizar el stock si hiciera falta
                producto_existente.stock = row['stock'] if pd.notna(row['stock']
                                                                    ) else producto_existente.stock

                # Guardar los cambios en la base de datos
                producto_existente.save()

                self.stdout.write(self.style.SUCCESS(f'Producto "{producto_existente.name}" actualizado.'))

            else:
                # Crear el nuevo producto
                producto = Producto.objects.create(
                    name=row['name'],
                    category=categoria,
                    price=row['price'] if pd.notna(row['price']) else None,
                    discount=row['discount'] if pd.notna(row['discount']) else 0,
                    stock=row['stock'] if pd.notna(row['stock']) else 1,
                )

                # mensaje para saber si se creo por consola
                self.stdout.write(self.style.SUCCESS(f'Producto "{producto.name}" creado.'))