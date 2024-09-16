

import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from registros.models import BuyerUser, SellerUser

# No es necesario agregar este comando a ningun lado
# Por el momento solo hay que poner en nuestra terminal
# python manage.py load_data


class Command(BaseCommand):
    help = 'Carga usuarios desde un archivo Excel'

    def handle(self, *args, **kwargs):
        # Ruta al archivo Excel
        file_path = 'registros/data/usuarios_compradores.xlsx'
        df = pd.read_excel(file_path)

        for index, row in df.iterrows():
            # Recupero los datos de las columnas
            email = row['email']
            password1 = str(row['password1'])
            password2 = str(row['password2'])
            first_name = row['first_name']
            last_name = row['last_name']
            cellphone = row['cellphone']
            province = row['province']
            address = row['address']
            role = row['role']
            
            # Verificar si el usuario ya existe
            user_existente = BuyerUser.objects.filter(email=email).first()

            # Actualizar campos del usuario existente
            if user_existente:
                if password1 and password2 and password1 == password2:
                    user_existente.password = make_password(password1)
                user_existente.first_name = first_name if pd.notna(first_name) else user_existente.first_name
                user_existente.last_name = last_name if pd.notna(last_name) else user_existente.last_name
                user_existente.cellphone = cellphone if pd.notna(cellphone) else user_existente.cellphone
                user_existente.province = province if pd.notna(province) else user_existente.province
                user_existente.address = address if pd.notna(address) else user_existente.address
                user_existente.role = role if pd.notna(role) else user_existente.role

                # Guardar los cambios en la base de datos
                user_existente.save()

                self.stdout.write(self.style.SUCCESS(f'Usuario "{user_existente.email}" actualizado.'))
            
            # Crear un nuevo usuario - Si no existe
            else:
                
                if password1 and password2 and password1 == password2:
                    password = make_password(password1)
                # Establecer una contraseña por defecto si no se proporciona
                else:
                    password = None  
                
                user = BuyerUser.objects.create(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    cellphone=cellphone,
                    province=province,
                    address=address,
                    role=role,
                )

                self.stdout.write(self.style.SUCCESS(f'Usuario "{user.email}" creado.'))
                
                
    def get_user_by_email(self, email):
        user = BuyerUser.objects.filter(email=email).first()
        if user is None:
            user = SellerUser.objects.filter(email=email).first()
        return user
