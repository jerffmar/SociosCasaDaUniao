# Idealização da Aplicação Web (Django-only)

A estrutura da aplicação seguirá uma arquitetura monolítica com o Django, onde o framework cuidará tanto da lógica de backend (APIs, banco de dados, regras de negócio) quanto da renderização do frontend (páginas HTML, formulários).

## Estrutura Geral de Arquivos (Django):

O código do projeto Django residirá em um diretório principal. A estrutura básica incluirá:

*   **Projeto Raiz (Ex:** `SociosCasaDaUniao`**)**
    *   `manage.py`: Utilitário de linha de comando do Django.
    *   `nome_do_projeto/` (diretório de configuração do projeto, ex: `config/` ou `SociosCasaDaUniao_project/`)
        *   `settings.py`: Configurações do projeto Django (INSTALLED_APPS, DATABASES, MIDDLEWARE, TEMPLATES, STATICFILES_DIRS, etc.).
        *   `urls.py`: Configuração de URL raiz do projeto.
        *   `wsgi.py`, `asgi.py`: Pontos de entrada para servidores WSGI/ASGI.
    *   `requirements.txt`: Lista de dependências Python (Django, Pillow, etc.).
    *   `apps/` (diretório opcional para agrupar os apps Django)
        *   `accounts/` (App para gerenciamento de usuários, autenticação, perfis)
            *   `models.py`: Modelo de usuário customizado.
            *   `views.py`: Lógica para login, logout, cadastro, recuperação de senha, perfil.
            *   `forms.py`: Formulários Django para login, cadastro, edição de perfil.
            *   `urls.py`: URLs específicas do app `accounts`.
            *   `templates/accounts/`: Templates HTML para as páginas de `accounts` (ex: `login.html`, `register.html`, `profile.html`).
            *   `static/accounts/`: Arquivos estáticos específicos do app (CSS, JS, imagens).
        *   `core/` (App para funcionalidades centrais, página inicial pós-login, etc.)
            *   `views.py`: Lógica para a página home, dashboard.
            *   `urls.py`: URLs do app `core`.
            *   `templates/core/`: Templates HTML para o app `core` (ex: `home.html`, `base.html`).
            *   `static/core/`: Arquivos estáticos do app `core`.
        *   `activities/`, `rifas/`, `caronas/` (Outros apps conforme necessidade, cada um com sua estrutura de `models.py`, `views.py`, `forms.py`, `urls.py`, `templates/app_name/`, `static/app_name/`)
    *   `templates/` (Diretório no nível do projeto para templates globais, como `base.html`, `404.html`, `500.html`)
    *   `static/` (Diretório no nível do projeto para arquivos estáticos globais - CSS, JS, imagens. Configurado em `STATICFILES_DIRS`)

## Detalhamento das Páginas e Funcionalidades (Implementação com Django):

1.  **Página Inicial / Login (`/login/` ou `/` se não autenticado):**
    *   **Propósito:** Ponto de entrada para usuários não autenticados.
    *   **View Django:** `accounts.views.LoginView` (pode ser uma `LoginView` customizada ou a `django.contrib.auth.views.LoginView`).
    *   **Template Django:** `accounts/login.html`.
    *   **Formulário Django:** `accounts.forms.LoginForm` (pode usar `django.contrib.auth.forms.AuthenticationForm`).
    *   **Conteúdo:** Um contêiner centralizado, contendo:
        *   Logo da instituição.
        *   Formulário de Login: Campos para Telefone (ou username/email) e Senha.
        *   Botões: "Login" (submete o formulário para a `LoginView`), "Cadastre-se" (link para a página de cadastro), "Recuperar Acesso" (link para a página de recuperação).
    *   **Funcionalidades:**
        *   A `LoginView` processa os dados do formulário.
        *   Em caso de sucesso, autentica o usuário e redireciona para a Página Home (`/home/`).
        *   Em caso de falha, re-renderiza `login.html` com mensagens de erro.
    *   **Navegação:** Links usando a tag `{% url 'nome_da_rota' %}` nos templates.
    *   **Layout:** O `login.html` pode estender um `base_public.html` ou similar, que inclui o Cabeçalho ("Centro Espirita Beneficente União do Vegetal - Núcleo Natal") e o Rodapé ("© 1961 a 2025...").

2.  **Página de Cadastro (`/register/`):**
    *   **Propósito:** Permitir que novos usuários criem uma conta.
    *   **View Django:** `accounts.views.RegisterView` (uma view customizada que lida com a criação do usuário).
    *   **Template Django:** `accounts/register.html`.
    *   **Formulário Django:** `accounts.forms.UserRegisterForm` (um `ModelForm` baseado no modelo de usuário customizado, ou um `UserCreationForm` customizado).
    *   **Conteúdo:** Formulário de cadastro com os campos necessários.
    *   **Funcionalidades:**
        *   A `RegisterView` processa o formulário.
        *   Em caso de sucesso, cria o novo usuário e redireciona (ex: para a página de login ou uma página de sucesso).
        *   Em caso de falha, re-renderiza `register.html` com mensagens de erro.

