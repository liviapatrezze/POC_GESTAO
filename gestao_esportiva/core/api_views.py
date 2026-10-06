# ============================================================
# VIEWS DA API
# ============================================================
# Este arquivo contém as classes responsáveis por disponibilizar
# os modelos do sistema através da API REST.
#
# IMPORTANTE:
# Estas classes pertencem à parte de BACKEND.
# O frontend poderá consumir estas APIs posteriormente.
# ============================================================

from rest_framework import viewsets

# Importamos somente os modelos que continuarão no sistema.
# Convite foi removido do projeto.
from .models import (
    Aluno,
    Esporte,
    Professor,
    Horario,
    Participacao,
)

# Importamos os serializers correspondentes aos modelos.
from .serializers import (
    AlunoSerializer,
    EsporteSerializer,
    ProfessorSerializer,
    HorarioSerializer,
    ParticipacaoSerializer,
)


# ============================================================
# API DE ALUNOS
# ============================================================
class AlunoViewSet(viewsets.ModelViewSet):

    # Define quais alunos podem ser consultados pela API.
    # A ordenação será pelo nome.
    queryset = Aluno.objects.all().order_by("nome")

    # Define qual serializer será utilizado.
    serializer_class = AlunoSerializer


# ============================================================
# API DE ESPORTES / MODALIDADES
# ============================================================
class EsporteViewSet(viewsets.ModelViewSet):

    # Busca todos os esportes cadastrados.
    queryset = Esporte.objects.all().order_by("nome")

    # Serializer responsável pelos dados dos esportes.
    serializer_class = EsporteSerializer


# ============================================================
# API DE PROFESSORES
# ============================================================
class ProfessorViewSet(viewsets.ModelViewSet):

    # Busca todos os professores cadastrados.
    queryset = Professor.objects.all().order_by("nome")

    # Serializer responsável pelos dados dos professores.
    serializer_class = ProfessorSerializer


# ============================================================
# API DE HORÁRIOS / AULAS
# ============================================================
class HorarioViewSet(viewsets.ModelViewSet):

    # Organiza os horários primeiro pelo dia da semana
    # e depois pelo horário de início.
    queryset = Horario.objects.all().order_by(
        "dia_semana",
        "hora_inicio"
    )

    # Serializer responsável pelos horários.
    serializer_class = HorarioSerializer


# ============================================================
# API DE PARTICIPAÇÃO / FREQUÊNCIA
# ============================================================
class ParticipacaoViewSet(viewsets.ModelViewSet):

    # Mostra as participações mais recentes primeiro.
    queryset = Participacao.objects.all().order_by(
        "-data_participacao"
    )

    # Serializer responsável pelo controle de presença.
    serializer_class = ParticipacaoSerializer
    