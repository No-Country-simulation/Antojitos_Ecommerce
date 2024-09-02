

from .models import Categoria
from django.core.cache import cache
# ver configuracion de caches en settings

# agregar context_procesors en settings


def get_categories_dropmenu(request):
    """
    :param request:
    :return: context

    Notes:
        Nos devuelve un diccionario comppleto de cateogiras, para la barra dropdown en el head de
        la app
    """
    categories_all = cache.get('categories_all')

    if not categories_all:
        # Obtener todas las categorías para la nav-top-bar si no están en caché
        categories_all = Categoria.objects.all()

        # Almacenamos en caché este context processor para evitar llamadas repetitivas
        # Cache for 1 hour
        cache.set('categories_all', categories_all, timeout=60 * 60)

    # Retornar el diccionario dentro de otro diccionario con listas/arrays para el contexto
    return {'categories_all': categories_all}