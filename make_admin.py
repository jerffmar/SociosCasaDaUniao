import os
import django
import sys

def main():
    # Adiciona o diretório do projeto ao sys.path
    # Isso garante que 'backend.settings' e 'backend.accounts.models' possam ser encontrados
    # Supondo que este script está na raiz do projeto e 'backend' é um diretório dentro dele.
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_root)

    # Configure o ambiente Django
    # Substitua 'backend.settings' pelo caminho correto para o seu arquivo settings.py
    # se ele estiver em um local diferente (ex: 'SociosCasaDaUniao.settings')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings') 
    try:
        django.setup()
    except Exception as e:
        print(f"Erro ao configurar o Django: {e}")
        print("Verifique se DJANGO_SETTINGS_MODULE está correto e se o script está no diretório raiz do projeto.")
        return

    # Importe seu modelo de usuário customizado
    # Ajuste o caminho de importação se o seu modelo estiver em um local diferente
    try:
        from backend.accounts.models import CustomUser
    except ImportError:
        print("Erro: Não foi possível importar 'CustomUser' de 'backend.accounts.models'.")
        print("Verifique o caminho do modelo e se o app 'accounts' está em INSTALLED_APPS.")
        return

    USER_PHONE_TO_MAKE_ADMIN = '84996733737'

    try:
        # Encontre o usuário pelo número de telefone
        user = CustomUser.objects.get(telefone=USER_PHONE_TO_MAKE_ADMIN)
        
        # Defina os atributos de administrador
        user.is_staff = True  # Permite acesso ao site de administração do Django
        user.is_superuser = True # Concede todas as permissões
        
        # Salve as alterações no banco de dados
        user.save()
        
        print(f"Usuário com telefone '{USER_PHONE_TO_MAKE_ADMIN}' agora é um administrador (staff e superuser).")
        
    except CustomUser.DoesNotExist:
        print(f"Erro: Usuário com telefone '{USER_PHONE_TO_MAKE_ADMIN}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == '__main__':
    main()
