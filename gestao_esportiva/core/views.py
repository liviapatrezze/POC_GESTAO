from datetime import date

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required

from .models import (
    Aluno,
    Esporte,
    Professor,
    Horario,
    MatriculaHorario,
    Participacao
)


# ============================================================
# ALUNOS
# ============================================================

@login_required
@permission_required("core.add_aluno", raise_exception=True)
def cadastrar_aluno(request):

    if request.method == "POST":

        nome = request.POST.get("nome")
        cpf = request.POST.get("cpf")
        telefone = request.POST.get("telefone")
        email = request.POST.get("email")
        data_nascimento = request.POST.get("data_nascimento")
        endereco = request.POST.get("endereco")
        numero = request.POST.get("numero")
        bairro = request.POST.get("bairro")
        cidade = request.POST.get("cidade")
        estado = request.POST.get("estado")
        imagem = request.FILES.get("imagem")

        if Aluno.objects.filter(cpf=cpf).exists():

            messages.error(
                request,
                "⚠️ Já existe um aluno cadastrado com este CPF."
            )

            return redirect("cadastrar_aluno")

        Aluno.objects.create(
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            email=email,
            data_nascimento=data_nascimento,
            endereco=endereco,
            numero=numero,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            imagem=imagem
        )

        messages.success(
            request,
            "✅ Aluno cadastrado com sucesso!"
        )

        return redirect("lista_alunos")

    return render(
        request,
        "alunos/cadastro.html"
    )


@login_required
@permission_required("core.view_aluno", raise_exception=True)
def lista_alunos(request):

    alunos = Aluno.objects.all().order_by("nome")

    return render(
        request,
        "alunos/lista.html",
        {
            "alunos": alunos
        }
    )


# ============================================================
# ESPORTES
# ============================================================

@login_required
def lista_esportes(request):

    esportes = Esporte.objects.filter(
        ativo=True
    )

    return render(
        request,
        "esportes/esportes.html",
        {
            "esportes": esportes
        }
    )


@login_required
@permission_required(
    "core.add_esporte",
    raise_exception=True
)
def cadastrar_esporte(request):

    if request.method == "POST":

        nome = request.POST.get("nome")
        descricao = request.POST.get("descricao")
        categoria = request.POST.get("categoria")
        imagem = request.FILES.get("imagem")

        Esporte.objects.create(
            nome=nome,
            descricao=descricao,
            categoria=categoria,
            imagem=imagem,
            ativo=True
        )

        messages.success(
            request,
            "✅ Esporte cadastrado com sucesso!"
        )

        return redirect("lista_esportes")

    return render(
        request,
        "esportes/cadastro.html"
    )


# ============================================================
# PROFESSORES
# ============================================================

@login_required
@permission_required(
    "core.add_professor",
    raise_exception=True
)
def cadastrar_professor(request):

    if request.method == "POST":

        nome = request.POST.get("nome")
        cpf = request.POST.get("cpf")
        telefone = request.POST.get("telefone")
        email = request.POST.get("email")
        imagem = request.FILES.get("imagem")

        # Verifica se o CPF foi informado
        # e se já existe outro professor com esse CPF.

        if cpf and Professor.objects.filter(
            cpf=cpf
        ).exists():

            messages.error(
                request,
                "⚠️ Já existe um professor cadastrado com este CPF."
            )

            return redirect(
                "lista_horarios"
            )

        Professor.objects.create(
            nome=nome,
            cpf=cpf if cpf else None,
            telefone=telefone,
            email=email,
            imagem=imagem,
            ativo=True
        )

        messages.success(
            request,
            "✅ Professor cadastrado com sucesso!"
        )

        # Temporariamente voltamos para a própria
        # tela de cadastro para testar a mensagem.

        return redirect(
            "cadastrar_professor"
        )

    return render(
        request,
        "professores/cadastro.html"
    )


# ============================================================
# HORÁRIOS
# ============================================================


@login_required
@permission_required(
    "core.add_horario",
    raise_exception=True
)
def cadastrar_horario(request):

    if request.method == "POST":

        esporte_id = request.POST.get("esporte")
        professor_id = request.POST.get("professor")
        dia_semana = request.POST.get("dia_semana")
        hora_inicio = request.POST.get("hora_inicio")
        hora_fim = request.POST.get("hora_fim")

        try:

            esporte = Esporte.objects.get(
                id=esporte_id,
                ativo=True
            )

        except Esporte.DoesNotExist:

            messages.error(
                request,
                "⚠️ Esporte inválido ou inativo."
            )

            return redirect(
                "cadastrar_horario"
            )

        try:

            professor = Professor.objects.get(
                id=professor_id,
                ativo=True
            )

        except Professor.DoesNotExist:

            messages.error(
                request,
                "⚠️ Professor inválido ou inativo."
            )

            return redirect(
                "cadastrar_horario"
            )

        horario = Horario(
            esporte=esporte,
            professor=professor,
            dia_semana=dia_semana,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            ativo=True
        )

        try:

            horario.full_clean()

        except Exception as erro:

            messages.error(
                request,
                f"⚠️ Não foi possível cadastrar o horário: {erro}"
            )

            return redirect(
                "cadastrar_horario"
            )

        horario.save()

        messages.success(
            request,
            "✅ Horário cadastrado com sucesso!"
        )

        return redirect(
            "lista_horarios"
        )

    esportes = Esporte.objects.filter(
        ativo=True
    ).order_by(
        "nome"
    )

    professores = Professor.objects.filter(
        ativo=True
    ).order_by(
        "nome"
    )

    return render(
        request,
        "horarios/cadastro.html",
        {
            "esportes": esportes,
            "professores": professores,
        }
    )


