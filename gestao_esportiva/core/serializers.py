# ============================================================
# SERIALIZERS DA API
# ============================================================
# Os serializers fazem a comunicação entre os modelos do Django
# e a API REST.
#
# Além de transformar os dados em JSON, eles também são um
# ótimo lugar para colocar validações dos dados recebidos pela
# API.
#
# IMPORTANTE:
# Estas validações fazem parte do BACKEND.
# O frontend poderá ter máscaras e validações próprias,
# mas o backend continua sendo responsável por conferir
# se os dados recebidos são válidos.
# ============================================================

import re

from rest_framework import serializers

from .models import (
    Aluno,
    Esporte,
    Professor,
    Horario,
    Participacao,
)


# ============================================================
# FUNÇÃO AUXILIAR - VALIDAÇÃO DE CPF
# ============================================================
def validar_cpf(cpf):
    """
    Valida um CPF brasileiro.

    O banco continua armazenando somente os 11 números.

    Exemplos aceitos depois da limpeza:
        12345678909

    Também podemos receber formatos como:
        123.456.789-09

    A pontuação será retirada antes da validação.
    """

    # Remove qualquer caractere que não seja número.
    cpf = re.sub(r"\D", "", cpf)

    # CPF precisa possuir exatamente 11 números.
    if len(cpf) != 11:
        raise serializers.ValidationError(
            "O CPF deve possuir 11 números."
        )

    # Impede CPFs formados por um único número repetido.
    # Exemplos:
    # 11111111111
    # 22222222222
    # 00000000000
    if cpf == cpf[0] * 11:
        raise serializers.ValidationError(
            "Informe um CPF válido."
        )

    # --------------------------------------------------------
    # CÁLCULO DO PRIMEIRO DÍGITO VERIFICADOR
    # --------------------------------------------------------

    soma = 0

    for indice in range(9):
        soma += int(cpf[indice]) * (10 - indice)

    resto = soma % 11

    if resto < 2:
        primeiro_digito = 0
    else:
        primeiro_digito = 11 - resto

    # Compara com o primeiro dígito verificador informado.
    if primeiro_digito != int(cpf[9]):
        raise serializers.ValidationError(
            "Informe um CPF válido."
        )

    # --------------------------------------------------------
    # CÁLCULO DO SEGUNDO DÍGITO VERIFICADOR
    # --------------------------------------------------------

    soma = 0

    for indice in range(10):
        soma += int(cpf[indice]) * (11 - indice)

    resto = soma % 11

    if resto < 2:
        segundo_digito = 0
    else:
        segundo_digito = 11 - resto

    # Compara com o segundo dígito verificador.
    if segundo_digito != int(cpf[10]):
        raise serializers.ValidationError(
            "Informe um CPF válido."
        )

    # Retornamos o CPF somente com números.
    return cpf


# ============================================================
# FUNÇÃO AUXILIAR - VALIDAÇÃO DE TELEFONE
# ============================================================
def validar_telefone(telefone):
    """
    Valida telefone brasileiro.

    Aceita 10 números:
        telefone fixo

    Ou 11 números:
        telefone celular

    Exemplos:
        1633334444
        16999998888

    Formatações como:
        (16) 3333-4444
        (16) 99999-8888

    também podem ser recebidas, pois a pontuação será retirada.
    """

    # Remove espaços, parênteses, hífen etc.
    telefone = re.sub(r"\D", "", telefone)

    # Telefone brasileiro normalmente possui 10 ou 11 números.
    if len(telefone) not in (10, 11):
        raise serializers.ValidationError(
            "O telefone deve possuir 10 ou 11 números."
        )

    # Retorna somente os números para manter o padrão do banco.
    return telefone


