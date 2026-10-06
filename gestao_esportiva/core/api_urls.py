# ============================================================
# ROTAS DA API
# ============================================================
# Este arquivo define os endereços que serão utilizados
# pelo frontend para acessar o backend.
#
# Exemplo:
#
# /api/alunos/
# /api/esportes/
# /api/professores/
# /api/horarios/
# /api/participacoes/
#
# O frontend poderá consumir essas rotas futuramente.
# ============================================================

from rest_framework.routers import DefaultRouter

from .api_views import (
    AlunoViewSet,
    EsporteViewSet,
    ProfessorViewSet,
    HorarioViewSet,
    ParticipacaoViewSet,
)


# Criação do roteador automático do Django REST Framework.
router = DefaultRouter()


# ============================================================
# REGISTRO DAS ROTAS
# ============================================================

router.register(
    r"alunos",
    AlunoViewSet,
    basename="aluno"
)

router.register(
    r"esportes",
    EsporteViewSet,
    basename="esporte"
)

router.register(
    r"professores",
    ProfessorViewSet,
    basename="professor"
)

router.register(
    r"horarios",
    HorarioViewSet,
    basename="horario"
)

router.register(
    r"participacoes",
    ParticipacaoViewSet,
    basename="participacao"
)


# Entrega as URLs geradas pelo router para o Django.
urlpatterns = router.urls