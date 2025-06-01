# Estrutura da Plataforma de Gestão para União do Vegetal

Este documento descreve a estrutura proposta de arquivos e diretórios para a plataforma de gestão da União do Vegetal, baseada em uma arquitetura **desacoplada** utilizando **Django como backend (API)** e **React como frontend**.

A estrutura visa manter uma separação clara entre a lógica de negócio e a interface do usuário, facilitando a manutenção e a evolução do projeto.

## Estrutura de Arquivos

### Backend (Django)

O backend Django será responsável por gerenciar o banco de dados, a autenticação, as regras de negócio e fornecer uma API RESTful para o frontend.

*   **Projeto Raiz (Ex:** `djangoreactproject` ou `SociosCasaDaUniao`**)**
    *   `.gitignore`: Especifica arquivos e diretórios a serem ignorados pelo Git.
    *   `manage.py`: Utilitário de linha de comando do Django para tarefas administrativas.
    *   `backend/`: Diretório raiz do projeto Django.
        *   `__init__.py`: Indica que `backend` é um pacote Python. Pode importar a instância Celery.
        *   `settings.py`: Arquivo principal de configuração do Django.
            *   Define `INSTALLED_APPS` para incluir apps do Django, apps de terceiros (como `rest_framework`, `corsheaders`) e apps customizados (`accounts`, `activities`, etc.).
            *   Configura `MIDDLEWARE`, incluindo `corsheaders.middleware.CorsMiddleware` para requisições cross-origin (CORS).
            *   Define configurações de `CORS`, como `CORS_ALLOWED_ORIGINS` ou `CORS_ORIGIN_WHITELIST`, para permitir comunicação com o frontend React.
            *   Configura o **Modelo de Usuário Customizado** (`AUTH_USER_MODEL`).
            *   Define configurações do **Django REST Framework** (`REST_FRAMEWORK`), incluindo classes de autenticação (ex: `JWTAuthentication`).
            *   Define configurações do **JWT** (`SIMPLE_JWT`).
            *   Configurações do **Celery** (broker, backend).
        *   `urls.py`: Configuração de URL raiz do Django.
            *   Inclui URLs do Django admin.
            *   Pode incluir URLs de autenticação do DRF (opcional).
            *   Inclui URLs dos apps customizados (accounts, activities, etc.) usando `include()`.
            *   Pode incluir URLs específicas do JWT (como `/api/token/` e `/api/token/refresh/`).
        *   `wsgi.py`: Ponto de entrada WSGI.
        *   `celery.py`: Configuração da instância **Celery**.
        *   `accounts/`: App Django para Gerenciamento de Usuários e Autenticação.
            *   `models.py`: Define o **Modelo de Usuário Customizado** (CustomUser), herdando de AbstractUser, com campos como username, email, phone, gender, date_of_birth, CPF, **Cargo**, **Grau** e **Equipe**.
            *   `serializers.py`: Define **Serializers** para **Registro**, **Login**, **Perfil de Usuário** e outros (com campos controlados por permissão).
            *   `views.py`: Implementa **Visualizações da API** para **Registro**, **Login** (retornando tokens JWT), **Logout**, **Obtenção/Atualização do Perfil do Usuário logado** e **de outros usuários** (com controle de permissão).
            *   `urls.py`: Define **endpoints de URL** para as visualizações da API em `accounts/`.
            *   `admin.py`: Registra modelos e formulários para o admin do Django, incluindo o modelo de usuário customizado.
            *   `forms.py`: Define formulários customizados para o admin (ex: CustomUserCreationForm).
        *   `activities/`: App Django para Gerenciamento de Atividades, Escalas e Equipes.
            *   `models.py`: Define modelos para **Eventos**, **Escalas**, **Equipes** e modelos intermediários para participação de usuários.
            *   `serializers.py`: Define **Serializers** para Eventos, Escalas, Equipes e dados de participação.
            *   `views.py`: Implementa **Visualizações da API** para CRUD de Eventos, Escalas, Equipes, listagem filtrada de eventos, confirmação de presença, seleção de itens de escala/lanche, listagem de membros de equipe, Quadro de Sócios, edição de atributos de sócios (Cargo, Equipe, Grau), Relatórios de Eventos. Implementa controle de permissão e pode chamar tarefas Celery.
            *   `urls.py`: Define **endpoints de URL** para as visualizações da API em `activities/`.
        *   `rifas/`: App Django para Gerenciamento de Rifas.
            *   `models.py`: Define o modelo para **Rifas**.
            *   `serializers.py`: Define o **Serializer** para Rifas.
            *   `views.py`: Implementa **Visualizações da API** para listar e cadastrar Rifas.
            *   `urls.py`: Define **endpoints de URL** para as APIs em `rifas/`.
        *   `caronas/`: App Django para Gerenciamento de Caronas.
            *   `models.py`: Define o modelo para **Caronas**.
            *   `serializers.py`: Define o **Serializer** para Caronas.
            *   `views.py`: Implementa **Visualizações da API** para listar ofertas/buscas de carona e criar novas.
            *   `urls.py`: Define **endpoints de URL** para as APIs em `caronas/`.
        *   `tasks/`: App ou módulo para Tarefas Assíncronas com Celery.
            *   `tasks.py`: Define **tarefas assíncronas** usando `@shared_task`. Exemplos: envio de notificações.

### Frontend (React)

O frontend React será responsável pela interface do usuário, consumindo a API fornecida pelo backend Django.

