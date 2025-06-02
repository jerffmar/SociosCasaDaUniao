from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

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

    # Define o email como o campo principal de autenticação [4]
    USERNAME_FIELD = 'email'
    # Mantém o campo username como obrigatório durante a criação de superusuário [4]
    REQUIRED_FIELDS = ['username']
    # Garante que o email seja único [4]
    email = models.EmailField(_('email address'), unique=True) # Tornar email único se ainda não for

    # Adiciona campos customizados baseados na idealização do frontend [3]
    # Campo para o telefone do sócio
    telefone = models.CharField(_('phone number'), max_length=15, blank=True, null=True)
    # Campo para o gênero do sócio, usando as opções definidas em CHAR_CHOICES
    genero = models.CharField("Gênero", max_length=1, choices=CHAR_CHOICES, blank=True, null=True)
    # Campo para a data de nascimento do sócio
    data_nascimento = models.DateField(_('birth date'), blank=True, null=True)
    # Campo para o CPF do sócio
    cpf = models.CharField(
        _('CPF'),
        max_length=14,
        unique=True,
        null=False,  # Alterado para True
        blank=False, # Adicionado/Alterado para True para consistência inicial
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

    class Meta:
        # Define nomes mais amigáveis para o modelo no painel administrativo
        verbose_name = "Sócio"
        verbose_name_plural = "Sócios"

    def __str__(self):
        # Define a representação em string do objeto CustomUser
        # Retorna o email, ou o username se o email não estiver definido (improvável com unique=True)
        return self.email or self.username

    # Método auxiliar para verificar se o usuário possui privilégios administrativos
    def has_administrative_privileges(self):
        """Verifica se o usuário possui algum cargo administrativo."""
        # Lista de cargos considerados administrativos conforme a idealização [3]
        admin_roles = ["Mestre Representante", "Mestre-Assistente", "Presidente"]
        # Verifica se algum dos cargos do usuário está na lista de cargos administrativos
        return self.cargos.filter(nome__in=admin_roles).exists()