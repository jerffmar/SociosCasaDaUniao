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

from .serializers import (
    UserRegisterSerializer, 
    UserLoginSerializer, 
    DirectPasswordResetSerializer,
    # Adicione aqui o serializer do perfil do usuário, ex: UserProfileSerializer
)

CustomUser = get_user_model()

class CustomLoginView(AuthLoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm # Já está correto
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
            phone_number = serializer.validated_data['phone'] # 'phone' do UserLoginSerializer
            password = serializer.validated_data['password']
            
            # A função authenticate usará os backends configurados em settings.py.
            # Nosso PhoneAuthBackend tentará autenticar usando phone_number.
            user = authenticate(request, username=phone_number, password=password)
            
            if user:
                if user.is_active:
                    login(request, user) 
                    return Response({
                        "message": "Login bem-sucedido.",
                        "user": { 
                            "email": user.email, # Ainda podemos retornar o email se desejado
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            # Adicione outros campos do usuário conforme necessário
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Conta desativada."}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"detail": "Telefone ou senha inválidos."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DirectPasswordResetAPIView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request, *args, **kwargs):
        serializer = DirectPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                new_password = serializer.save()
                return Response({
                    "message": "Sua senha foi redefinida com sucesso.",
                    "new_password": new_password
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": "Ocorreu um erro interno ao tentar redefinir a senha."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        error_messages = []
        if "non_field_errors" in serializer.errors:
            error_messages.extend(serializer.errors["non_field_errors"])
        else:
            for field, errors in serializer.errors.items():
                error_messages.append(f"{field.replace('_', ' ').capitalize()}: {', '.join(errors)}")
        
        return Response({"detail": " ".join(error_messages) if error_messages else "Dados inválidos."}, status=status.HTTP_400_BAD_REQUEST)

# Adicione ou descomente UserProfileView
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    # serializer_class = UserProfileSerializer # Substitua pelo seu serializer de perfil
    permission_classes = [IsAuthenticated] # Geralmente requer autenticação

    def get_object(self):
        # Retorna o perfil do usuário logado
        return self.request.user

    # Você pode adicionar lógica personalizada para update (PUT/PATCH) se necessário
