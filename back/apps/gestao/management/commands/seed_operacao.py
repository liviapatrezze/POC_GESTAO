from django.core.management.base import BaseCommand

from apps.gestao.seeds.operacao import popular


class Command(BaseCommand):
    help = "Substitui alunos, turmas, matrículas e presenças por uma operação simulada de três meses."

    def handle(self, *args: object, **options: object) -> None:
        resumo = popular()
        self.stdout.write(self.style.SUCCESS("Operação simulada gravada."))
        self.stdout.write(
            f"Período: {resumo['inicio']:%d/%m/%Y} a {resumo['fim']:%d/%m/%Y} ({resumo['dias']} dias)."
        )
        self.stdout.write(
            "Alunos {alunos}, professores {professores}, esportes {esportes}, "
            "turmas {turmas}, matrículas {matriculas}, presenças {participacoes}.".format(**resumo)
        )
