from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse_lazy
from .forms import LoginForm # Certifique-se que é o LoginForm que acabamos de revisar
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken # Se estiver usando JWT para tokens
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView
from .serializers import (
    UserRegisterSerializer, 
    UserLoginSerializer, 
    DirectPasswordResetSerializer,
    CustomTokenObtainPairSerializer, # Importe o novo serializer
    UserProfileSerializer # Importe o serializer de perfil
)

CustomUser = get_user_model()

class CustomLoginView(AuthLoginView):
    template_name = 'accounts/login.html'  # Certifique-se de que este caminho está correto
    authentication_form = LoginForm
    success_url = reverse_lazy('core:home')
    # LOGIN_REDIRECT_URL em settings.py também é respeitado.

class CustomLogoutView(auth_views.LogoutView):
    # LOGOUT_REDIRECT_URL em settings.py cuida do redirecionamento.
    pass

class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                {"message": "Usuário registrado com sucesso."},
                status=status.HTTP_201_CREATED
            )
        except DRFValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone']
            password = serializer.validated_data['password']
            user = authenticate(request, username=phone_number, password=password)
            
            if user:
                if user.is_active:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        "message": "Login bem-sucedido.",
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user": {
                            "id": user.id,
                            "phone": user.telefone,
                            "email": user.email,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Conta desativada."}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"detail": "Telefone ou senha inválidos."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DirectPasswordResetAPIView(APIView): # Ou generics.GenericAPIView se preferir
    permission_classes = [AllowAny] 

    def post(self, request, *args, **kwargs):
        serializer = DirectPasswordResetSerializer(data=request.data, context={'request': request}) # Adicione context se necessário
        if serializer.is_valid():
            try:
                # O método save() do serializer agora retorna a nova senha gerada
                generated_password = serializer.save() 
                
                return Response({
                    "detail": "Senha redefinida com sucesso. Sua nova senha é:", # Mensagem ajustada
                    "new_password": generated_password # Inclui a nova senha na resposta
                }, status=status.HTTP_200_OK)
            except Exception as e:
                # Logar o erro 'e' aqui é crucial para depuração
                print(f"Erro interno não tratado ao redefinir senha: {e}") 
                return Response({"detail": "Ocorreu um erro interno ao tentar redefinir a senha."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Lógica para formatar erros de validação (como estava antes)
        error_messages = []
        if "non_field_errors" in serializer.errors:
            error_messages.extend(serializer.errors["non_field_errors"])
        else:
            for field, errors in serializer.errors.items():
                # Evita adicionar o campo 'Generated password' se ele aparecer nos erros
                # pois não é um campo de entrada.
                if field != 'generated_password':
                    error_messages.append(f"{field.replace('_', ' ').capitalize()}: {', '.join(errors)}")
        
        return Response({"detail": " ".join(error_messages) if error_messages else "Dados inválidos."}, status=status.HTTP_400_BAD_REQUEST)

# Adicione ou descomente UserProfileView
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated] # Apenas usuários autenticados podem acessar

    def get_object(self):
        # Garante que o usuário só possa ver/editar seu próprio perfil
        return self.request.user

    # Você pode adicionar lógica personalizada para update (PUT/PATCH) se necessário

class CustomTokenObtainPairView(BaseTokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
