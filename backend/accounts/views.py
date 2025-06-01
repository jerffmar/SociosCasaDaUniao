from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import LoginForm
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer
from .models import CustomUser

class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    # LOGIN_REDIRECT_URL em settings.py cuida do redirecionamento de sucesso.

class CustomLogoutView(auth_views.LogoutView):
    # LOGOUT_REDIRECT_URL em settings.py cuida do redirecionamento.
    pass

class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({
                "user": { # Você pode querer um serializer diferente para a resposta do usuário
                    "id": user.id,
                    "name": user.first_name, # ou user.username
                    "email": user.email
                },
                "message": "Usuário cadastrado com sucesso. Você pode fazer login agora."
            }, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            # Retorna os erros de validação específicos do serializer
            return Response({"message": "Erro de validação.", "errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Captura outras exceções genéricas
            return Response({"message": f"Ocorreu um erro inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create your views here.