*   `frontend/`: Diretório raiz do aplicativo React.
    *   `package.json`: Configuração do Node.js/NPM/Yarn. Lista dependências (react, axios, react-router-dom, bootstrap, etc.) e scripts (start, build). Pode incluir proxy para API em desenvolvimento.
    *   `public/`: Diretório para arquivos estáticos públicos (ex: `index.html`, favicon).
        *   `index.html`: Arquivo HTML principal onde o aplicativo React é renderizado. Pode incluir links para CSS externo.
    *   `src/`: Diretório do código fonte do React.
        *   `index.js`: Ponto de entrada do aplicativo React. Renderiza o componente App no DOM. Pode importar estilos globais.
        *   `App.js`: Componente principal do aplicativo React. Configura o **roteamento** usando `react-router-dom`. Define as rotas principais.
        *   `index.css`: Estilos CSS globais.
        *   `App.css`: Estilos CSS específicos do layout principal. Pode importar Bootstrap CSS.
        *   `pages/`: Diretório contendo os componentes das páginas principais.
            *   `LoginPage.js`: Interface da **Página de Login**. Contém formulário (Telefone, Senha), botões (Login, Cadastre-se, Recuperar Acesso). Chama API de login.
            *   `RegisterPage.js`: **Página de Cadastro**. Contém formulário. Chama API de registro.
            *   `RecoverAccessPage.js`: **Página de Recuperação de Acesso**.
            *   `HomePage.js`: **Página Home** (restrita a usuários autenticados). Gerencia a exibição do painel lateral e área de conteúdo principal com base nas sub-rotas. Inclui logout.
        *   `components/`: Diretório para componentes reutilizáveis e componentes específicos de funcionalidades.
            *   `Layout.js`: Componente de layout base (cabeçalho, rodapé, área de conteúdo).
            *   `Header.js`: **Cabeçalho** estático.
            *   `Footer.js`: **Rodapé** estático.
            *   `Sidebar.js`: **Painel lateral** da Home. Exibe foto de perfil e menus/submenus (Meu Perfil, Atividades, Rifas, Caronas, Assistência). Visibilidade controlada pelo **Cargo**.
            *   `HomeContent.js`: Renderiza o conteúdo da área principal da Home com base na rota ativa.
            *   `ProfileForm.js`: Formulário para **Editar Perfil**. Campos pessoais editáveis pelo usuário, campos administrativos (**Cargo**, **Grau**, **Equipe**) editáveis apenas por usuários com privilégios.
            *   `CalendarView.js`: Componente para exibir o **Calendário**. Busca eventos agendados. Permite clicar nas datas.
            *   `EventDetails.js`: Exibe **detalhes de um evento**. Lógica para confirmar presença e selecionar itens de escala/lanche (dropdowns).
            *   `TeamMembersList.js`: Exibe tabela de membros da **Minha Equipe**.
            *   `ScalesListView.js`: Exibe as **Escalas** cadastradas.
            *   `ScheduleEventForm.js`: Formulário para **Agendar Evento** (visível para Mestre Assistente).
            *   `EditScalesForm.js`: Formulário para **Editar Escalas** (visível para Mestre Assistente ou Orgã).
            *   `EditTeamsView.js`: Componente para **Editar Equipes** (visível para Mestre Assistente ou Orgã). Exibe tabelas das equipes e permite mover sócios.
            *   `RifasList.js`: Lista as **Rifas** disponíveis.
            *   `AddRifaForm.js`: Formulário para **Cadastrar Rifa**.
            *   `FindRide.js`: Interface para **Buscar Carona**.
            *   `OfferRide.js`: Interface para **Oferecer Carona**.
            *   `MembersTable.js`: Tabela do **Quadro de Sócios** (visível para Mestre Assistente e Mestre Representante). Exibe todos os sócios com campos editáveis (Cargo, Equipe, Grau).
            *   `EventReports.js`: Exibe o **Relatório de Eventos**.
            *   `Modal.js`: Componente genérico para exibir **modais**.
            *   `Table.js`: Componente reutilizável para renderizar **tabelas**.
            *   `Form.js`: Componente genérico ou utilitários para **formulários** (pode usar React Hook Form).
            *   `Button.js`: Componente reutilizável para **botões**.
            *   `Dropdown.js`: Componente reutilizável para menus **dropdown**.
            *   `DatePicker.js`/`TimePicker.js`: Componentes para seleção de **data e hora** (pode usar Material UI X Pickers).
            *   `NotificationDisplay.js`: Componente para exibir **notificações no navegador**.
        *   `services/`: Diretório contendo a lógica para chamadas de API.
            *   `apiService.js`: Arquivo(s) centralizado(s) para realizar **requisições HTTP** (usando Axios) para o backend. Inclui lógica para adicionar **token JWT** nos cabeçalhos.
        *   `context/`: Diretório para Contextos do React ou gerenciamento de estado.
            *   `AuthContext.js`: Usa Context API ou biblioteca de gerenciamento de estado para gerenciar o **estado de autenticação** do usuário (logado/deslogado, dados do usuário, tokens).
        *   `utils/`: Diretório para funções utilitárias.
            *   `notifications.js`: Lógica para solicitar permissão e disparar **notificações no navegador**.
        *   `assets/`: Diretório para arquivos de mídia (imagens, ícones, etc.).

Esta estrutura detalha os principais arquivos e componentes necessários, seguindo a abordagem desacoplada e incorporando as funcionalidades descritas para a plataforma.