3.  **Página de Recuperação de Acesso (`/password_reset/`, etc.):**
    *   **Propósito:** Permitir que usuários recuperem o acesso à conta.
    *   **Views Django:** Utilizar as views embutidas do Django em `django.contrib.auth.views` (ex: `PasswordResetView`, `PasswordResetDoneView`, `PasswordResetConfirmView`, `PasswordResetCompleteView`).
    *   **Templates Django:** Criar os templates correspondentes (ex: `accounts/password_reset_form.html`, `accounts/password_reset_done.html`, etc.) conforme a documentação do Django.
    *   **Formulários Django:** As views embutidas utilizam formulários como `PasswordResetForm` e `SetPasswordForm`.
    *   **Conteúdo/Funcionalidades:** Fluxo padrão de reset de senha (solicitar email/usuário, enviar email com link, permitir definir nova senha).

4.  **Página Home (`/home/` ou `/dashboard/`):**
    *   **Propósito:** Área principal para usuários autenticados.
    *   **View Django:** `core.views.HomePageView` (ou `dashboard.views.DashboardView`).
    *   **Template Django:** `core/home.html` (ou `dashboard/dashboard.html`).
    *   **Layout:** Estrutura com um Painel Lateral (Sidebar) e uma área de Conteúdo Principal, implementados diretamente no HTML do template ou com `includes` (ex: `{% include 'includes/sidebar.html' %}`).
    *   **Acesso:** Restrita a usuários autenticados usando o decorator `@login_required` ou o `LoginRequiredMixin` na view.
    *   **Funcionalidades:** A `HomePageView` pode buscar dados relevantes para o usuário e passá-los para o template `home.html`. O template exibirá esses dados e os links de navegação no painel lateral. Diferentes seções da "Home" podem ser URLs distintas que renderizam templates diferentes ou a mesma view que renderiza seções diferentes condicionalmente.

5.  **Painel Lateral (Sidebar) na Página Home:**
    *   **Implementação:** Parte do template `core/home.html` ou um template separado incluído (ex: `includes/sidebar.html`).
    *   **Conteúdo:**
        *   Área para foto de perfil do usuário logado (acessível via `request.user` no template).
        *   Lista de menus de navegação (Meu Perfil, Atividades, Rifas, Caronas, Assistência) como links `<a>` usando `{% url %}`.
    *   **Menus/Submenus:** Implementados com HTML e CSS. A lógica para exibir/ocultar submenus pode ser feita com JavaScript simples (Vanilla JS) se necessário, ou puramente CSS.

6.  **Outras Funcionalidades (Calendário, Editar Perfil, Quadro de Sócios, etc.):**
    *   Cada funcionalidade principal teria seu próprio conjunto de:
        *   **Views Django:** Para processar requisições e buscar/salvar dados.
        *   **Templates Django:** Para exibir a interface da funcionalidade.
        *   **Formulários Django:** Para entrada de dados.
        *   **URLs:** Mapeando para as views correspondentes.
    *   Por exemplo, "Editar Perfil" seria uma view em `accounts.views` com um template `accounts/profile_edit.html` e um `ModelForm` para o modelo de usuário.

**Considerações Adicionais para Django-only:**

*   **Arquivos Estáticos:** CSS, JavaScript (para interatividade leve), e imagens serão gerenciados pelo `django.contrib.staticfiles`.
*   **Interatividade:** Para interações dinâmicas sem recarregar a página inteira (ex: atualizar uma parte de uma tabela), pode-se usar JavaScript (Vanilla JS ou bibliotecas como HTMX ou Alpine.js) para fazer requisições AJAX para views Django que retornam fragmentos de HTML ou JSON.
*   **Notificações:** Podem ser implementadas usando o `django.contrib.messages` framework para mensagens flash, ou com JavaScript para notificações mais dinâmicas no navegador (possivelmente com AJAX para buscar novas notificações).

---

Gerar *todo* o código necessário para implementar todas essas funcionalidades é uma tarefa extensa que vai além de uma única resposta. Envolve a criação de múltiplos arquivos Python (models, views, forms, urls), arquivos HTML (templates), e possivelmente arquivos CSS e JavaScript.

No entanto, posso fornecer exemplos de código para partes específicas para ajudá-lo a começar. Por exemplo, posso gerar:

1.  A estrutura básica de um app `accounts` com o modelo de usuário.
2.  Uma view e template simples para a página de login.
3.  A configuração de URL correspondente.

