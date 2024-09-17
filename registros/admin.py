from django.contrib import admin

from registros.models import SellerUser



# Register your models here.
class SellerUserAdmin(admin.ModelAdmin):
    pass
    # establece estos campos solo como lectura
    # readonly_fields = ('created', 'updated')
    
    
admin.site.register(SellerUser, SellerUserAdmin)