# ============================================================
# SERIALIZER DE ALUNOS
# ============================================================
class AlunoSerializer(serializers.ModelSerializer):

    # Aceita CPF formatado:
    # 408.946.438-27
    #
    # A função validate_cpf() posteriormente
    # remove a formatação e mantém somente os números.
    cpf = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=14
    )

    # Aceita telefone formatado:
    # (16) 99991-8248
    telefone = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=15
    )

    class Meta:
        model = Aluno
        fields = "__all__"

        extra_kwargs = {
            "nome": {
                "required": True,
                "allow_blank": False,
            },
            "endereco": {
                "required": True,
                "allow_blank": False,
            },
            "numero": {
                "required": True,
                "allow_blank": False,
            },
            "estado": {
                "required": True,
                "allow_blank": False,
            },
        }

    def validate_cpf(self, value):
        return validar_cpf(value)

    def validate_telefone(self, value):

        if not value:
            return value

        return validar_telefone(value)

    # --------------------------------------------------------
    # VALIDAÇÃO DO CPF DO ALUNO
    # --------------------------------------------------------
    def validate_cpf(self, value):

        # A função também remove a pontuação.
        return validar_cpf(value)

    # --------------------------------------------------------
    # VALIDAÇÃO DO TELEFONE DO ALUNO
    # --------------------------------------------------------
    def validate_telefone(self, value):

        # Telefone é opcional no modelo.
        # Se estiver vazio, permitimos o cadastro.
        if not value:
            return value

        return validar_telefone(value)


# ============================================================
# SERIALIZER DE ESPORTES
# ============================================================
class EsporteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Esporte
        fields = "__all__"


# ============================================================
# SERIALIZER DE PROFESSORES
# ============================================================
class ProfessorSerializer(serializers.ModelSerializer):

    # Aceita CPF com pontuação no formulário.
    cpf = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=14
    )

    # Aceita telefone com máscara.
    telefone = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=15
    )

    class Meta:
        model = Professor
        fields = "__all__"

        extra_kwargs = {
            "nome": {
                "required": True,
                "allow_blank": False,
            },
        }

    def validate_cpf(self, value):
        return validar_cpf(value)

    def validate_telefone(self, value):

        if not value:
            return value

        return validar_telefone(value)

    
    # --------------------------------------------------------
    # VALIDAÇÃO DO CPF DO PROFESSOR
    # --------------------------------------------------------
    def validate_cpf(self, value):

        return validar_cpf(value)

    # --------------------------------------------------------
    # VALIDAÇÃO DO TELEFONE DO PROFESSOR
    # --------------------------------------------------------
    def validate_telefone(self, value):

        if not value:
            return value

        return validar_telefone(value)


# ============================================================
# SERIALIZER DE HORÁRIOS
# ============================================================
class HorarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Horario
        fields = "__all__"

    # --------------------------------------------------------
    # VALIDAÇÕES DO HORÁRIO
    # --------------------------------------------------------
    def validate(self, attrs):
        """
        Executa validações que dependem de mais de um campo.

        Aqui conseguimos comparar:
        - hora_inicio
        - hora_fim

        Também verificamos se:
        - o professor está ativo;
        - o esporte está ativo.
        """

        # ----------------------------------------------------
        # OBTÉM OS DADOS RECEBIDOS
        # ----------------------------------------------------

        hora_inicio = attrs.get("hora_inicio")
        hora_fim = attrs.get("hora_fim")

        esporte = attrs.get("esporte")
        professor = attrs.get("professor")

        # ----------------------------------------------------
        # VALIDAÇÃO DAS HORAS
        # ----------------------------------------------------

        # Verifica se a hora inicial e final foram informadas.
        if not hora_inicio or not hora_fim:
            raise serializers.ValidationError(
                "A hora de início e a hora de fim são obrigatórias."
            )

        # A hora final precisa ser posterior à hora inicial.
        if hora_fim <= hora_inicio:
            raise serializers.ValidationError(
                "A hora de fim deve ser posterior à hora de início."
            )

        # ----------------------------------------------------
        # VALIDAÇÃO DO ESPORTE
        # ----------------------------------------------------

        # O esporte precisa existir e estar ativo.
        if esporte and not esporte.ativo:
            raise serializers.ValidationError(
                "Não é possível criar um horário para um esporte inativo."
            )

        # ----------------------------------------------------
        # VALIDAÇÃO DO PROFESSOR
        # ----------------------------------------------------

        # O professor precisa existir e estar ativo.
        if professor and not professor.ativo:
            raise serializers.ValidationError(
                "Não é possível criar um horário para um professor inativo."
            )

        # Se todas as regras forem atendidas,
        # os dados podem continuar o processo de cadastro.
        return attrs


# ============================================================
# SERIALIZER DE PARTICIPAÇÃO / FREQUÊNCIA
# ============================================================
class ParticipacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participacao
        fields = "__all__"