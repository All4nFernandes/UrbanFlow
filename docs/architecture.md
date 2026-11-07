# UrbanFlow — arquitetura inicial simplificada

## Estrutura

Começaremos com um monólito Django renderizado no servidor. O primeiro app é `accounts`, que concentra usuário customizado, autenticação, papéis e painel. A criação de chamados/mapa entra em seguida como domínio próprio, sem misturar seus modelos ao app de contas.

```text
UrbanFlow/
  manage.py
  urbanflow/                 # settings e URLs do projeto Django
  accounts/                  # usuários, papéis, login e painel
  templates/accounts/        # templates de autenticação e painéis
  db.sqlite3                 # banco local criado por Django
```

## Stack

- Python 3.12 e Django 5.2 LTS.
- Templates Django para interface responsiva; Leaflet para o mapa.
- SQLite local para começar sem instalar outro servidor.
- PostgreSQL + PostGIS como banco de produção, quando o fluxo básico estiver pronto.

## Papéis e acesso

| Ação | Requerente | Fiscal/auditor | Superuser |
|---|---:|---:|---:|
| Criar chamado | Sim | Não | Sim |
| Ver detalhes dos próprios | Sim | Sim | Sim |
| Ver status público de outros | Sim | Sim | Sim |
| Ver todos e relatórios | Não | Sim | Sim |
| Excluir dados | Não | Não | Sim |
| Gerenciar usuários/departamentos | Não | Não | Sim |

O usuário terá um campo `role` com `requester`, `auditor` ou `superuser`. O limite de quatro fiscais e um superuser é global nesta instalação. A tela de cadastro público nunca permitirá escolher ou alterar o próprio papel; esse controle fica restrito à administração.

## Telas e autorização

- Um painel escolhe o template ou os blocos correspondentes ao papel do usuário.
- As views verificam autenticação, papel, propriedade do chamado e ação permitida antes de ler ou alterar dados.
- Requerente recebe detalhes completos somente dos próprios chamados; a consulta pública retorna campos mínimos e status.
- Fiscal tem leitura ampla, sem rotas de exclusão.
- Superuser acessa ações administrativas. Exclusões devem gerar registro de auditoria; preferir exclusão lógica.

Mostrar/esconder menus nos templates melhora a experiência, mas não protege uma rota. Cada view precisa negar uma requisição sem permissão.

## Mapa e coordenadas

Leaflet fornece o ponto do clique (`e.latlng`). No MVP, o formulário envia latitude e longitude à view; Django valida os intervalos e os armazena em campos decimais. O mapa consulta apenas os dados que o papel pode ver. Ao migrar para PostGIS, converteremos os pontos para geometria SRID 4326 e criaremos índice espacial.

## Banco e migrações

Django será a fonte única do schema. Criar `accounts.User` herdando de `AbstractUser` e configurar `AUTH_USER_MODEL` antes de executar a primeira migração. Não aplicar SQL manual paralelo. O arquivo SQL antigo está desativado; substituiremos a modelagem por modelos e migrações Django.

SQLite torna a primeira instalação local simples, mas não é o banco final de uma implantação urbana em larga escala. Antes de produção, migrar para PostgreSQL/PostGIS, configurar credenciais por variáveis de ambiente e confirmar backups, restauração, logs, retenção e limites de taxa.

## Ordem de implementação

1. Instalar Django no `.venv` e criar o projeto.
2. Criar `accounts`, usuário customizado, admin e migrações iniciais.
3. Implementar login/logout e painéis por papel.
4. Adicionar models, formulários e views de chamados com autorização.
5. Integrar Leaflet e captura do clique.
6. Criar departments e administração restrita ao superuser.
7. Planejar a migração para PostgreSQL/PostGIS e implantação.

