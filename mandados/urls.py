from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.listar_alvos, name='listar_alvos'),
    path('editar/<int:id_pessoa>/', views.editar_alvo, name='editar_alvo'),
]