Você gostaria de ver exemplos de código para uma parte específica, como a configuração inicial da página de login dentro de uma estrutura Django? Isso poderia incluir:

*   `accounts/models.py` (com um `CustomUser` básico)
*   `accounts/forms.py` (com um `LoginForm`)
*   `accounts/views.py` (com uma `login_view` simples)
*   `accounts/templates/accounts/login.html` (um template básico de login)
*   `accounts/urls.py` e a inclusão no `urls.py` do projeto.

Me diga como você gostaria de prosseguir!<!-- filepath: c:\Users\jerff_xm9xnz6\OneDrive\VS Code\Projects\SociosCasaDaUniao\IDEA.MD -->
# Idealização da Aplicação Web (Django-only)

A estrutura da aplicação seguirá uma arquitetura monolítica com o Django, onde o framework cuidará tanto da lógica de backend (APIs, banco de dados, regras de negócio) quanto da renderização do frontend (páginas HTML, formulários).

## Estrutura Geral de Arquivos (Django):

O código do projeto Django residirá em um diretório principal. A estrutura básica incluirá:

*   **Projeto Raiz (Ex:** `SociosCasaDaUniao`**)**
    *   `manage.py`: Utilitário de linha de comando do Django.
    *   `nome_do_projeto/` (diretório de configuração do projeto, ex: `config/` ou `SociosCasaDaUniao_project/`)
        *   `settings.py`: Configurações do projeto Django (INSTALLED_APPS, DATABASES, MIDDLEWARE, TEMPLATES, STATICFILES_DIRS, etc.).
        *   `urls.py`: Configuração de URL raiz do projeto.
        *   `wsgi.py`, `asgi.py`: Pontos de entrada para servidores WSGI/ASGI.
    *   `requirements.txt`: Lista de dependências Python (Django, Pillow, etc.).
    *   `apps/` (diretório opcional para agrupar os apps Django)
        *   `accounts/` (App para gerenciamento de usuários, autenticação, perfis)
            *   `models.py`: Modelo de usuário customizado.
            *   `views.py`: Lógica para login, logout, cadastro, recuperação de senha, perfil.
            *   `forms.py`: Formulários Django para login, cadastro, edição de perfil.
            *   `urls.py`: URLs específicas do app `accounts`.
            *   `templates/accounts/`: Templates HTML para as páginas de `accounts` (ex: `login.html`, `register.html`, `profile.html`).
            *   `static/accounts/`: Arquivos estáticos específicos do app (CSS, JS, imagens).
        *   `core/` (App para funcionalidades centrais, página inicial pós-login, etc.)
            *   `views.py`: Lógica para a página home, dashboard.
            *   `urls.py`: URLs do app `core`.
            *   `templates/core/`: Templates HTML para o app `core` (ex: `home.html`, `base.html`).
            *   `static/core/`: Arquivos estáticos do app `core`.
        *   `activities/`, `rifas/`, `caronas/` (Outros apps conforme necessidade, cada um com sua estrutura de `models.py`, `views.py`, `forms.py`, `urls.py`, `templates/app_name/`, `static/app_name/`)
    *   `templates/` (Diretório no nível do projeto para templates globais, como `base.html`, `404.html`, `500.html`)
    *   `static/` (Diretório no nível do projeto para arquivos estáticos globais - CSS, JS, imagens. Configurado em `STATICFILES_DIRS`)

## Detalhamento das Páginas e Funcionalidades (Implementação com Django):

1.  **Página Inicial / Login (`/login/` ou `/` se não autenticado):**
    *   **Propósito:** Ponto de entrada para usuários não autenticados.
    *   **View Django:** `accounts.views.LoginView` (pode ser uma `LoginView` customizada ou a `django.contrib.auth.views.LoginView`).
    *   **Template Django:** `accounts/login.html`.
    *   **Formulário Django:** `accounts.forms.LoginForm` (pode usar `django.contrib.auth.forms.AuthenticationForm`).
    *   **Conteúdo:** Um contêiner centralizado, contendo:
        *   Logo da instituição.
        *   Formulário de Login: Campos para Telefone (ou username/email) e Senha.
        *   Botões: "Login" (submete o formulário para a `LoginView`), "Cadastre-se" (link para a página de cadastro), "Recuperar Acesso" (link para a página de recuperação).
    *   **Funcionalidades:**
        *   A `LoginView` processa os dados do formulário.
        *   Em caso de sucesso, autentica o usuário e redireciona para a Página Home (`/home/`).
        *   Em caso de falha, re-renderiza `login.html` com mensagens de erro.
    *   **Navegação:** Links usando a tag `{% url 'nome_da_rota' %}` nos templates.
    *   **Layout:** O `login.html` pode estender um `base_public.html` ou similar, que inclui o Cabeçalho ("Centro Espirita Beneficente União do Vegetal - Núcleo Natal") e o Rodapé ("© 1961 a 2025...").

