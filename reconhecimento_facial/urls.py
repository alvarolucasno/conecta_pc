from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.reconhecimento_facial, name='reconhecimento_facial'),
]