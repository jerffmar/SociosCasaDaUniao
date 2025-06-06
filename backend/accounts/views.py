from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse_lazy, reverse # Adicionado reverse
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic import TemplateView, FormView, UpdateView, CreateView # Adicionado CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages # Adicionado messages
from .forms import (
    UserLoginForm, 
    UserRegisterForm, 
    PasswordRecoveryForm, 
    UserProfileForm,
    # CustomSetPasswordForm # Se você criou este formulário
)
from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.contrib.auth import get_user_model, authenticate, login
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

class CustomLoginView(LoginView):
    template_name = 'index.html'
    form_class = UserLoginForm # Use seu formulário customizado se tiver um
    redirect_authenticated_user = True # Redireciona se o usuário já estiver logado

    def get_success_url(self):
        return reverse_lazy('core:home') # Corrigido para usar o namespace correto

    def form_invalid(self, form):
        messages.error(self.request, "Telefone ou senha inválidos. Por favor, tente novamente.")
        return super().form_invalid(form)

class CustomLogoutView(auth_views.LogoutView):
    # LOGOUT_REDIRECT_URL em settings.py cuida do redirecionamento.
    next_page = 'login'
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserRegisterAPIView(generics.CreateAPIView):  # Renomeado de UserRegisterView
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

class UserLoginView(generics.GenericAPIView): # Esta é a view que o frontend chama para /api/accounts/login/
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
                    login(request, user) # Estabelece a sessão Django
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

class UserRegisterPageView(CreateView): # Alterado de FormView para CreateView para lidar com a criação do usuário
    template_name = 'accounts/register_page.html' # Caminho dentro do diretório 'templates'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login') # Redireciona para a página de login após o registro

    def form_valid(self, form):
        user = form.save()
        # Logar o usuário automaticamente após o registro, se desejado
        # login(self.request, user) 
        messages.success(self.request, 'Cadastro realizado com sucesso! Faça login para continuar.')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Adiciona uma mensagem de erro genérica se houver erros no formulário
        # Os erros específicos dos campos já são tratados pelo Django e pelo template
        messages.error(self.request, "Por favor, corrija os erros no formulário.")
        return super().form_invalid(form)


class PasswordRecoveryView(FormView):
    template_name = 'accounts/password_recovery_page.html' # Caminho dentro do diretório 'templates'
    form_class = PasswordRecoveryForm # Seu formulário de recuperação de senha
    success_url = reverse_lazy('login') # Ou para uma página de "instruções enviadas"

    def form_valid(self, form):
        # Aqui você implementaria a lógica de recuperação de senha
        # Por exemplo, encontrar o usuário, gerar uma nova senha ou um link de reset
        # Para o exemplo de exibição da nova senha diretamente:
        try:
            new_password = form.reset_password() # Supondo que seu form tenha esse método
            messages.success(self.request, f"Sua nova senha é: {new_password}. Por favor, guarde-a em um local seguro e faça login.")
            return super().form_valid(form)
        except get_user_model().DoesNotExist:
            messages.error(self.request, "Usuário não encontrado com os dados fornecidos.")
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f"Ocorreu um erro: {e}")
            return self.form_invalid(form)

# View para a página de edição de perfil (baseada em Django Templates)
class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html' # Caminho dentro do diretório 'templates'
    # success_url = reverse_lazy('profile_edit_page') # Redireciona para a mesma página ou para 'core_home'
    
    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return reverse('profile_edit_page') # Redireciona de volta para a página de edição

    def form_invalid(self, form):
        messages.error(self.request, "Não foi possível atualizar o perfil. Verifique os erros abaixo.")
        return super().form_invalid(form)

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class LogoutAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout bem-sucedido."}, status=205)
        except Exception as e:
            return Response({"error": "Token inválido ou ausente."}, status=400)
