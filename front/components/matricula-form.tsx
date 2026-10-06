"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useMemo, useState } from "react";
import { useFecharCadastro } from "@/components/cadastro-modal";
import { createJson, updateJson } from "@/lib/gestao-api";
import type { Aluno, Esporte, Horario, Matricula } from "@/lib/gestao-types";

type MatriculaFormProps = {
  alunos: Aluno[];
  esportes: Esporte[];
  horarios: Horario[];
  matricula?: Matricula;
};

export function MatriculaForm({ alunos, esportes, horarios, matricula }: MatriculaFormProps) {
  const router = useRouter();
  const fechar = useFecharCadastro();
  const horarioAtual = horarios.find((horario) => horario.id === matricula?.horario);
  const [esporteId, setEsporteId] = useState(horarioAtual ? String(horarioAtual.esporte) : "");
  const [erro, setErro] = useState("");
  const [pending, setPending] = useState(false);
  const horariosDoEsporte = useMemo(
    () =>
      horarios.filter(
        (horario) =>
          String(horario.esporte) === esporteId && (horario.ativo || horario.id === matricula?.horario),
      ),
    [horarios, esporteId, matricula?.horario],
  );

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    setPending(true);
    setErro("");
    try {
      if (matricula) {
        await updateJson(`/api/matriculas/${matricula.id}/`, {
          aluno: Number(data.get("aluno")),
          horario: Number(data.get("horario")),
        });
      } else {
        await createJson("/api/matriculas/", {
          aluno: Number(data.get("aluno")),
          horario: Number(data.get("horario")),
        });
      }
      if (fechar) {
        fechar();
      } else {
        router.push("/matriculas");
      }
      router.refresh();
    } catch (error) {
      setErro(error instanceof Error ? error.message : "Não foi possível salvar a matrícula.");
      setPending(false);
    }
  }

  return (
    <form className="form-grid" onSubmit={handleSubmit} aria-busy={pending}>
      {erro ? <p className="error span-2" role="alert">{erro}</p> : null}
      <label>
        Aluno
        <select name="aluno" required defaultValue={matricula ? String(matricula.aluno) : ""}>
          <option value="" disabled>
            Selecione
          </option>
          {alunos.filter((aluno) => aluno.ativo || aluno.id === matricula?.aluno).map((aluno) => (
            <option key={aluno.id} value={aluno.id}>
              {aluno.nome}
            </option>
          ))}
        </select>
      </label>
      <label>
        Esporte
        <select
          value={esporteId}
          required
          onChange={(event) => setEsporteId(event.target.value)}
        >
          <option value="" disabled>
            Selecione
          </option>
          {esportes.filter((esporte) => esporte.ativo || esporte.id === horarioAtual?.esporte).map((esporte) => (
            <option key={esporte.id} value={esporte.id}>
              {esporte.nome}
            </option>
          ))}
        </select>
      </label>
      <label className="span-2">
        Horário
        <select name="horario" required defaultValue={matricula ? String(matricula.horario) : ""}>
          <option value="" disabled>
            Selecione
          </option>
          {horariosDoEsporte.map((horario) => (
            <option key={horario.id} value={horario.id}>
              {horario.dia_semana_display} · {horario.hora_inicio.slice(0, 5)} às{" "}
              {horario.hora_fim.slice(0, 5)} · {horario.professor_nome}
            </option>
          ))}
        </select>
      </label>
      <button type="submit" disabled={pending}>
        {pending ? "Salvando..." : matricula ? "Salvar" : "Matricular"}
      </button>
    </form>
  );
}
