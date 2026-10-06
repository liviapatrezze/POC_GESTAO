from django.urls import path

from apps.gestao.views import (
    AlunoViewSet,
    EsporteViewSet,
    HorarioViewSet,
    MatriculaViewSet,
    ParticipacaoViewSet,
    ProfessorViewSet,
)


def resource(prefix: str, viewset: type, name: str) -> list:
    collection = viewset.as_view({"get": "list", "post": "create"})
    detail = viewset.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }
    )
    return [
        path(f"{prefix}/", collection, name=name),
        path(prefix, collection),
        path(f"{prefix}/<int:pk>/", detail, name=f"{name}-detail"),
        path(f"{prefix}/<int:pk>", detail),
    ]


presenca = MatriculaViewSet.as_view({"post": "presenca"})

urlpatterns = [
    *resource("alunos", AlunoViewSet, "aluno"),
    *resource("esportes", EsporteViewSet, "esporte"),
    *resource("professores", ProfessorViewSet, "professor"),
    *resource("horarios", HorarioViewSet, "horario"),
    *resource("matriculas", MatriculaViewSet, "matricula"),
    *resource("participacoes", ParticipacaoViewSet, "participacao"),
    path("matriculas/<int:pk>/presenca/", presenca, name="matricula-presenca"),
    path("matriculas/<int:pk>/presenca", presenca),
]
