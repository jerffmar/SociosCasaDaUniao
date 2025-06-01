
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError # Renomeado para evitar conflito

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(write_only=True, required=True, max_length=150) # Para username e first_name

    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'password', 'password_confirm', 'cpf', 'telefone')
        extra_kwargs = {
            'cpf': {'required': False, 'allow_blank': True, 'allow_null': True},
            'telefone': {'required': False, 'allow_blank': True, 'allow_null': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "As senhas não coincidem."})
        
        # Validar unicidade do email (embora o modelo já faça isso, é bom ter no serializer)
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Este email já está cadastrado."})

        # Validar unicidade do username (que será o 'name' do formulário)
        # Se o username for diferente do email e precisar ser único.
        # No nosso caso, CustomUser.USERNAME_FIELD é 'email', mas 'username' ainda é um campo único de AbstractUser.
        # Vamos usar o 'name' como 'username' e 'first_name'.
        if CustomUser.objects.filter(username=attrs['name']).exists():
            # Poderíamos gerar um username único se 'name' não for único,
            # ou pedir um username separado. Por ora, vamos exigir que 'name' (como username) seja único.
            raise serializers.ValidationError({"name": "Este nome de usuário (name) já está em uso."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['name'], # Usando 'name' como username
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['name'], # Usando 'name' como first_name
            cpf=validated_data.get('cpf'),
            telefone=validated_data.get('telefone')
        )
        # Como USERNAME_FIELD é 'email', o login será com email.
        # O campo 'username' de AbstractUser ainda existe e precisa ser único.
        return user
