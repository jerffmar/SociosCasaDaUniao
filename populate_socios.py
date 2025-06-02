import os
import django
from faker import Faker
from datetime import date
import random

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings') # Substitua 'backend.settings' pelo caminho correto do seu arquivo settings.py
django.setup()

from accounts.models import CustomUser # Importe seu modelo CustomUser

fake = Faker('pt_BR') # Usar localidade pt_BR para dados mais realistas

def create_fake_socios(n=10):
    created_count = 0
    telefones_usados = set(CustomUser.objects.values_list('telefone', flat=True)) # Carrega telefones existentes

    for _ in range(n):
        name = fake.name()
        
        # Gera um telefone único
        while True:
            # Gera um número de telefone com 10 ou 11 dígitos
            num_digits = random.choice([10, 11])
            telefone_numerico = ''.join([str(random.randint(0, 9)) for _ in range(num_digits)])
            if telefone_numerico not in telefones_usados:
                telefones_usados.add(telefone_numerico)
                break
        
        # Email pode ser opcional (50% de chance de ter um email)
        email = fake.email() if random.choice([True, False]) else None
        if email:
            # Garante que o email seja único se fornecido
            email_base = email.split('@')[0]
            email_domain = email.split('@')[1]
            count = 1
            while CustomUser.objects.filter(email=email).exists():
                email = f"{email_base}{count}@{email_domain}"
                count += 1

        # Gera data de nascimento (entre 18 e 70 anos atrás)
        start_date = date(date.today().year - 70, 1, 1)
        end_date = date(date.today().year - 18, 12, 31)
        data_nascimento = fake.date_between_dates(date_start=start_date, date_end=end_date)
        
        password = "password123" # Senha padrão para todos os usuários fictícios

        try:
            user = CustomUser.objects.create_user(
                name=name,
                telefone=telefone_numerico,
                email=email,
                data_nascimento=data_nascimento,
                password=password
            )
            print(f"Sócio '{user.name}' com telefone '{user.telefone}' criado com sucesso.")
            created_count += 1
        except Exception as e:
            print(f"Erro ao criar sócio {name}: {e}")
            # Se o email for a causa da duplicidade e for opcional, podemos tentar sem ele
            if email and "email" in str(e).lower():
                try:
                    user = CustomUser.objects.create_user(
                        name=name,
                        telefone=telefone_numerico,
                        email=None, # Tenta criar sem email
                        data_nascimento=data_nascimento,
                        password=password
                    )
                    print(f"Sócio '{user.name}' (sem email) com telefone '{user.telefone}' criado com sucesso.")
                    created_count += 1
                except Exception as e_no_email:
                     print(f"Erro ao criar sócio {name} (sem email): {e_no_email}")


    print(f"\n{created_count} sócios fictícios criados.")

if __name__ == '__main__':
    print("Iniciando a criação de sócios fictícios...")
    create_fake_socios(10)
    print("Criação de sócios fictícios concluída.")