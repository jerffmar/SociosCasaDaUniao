from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser # Importe seu modelo CustomUser CORRETAMENTE

# Opcional: Crie uma classe Admin para personalizar a exibição do CustomUser
class CustomUserAdmin(UserAdmin):
    # Método para exibir o nome completo
    def get_nome_completo(self, obj):
        return obj.get_full_name() # Assumindo que CustomUser tem get_full_name()
    get_nome_completo.short_description = 'Nome Completo' # Define o cabeçalho da coluna

    # Método para exibir o valor legível do campo 'grau'
    def display_grau(self, obj):
        return obj.get_grau_display() # Chama o método get_grau_display() do modelo
    display_grau.short_description = 'Grau' # Nome da coluna no admin

    # Método para exibir o valor legível do campo 'equipe'
    def display_equipe(self, obj):
        return obj.get_equipe_display() # Chama o método get_equipe_display() do modelo
    display_equipe.short_description = 'Equipe' # Nome da coluna no admin

    # Método para exibir o valor legível do campo 'cargo'
    def display_cargo(self, obj):
        # Se cargo for ManyToManyField
        return ", ".join([cargo.nome for cargo in obj.cargos.all()]) if hasattr(obj, 'cargos') else '-'
        # Se cargo for CharField com choices
        # return obj.get_cargo_display()
    display_cargo.short_description = 'Cargo'

    # Adicione 'telefone' e 'cpf' aos campos exibidos na lista de usuários
    list_display = ('telefone', 'email', 'get_nome_completo', 'display_grau', 'display_equipe', 'display_cargo', 'is_staff', 'is_active',) # Adicionado 'display_cargo'
    # Adicione 'telefone' e 'cpf' aos campos de busca
    search_fields = ('telefone', 'email', 'first_name', 'last_name', 'cpf',)
    # Adicione 'telefone' e 'cpf' aos campos de filtro
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'equipe', 'grau',) # 'cargo' foi removido temporariamente
    
    # Se você adicionou campos customizados ao seu CustomUser que não estão no UserAdmin padrão,
    # você precisará adicioná-los aos fieldsets para que apareçam no formulário de edição.
    # Copie os fieldsets do UserAdmin e adicione seus campos.
    # Exemplo básico, você precisará ajustar conforme os campos do seu CustomUser:
    fieldsets = (
        (None, {'fields': ('telefone', 'password')}), # 'telefone' é o seu USERNAME_FIELD
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email', 'data_nascimento', 'cpf', 'genero', 'profile_picture')}), # Adicionado 'profile_picture'
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
        ('Informações Adicionais', {'fields': ('equipe', 'grau', 'cargos')}), # Alterado 'cargo' para 'cargos'
    )
    # Se 'telefone' é seu USERNAME_FIELD, ele já deve estar no primeiro fieldset.
    # Se você tem um campo 'username' tradicional e 'telefone' é um campo adicional, ajuste.
    # No seu caso, 'telefone' é o USERNAME_FIELD.

    # Para campos many-to-many como 'cargo', se for um ManyToManyField:
    # filter_horizontal = ('groups', 'user_permissions', 'cargo') # Exemplo se 'cargo' for M2M

    # Se 'cargo' for um CharField com choices ou ForeignKey, ele já deve aparecer nos fieldsets acima.

# Registre seu CustomUser com a classe Admin personalizada (ou sem ela para o padrão)
admin.site.register(CustomUser, CustomUserAdmin)

# Se você não quiser personalizar a exibição no admin inicialmente,
# você pode simplesmente fazer:
# admin.site.register(CustomUser)
# Mas usar UserAdmin (ou uma subclasse) é recomendado para modelos de usuário.
