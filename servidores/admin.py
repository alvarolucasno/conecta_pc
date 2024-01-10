from django.contrib import admin
from .models import Servidor, Cargo

class ServidorAdmin(admin.ModelAdmin):
    model = Servidor
    list_display = ('email_funcional', 'nome_completo', 'cpf')
    search_fields = ('email_funcional', 'nome_completo', 'cpf')
    ordering = ('email_funcional',)
    exclude = ('avatar', 'updated_by')

admin.site.register(Servidor, ServidorAdmin)

admin.site.register(Cargo)
