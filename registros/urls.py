

from django.urls import path
from registros import views


urlpatterns = [
    # path('registro/', views.VRegistro.as_view(), name="Registro"),
    
    path('registro/', views.registro, name="Register"),
    path('registro/widget_registro/', views.registro_widget, name="Widget_Register"),
    path('registtro/close_session', views.close_session, name="Close_Session"),

    # Profile Page User
    path('profile/', views.profile_page, name="Profile_Page"),
    
]