import re

from rest_framework import serializers


def validar_cpf(cpf: str) -> str:
    digitos = re.sub(r"\D", "", cpf)
    if len(digitos) != 11:
        raise serializers.ValidationError("O CPF deve possuir 11 números.")
    if digitos == digitos[0] * 11:
        raise serializers.ValidationError("Informe um CPF válido.")

    def digito(base: str, peso_inicial: int) -> int:
        soma = sum(int(numero) * peso for numero, peso in zip(base, range(peso_inicial, 1, -1)))
        resto = soma % 11
        if resto < 2:
            return 0
        return 11 - resto

    if digito(digitos[:9], 10) != int(digitos[9]):
        raise serializers.ValidationError("Informe um CPF válido.")
    if digito(digitos[:10], 11) != int(digitos[10]):
        raise serializers.ValidationError("Informe um CPF válido.")
    return digitos


def validar_telefone(telefone: str) -> str:
    digitos = re.sub(r"\D", "", telefone)
    if not digitos:
        return ""
    if len(digitos) not in (10, 11):
        raise serializers.ValidationError("O telefone deve possuir 10 ou 11 números.")
    return digitos
