from django.contrib import admin

from .models import (
    Aluno,
    Esporte,
    Professor,
    Horario,
    Participacao,
)


# ============================================================
# REGISTRO DOS MODELOS NO DJANGO ADMIN
# ============================================================
#
# Estes registros permitem que os modelos sejam administrados
# através do painel /admin/ do Django.
#
# O modelo Convite foi retirado do projeto porque o sistema
# será utilizado pelos professores para controle de alunos,
# esportes, horários e frequência.
# ============================================================


admin.site.register(Aluno)
admin.site.register(Esporte)
admin.site.register(Professor)
admin.site.register(Horario)
admin.site.register(Participacao)