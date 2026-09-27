# POC Gestão

Monolito em um repositório: API Django em `back` e interface Next.js em `front`. O navegador fala com o Next na porta 3000; o Next encaminha `/api/*` para o Django na porta 8000.

## Back

```bash
cd back
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Ambientes: `config.settings.dev` (padrão), `config.settings.test` e `config.settings.prod`.

```bash
DJANGO_SETTINGS_MODULE=config.settings.test python manage.py test
```

## Front

```bash
cd front
npm install
npm run dev
```

A URL da API vem de `API_URL` (padrão `http://127.0.0.1:8000`). O exemplo está em `front/.env.example`.

Abra `http://localhost:3000`. A página mostra o healthcheck e o CRUD de itens.
