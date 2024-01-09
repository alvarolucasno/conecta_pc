from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email_funcional', 'nome_completo', 'cpf', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'nome_completo')
    fieldsets = (
        (None, {'fields': ('email_funcional', 'password')}),
        ('Informações Pessoais', {'fields': ('nome_completo', 'cpf')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 
                                   'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email_funcional', 'nome_completo', 'cpf', 'password1', 'password2', 
                       'is_active', 'is_staff')}
        ),
    )
    search_fields = ('email_funcional', 'nome_completo', 'cpf')
    ordering = ('email_funcional',)
    
    model = CustomUser
    verbose_name_plural = "Usuários"

admin.site.register(CustomUser, CustomUserAdmin)
