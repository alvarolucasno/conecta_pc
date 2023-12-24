from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.listar_presos, name='listar_presos'),
    path('cadastrar_preso', views.cadastrar_preso, name='cadastrar_preso'),
    path('editar_preso/<int:preso_id>/', views.editar_preso, name='editar_preso'),
]