@login_required
def lista_horarios(request):

    horarios = Horario.objects.select_related(
        "esporte",
        "professor"
    ).filter(
        ativo=True
    ).order_by(
        "dia_semana",
        "hora_inicio"
    )

    return render(
        request,
        "horarios/lista.html",
        {
            "horarios": horarios
        }
    )


# ============================================================
# API DE MATRÍCULAS
# ============================================================

@login_required
def api_matriculas(request):

    matriculas = MatriculaHorario.objects.select_related(
        "aluno",
        "horario",
        "horario__esporte",
        "horario__professor"
    ).all()

    hoje = date.today()

    dados = []

    for matricula in matriculas:

        participacao = Participacao.objects.filter(
            matricula=matricula,
            data_participacao=hoje
        ).first()

        if participacao is None:
            presenca = None
        else:
            presenca = participacao.presente

        dados.append({

            "id": matricula.id,

            "aluno": matricula.aluno.nome,

            "foto": (
                matricula.aluno.imagem.url
                if matricula.aluno.imagem
                else ""
            ),

            "esporte": matricula.horario.esporte.nome,

            "professor": matricula.horario.professor.nome,

            "dia_semana": matricula.horario.dia_semana,

            "hora_inicio": str(
                matricula.horario.hora_inicio
            ),

            "hora_fim": str(
                matricula.horario.hora_fim
            ),

            "ativo": matricula.ativo,

            "presente": presenca,
        })

    return JsonResponse({
        "matriculas": dados
    })


# ============================================================
# CADASTRAR MATRÍCULA
# ============================================================

@login_required
@permission_required(
    "core.add_matriculahorario",
    raise_exception=True
)
def cadastrar_matricula(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "sucesso": False,
                "erro": "Método não permitido."
            },
            status=405
        )

    aluno_id = request.POST.get(
        "aluno_id"
    )

    horario_id = request.POST.get(
        "horario_id"
    )

    if not aluno_id or not horario_id:

        return JsonResponse(
            {
                "sucesso": False,
                "erro": "Aluno e horário são obrigatórios."
            },
            status=400
        )

    try:

        aluno = Aluno.objects.get(
            id=aluno_id
        )

    except Aluno.DoesNotExist:

        return JsonResponse(
            {
                "sucesso": False,
                "erro": "Aluno não encontrado."
            },
            status=404
        )

    try:

        horario = Horario.objects.select_related(
            "esporte",
            "professor"
        ).get(
            id=horario_id
        )

    except Horario.DoesNotExist:

        return JsonResponse(
            {
                "sucesso": False,
                "erro": "Horário não encontrado."
            },
            status=404
        )

    # Verifica se o aluno está ativo

    if not aluno.ativo:

        return JsonResponse(
            {
                "sucesso": False,
                "erro":
                    "Não é possível matricular um aluno inativo."
            },
            status=400
        )

    # Verifica se o horário está ativo

    if not horario.ativo:

        return JsonResponse(
            {
                "sucesso": False,
                "erro":
                    "Não é possível matricular em um horário inativo."
            },
            status=400
        )

    # Verifica se o esporte está ativo

    if not horario.esporte.ativo:

        return JsonResponse(
            {
                "sucesso": False,
                "erro":
                    "Não é possível matricular em um esporte inativo."
            },
            status=400
        )

    # Verifica se o professor está ativo

    if not horario.professor.ativo:

        return JsonResponse(
            {
                "sucesso": False,
                "erro":
                    "Não é possível matricular em um horário de professor inativo."
            },
            status=400
        )

    # Verifica matrícula duplicada

    if MatriculaHorario.objects.filter(
        aluno=aluno,
        horario=horario
    ).exists():

        return JsonResponse(
            {
                "sucesso": False,
                "erro":
                    "Este aluno já está matriculado neste horário."
            },
            status=400
        )

    # Cria a matrícula

    matricula = MatriculaHorario.objects.create(
        aluno=aluno,
        horario=horario
    )

    return JsonResponse(
        {
            "sucesso": True,
            "matricula_id": matricula.id,
            "mensagem":
                "Matrícula realizada com sucesso."
        }
    )


# ============================================================
# ALTERAR STATUS DA MATRÍCULA
# ============================================================

