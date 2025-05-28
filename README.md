**Passos para configurar e executar o projeto Django:**
1.  **Instale as dependências base:**
    `
    `pip install Django djangorestframework django-cors-headers` (Mesmo que não use DRF diretamente, `djangorestframework` é uma boa prática para APIs e `corsheaders` é essencial).
2.  **Faça as migrações do banco de dados:**
    `python manage.py makemigrations`
    `python manage.py migrate`
3.  **Crie um superusuário para acessar o admin (opcional, mas recomendado):**
    `python manage.py createsuperuser`
4.  **Execute o servidor de desenvolvimento:**
    `python manage.py runserver`

O servidor Django estará rodando em `http://127.0.0.1:8000/`. As URLs da API estarão em `http://127.0.0.1:8000/api/`.