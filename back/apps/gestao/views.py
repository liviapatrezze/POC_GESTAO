from datetime import date

from django.db.models import OuterRef, Subquery
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.gestao.models import Aluno, Esporte, Horario, MatriculaHorario, Participacao, Professor
from apps.gestao.serializers import (
    AlunoSerializer,
    EsporteSerializer,
    HorarioSerializer,
    MatriculaSerializer,
    ParticipacaoSerializer,
    ProfessorSerializer,
)


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer


class EsporteViewSet(viewsets.ModelViewSet):
    queryset = Esporte.objects.all()
    serializer_class = EsporteSerializer


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer


class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.select_related("esporte", "professor")
    serializer_class = HorarioSerializer


class MatriculaViewSet(viewsets.ModelViewSet):
    serializer_class = MatriculaSerializer

    def get_queryset(self):
        presenca = Participacao.objects.filter(
            matricula=OuterRef("pk"),
            data_participacao=date.today(),
        ).values("presente")[:1]
        return MatriculaHorario.objects.select_related(
            "aluno",
            "horario__esporte",
            "horario__professor",
        ).annotate(presente_hoje=Subquery(presenca))

    @action(detail=True, methods=["post"])
    def presenca(self, request: Request, pk: int | None = None) -> Response:
        matricula = self.get_object()
        presente = request.data.get("presente")
        if not isinstance(presente, bool):
            return Response(
                {"presente": ["Informe verdadeiro ou falso."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        participacao, _criada = Participacao.objects.update_or_create(
            matricula=matricula,
            data_participacao=date.today(),
            defaults={"presente": presente},
        )
        return Response(
            {
                "matricula": matricula.id,
                "presente": participacao.presente,
                "data": participacao.data_participacao,
            }
        )


class ParticipacaoViewSet(viewsets.ModelViewSet):
    queryset = Participacao.objects.select_related("matricula")
    serializer_class = ParticipacaoSerializer
