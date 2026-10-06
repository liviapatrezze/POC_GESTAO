from django.contrib import admin

from apps.gestao.models import Aluno, Esporte, Horario, MatriculaHorario, Participacao, Professor


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf", "cidade", "ativo")
    search_fields = ("nome", "cpf")


@admin.register(Esporte)
class EsporteAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "ativo")


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf", "ativo")


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ("esporte", "professor", "dia_semana", "hora_inicio", "hora_fim", "ativo")


@admin.register(MatriculaHorario)
class MatriculaHorarioAdmin(admin.ModelAdmin):
    list_display = ("aluno", "horario", "ativo")


@admin.register(Participacao)
class ParticipacaoAdmin(admin.ModelAdmin):
    list_display = ("matricula", "data_participacao", "presente")
