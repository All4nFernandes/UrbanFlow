# UrbanFlow

Sistema web para abertura e acompanhamento de chamados urbanos georreferenciados. A interface responsiva usa templates Django e Leaflet; o banco local usa SQLite. O desenvolvimento pode ser feito pelo VS Code, sem Docker.

## Estado do projeto

Implementado:
- Login por CPF ou nome de usuário e cadastro de requerentes.
- Papéis requester, auditor e superuser, com autorização nas views e no Django Admin.
- Painel com mapa, abertura de chamados, detalhes e status público.
- Edicao e exclusao de chamados somente pelo superuser; a exclusao exige confirmacao e envio por POST com CSRF.
- Seleção no mapa para preencher latitude e longitude.
- CSS e JavaScript da aplicação em arquivos estáticos.

Ainda planejado:
- Departamentos e encaminhamento de chamados.
- Limites automáticos de quantidade por papel.
- Relatórios dedicados, histórico, notificações e API REST.
- PostgreSQL/PostGIS e configuração de produção.

O limite de quatro fiscais e qualquer limite de superusers ainda não são aplicados pelo sistema.

## Tecnologias

- Python 3.12
- Django 5.2
- SQLite no desenvolvimento
- Leaflet e tiles do OpenStreetMap

O fluxo atual é navegador → URL Django → view → formulário/modelo → SQLite → template. Ainda não existe API REST. O mapa depende de conexão com a internet para carregar Leaflet e os tiles.

## Requisitos

- Windows com Python 3.12 instalado.
- Visual Studio Code com esta pasta aberta.
- Não é necessário instalar Docker, Docker Compose ou um servidor de banco.

## Instalação e execução no VS Code

Abra o terminal PowerShell integrado na raiz do projeto. Se ainda não houver ambiente virtual, crie-o:

    py -3.12 -m venv .venv

Ative o ambiente e instale as dependências:

    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt

Se o PowerShell bloquear a ativação, permita scripts apenas nesta sessão e tente novamente:

    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\.venv\Scripts\Activate.ps1

Prepare o banco e inicie o servidor:

    python manage.py check
    python manage.py migrate
    python manage.py runserver

Acesse http://127.0.0.1:8000/. Para encerrar o servidor, pressione Ctrl+C no terminal.

Quando modelos forem alterados, gere e aplique as migrações:

    python manage.py makemigrations
    python manage.py migrate

Não é necessário executar makemigrations a cada inicialização.

## Acesso administrativo

Se ainda não houver superuser, crie um após aplicar as migrações:

    python manage.py createsuperuser

O comando solicita usuário, e-mail, CPF e senha. A senha não aparece enquanto é digitada. O manager UrbanFlow atribui o papel superuser. Não crie outro se já houver uma conta administrativa.

Para redefinir a senha de uma conta:

    python manage.py changepassword Prefeitura01

Troque Prefeitura01 pelo nome de usuário correto.

## URLs

| Caminho | Uso |
| --- | --- |
| / | Redireciona para painel ou login |
| /login/ | Login por CPF ou usuário |
| /logout/ | Logout por POST com CSRF |
| /accounts/cadastro/ | Cadastro de requerente |
| /chamados/ | Painel e mapa |
| /chamados/novo/ | Abertura de chamado |
| /chamados/<id>/ | Detalhes ou status público |
| /chamados/<id>/editar/ | Edicao restrita ao superuser |
| /chamados/<id>/excluir/ | Confirmacao e exclusao restritas ao superuser |
| /admin/ | Administração do superuser |

Os templates usam nomes de rota Django, como cases:list, cases:create, login e logout, em vez de repetir caminhos fixos.

## Papéis atuais

| Papel | Acesso |
| --- | --- |
| requester | Abre chamados, vê os detalhes dos próprios e o status público dos demais |
| auditor | Consulta todos os chamados e o mapa; não gerencia dados no Django Admin |
| superuser | Cria, edita e exclui chamados; gerencia usuarios pelo Django Admin |

## Estrutura principal

    accounts/                 Usuários, autenticação e permissões
    cases/                    Chamados, views, formulários e templates
    cases/static/cases/css/   Estilos da interface
    cases/static/cases/js/    JavaScript dos mapas
    config/                   Settings e URLs do projeto
    database/                 Documentos do banco e material legado
    backups/                  Cópias locais de segurança
    manage.py                 Utilitário de gerenciamento Django
    requirements.txt          Dependências Python

O JavaScript da interface não fica embutido no HTML. case-form-map.js controla a seleção de localização e case-list-map.js desenha os marcadores. O template serializa os dados do mapa como JSON usando json_script.

## Banco e arquivos estáticos

O banco de desenvolvimento é db.sqlite3 e deve ser atualizado pelas migrações Django. Não execute o SQL legado em database/migrations/001_initial_schema.sql. A pasta backups/ é ignorada pelo Git; mantenha cópias importantes também fora do computador.

No desenvolvimento, o Django serve os arquivos estáticos. Em produção, configure armazenamento e entrega próprios e execute:

    python manage.py collectstatic

O uso dos tiles do OpenStreetMap em produção deve respeitar os termos e limites do provedor.

## Antes de produção

A configuração atual é apenas de desenvolvimento: DEBUG está ligado, SECRET_KEY está no arquivo, ALLOWED_HOSTS está vazio e o banco é SQLite. Não publique essa configuração como está.

Antes de disponibilizar o sistema:
1. Mova SECRET_KEY para variável de ambiente; desative DEBUG e configure ALLOWED_HOSTS.
2. Configure HTTPS, cookies seguros, CSRF, backups e recuperação.
3. Migre para PostgreSQL/PostGIS.
4. Implemente departamentos, encaminhamento e limites por papel.
5. Adicione testes automatizados, logs, monitoramento e processo de deploy.

Comandos úteis:

    python manage.py check
    python manage.py showmigrations
    python manage.py migrate
    python manage.py shell