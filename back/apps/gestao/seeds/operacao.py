import random
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from django.db import connection, transaction
from django.db.models import Model

from apps.gestao.models import Aluno, Esporte, Horario, MatriculaHorario, Participacao, Professor
from apps.gestao.seeds.catalogo import BAIRROS, ESPORTES, NOMES, PROFESSORES, RUAS, TURMAS

TZ = ZoneInfo("America/Sao_Paulo")
SEMANAS = 14
DIAS = {"SEG": 0, "TER": 1, "QUA": 2, "QUI": 3, "SEX": 4, "SAB": 5, "DOM": 6}


def inicio_operacao(hoje: date) -> date:
    bruto = hoje - timedelta(days=7 * SEMANAS)
    return bruto - timedelta(days=bruto.weekday())


def cpf_valido(indice: int) -> str:
    base = f"{100000000 + indice * 137:09d}"[-9:]

    def digito(numeros: str, peso_inicial: int) -> int:
        soma = sum(int(numero) * peso for numero, peso in zip(numeros, range(peso_inicial, 1, -1)))
        resto = soma % 11
        if resto < 2:
            return 0
        return 11 - resto

    primeiro = digito(base, 10)
    segundo = digito(f"{base}{primeiro}", 11)
    return f"{base}{primeiro}{segundo}"


def instante(dia: date, hora: time) -> datetime:
    return datetime.combine(dia, hora, TZ)


def gravar_instantes(objetos: list[Model], campo: str, valores: list[datetime]) -> None:
    if not objetos:
        return
    modelo = objetos[0].__class__
    tabela = modelo._meta.db_table
    coluna = modelo._meta.get_field(campo).column
    chave = modelo._meta.pk.column
    with connection.cursor() as cursor:
        cursor.executemany(
            f"UPDATE {tabela} SET {coluna} = %s WHERE {chave} = %s",
            [(valor, objeto.pk) for objeto, valor in zip(objetos, valores, strict=True)],
        )
    for objeto, valor in zip(objetos, valores, strict=True):
        setattr(objeto, campo, valor)


def entrada_semana(indice: int) -> int:
    if indice >= 35:
        return 9
    if indice >= 28:
        return 5
    return 0


def saida_semana(indice: int) -> int | None:
    if indice in (38, 39):
        return 8
    return None


def datas_de_aula(dia_codigo: str, inicio: date, fim: date) -> list[date]:
    if fim < inicio:
        return []
    alvo = DIAS[dia_codigo]
    atual = inicio + timedelta(days=(alvo - inicio.weekday()) % 7)
    encontros: list[date] = []
    while atual <= fim:
        encontros.append(atual)
        atual += timedelta(days=7)
    return encontros


def esta_presente(aluno_idx: int, dia: date, inicio: date) -> bool:
    taxa = 0.62 + (aluno_idx % 7) * 0.05
    recesso = inicio + timedelta(days=21)
    if recesso <= dia <= recesso + timedelta(days=4):
        taxa -= 0.22
    sorteio = random.Random(aluno_idx * 10007 + dia.toordinal())
    return sorteio.random() < max(taxa, 0.2)


def limpar() -> None:
    Participacao.objects.all().delete()
    MatriculaHorario.objects.all().delete()
    Horario.objects.all().delete()
    Aluno.objects.all().delete()
    Professor.objects.all().delete()
    Esporte.objects.all().delete()


def criar_pessoas(inicio: date) -> tuple[list[Esporte], list[Professor], list[Aluno]]:
    esportes = Esporte.objects.bulk_create(
        [
            Esporte(nome=nome, categoria=categoria, descricao=descricao, ativo=True)
            for nome, categoria, descricao in ESPORTES
        ]
    )
    professores = Professor.objects.bulk_create(
        [
            Professor(nome=nome, cpf=cpf_valido(800 + indice), telefone=telefone, email=email, ativo=ativo)
            for indice, (nome, telefone, email, ativo) in enumerate(PROFESSORES)
        ]
    )
    cadastros = [
        instante(inicio + timedelta(weeks=entrada_semana(indice)) - timedelta(days=2), time(10, 0))
        for indice in range(len(NOMES))
    ]
    alunos = Aluno.objects.bulk_create(
        [
            Aluno(
                nome=nome,
                cpf=cpf_valido(indice + 1),
                telefone=f"1699{indice + 2000000:07d}"[-11:],
                email=f"aluno{indice + 1}@sportbridge.local",
                data_nascimento=date(2012, 3, 1) + timedelta(days=indice * 47)
                if indice < 30
                else date(1990, 5, 12) + timedelta(days=indice * 19),
                endereco=RUAS[indice % len(RUAS)],
                numero=str(120 + indice),
                bairro=BAIRROS[indice % len(BAIRROS)],
                cidade="Ibitinga",
                estado="SP",
                ativo=saida_semana(indice) is None,
            )
            for indice, nome in enumerate(NOMES)
        ]
    )
    gravar_instantes(alunos, "data_cadastro", cadastros)
    return esportes, professores, alunos


