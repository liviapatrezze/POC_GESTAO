# POC Gestão

Monolito em um único repositório. A interface fica em `front`, a API em `back` e o banco sobe com Docker Compose. Em desenvolvimento são três processos: Postgres, Django e Next.js.

## Stacks

| Parte | Tecnologia | Papel |
| --- | --- | --- |
| Front | Next.js 16, React 19, TypeScript | Páginas e chamadas à API |
| Back | Python 3, Django 5.2, Django REST Framework | API JSON, modelos e migrações |
| Banco | PostgreSQL 17 (imagem `postgres:17-alpine`) | Dados de desenvolvimento |
| Acesso ao banco | psycopg 3 | Driver usado pelo Django |
| Dev | Docker Compose e o launch **Start** do Cursor | Sobe os três processos juntos |

Os testes do Django usam SQLite em memória. O Postgres é o banco de desenvolvimento e o previsto para produção.

## Como tudo se conecta

O navegador só fala com o Next, em `http://localhost:3000`. Pedidos que começam com `/api` são encaminhados pelo Next para o Django em `http://127.0.0.1:8000`. O Django lê e grava no Postgres publicado na porta **5433** do host.

```text
Navegador
  │  http://localhost:3000
  ▼
Next.js (front)
  │  rewrite /api/*  →  http://127.0.0.1:8000/api/*
  ▼
Django (back)
  │  psycopg, banco poc_gestao, usuário poc
  ▼
Postgres (Docker, porta 5433)
```

A porta do host é 5433, não 5432, para não disputar com outro Postgres que já esteja nessa máquina. Dentro do container o Postgres continua na 5432. O mapeamento está em `docker-compose.yml`.

Há dois caminhos até a API:

- No navegador, `fetch("/api/...")` passa pelo rewrite do Next (`front/next.config.ts`). A variável `API_URL` (padrão `http://127.0.0.1:8000`) define o destino.
- Na renderização do servidor Next, a mesma função chama o Django direto em `API_URL`, sem voltar para a porta 3000.

O Django aceita as rotas da API com e sem barra no final, porque o proxy do Next pode entregar o `POST` sem a barra.

## Estrutura

```text
POC_GESTAO/
  docker-compose.yml          Postgres
  .vscode/launch.json         Launch Start, Postgres, Back e Front
  back/
    manage.py
    requirements.txt
    .env.example
    config/settings/          base, dev, test e prod
    apps/health/              GET /api/health/
    apps/hello/               GET /api/hello/  (Hello, world gravado na migração)
    apps/items/               CRUD /api/items/
  front/
    app/                      Página inicial
    components/               Formulário, lista e quadro de itens
    lib/api.ts                Chamadas tipadas
    .env.example              API_URL
```

## Pré-requisitos

- Docker com Docker Compose
- Python 3
- Node.js com npm

Credenciais locais do banco, iguais no Compose e no Django de desenvolvimento:

| Variável | Valor |
| --- | --- |
| Banco | `poc_gestao` |
| Usuário | `poc` |
| Senha | `poc` |
| Host | `127.0.0.1` |
| Porta no host | `5433` |

## Primeira execução

Na raiz do repositório:

```bash
docker compose up -d
```

Espere o healthcheck. Para conferir:

```bash
docker compose exec postgres pg_isready -U poc -d poc_gestao
```

API:

```bash
cd back
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

`migrate` cria as tabelas e grava a linha `Hello, world` em `apps.hello`. O arquivo `.env` é local e não entra no Git. Sem ele, o settings de desenvolvimento já usa os mesmos valores padrão do Compose.

Interface, em outro terminal:

```bash
cd front
npm install
npm run dev
```

Abra `http://localhost:3000`. A página mostra `Hello, world` vindo do Postgres, o status da API e o CRUD de itens.

## Pelo launch do Cursor

No painel **Run and Debug**, escolha **Start** e rode. Esse compound sobe, em paralelo:

1. **Postgres:** `docker compose up` na raiz. O log do banco fica nesse terminal. Parar o debug envia Ctrl+C para o Compose e encerra o container.
2. **Back:** espera `pg_isready` no container, roda `migrate` e sobe o Django em `127.0.0.1:8000`.
3. **Front:** `npm run dev` na porta 3000.

**Postgres**, **Back** e **Front** também existem sozinhos, se você quiser subir só uma parte. O virtualenv e o `npm install` precisam ter sido feitos antes; o launch não instala dependências.

## O que a tela faz

- **Hello, world:** a migração `back/apps/hello/migrations/0002_seed_hello.py` insere a mensagem. `GET /api/hello/` devolve `{ "mensagem": "Hello, world" }` e a página inicial exibe esse texto.
- **API: ok:** `GET /api/health/` devolve `{ "status": "ok" }`.
- **Itens:** criar, listar e excluir em `/api/items/`. Cada item tem título, descrição e data de criação.

## API

| Método | Caminho | Uso |
| --- | --- | --- |
| GET | `/api/health/` | Saúde da API |
| GET | `/api/hello/` | Mensagem gravada no Postgres |
| GET, POST | `/api/items/` | Lista e criação |
| GET, PUT, PATCH, DELETE | `/api/items/<id>/` | Um item |

O admin do Django fica em `http://127.0.0.1:8000/admin/`. Não há usuário criado. Para entrar:

```bash
cd back
source .venv/bin/activate
python manage.py createsuperuser
```

## Ambientes do Django

O módulo padrão é `config.settings.dev` (`manage.py` e `back/.env.example`).

| Módulo | Quando | Banco |
| --- | --- | --- |
| `config.settings.dev` | `runserver` local | Postgres em `127.0.0.1:5433` |
| `config.settings.test` | `manage.py test` | SQLite em memória |
| `config.settings.prod` | WSGI/ASGI | Variáveis de ambiente; `DEBUG` fica desligado |

Em produção, `SECRET_KEY` e `ALLOWED_HOSTS` são obrigatórios. O banco vem de `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` e `DB_PORT`. O modelo está em `back/.env.example`. Não use a senha `poc` fora da máquina local.

Testes:

```bash
cd back
source .venv/bin/activate
DJANGO_SETTINGS_MODULE=config.settings.test python manage.py test
```

No front:

```bash
cd front
npx tsc --noEmit
npm run lint
```

## Parar

Pelo launch, pare o debug **Start**. Isso encerra o Compose, o Django e o Next.

Pelo terminal:

```bash
docker compose down
```

`down` remove o container e mantém o volume `postgres-data`, então a mensagem e os itens continuam na próxima subida. Para apagar os dados também:

```bash
docker compose down -v
```

Na subida seguinte, `migrate` recria o schema e grava de novo o `Hello, world`.
