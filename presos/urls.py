from django.urls import path, include
from . import views

urlpatterns = [
    #path('', views.listar_alvos, name='listar_alvos'),
    path('cadastrar', views.cadastrar, name='cadastrar'),
]