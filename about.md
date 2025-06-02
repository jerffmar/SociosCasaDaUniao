# Página Inicial (/index)

A página inicial é uma tela de login simples, com:
- Logo central da instituição.
- Campos: **Telefone** e **Senha**.
- Botões: **Login**, **Cadastre-se**, **Recuperar Acesso**.

**Cabeçalho:**  
Centro Espírita Beneficente União do Vegetal - Núcleo Natal

**Rodapé:**  
© 1961 a 2025 - Centro Espírita Beneficente União do Vegetal - Núcleo Natal. Rua Lote 35 a (Chacara Grande Navio) Nisia Floresta - RN, 59.164-000

> Apenas as páginas "Cadastre-se" e "Recuperar acesso" são visíveis para não autenticados.

---

# Página Home (/home)

Acesso restrito a usuários autenticados. Não autenticados são redirecionados para a página inicial.

## Estrutura

- **Menu lateral:** Ícone de perfil que exibe:
    - Foto do usuário.
    - Menus:
        - **Meu Perfil:** Editar dados pessoais (Nome, Telefone, Gênero, Data de Nascimento, CPF). Campos Cargo, Grau e Equipe são atribuídos por administradores (Mestre Representante, Mestre-Assistente, Presidente).
        - **Atividades:**
            - **Calendário:** Mostra sessões agendadas. Selecionando uma data, exibe detalhes do evento e permite confirmar presença. Se o usuário for da equipe do evento, pode escolher Escala e Lanche.
            - **Minha Equipe:** Exibe membros e graus da equipe do usuário. Se não houver equipe, mostra aviso.
            - **Escalas:** Abas com atividades, mostrando detalhes como descrição, período, horários e nível.
            - **Agendar Evento** (Mestre Assistente): Botões para criar Sessão, Mutirão, Preparo ou Evento, com formulário detalhado.
            - **Editar Escalas** (Mestre Assistente/Orgã): Formulário para adicionar/editar escalas, com campos de nome, descrição, horários, período e nível.
            - **Editar Equipes** (Mestre Assistente/Orgã): Três tabelas para gerenciar membros das equipes, com opção de mover usuários entre equipes.
        - **Rifas:** Listagem e cadastro de rifas.
        - **Caronas:** Buscar ou oferecer carona.
        - **Assistência** (Mestre Assistente/Representante):
            - **Quadro de Sócios:** Tabela de usuários, cargos, equipes e graus, com edição.
            - **Relatório de Eventos:** Lista de eventos realizados, participantes e contribuições.

**Cabeçalho e rodapé** 

iguais à página inicial. Permanente para todas as páginas.

**Conteúdo principal:**

Calendário do mês atual com sessões agendadas. Balão Lateral com cerca de 1/3 da área total do conteúdo contendo notificações. Balão no rodapé do calendário com conteúdo dinâmico conforme seleção das datas do usuário.