2.  **Página de Cadastro (`/register/`):**
    *   **Propósito:** Permitir que novos usuários criem uma conta.
    *   **View Django:** `accounts.views.RegisterView` (uma view customizada que lida com a criação do usuário).
    *   **Template Django:** `accounts/register.html`.
    *   **Formulário Django:** `accounts.forms.UserRegisterForm` (um `ModelForm` baseado no modelo de usuário customizado, ou um `UserCreationForm` customizado).
    *   **Conteúdo:** Formulário de cadastro com os campos necessários.
    *   **Funcionalidades:**
        *   A `RegisterView` processa o formulário.
        *   Em caso de sucesso, cria o novo usuário e redireciona (ex: para a página de login ou uma página de sucesso).
        *   Em caso de falha, re-renderiza `register.html` com mensagens de erro.

3.  **Página de Recuperação de Acesso (`/password_reset/`, etc.):**
    *   **Propósito:** Permitir que usuários recuperem o acesso à conta.
    *   **Views Django:** Utilizar as views embutidas do Django em `django.contrib.auth.views` (ex: `PasswordResetView`, `PasswordResetDoneView`, `PasswordResetConfirmView`, `PasswordResetCompleteView`).
    *   **Templates Django:** Criar os templates correspondentes (ex: `accounts/password_reset_form.html`, `accounts/password_reset_done.html`, etc.) conforme a documentação do Django.
    *   **Formulários Django:** As views embutidas utilizam formulários como `PasswordResetForm` e `SetPasswordForm`.
    *   **Conteúdo/Funcionalidades:** Fluxo padrão de reset de senha (solicitar email/usuário, enviar email com link, permitir definir nova senha).

4.  **Página Home (`/home/` ou `/dashboard/`):**
    *   **Propósito:** Área principal para usuários autenticados.
    *   **View Django:** `core.views.HomePageView` (ou `dashboard.views.DashboardView`).
    *   **Template Django:** `core/home.html` (ou `dashboard/dashboard.html`).
    *   **Layout:** Estrutura com um Painel Lateral (Sidebar) e uma área de Conteúdo Principal, implementados diretamente no HTML do template ou com `includes` (ex: `{% include 'includes/sidebar.html' %}`).
    *   **Acesso:** Restrita a usuários autenticados usando o decorator `@login_required` ou o `LoginRequiredMixin` na view.
    *   **Funcionalidades:** A `HomePageView` pode buscar dados relevantes para o usuário e passá-los para o template `home.html`. O template exibirá esses dados e os links de navegação no painel lateral. Diferentes seções da "Home" podem ser URLs distintas que renderizam templates diferentes ou a mesma view que renderiza seções diferentes condicionalmente.

5.  **Painel Lateral (Sidebar) na Página Home:**
    *   **Implementação:** Parte do template `core/home.html` ou um template separado incluído (ex: `includes/sidebar.html`).
    *   **Conteúdo:**
        *   Área para foto de perfil do usuário logado (acessível via `request.user` no template).
        *   Lista de menus de navegação (Meu Perfil, Atividades, Rifas, Caronas, Assistência) como links `<a>` usando `{% url %}`.
    *   **Menus/Submenus:** Implementados com HTML e CSS. A lógica para exibir/ocultar submenus pode ser feita com JavaScript simples (Vanilla JS) se necessário, ou puramente CSS.

6.  **Outras Funcionalidades (Calendário, Editar Perfil, Quadro de Sócios, etc.):**
    *   Cada funcionalidade principal teria seu próprio conjunto de:
        *   **Views Django:** Para processar requisições e buscar/salvar dados.
        *   **Templates Django:** Para exibir a interface da funcionalidade.
        *   **Formulários Django:** Para entrada de dados.
        *   **URLs:** Mapeando para as views correspondentes.
    *   Por exemplo, "Editar Perfil" seria uma view em `accounts.views` com um template `accounts/profile_edit.html` e um `ModelForm` para o modelo de usuário.

**Considerações Adicionais para Django-only:**

*   **Arquivos Estáticos:** CSS, JavaScript (para interatividade leve), e imagens serão gerenciados pelo `django.contrib.staticfiles`.
*   **Interatividade:** Para interações dinâmicas sem recarregar a página inteira (ex: atualizar uma parte de uma tabela), pode-se usar JavaScript (Vanilla JS ou bibliotecas como HTMX ou Alpine.js) para fazer requisições AJAX para views Django que retornam fragmentos de HTML ou JSON.
*   **Notificações:** Podem ser implementadas usando o `django.contrib.messages` framework para mensagens flash, ou com JavaScript para notificações mais dinâmicas no navegador (possivelmente com AJAX para buscar novas notificações).
