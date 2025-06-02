from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import re

CustomUser = get_user_model()

class PhoneAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            # No fluxo normal do AuthenticationForm, 'username' será o valor do campo username do formulário.
            # Esta linha é um fallback, mas geralmente 'username' já virá preenchido.
            phone_number_input = kwargs.get(CustomUser.USERNAME_FIELD)
        else:
            phone_number_input = username

        if not phone_number_input:
            return None

        # Limpa o número de telefone para conter apenas dígitos
        # Assumindo que o telefone no banco de dados também está armazenado apenas com dígitos ou
        # que a comparação será feita de forma consistente.
        cleaned_phone = re.sub(r'\D', '', str(phone_number_input))
        if not cleaned_phone:
            return None

        try:
            # Tenta encontrar o usuário pelo campo 'telefone'
            user = CustomUser.objects.get(telefone=cleaned_phone)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except CustomUser.DoesNotExist:
            # Se não encontrar por telefone, retorna None.
            # O ModelBackend padrão (se ainda estiver configurado e se o USERNAME_FIELD for email)
            # poderia tentar autenticar por email, mas o objetivo aqui é focar no telefone.
            return None
        except Exception:
            # Qualquer outra exceção durante a busca ou verificação
            return None
        return None # Falha na autenticação

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None