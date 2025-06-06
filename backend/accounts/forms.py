from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser # Importar o modelo CustomUser

class UserLoginForm(AuthenticationForm): # Renomeado de LoginForm para UserLoginForm
    username = forms.CharField(
        label=_("Telefone"),
        strip=False,
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': '(XX) XXXXX-XXXX'})
    )
    # A senha já é herdada de AuthenticationForm

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

class UserRegisterForm(UserCreationForm):
    # Adicionar campos do CustomUser que não estão no UserCreationForm padrão
    # e que você quer no formulário de registro.
    # O UserCreationForm já lida com username (que será o telefone), password1, password2.
    # Precisamos adicionar email, nome_completo (que será dividido em first_name e last_name),
    # data_nascimento, cpf.
    
    email = forms.EmailField(label=_("Email"), required=True)
    nome_completo = forms.CharField(label=_("Nome Completo"), max_length=150, required=True)
    data_nascimento = forms.DateField(label=_("Data de Nascimento"), widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    cpf = forms.CharField(label=_("CPF (somente números)"), max_length=11, required=True, help_text=_("Digite apenas os números do CPF."))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "nome_completo", "data_nascimento", "cpf") # username aqui será o campo 'telefone'

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        # Adicione validações de CPF aqui se necessário (ex: formato, dígitos verificadores)
        # Por enquanto, apenas remove não dígitos
        return ''.join(filter(str.isdigit, cpf))

    def save(self, commit=True):
        user = super().save(commit=False)
        # Dividir nome_completo em first_name e last_name
        nome_completo_str = self.cleaned_data.get('nome_completo')
        parts = nome_completo_str.strip().split(' ', 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ''
        
        user.data_nascimento = self.cleaned_data.get('data_nascimento')
        user.cpf = self.cleaned_data.get('cpf')
        # O email já é tratado pelo UserCreationForm se estiver nos fields.
        # O telefone (username) também.
        
        if commit:
            user.save()
        return user

class PasswordRecoveryForm(forms.Form):
    # Este formulário é para a etapa inicial de recuperação,
    # onde o usuário informa dados para ser identificado.
    cpf = forms.CharField(label=_("CPF (somente números)"), max_length=11, required=True)
    data_nascimento = forms.DateField(label=_("Data de Nascimento"), widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    telefone = forms.CharField(label=_("Telefone (somente números, com DDD)"), max_length=11, required=True)

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        return ''.join(filter(str.isdigit, cpf))

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        return ''.join(filter(str.isdigit, telefone))

    def get_user(self):
        """
        Retorna o usuário se os dados corresponderem, caso contrário None.
        """
        try:
            user = CustomUser.objects.get(
                cpf=self.cleaned_data.get('cpf'),
                data_nascimento=self.cleaned_data.get('data_nascimento'),
                telefone=self.cleaned_data.get('telefone')
            )
            return user
        except CustomUser.DoesNotExist:
            return None
        except Exception: # Outros erros possíveis
            return None
            
    def reset_password(self):
        """
        Encontra o usuário e redefine a senha.
        Este método é um exemplo, a lógica real de reset pode variar
        (ex: enviar email com link, gerar senha temporária).
        Para o caso de gerar e mostrar a senha:
        """
        user = self.get_user()
        if user:
            # Gerar uma nova senha aleatória (exemplo simples)
            # Em produção, use algo mais robusto ou envie um link de reset.
            import random, string
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user.set_password(new_password)
            user.save()
            return new_password
        raise CustomUser.DoesNotExist("Usuário não encontrado com os dados fornecidos.")


class UserProfileForm(forms.ModelForm):
    # Campo para o nome completo, que será dividido em first_name e last_name na view ou no save do form.
    nome_completo = forms.CharField(label=_("Nome Completo"), max_length=150, required=True)
    # Campo para limpar a foto de perfil
    profile_picture_clear = forms.BooleanField(label=_("Remover foto atual"), required=False, widget=forms.CheckboxInput)


    class Meta:
        model = CustomUser
        fields = [
            'profile_picture', 'nome_completo', 'email', 'telefone', 
            'data_nascimento', 'cpf', 'genero', 
            # 'cargos', 'grau', 'equipe' # Estes campos podem ser controlados por permissão
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        help_texts = {
            'telefone': _('Formato: (XX) XXXXX-XXXX ou apenas números.'),
            'cpf': _('Apenas números.'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Preencher nome_completo a partir de first_name e last_name da instância
        if self.instance and self.instance.pk:
            self.fields['nome_completo'].initial = self.instance.get_full_name()
            # Tornar campos não editáveis pelo usuário comum
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['cpf'].widget.attrs['readonly'] = True
            # Adicionar placeholder para telefone
            self.fields['telefone'].widget.attrs['placeholder'] = '(XX) XXXXX-XXXX'


            # Lógica para campos administrativos (cargo, grau, equipe)
            # Se o usuário logado não for admin, esses campos podem ser desabilitados ou não incluídos.
            # Isso geralmente é melhor tratado na view ou no __init__ do form,
            # verificando as permissões do request.user.
            # Exemplo:
            # if not self.request.user.is_staff: # Supondo que 'request' foi passado para o form
            #     for field_name in ['cargos', 'grau', 'equipe']:
            #         if field_name in self.fields:
            #             self.fields[field_name].disabled = True


    def clean_nome_completo(self):
        nome_completo = self.cleaned_data.get('nome_completo')
        if not nome_completo or len(nome_completo.strip().split()) < 1:
            raise forms.ValidationError(_("Por favor, insira o nome completo."))
        return nome_completo

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        # Se o CPF for readonly, ele não estará em cleaned_data se não for alterado.
        # Se estiver editando, o CPF da instância deve ser usado.
        if self.instance and self.instance.pk:
            return self.instance.cpf # Mantém o CPF original se não for editável
        # Adicione validações se for editável
        return ''.join(filter(str.isdigit, cpf))
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance and self.instance.pk:
            return self.instance.email # Mantém o email original
        # Adicione validações se for editável e único
        return email


    def save(self, commit=True):
        # Lidar com a divisão de nome_completo para first_name e last_name
        nome_completo_str = self.cleaned_data.get('nome_completo')
        parts = nome_completo_str.strip().split(' ', 1)
        self.instance.first_name = parts[0]
        self.instance.last_name = parts[1] if len(parts) > 1 else ''
        
        # Lidar com a limpeza da foto de perfil
        if self.cleaned_data.get('profile_picture_clear'):
            if self.instance.profile_picture: # Verifica se há uma foto para limpar
                self.instance.profile_picture.delete(save=False) # Deleta o arquivo
                self.instance.profile_picture = None # Limpa o campo no modelo

        # Se uma nova foto foi enviada E profile_picture_clear não foi marcado,
        # o ModelForm já lida com a atribuição da nova foto.
        # Se profile_picture_clear foi marcado, e uma nova foto também foi enviada,
        # a nova foto prevalecerá sobre a limpeza, a menos que a lógica de limpeza
        # seja ajustada para priorizar a limpeza. O comportamento padrão do ClearableFileInput
        # é que se um novo arquivo é enviado, ele substitui o antigo, e a checkbox de limpar
        # é para limpar o valor existente se nenhum novo arquivo for enviado.

        return super().save(commit=commit)

# Se você precisar de um formulário específico para definir senha (ex: admin ou perfil do usuário)
# class CustomSetPasswordForm(SetPasswordForm):
#     pass