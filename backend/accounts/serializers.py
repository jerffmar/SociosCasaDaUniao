from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import CustomUser # Certifique-se que CustomUser está importado
import random
import string

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
    phone = serializers.CharField() # Alterado de 'telefone' para 'phone' para corresponder ao frontend
    password = serializers.CharField(write_only=True)

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