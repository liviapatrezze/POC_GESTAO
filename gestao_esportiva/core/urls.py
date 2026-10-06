from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [

    # ============================================================
    # PÁGINA INICIAL
    # ============================================================

    path(
        "",
        views.lista_alunos,
        name="inicio"
    ),

    # ============================================================
    # LOGIN
    # ============================================================

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="login.html"
        ),
        name="login"
    ),

    # ============================================================
    # LOGOUT
    # ============================================================

    path(
        "logout/",
        auth_views.LogoutView.as_view(
            next_page="/login/"
        ),
        name="logout"
    ),
    
    # ============================================================
    # ALUNOS
    # ============================================================

    path(
        "alunos/",
        views.lista_alunos,
        name="lista_alunos"
    ),

    path(
        "alunos/novo/",
        views.cadastrar_aluno,
        name="cadastrar_aluno"
    ),

    # ============================================================
    # ESPORTES
    # ============================================================

    path(
        "esportes/",
        views.lista_esportes,
        name="lista_esportes"
    ),

    path(
        "esportes/novo/",
        views.cadastrar_esporte,
        name="cadastrar_esporte"
    ),

    # ============================================================
    # PROFESSORES
    # ============================================================

    path(
        "professores/novo/",
        views.cadastrar_professor,
        name="cadastrar_professor"
    ),

    # ============================================================
    # HORÁRIOS
    # ============================================================

    path(
        "horarios/novo/",
        views.cadastrar_horario,
        name="cadastrar_horario"
    ),

    path(
        "horarios/",
        views.lista_horarios,
        name="lista_horarios"
    ),

    # ============================================================
    # API DE MATRÍCULAS
    # ============================================================

    path(
        "api/matriculas/",
        views.api_matriculas,
        name="api_matriculas"
    ),

    # ============================================================
    # API DE ALUNOS PARA NOVA MATRÍCULA
    # ============================================================

    path(
        "api/alunos-matricula/",
        views.api_alunos_matricula,
        name="api_alunos_matricula"
    ),

    # ============================================================
    # API DE ESPORTES PARA NOVA MATRÍCULA
    # ============================================================

    path(
        "api/esportes-matricula/",
        views.api_esportes_matricula,
        name="api_esportes_matricula"
    ),

    # ============================================================
    # API DE HORÁRIOS PARA NOVA MATRÍCULA
    # ============================================================

    path(
        "api/horarios-matricula/",
        views.api_horarios_matricula,
        name="api_horarios_matricula"
    ),

    # ============================================================
    # CADASTRAR MATRÍCULA
    # ============================================================

    path(
        "api/matriculas/cadastrar/",
        views.cadastrar_matricula,
        name="cadastrar_matricula"
    ),

    # ============================================================
    # MATRÍCULAS
    # ============================================================

    path(
        "matriculas/",
        views.lista_matriculas,
        name="lista_matriculas"
    ),

    # ============================================================
    # NOVA MATRÍCULA
    # ============================================================

    path(
        "matriculas/nova/",
        views.nova_matricula,
        name="nova_matricula"
    ),

    # ============================================================
    # ALTERAR STATUS DA MATRÍCULA
    # ============================================================

    path(
        "api/matriculas/status/",
        views.alterar_status_matricula,
        name="alterar_status_matricula"
    ),

    # ============================================================
    # API DE FREQUÊNCIA
    # ============================================================

    path(
        "api/presenca/",
        views.registrar_presenca,
        name="registrar_presenca"
    ),

    # ============================================================
    # FREQUÊNCIA
    # ============================================================

    path(
        "frequencia/",
        views.lista_frequencia,
        name="lista_frequencia"
    ),
]