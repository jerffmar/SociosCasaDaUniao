import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

def user_profile_pic_path(instance, filename):
    """
    Gera o caminho para a foto de perfil do usuário.
    Salva como: profile_pics/12345678900.png
    Onde 12345678900 é o CPF limpo do usuário.
    Nota: Esta função apenas define o nome do arquivo com a extensão .png.
    Não converte o formato do arquivo. Se um JPEG for carregado, será salvo
    como <cpf>.png, mas o conteúdo ainda será JPEG.
    Para conversão real, seria necessário processamento adicional.
    """
    # Limpa o CPF para usar no nome do arquivo
    # Garante que instance.cpf existe e não é None, e remove não dígitos
    cpf_cleaned = ''.join(filter(str.isdigit, str(instance.cpf))) if instance.cpf else 'unknown_cpf'
    
    # Define a extensão como .png, conforme solicitado
    ext = 'png' 
    
    new_filename = f"{cpf_cleaned}.{ext}"
    
    return os.path.join('profile_pics', new_filename)

# Opções para o campo Gênero
CHAR_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Feminino'),
]

# Opções para o campo Equipe
EQUIPE_CHOICES = [
    ('N', 'Nenhum'),
    ('A', 'Amarela'),
    ('V', 'Verde'),
]

# Opções para o campo Grau
GRAU_CHOICES = [
    ('N', 'Nenhum'),
    ('S', 'Sócio'),
    ('CI', 'Corpo Instrutivo'),
    ('C', 'Conselho'),
    ('M', 'Mestre'),
]

# Modelo para representar os cargos dentro da UDV
class Cargo(models.Model):
    """Representa um cargo ou função dentro da estrutura da UDV."""
    # Nome do cargo (ex: Mestre Representante, Mestre Assistente, Presidente)
    nome = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

    def __str__(self):
        # Representação em string do objeto Cargo será seu nome
        return self.nome

# Modelo de usuário customizado herdando de AbstractUser
class CustomUser(AbstractUser):
    """Modelo de usuário customizado para a plataforma de gestão da UDV."""
    # AbstractUser já fornece campos como username, first_name, last_name,
    # email, password, is_staff, is_active, date_joined, etc.

    # Define o telefone como o campo principal de autenticação
    USERNAME_FIELD = 'telefone'
    # Campos obrigatórios ao criar um superusuário via createsuperuser.
    # 'username' (de AbstractUser) e 'email' ainda são úteis.
    REQUIRED_FIELDS = ['username', 'email']
    
    # Garante que o email seja único e obrigatório
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)

    # Adiciona campos customizados baseados na idealização do frontend [3]
    # Campo para o telefone do sócio - agora é o USERNAME_FIELD
    telefone = models.CharField(
        _('phone number'), 
        max_length=15, 
        unique=True, # Telefone deve ser único para ser USERNAME_FIELD
        blank=False, # Não pode ser branco
        null=False   # Não pode ser nulo
    )
    # Campo para o gênero do sócio, usando as opções definidas em CHAR_CHOICES
    genero = models.CharField("Gênero", max_length=1, choices=CHAR_CHOICES, blank=True, null=True)
    # Campo para a data de nascimento do sócio
    data_nascimento = models.DateField(_('birth date'), blank=True, null=True)
    # Campo para o CPF do sócio
    cpf = models.CharField(
        _('CPF'),
        max_length=14,
        unique=True,
        null=False, 
        blank=False, 
        help_text=_('Formato: 000.000.000-00')
    )

    # Relacionamento ManyToMany para permitir que um sócio tenha múltiplos cargos [3]
    cargos = models.ManyToManyField(Cargo, verbose_name="Cargos", blank=True)

    # Campo para a equipe do sócio, usando as opções definidas em EQUIPE_CHOICES
    equipe = models.CharField("Equipe", max_length=1, choices=EQUIPE_CHOICES, default='N')

    # Campo para o grau do sócio, usando as opções definidas em GRAU_CHOICES
    grau = models.CharField("Grau", max_length=2, choices=GRAU_CHOICES, default='N')

    # Adicionar related_name para evitar conflitos com o User model padrão
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_set", # Nome alterado
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_set", # Nome alterado
        related_query_name="user",
    )

    # Adicionando campo para foto de perfil
    profile_picture = models.ImageField(
        _('profile picture'),
        upload_to=user_profile_pic_path,  # Função customizada para o caminho
        null=True,
        blank=True
    )

    class Meta:
        # Define nomes mais amigáveis para o modelo no painel administrativo
        verbose_name = "Sócio"
        verbose_name_plural = "Sócios"

    def __str__(self):
        # Define a representação em string do objeto CustomUser
        # Retorna o nome completo em vez do telefone
        return f"{self.first_name} {self.last_name}"

    # Método auxiliar para verificar se o usuário possui privilégios administrativos
    def has_administrative_privileges(self):
        """Verifica se o usuário possui algum cargo administrativo."""
        # Lista de cargos considerados administrativos conforme a idealização [3]
        admin_roles = ["Mestre Representante", "Mestre-Assistente", "Presidente"]
        # Verifica se algum dos cargos do usuário está na lista de cargos administrativos
        return self.cargos.filter(nome__in=admin_roles).exists()

    # Sobrescrever o método save para deletar a foto antiga se uma nova for carregada
    # ou se a foto for limpa.
    def save(self, *args, **kwargs):
        try:
            this = CustomUser.objects.get(id=self.id)
            if this.profile_picture != self.profile_picture:
                if this.profile_picture: # Verifica se a foto antiga existe
                    if os.path.isfile(this.profile_picture.path):
                        os.remove(this.profile_picture.path)
        except CustomUser.DoesNotExist: 
            pass # Objeto é novo, não há foto antiga
        except ValueError:
            pass # Pode ocorrer se o campo de imagem estiver vazio e .path for acessado

        super(CustomUser, self).save(*args, **kwargs)