def criar_turmas(
    inicio: date,
    hoje: date,
    esportes: list[Esporte],
    professores: list[Professor],
    alunos: list[Aluno],
) -> list[MatriculaHorario]:
    horarios = Horario.objects.bulk_create(
        [
            Horario(
                esporte=esportes[esporte],
                professor=professores[professor],
                dia_semana=dia,
                hora_inicio=time.fromisoformat(hora_inicio),
                hora_fim=time.fromisoformat(hora_fim),
                ativo=ativo,
            )
            for esporte, professor, dia, hora_inicio, hora_fim, _alunos, ativo, _semanas in TURMAS
        ]
    )
    matriculas: list[MatriculaHorario] = []
    datas: list[datetime] = []
    for horario, plano in zip(horarios, TURMAS, strict=True):
        _, _, _, _, _, indices, _, semanas = plano
        fim_turma = hoje if semanas is None else min(hoje, inicio + timedelta(weeks=semanas))
        for indice in indices:
            comeco = inicio + timedelta(weeks=entrada_semana(indice))
            if comeco > fim_turma:
                continue
            fim_aluno = fim_turma
            saida = saida_semana(indice)
            if saida is not None:
                fim_aluno = min(fim_aluno, inicio + timedelta(weeks=saida))
            datas.append(instante(comeco, time(9, 0)))
            matriculas.append(
                MatriculaHorario(
                    aluno=alunos[indice],
                    horario=horario,
                    ativo=saida is None and horario.ativo and fim_aluno >= hoje,
                )
            )
    criadas = MatriculaHorario.objects.bulk_create(matriculas)
    gravar_instantes(criadas, "data_matricula", datas)
    return criadas


def fim_da_matricula(matricula: MatriculaHorario, horario: Horario, inicio: date, hoje: date, aluno_idx: int) -> date:
    fim = hoje
    saida = saida_semana(aluno_idx)
    if saida is not None:
        fim = min(fim, inicio + timedelta(weeks=saida))
    if not horario.ativo:
        fim = min(fim, inicio + timedelta(weeks=8))
    return fim


def criar_presencas(inicio: date, hoje: date, matriculas: list[MatriculaHorario]) -> int:
    horarios = {horario.pk: horario for horario in Horario.objects.all()}
    indice_por_nome = {nome: indice for indice, nome in enumerate(NOMES)}
    por_turma: dict[int, list[MatriculaHorario]] = {}
    for matricula in matriculas:
        por_turma.setdefault(matricula.horario_id, []).append(matricula)

    sem_chamada_hoje: set[int] = set()
    falta_forcada: set[int] = set()
    for horario_id, grupo in por_turma.items():
        horario = horarios[horario_id]
        if DIAS[horario.dia_semana] != hoje.weekday():
            continue
        vigentes = [
            item
            for item in grupo
            if item.data_matricula.astimezone(TZ).date()
            <= hoje
            <= fim_da_matricula(item, horario, inicio, hoje, indice_por_nome[item.aluno.nome])
        ]
        vigentes.sort(key=lambda item: item.aluno_id)
        for item in vigentes[-2:]:
            sem_chamada_hoje.add(item.pk)
        chamados = [item for item in vigentes if item.pk not in sem_chamada_hoje]
        if chamados:
            falta_forcada.add(chamados[0].pk)

    registros: list[Participacao] = []
    registros_em: list[datetime] = []
    for matricula in matriculas:
        horario = horarios[matricula.horario_id]
        aluno_idx = indice_por_nome[matricula.aluno.nome]
        comeco = matricula.data_matricula.astimezone(TZ).date()
        fim = fim_da_matricula(matricula, horario, inicio, hoje, aluno_idx)
        for encontro in datas_de_aula(horario.dia_semana, comeco, fim):
            if (
                encontro < hoje
                and encontro > inicio + timedelta(days=14)
                and (encontro.toordinal() + horario.pk) % 9 == 0
            ):
                continue
            if encontro == hoje and matricula.pk in sem_chamada_hoje:
                continue
            presente = (
                False
                if encontro == hoje and matricula.pk in falta_forcada
                else esta_presente(aluno_idx, encontro, inicio)
            )
            registros_em.append(instante(encontro, horario.hora_fim))
            registros.append(
                Participacao(
                    matricula=matricula,
                    data_participacao=encontro,
                    presente=presente,
                )
            )
    criadas = Participacao.objects.bulk_create(registros, batch_size=500)
    gravar_instantes(criadas, "data_registro", registros_em)
    return len(criadas)


def popular(hoje: date | None = None) -> dict[str, int | date]:
    hoje = hoje or date.today()
    inicio = inicio_operacao(hoje)
    with transaction.atomic():
        limpar()
        esportes, professores, alunos = criar_pessoas(inicio)
        matriculas = criar_turmas(inicio, hoje, esportes, professores, alunos)
        participacoes = criar_presencas(inicio, hoje, matriculas)
    return {
        "inicio": inicio,
        "fim": hoje,
        "dias": (hoje - inicio).days,
        "alunos": len(alunos),
        "professores": len(professores),
        "esportes": len(esportes),
        "turmas": Horario.objects.count(),
        "matriculas": len(matriculas),
        "participacoes": participacoes,
    }
