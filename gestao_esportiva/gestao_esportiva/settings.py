"""
Django settings for gestao_esportiva project.

Configurações principais do sistema de gestão esportiva.
"""


from pathlib import Path


# ============================================================
# CONFIGURAÇÃO GERAL DO PROJETO
# ============================================================

# Caminho principal do projeto.
# Usado para localizar banco de dados, arquivos de mídia, etc.
BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SEGURANÇA
# ============================================================

# Chave de segurança do Django.
# NÃO compartilhar esta chave em projetos publicados na internet.
SECRET_KEY = 'django-insecure-oqr+_^896vvxzz9kubb)3w46-4f3dg(u83du=5ykri#&^4(pw)'


# True = modo de desenvolvimento
# False = usar quando o sistema estiver em produção.
DEBUG = True


# Endereços permitidos para acessar o sistema.
# Durante o desenvolvimento local podemos deixar vazio.
ALLOWED_HOSTS = []


# ============================================================
# APLICATIVOS INSTALADOS
# ============================================================

INSTALLED_APPS = [

    # Administração do Django
    'django.contrib.admin',

    # Sistema de usuários/autenticação
    'django.contrib.auth',

    # Sistema de tipos de conteúdo
    'django.contrib.contenttypes',

    # Sessões de usuários
    'django.contrib.sessions',

    # Sistema de mensagens
    'django.contrib.messages',

    # Arquivos estáticos (CSS, JavaScript etc.)
    'django.contrib.staticfiles',

    # ========================================================
    # DJANGO REST FRAMEWORK
    # ========================================================
    # Biblioteca utilizada para construir a API REST
    # do sistema.
    #
    # A API será utilizada posteriormente pelo FRONTEND
    # para enviar e receber dados do BACKEND.
    #
    # RESPONSÁVEL: BACKEND
    # ========================================================
    'rest_framework',


    # Aplicação principal do nosso sistema
    'core',
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [

    # Segurança
    'django.middleware.security.SecurityMiddleware',

    # Sessões
    'django.contrib.sessions.middleware.SessionMiddleware',

    # Recursos HTTP comuns
    'django.middleware.common.CommonMiddleware',

    # Proteção contra CSRF
    'django.middleware.csrf.CsrfViewMiddleware',

    # Autenticação dos usuários
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # Mensagens do sistema
    'django.contrib.messages.middleware.MessageMiddleware',

    # Proteção contra carregamento da página em iframe
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================================================
# CONFIGURAÇÃO DE URLS
# ============================================================

# Arquivo principal de URLs do projeto.
ROOT_URLCONF = 'gestao_esportiva.urls'


# ============================================================
# CONFIGURAÇÃO DOS TEMPLATES / FRONTEND
# ============================================================

TEMPLATES = [

    {
        # Sistema de templates utilizado pelo Django
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Diretórios adicionais para templates.
        # Podemos adicionar uma pasta "templates" futuramente.
        'DIRS': [],

        # Procura templates dentro das aplicações.
        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                # Permite acessar informações da requisição
                # dentro dos templates.
                'django.template.context_processors.request',

                # Informações do usuário autenticado
                'django.contrib.auth.context_processors.auth',

                # Mensagens do sistema
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ============================================================
# SERVIDOR
# ============================================================

WSGI_APPLICATION = 'gestao_esportiva.wsgi.application'


# ============================================================
# BANCO DE DADOS
# ============================================================

# Atualmente estamos utilizando SQLite.
#
# Futuramente podemos trocar para MySQL ou PostgreSQL
# se o projeto precisar.

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.sqlite3',

        # Arquivo do banco de dados
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ============================================================
# VALIDAÇÃO DE SENHAS
# ============================================================

# Regras utilizadas pelo Django para validar senhas.

AUTH_PASSWORD_VALIDATORS = [

    # Evita senhas muito parecidas com dados do usuário
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    # Exige tamanho mínimo
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    # Evita senhas muito comuns
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    # Evita senhas somente numéricas
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ============================================================
# IDIOMA E HORÁRIO
# ============================================================

# Idioma padrão do sistema.
LANGUAGE_CODE = 'en-us'

# Fuso horário de São Paulo - Brasil.
TIME_ZONE = 'America/Sao_Paulo'

# Ativa internacionalização.
USE_I18N = True

# Ativa suporte a fusos horários.
USE_TZ = True


# ============================================================
# ARQUIVOS ESTÁTICOS - FRONTEND
# ============================================================

# Arquivos utilizados pelo frontend:
#
# CSS
# JavaScript
# Ícones
# Outros arquivos estáticos

STATIC_URL = 'static/'


# ============================================================
# ARQUIVOS DE MÍDIA - UPLOADS
# ============================================================

# URL utilizada para acessar arquivos enviados pelos usuários.
#
# Exemplos:
# /media/alunos/foto.jpg
# /media/esportes/futebol.jpg
# /media/professores/professor.jpg

MEDIA_URL = '/media/'


# Pasta física onde as imagens serão armazenadas.
#
# Estrutura esperada:
#
# media/
# ├── alunos/
# ├── esportes/
# └── professores/

MEDIA_ROOT = BASE_DIR / 'media'


# ============================================================
# AUTENTICAÇÃO
# ============================================================

# Página de login do sistema
LOGIN_URL = '/login/'

# Página para onde o usuário será enviado após o login
LOGIN_REDIRECT_URL = '/'

# Página para onde o usuário será enviado após sair
LOGOUT_REDIRECT_URL = '/login/'