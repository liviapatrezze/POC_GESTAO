from django.db import models


# ============================================================
# ALUNO
# ============================================================
# Representa o aluno cadastrado no sistema.
#
# IMPORTANTE:
# Este modelo pertence à estrutura principal do sistema.
# O banco de dados definitivo será configurado posteriormente
# pelo responsável pelo banco de dados.
# ============================================================

class Aluno(models.Model):

    nome = models.CharField(
        max_length=150
    )

    cpf = models.CharField(
        max_length=11,
        unique=True
    )

    telefone = models.CharField(
        max_length=11,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    data_nascimento = models.DateField(
        null=True,
        blank=True
    )

    endereco = models.CharField(
        max_length=200
    )

    numero = models.CharField(
        max_length=10
    )

    bairro = models.CharField(
        max_length=100,
        blank=True,
        default=''
    )

    cidade = models.CharField(
        max_length=100,
        blank=True,
        default=''
    )

    estado = models.CharField(
        max_length=2
    )

    # Foto do aluno
    imagem = models.ImageField(
        upload_to='alunos/',
        blank=True,
        null=True
    )

    # Data em que o cadastro foi criado
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )

    # Permite ativar/desativar o aluno sem apagar seu histórico
    ativo = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.nome


# ============================================================
# ESPORTE
# ============================================================
# Representa uma modalidade esportiva cadastrada no sistema.
# ============================================================

class Esporte(models.Model):

    nome = models.CharField(
        max_length=100
    )

    # Imagem da modalidade
    imagem = models.ImageField(
        upload_to='esportes/',
        blank=True,
        null=True
    )

    descricao = models.TextField(
        blank=True
    )

    categoria = models.CharField(
        max_length=100,
        blank=True
    )

    # Permite desativar o esporte sem apagar seu histórico
    ativo = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.nome


# ============================================================
# PROFESSOR / INSTRUTOR
# ============================================================
# Representa o professor ou instrutor responsável pelas aulas.
# ============================================================

class Professor(models.Model):

    nome = models.CharField(
        max_length=150
    )

    cpf = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True
    )

    telefone = models.CharField(
        max_length=11,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    # Foto do professor
    imagem = models.ImageField(
        upload_to='professores/',
        blank=True,
        null=True
    )

    # Permite ativar/desativar o professor
    # sem apagar seu histórico.
    ativo = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.nome


# ============================================================
# HORÁRIO
# ============================================================
# Representa o horário recorrente de uma modalidade.
#
# O horário representa uma programação semanal.
# ============================================================

class Horario(models.Model):

    DIAS_SEMANA = [
        ('SEG', 'Segunda-feira'),
        ('TER', 'Terça-feira'),
        ('QUA', 'Quarta-feira'),
        ('QUI', 'Quinta-feira'),
        ('SEX', 'Sexta-feira'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo'),
    ]

    # Modalidade esportiva
    esporte = models.ForeignKey(
        Esporte,
        on_delete=models.CASCADE,
        related_name='horarios'
    )

    # Professor responsável
    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        related_name='horarios'
    )

    # Dia da semana
    dia_semana = models.CharField(
        max_length=3,
        choices=DIAS_SEMANA
    )

    # Horário de início
    hora_inicio = models.TimeField()

    # Horário de término
    hora_fim = models.TimeField()

    # Permite ativar/desativar o horário
    ativo = models.BooleanField(
        default=True
    )

    # Validação do horário
    def clean(self):

        from django.core.exceptions import ValidationError

        if self.hora_inicio >= self.hora_fim:

            raise ValidationError(
                "O horário de término deve ser maior que o horário de início."
            )

    def __str__(self):
        return (
            f"{self.esporte} - "
            f"{self.professor} - "
            f"{self.get_dia_semana_display()} - "
            f"{self.hora_inicio} às {self.hora_fim}"
        )


# ============================================================
# MATRÍCULA NO HORÁRIO
# ============================================================
# Cria a relação entre ALUNO e HORÁRIO.
#
# Antes de registrar uma frequência, o aluno precisa
# estar matriculado naquele horário.
# ============================================================

class MatriculaHorario(models.Model):

    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        related_name='matriculas_horarios'
    )

    horario = models.ForeignKey(
        Horario,
        on_delete=models.CASCADE,
        related_name='matriculas_alunos'
    )

    # Permite cancelar/desativar a matrícula
    # sem apagar o histórico.
    ativo = models.BooleanField(
        default=True
    )

    # Data em que a matrícula foi criada
    data_matricula = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.aluno} - {self.horario}"

    class Meta:

        # Impede que o mesmo aluno seja matriculado
        # duas vezes no mesmo horário.
        constraints = [
            models.UniqueConstraint(
                fields=['aluno', 'horario'],
                name='unico_aluno_horario'
            )
        ]


# ============================================================
# PARTICIPAÇÃO / FREQUÊNCIA
# ============================================================
# Registra a presença ou ausência do aluno em uma aula.
#
# A participação agora está ligada à MATRICULA.
#
# Isso significa que:
#
# PARTICIPAÇÃO
#       ↓
# MATRÍCULA
#       ↓
# ALUNO + HORÁRIO
#
# Dessa forma, não precisamos mais armazenar
# aluno e horário diretamente aqui.
# ============================================================

class Participacao(models.Model):

    # Matrícula do aluno no horário
    matricula = models.ForeignKey(
        MatriculaHorario,
        on_delete=models.CASCADE,
        related_name='participacoes'
    )

    # Data em que a aula aconteceu
    data_participacao = models.DateField()

    # Indica se o aluno esteve presente
    presente = models.BooleanField(
        default=False
    )

    # Data/hora em que o registro foi criado
    data_registro = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.matricula.aluno} - "
            f"{self.matricula.horario.esporte} - "
            f"{self.data_participacao}"
        )

    class Meta:

        # Impede que a mesma matrícula tenha
        # dois registros de frequência na mesma data.
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'matricula',
                    'data_participacao'
                ],
                name='unico_matricula_data'
            )
        ]