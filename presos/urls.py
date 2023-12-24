from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.listar_presos, name='listar_presos'),
    path('cadastrar', views.cadastrar, name='cadastrar'),
]