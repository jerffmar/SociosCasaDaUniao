from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import CustomUser # Certifique-se que CustomUser está importado
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model # Se já não estiver importado
import re # Para limpar o número de telefone
import random
import string
from django.contrib.auth import authenticate


CustomUser = get_user_model()

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    while True:
        password_list = []
        # Pelo menos uma minúscula
        password_list.append(random.choice(string.ascii_lowercase))
        # Pelo menos uma maiúscula
        password_list.append(random.choice(string.ascii_uppercase))
        # Pelo menos um dígito
        password_list.append(random.choice(string.digits))
        
        remaining_length = length - len(password_list)
        if remaining_length > 0:
            password_list.extend(random.choice(characters) for _ in range(remaining_length))
        
        random.shuffle(password_list)
        password = "".join(password_list)

        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            len(password) == length):
            return password

class UserRegisterSerializer(serializers.ModelSerializer):
    # Campos que vêm do frontend
    email = serializers.EmailField(required=True)
    nome_completo = serializers.CharField(write_only=True, required=True, label="Nome Completo")
    telefone = serializers.CharField(required=True, max_length=15)
    data_nascimento = serializers.DateField(required=True)
    cpf = serializers.CharField(required=True, max_length=14)
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'},
        # validators=[validate_password] # Pode ser adicionado aqui também, mas faremos no método validate para melhor feedback
    )
    password2 = serializers.CharField(write_only=True, required=True, label="Confirmar Senha", style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'first_name',       # Será preenchido a partir de nome_completo
            'last_name',        # Será preenchido a partir de nome_completo
            'telefone',
            'data_nascimento',
            'cpf',
            'password',         # ModelSerializer lida com isso para chamar set_password
            'nome_completo',    # Incluído aqui porque é um campo declarado no serializer
            'password2'         # Incluído aqui porque é um campo declarado no serializer
        ]
        extra_kwargs = {
            # Como first_name e last_name são derivados, não são obrigatórios diretamente do request.
            'first_name': {'required': False},
            'last_name': {'required': False},
            # password, nome_completo e password2 já são write_only pela sua declaração.
        }

    def validate_email(self, value):
        email = value.lower()
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Este e-mail já está cadastrado.")
        return email

    def validate_cpf(self, value):
        cleaned_cpf = ''.join(filter(str.isdigit, value))
        if len(cleaned_cpf) != 11:
            raise serializers.ValidationError("CPF deve conter 11 dígitos numéricos.")
        if CustomUser.objects.filter(cpf=cleaned_cpf).exists():
            raise serializers.ValidationError("Este CPF já está cadastrado.")
        return cleaned_cpf

    def validate_telefone(self, value):
        cleaned_telefone = ''.join(filter(str.isdigit, value))
        if not (10 <= len(cleaned_telefone) <= 11):
             raise serializers.ValidationError("Telefone inválido. Use apenas números, incluindo DDD (10 ou 11 dígitos).")
        return cleaned_telefone

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError({"password2": "As senhas não coincidem."})

        # Validação de força da senha
        try:
            # O usuário ainda não existe neste ponto para UserRegisterSerializer,
            # então não podemos passar o objeto user para validate_password.
            # Se você tiver UserAttributeSimilarityValidator, ele pode não funcionar idealmente aqui
            # ou pode precisar ser desabilitado/ajustado para o contexto de registro.
            validate_password(password)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        # Processa nome_completo para first_name e last_name
        # 'nome_completo' foi definido como campo no serializer
        nome_completo_str = attrs.get('nome_completo') 
        if not nome_completo_str:
            # Esta validação é importante se nome_completo não for required=True no campo,
            # ou para garantir que não seja apenas espaços em branco.
            raise serializers.ValidationError({"nome_completo": "Este campo é obrigatório."})

        parts = nome_completo_str.strip().split(' ', 1)
        attrs['first_name'] = parts[0]
        attrs['last_name'] = parts[1] if len(parts) > 1 else ''

        if not attrs['first_name']:
            raise serializers.ValidationError({"nome_completo": "O nome não pode estar vazio."})
            
        # Remove campos que não são do modelo para não passá-los para create()
        # ou para o ModelSerializer tentar mapeá-los diretamente.
        attrs.pop('password2', None)
        attrs.pop('nome_completo', None)
            
        return attrs

    def create(self, validated_data):
        # validated_data aqui contém os campos de Meta.fields e o que foi retornado de validate()
        # 'password2' e 'nome_completo' já foram removidos em validate()
        
        # 'first_name' e 'last_name' foram adicionados a validated_data (attrs) no método validate.
        
        # Remove 'nome_completo' e 'password2' de validated_data antes de chamar create_user,
        # pois não são campos diretos do modelo CustomUser.
        validated_data.pop('nome_completo', None)
        validated_data.pop('password2', None)
        
        user = CustomUser.objects.create_user(
            username=validated_data['email'], # Adicionar username aqui, usando o email
            email=validated_data['email'],
            password=validated_data['password'], # create_user lida com o hashing
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            telefone=validated_data.get('telefone'), # Usar .get() para campos que podem não estar presentes
            data_nascimento=validated_data.get('data_nascimento'), # Usar .get()
            cpf=validated_data.get('cpf') # Usar .get()
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    """
    Serializador para o login do usuário via API, esperando telefone e senha.
    """
    phone = serializers.CharField(
        max_length=20, # Ou o tamanho que você usa para telefone
        label="Telefone",
        help_text="Número de telefone para login."
    )
    password = serializers.CharField(
        label="Senha",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True, # Importante para não retornar a senha
        help_text="Senha para login."
    )

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if not phone or not password:
            # Este erro seria diferente do que você está vendo, mas é uma boa prática.
            raise serializers.ValidationError("Telefone e senha são obrigatórios.", code='authorization')
        
        # Nenhuma validação de 'email' aqui.
        return attrs

class DirectPasswordResetSerializer(serializers.Serializer):
    cpf = serializers.CharField(required=True)
    data_nascimento = serializers.DateField(required=True, input_formats=['%Y-%m-%d'])
    telefone = serializers.CharField(required=True)
    user = None # Para armazenar o usuário encontrado

    def validate_cpf(self, value):
        cpf_cleaned = ''.join(filter(str.isdigit, value))
        if len(cpf_cleaned) != 11:
            raise serializers.ValidationError("CPF deve conter 11 dígitos.")
        return cpf_cleaned

    def validate_telefone(self, value):
        telefone_cleaned = ''.join(filter(str.isdigit, value))
        if not (10 <= len(telefone_cleaned) <= 11):
             raise serializers.ValidationError("Telefone inválido. Deve ter 10 ou 11 dígitos.")
        return telefone_cleaned

    def validate(self, attrs):
        cpf = attrs.get('cpf')
        data_nascimento = attrs.get('data_nascimento')
        telefone = attrs.get('telefone')

        try:
            self.user = CustomUser.objects.get(
                cpf=cpf,
                data_nascimento=data_nascimento,
                telefone=telefone
            )
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Dados incorretos ou usuário não encontrado.")
        except Exception as e:
            # Para depuração, você pode logar 'e'
            raise serializers.ValidationError("Erro ao validar os dados.")
        
        attrs['user'] = self.user
        return attrs

    def save(self):
        if not self.user: # Deve ser definido na validação
            raise Exception("Usuário não encontrado ou validação não executada.")
        
        new_password = generate_random_password(8)
        self.user.set_password(new_password)
        self.user.save()
        return new_password

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Adicione claims customizadas ao token se desejar
        # token['first_name'] = user.first_name
        # token['phone'] = user.telefone # Exemplo
        return token

    def validate(self, attrs):
        # O campo 'username' no attrs será o que o frontend enviar como 'phone'
        # se alterarmos o nome do campo no serializer ou se o frontend enviar 'username'
        # Para manter o frontend enviando 'phone', precisamos pegar 'phone' de attrs
        
        phone_input = attrs.get("phone") # Espera que o frontend envie 'phone'
        password = attrs.get("password")

        if not phone_input or not password:
            raise serializers.ValidationError("Telefone e senha são obrigatórios.", code="authorization")

        # Limpa o número de telefone para conter apenas dígitos
        cleaned_phone = re.sub(r'\D', '', str(phone_input))
        if not cleaned_phone:
            raise serializers.ValidationError("Número de telefone inválido.", code="authorization")

        # Tenta encontrar o usuário pelo telefone
        try:
            user = CustomUser.objects.get(telefone=cleaned_phone)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Nenhum usuário ativo encontrado com este telefone.", code="authorization")
        
        # Autentica usando o backend PhoneAuthBackend (ou qualquer backend configurado)
        # Passamos o 'username' como o telefone para o PhoneAuthBackend
        self.user = self.context['request'].user = user # Necessário para que o authenticate funcione corretamente com o request
        authenticated_user = authenticate(request=self.context.get('request'), username=cleaned_phone, password=password)

        if not authenticated_user:
            raise serializers.ValidationError("Telefone ou senha inválidos.", code="authorization")

        if not authenticated_user.is_active:
            raise serializers.ValidationError("Conta de usuário desativada.", code="authorization")
        
        # O super().validate() espera 'username' e 'password' no attrs.
        # Como já autenticamos, podemos construir os dados esperados por ele ou
        # diretamente retornar os tokens. Para maior compatibilidade, vamos
        # simular o que o super().validate() faria após a autenticação.
        
        # Atualiza attrs para o que o super().validate() esperaria
        # O 'username' aqui deve ser o USERNAME_FIELD do usuário encontrado
        attrs[self.username_field] = getattr(authenticated_user, self.username_field)
        attrs['password'] = password # A senha já está aqui

        # Agora chame o super().validate() com os dados corretos
        # No entanto, como já fizemos a autenticação e temos o usuário,
        # podemos simplesmente retornar os tokens.
        
        refresh = self.get_token(authenticated_user)

        data = {}
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        
        # Adicionar dados do usuário à resposta, se desejado
        data["user"] = {
            "id": authenticated_user.id,
            "phone": authenticated_user.telefone,
            "email": authenticated_user.email,
            "first_name": authenticated_user.first_name,
            "last_name": authenticated_user.last_name,
        }
        
        return data

        

    # Adicione o campo 'phone' ao serializer para que ele seja esperado
    phone = serializers.CharField(write_only=True, required=True)
    # O campo 'password' já é herdado e é write_only=True, required=True

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 
            'email', 
            'nome_completo', # Assumindo que você tem este campo
            'first_name', # Se estiver usando os campos padrão do Django
            'last_name',  # Se estiver usando os campos padrão do Django
            'telefone', 
            'data_nascimento',
            'genero',
            'cpf',
            'cargo',
            'grau',
            'equipe',
            'profile_pic_url', # Se você tiver um campo/método para a URL da foto
            'is_staff',        # Para verificar se é admin/staff
            'is_superuser',    # Para verificar se é superuser
            # Adicione quaisquer outros campos que o frontend precise
        ]
        read_only_fields = [
            'id', 'email', 'is_staff', 'is_superuser', # Campos que o usuário não deve editar diretamente via este serializer
            'cargo', 'grau', 'equipe' # Geralmente atribuídos por admins
        ] 

    # Se 'profile_pic_url' não for um campo direto do modelo, 
    # mas um método ou property, você pode usar SerializerMethodField:
    # profile_pic_url = serializers.SerializerMethodField()
    # def get_profile_pic_url(self, obj):
    #     if obj.profile_pic: # Supondo que 'profile_pic' seja um ImageField
    #         return self.context['request'].build_absolute_uri(obj.profile_pic.url)
    #     return None # Ou uma URL de imagem padrão