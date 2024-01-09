from django.contrib import admin
from .models import Servidor

class ServidorAdmin(admin.ModelAdmin):
    model = Servidor
    list_display = ('email_funcional', 'nome_completo', 'cpf')
    search_fields = ('email_funcional', 'nome_completo', 'cpf')
    ordering = ('email_funcional',)

    # Adicione esta linha para excluir campos específicos
    exclude = ('avatar', 'updated_by')

admin.site.register(Servidor, ServidorAdmin)