@login_required
@permission_required(
    "core.change_matriculahorario",
    raise_exception=True
)
@csrf_exempt
def alterar_status_matricula(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "sucesso": False,
                "erro": "Método não permitido."
            },
            status=405
        )

    matricula_id = request.POST.get(
        "matricula_id"
    )

    ativo = request.POST.get(
        "ativo"
    ) == "true"

    matricula = MatriculaHorario.objects.get(
        id=matricula_id
    )

    matricula.ativo = ativo

    matricula.save()

    return JsonResponse(
        {
            "sucesso": True,
            "matricula_id": matricula.id,
            "ativo": matricula.ativo
        }
    )


# ============================================================
# MATRÍCULAS
# ============================================================

@login_required
@permission_required(
    "core.view_matriculahorario",
    raise_exception=True
)
def lista_matriculas(request):

    return render(
        request,
        "matriculas/lista.html"
    )


# ============================================================
# FREQUÊNCIA
# ============================================================

@login_required
@permission_required(
    "core.view_participacao",
    raise_exception=True
)
def lista_frequencia(request):

    return render(
        request,
        "frequencia/lista.html"
    )


# ============================================================
# REGISTRAR / ALTERAR PRESENÇA
# ============================================================

@login_required
@csrf_exempt
def registrar_presenca(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "sucesso": False,
                "erro": "Método não permitido."
            },
            status=405
        )

    pode_adicionar = request.user.has_perm(
        "core.add_participacao"
    )

    pode_alterar = request.user.has_perm(
        "core.change_participacao"
    )

    if not pode_adicionar and not pode_alterar:

        return JsonResponse(
            {
                "sucesso": False,
                "erro":
                    "Você não possui permissão para registrar ou alterar a frequência."
            },
            status=403
        )

    matricula_id = request.POST.get(
        "matricula_id"
    )

    presente = request.POST.get(
        "presente"
    ) == "true"

    matricula = MatriculaHorario.objects.get(
        id=matricula_id
    )

    participacao_existente = Participacao.objects.filter(
        matricula=matricula,
        data_participacao=date.today()
    ).first()

    if participacao_existente:

        if not pode_alterar:

            return JsonResponse(
                {
                    "sucesso": False,
                    "erro":
                        "Você não possui permissão para alterar este registro."
                },
                status=403
            )

    else:

        if not pode_adicionar:

            return JsonResponse(
                {
                    "sucesso": False,
                    "erro":
                        "Você não possui permissão para adicionar este registro."
                },
                status=403
            )

    participacao, criada = Participacao.objects.update_or_create(
        matricula=matricula,
        data_participacao=date.today(),
        defaults={
            "presente": presente
        }
    )

    return JsonResponse(
        {
            "sucesso": True,
            "matricula_id": matricula.id,
            "presente": participacao.presente,
            "data": str(
                participacao.data_participacao
            )
        }
    )


# ============================================================
# API DE ALUNOS ATIVOS PARA MATRÍCULA
# ============================================================

@login_required
@permission_required(
    "core.add_matriculahorario",
    raise_exception=True
)
def api_alunos_matricula(request):

    alunos = Aluno.objects.filter(
        ativo=True
    ).order_by(
        "nome"
    )

    dados = []

    for aluno in alunos:

        dados.append({
            "id": aluno.id,
            "nome": aluno.nome,
        })

    return JsonResponse({
        "alunos": dados
    })


# ============================================================
# API DE HORÁRIOS ATIVOS PARA MATRÍCULA
# ============================================================

@login_required
@permission_required(
    "core.add_matriculahorario",
    raise_exception=True
)
def api_horarios_matricula(request):

    esporte_id = request.GET.get(
        "esporte_id"
    )

    horarios = Horario.objects.select_related(
        "esporte",
        "professor"
    ).filter(
        ativo=True,
        esporte__ativo=True,
        professor__ativo=True
    )

    # Se um esporte foi selecionado,
    # mostra somente os horários desse esporte

    if esporte_id:

        horarios = horarios.filter(
            esporte_id=esporte_id
        )

    horarios = horarios.order_by(
        "dia_semana",
        "hora_inicio"
    )

    dados = []

    for horario in horarios:

        dados.append({

            "id": horario.id,

            "esporte":
                horario.esporte.nome,

            "professor":
                horario.professor.nome,

            "dia_semana":
                horario.get_dia_semana_display(),

            "hora_inicio":
                horario.hora_inicio.strftime("%H:%M"),

            "hora_fim":
                horario.hora_fim.strftime("%H:%M"),

        })

    return JsonResponse({
        "horarios": dados
    })


# ============================================================
# TELA DE NOVA MATRÍCULA
# ============================================================

@login_required
@permission_required(
    "core.add_matriculahorario",
    raise_exception=True
)
def nova_matricula(request):

    return render(
        request,
        "matriculas/nova.html"
    )


# ============================================================
# API DE ESPORTES ATIVOS PARA MATRÍCULA
# ============================================================

@login_required
@permission_required(
    "core.add_matriculahorario",
    raise_exception=True
)
def api_esportes_matricula(request):

    esportes = Esporte.objects.filter(
        ativo=True
    ).order_by(
        "nome"
    )

    dados = []

    for esporte in esportes:

        dados.append({
            "id": esporte.id,
            "nome": esporte.nome,
        })

    return JsonResponse({
        "esportes": dados
    })