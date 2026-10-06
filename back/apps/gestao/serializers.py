from datetime import date

from rest_framework import serializers

from apps.gestao.models import Aluno, Esporte, Horario, MatriculaHorario, Participacao, Professor
from apps.gestao.validators import validar_cpf, validar_telefone


class AtivoField(serializers.BooleanField):
    def __init__(self, **kwargs: object) -> None:
        kwargs.setdefault("default", True)
        kwargs.setdefault("required", False)
        super().__init__(**kwargs)

    def get_value(self, dictionary: object) -> object:
        if isinstance(dictionary, dict) and self.field_name not in dictionary:
            return serializers.empty
        return super().get_value(dictionary)


class AlunoSerializer(serializers.ModelSerializer):
    cpf = serializers.CharField(max_length=14)
    telefone = serializers.CharField(required=False, allow_blank=True, max_length=15)
    ativo = AtivoField()

    class Meta:
        model = Aluno
        fields = [
            "id",
            "nome",
            "cpf",
            "telefone",
            "email",
            "data_nascimento",
            "endereco",
            "numero",
            "bairro",
            "cidade",
            "estado",
            "imagem",
            "data_cadastro",
            "ativo",
        ]
        read_only_fields = ["id", "data_cadastro"]

    def validate_cpf(self, value: str) -> str:
        return validar_cpf(value)

    def validate_telefone(self, value: str) -> str:
        return validar_telefone(value)


class EsporteSerializer(serializers.ModelSerializer):
    ativo = AtivoField()

    class Meta:
        model = Esporte
        fields = ["id", "nome", "imagem", "descricao", "categoria", "ativo"]
        read_only_fields = ["id"]


class ProfessorSerializer(serializers.ModelSerializer):
    cpf = serializers.CharField(max_length=14)
    telefone = serializers.CharField(required=False, allow_blank=True, max_length=15)
    ativo = AtivoField()

    class Meta:
        model = Professor
        fields = ["id", "nome", "cpf", "telefone", "email", "imagem", "ativo"]
        read_only_fields = ["id"]

    def validate_cpf(self, value: str) -> str:
        return validar_cpf(value)

    def validate_telefone(self, value: str) -> str:
        return validar_telefone(value)


class HorarioSerializer(serializers.ModelSerializer):
    esporte_nome = serializers.CharField(source="esporte.nome", read_only=True)
    professor_nome = serializers.CharField(source="professor.nome", read_only=True)
    dia_semana_display = serializers.CharField(source="get_dia_semana_display", read_only=True)
    ativo = AtivoField()

    class Meta:
        model = Horario
        fields = [
            "id",
            "esporte",
            "esporte_nome",
            "professor",
            "professor_nome",
            "dia_semana",
            "dia_semana_display",
            "hora_inicio",
            "hora_fim",
            "ativo",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs: dict[str, object]) -> dict[str, object]:
        inicio = attrs.get("hora_inicio", getattr(self.instance, "hora_inicio", None))
        fim = attrs.get("hora_fim", getattr(self.instance, "hora_fim", None))
        esporte = attrs.get("esporte", getattr(self.instance, "esporte", None))
        professor = attrs.get("professor", getattr(self.instance, "professor", None))
        if inicio is None or fim is None:
            raise serializers.ValidationError("A hora de início e a hora de fim são obrigatórias.")
        if fim <= inicio:
            raise serializers.ValidationError("A hora de fim deve ser posterior à hora de início.")
        if isinstance(esporte, Esporte) and not esporte.ativo:
            raise serializers.ValidationError("Não é possível criar um horário para um esporte inativo.")
        if isinstance(professor, Professor) and not professor.ativo:
            raise serializers.ValidationError("Não é possível criar um horário para um professor inativo.")
        dia = attrs.get("dia_semana", getattr(self.instance, "dia_semana", None))
        if (
            isinstance(esporte, Esporte)
            and isinstance(professor, Professor)
            and inicio is not None
            and fim is not None
            and isinstance(dia, str)
        ):
            conflito = Horario.objects.filter(
                esporte=esporte,
                professor=professor,
                dia_semana=dia,
                hora_inicio=inicio,
                hora_fim=fim,
            )
            if self.instance is not None:
                conflito = conflito.exclude(pk=self.instance.pk)
            if conflito.exists():
                raise serializers.ValidationError(
                    "Já existe uma turma com este esporte, professor, dia e faixa de hora."
                )
        return attrs


class MatriculaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source="aluno.nome", read_only=True)
    aluno_imagem = serializers.ImageField(source="aluno.imagem", read_only=True)
    esporte = serializers.CharField(source="horario.esporte.nome", read_only=True)
    professor = serializers.CharField(source="horario.professor.nome", read_only=True)
    dia_semana = serializers.CharField(source="horario.dia_semana", read_only=True)
    dia_semana_display = serializers.CharField(source="horario.get_dia_semana_display", read_only=True)
    hora_inicio = serializers.TimeField(source="horario.hora_inicio", read_only=True)
    hora_fim = serializers.TimeField(source="horario.hora_fim", read_only=True)
    presente_hoje = serializers.SerializerMethodField()
    ativo = AtivoField()

    class Meta:
        model = MatriculaHorario
        fields = [
            "id",
            "aluno",
            "horario",
            "ativo",
            "data_matricula",
            "aluno_nome",
            "aluno_imagem",
            "esporte",
            "professor",
            "dia_semana",
            "dia_semana_display",
            "hora_inicio",
            "hora_fim",
            "presente_hoje",
        ]
        read_only_fields = ["id", "data_matricula"]

    def get_presente_hoje(self, obj: MatriculaHorario) -> bool | None:
        if "presente_hoje" in obj.__dict__:
            valor = obj.__dict__["presente_hoje"]
            if valor is None:
                return None
            return bool(valor)
        participacao = obj.participacoes.filter(data_participacao=date.today()).first()
        if participacao is None:
            return None
        return participacao.presente

    def validate(self, attrs: dict[str, object]) -> dict[str, object]:
        if self.instance is not None:
            return attrs
        aluno = attrs.get("aluno")
        horario = attrs.get("horario")
        if not isinstance(aluno, Aluno) or not isinstance(horario, Horario):
            raise serializers.ValidationError("Aluno e horário são obrigatórios.")
        if not aluno.ativo:
            raise serializers.ValidationError("Não é possível matricular um aluno inativo.")
        if not horario.ativo:
            raise serializers.ValidationError("Não é possível matricular em um horário inativo.")
        if not horario.esporte.ativo:
            raise serializers.ValidationError("Não é possível matricular em um esporte inativo.")
        if not horario.professor.ativo:
            raise serializers.ValidationError("Não é possível matricular em um horário de professor inativo.")
        if MatriculaHorario.objects.filter(aluno=aluno, horario=horario).exists():
            raise serializers.ValidationError("Este aluno já está matriculado neste horário.")
        return attrs


class ParticipacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participacao
        fields = ["id", "matricula", "data_participacao", "presente", "data_registro"]
        read_only_fields = ["id", "data_registro"]
