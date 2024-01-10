from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.listar_servidores, name='listar_servidores'),
    #path('cadastrar_preso', views.cadastrar_preso, name='cadastrar_preso'),
    path('detalhar_servidor/<int:servidor_id>/', views.detalhar_servidor, name='detalhar_servidor'),
]