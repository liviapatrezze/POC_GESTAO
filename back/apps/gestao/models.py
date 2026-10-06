from django.core.exceptions import ValidationError
from django.db import models


class Aluno(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=11, blank=True)
    email = models.EmailField(blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    endereco = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100, blank=True, default="")
    cidade = models.CharField(max_length=100, blank=True, default="")
    estado = models.CharField(max_length=2)
    imagem = models.ImageField(upload_to="alunos/", blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome


class Esporte(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to="esportes/", blank=True, null=True)
    descricao = models.TextField(blank=True)
    categoria = models.CharField(max_length=100, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome


class Professor(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=11, blank=True)
    email = models.EmailField(blank=True)
    imagem = models.ImageField(upload_to="professores/", blank=True, null=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome


class Horario(models.Model):
    DIAS_SEMANA = [
        ("SEG", "Segunda-feira"),
        ("TER", "Terça-feira"),
        ("QUA", "Quarta-feira"),
        ("QUI", "Quinta-feira"),
        ("SEX", "Sexta-feira"),
        ("SAB", "Sábado"),
        ("DOM", "Domingo"),
    ]

    esporte = models.ForeignKey(
        Esporte,
        on_delete=models.CASCADE,
        related_name="horarios",
    )
    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        related_name="horarios",
    )
    dia_semana = models.CharField(max_length=3, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["dia_semana", "hora_inicio"]

    def clean(self) -> None:
        if self.hora_inicio and self.hora_fim and self.hora_inicio >= self.hora_fim:
            raise ValidationError(
                "O horário de término deve ser maior que o horário de início."
            )

    def __str__(self) -> str:
        return (
            f"{self.esporte} - {self.professor} - "
            f"{self.get_dia_semana_display()} - {self.hora_inicio} às {self.hora_fim}"
        )


class MatriculaHorario(models.Model):
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        related_name="matriculas_horarios",
    )
    horario = models.ForeignKey(
        Horario,
        on_delete=models.CASCADE,
        related_name="matriculas_alunos",
    )
    ativo = models.BooleanField(default=True)
    data_matricula = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["aluno", "horario"],
                name="unico_aluno_horario",
            )
        ]

    def __str__(self) -> str:
        return f"{self.aluno} - {self.horario}"


class Participacao(models.Model):
    matricula = models.ForeignKey(
        MatriculaHorario,
        on_delete=models.CASCADE,
        related_name="participacoes",
    )
    data_participacao = models.DateField()
    presente = models.BooleanField(default=False)
    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_participacao"]
        constraints = [
            models.UniqueConstraint(
                fields=["matricula", "data_participacao"],
                name="unico_matricula_data",
            )
        ]

    def __str__(self) -> str:
        return f"{self.matricula.aluno} - {self.data_participacao}"
