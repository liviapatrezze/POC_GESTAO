from django.contrib import admin
from django.urls import path, include

# Importa as URLs da nossa API REST.
# A API ficará disponível através do prefixo /api/
from core.api_urls import urlpatterns as api_urlpatterns


# Configurações de arquivos de mídia
from django.conf import settings
from django.conf.urls.static import static


# ============================================================
# ROTAS PRINCIPAIS DO SISTEMA
# ============================================================

urlpatterns = [

    # ========================================================
    # DJANGO ADMIN
    # ========================================================
    # Endereço:
    # /admin/
    #
    # Permite administrar os dados através do painel
    # administrativo do Django.
    # ========================================================
    path("admin/", admin.site.urls),


    # ========================================================
    # PÁGINAS HTML DO SISTEMA
    # ========================================================
    # Estas são as páginas que já existiam no projeto.
    #
    # Exemplos:
    # /alunos/
    # /alunos/novo/
    # /esportes/
    #
    # Responsabilidade relacionada às páginas do sistema.
    # ========================================================
    path("", include("core.urls")),


    # ========================================================
    # API REST
    # ========================================================
    # Todas as rotas da API começarão com:
    #
    # /api/
    #
    # Exemplos:
    #
    # /api/alunos/
    # /api/esportes/
    # /api/professores/
    # /api/horarios/
    # /api/participacoes/
    # /api/convites/
    #
    # O frontend deverá utilizar essas URLs para conversar
    # com o backend.
    #
    # IMPORTANTE:
    # O frontend NÃO acessa o banco de dados diretamente.
    # Ele faz requisições para a API.
    #
    # A configuração definitiva do banco de dados ficará
    # sob responsabilidade do integrante responsável pelo banco.
    # ========================================================
    path("api/", include(api_urlpatterns)),
]


# ============================================================
# ARQUIVOS DE MÍDIA
# ============================================================
#
# Durante o desenvolvimento, o Django utiliza esta
# configuração para permitir que as imagens armazenadas
# na pasta "media/" sejam exibidas no navegador.
#
# Estrutura esperada:
#
# media/
# ├── alunos/
# ├── esportes/
# └── professores/
#
# Esta configuração é utilizada somente quando DEBUG=True.
# ============================================================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )