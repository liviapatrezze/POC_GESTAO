from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.gestao.models import Aluno, Esporte, Horario, MatriculaHorario, Professor


class GestaoApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.esporte = Esporte.objects.create(nome="Futsal", categoria="Coletivo")
        self.professor = Professor.objects.create(nome="Ana", cpf="15350946056")

    def test_cria_aluno_com_cpf_valido(self) -> None:
        response = self.client.post(
            "/api/alunos/",
            {
                "nome": "João Silva",
                "cpf": "529.982.247-25",
                "telefone": "(16) 99999-8888",
                "endereco": "Rua A",
                "numero": "10",
                "estado": "SP",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["cpf"], "52998224725")
        self.assertEqual(response.json()["telefone"], "16999998888")
        self.assertTrue(response.json()["ativo"])

    def test_formulario_sem_ativo_grava_aluno_ativo(self) -> None:
        response = self.client.post(
            "/api/alunos/",
            {
                "nome": "Formulário",
                "cpf": "15350946056",
                "endereco": "Rua D",
                "numero": "2",
                "estado": "RJ",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json()["ativo"])

    def test_rejeita_cpf_invalido(self) -> None:
        response = self.client.post(
            "/api/alunos/",
            {
                "nome": "João Silva",
                "cpf": "111.111.111-11",
                "endereco": "Rua A",
                "numero": "10",
                "estado": "SP",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rejeita_horario_com_fim_antes_do_inicio(self) -> None:
        response = self.client.post(
            "/api/horarios/",
            {
                "esporte": self.esporte.id,
                "professor": self.professor.id,
                "dia_semana": "SEG",
                "hora_inicio": "10:00",
                "hora_fim": "09:00",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rejeita_turma_repetida(self) -> None:
        payload = {
            "esporte": self.esporte.id,
            "professor": self.professor.id,
            "dia_semana": "SEG",
            "hora_inicio": "08:00",
            "hora_fim": "09:00",
        }
        primeira = self.client.post("/api/horarios/", payload, format="json")
        self.assertEqual(primeira.status_code, status.HTTP_201_CREATED)
        repetida = self.client.post("/api/horarios/", payload, format="json")
        self.assertEqual(repetida.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Horario.objects.count(), 1)

    def test_matricula_e_presenca_de_hoje(self) -> None:
        aluno = Aluno.objects.create(
            nome="Maria",
            cpf="39053344705",
            endereco="Rua B",
            numero="20",
            estado="SP",
        )
        horario = Horario.objects.create(
            esporte=self.esporte,
            professor=self.professor,
            dia_semana="TER",
            hora_inicio="08:00",
            hora_fim="09:00",
        )
        criar = self.client.post(
            "/api/matriculas/",
            {"aluno": aluno.id, "horario": horario.id},
            format="json",
        )
        self.assertEqual(criar.status_code, status.HTTP_201_CREATED)
        matricula_id = criar.json()["id"]

        duplicada = self.client.post(
            "/api/matriculas/",
            {"aluno": aluno.id, "horario": horario.id},
            format="json",
        )
        self.assertEqual(duplicada.status_code, status.HTTP_400_BAD_REQUEST)

        presenca = self.client.post(
            f"/api/matriculas/{matricula_id}/presenca/",
            {"presente": True},
            format="json",
        )
        self.assertEqual(presenca.status_code, status.HTTP_200_OK)
        self.assertTrue(presenca.json()["presente"])
        self.assertEqual(MatriculaHorario.objects.count(), 1)


class SeedOperacaoTests(TestCase):
    def test_cobre_pelo_menos_tres_meses(self) -> None:
        from datetime import date, timedelta

        from apps.gestao.models import Participacao
        from apps.gestao.seeds.operacao import popular

        hoje = date(2026, 10, 5)
        resumo = popular(hoje)
        primeira = Participacao.objects.order_by("data_participacao").first()
        ultima = Participacao.objects.order_by("-data_participacao").first()
        self.assertIsNotNone(primeira)
        self.assertIsNotNone(ultima)
        assert primeira is not None
        assert ultima is not None
        self.assertLessEqual(primeira.data_participacao, hoje - timedelta(days=90))
        self.assertEqual(ultima.data_participacao, hoje)
        self.assertGreaterEqual(int(resumo["dias"]), 90)
        self.assertGreater(int(resumo["participacoes"]), 400)
        self.assertTrue(Participacao.objects.filter(presente=True).exists())
        self.assertTrue(Participacao.objects.filter(presente=False, data_participacao=hoje).exists())
        self.assertTrue(MatriculaHorario.objects.filter(ativo=False).exists())
        self.assertTrue(Aluno.objects.filter(ativo=False).exists())
        self.assertTrue(Horario.objects.filter(ativo=False).exists())

