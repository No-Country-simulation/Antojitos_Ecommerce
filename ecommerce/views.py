

from django.shortcuts import render
from registros.models import SellerUser


# Create your views here.
def home(request):
    
    # Obtener todos los vendedores
    vendedores = SellerUser.objects.all()
    
    context = {'vendedores': vendedores}

    
    return render(request, "ecommerce/home.html", context)