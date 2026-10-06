"use client";

import { useCallback, useState } from "react";
import { useRouter } from "next/navigation";
import { AlunoForm } from "@/components/aluno-form";
import { FormModal } from "@/components/cadastro-modal";
import { HorarioForm } from "@/components/horario-form";
import { registrarPresenca } from "@/lib/gestao-api";
import type { Aluno, Esporte, Horario, Matricula, Professor } from "@/lib/gestao-types";
import { rotuloTurma } from "@/lib/turma";

type FrequenciaTabelaProps = {
  horarios: Horario[];
  matriculas: Matricula[];
  alunos: Aluno[];
  esportes: Esporte[];
  professores: Professor[];
};

export function FrequenciaTabela({
  horarios,
  matriculas,
  alunos,
  esportes,
  professores,
}: FrequenciaTabelaProps) {
  const router = useRouter();
  const [erro, setErro] = useState("");
  const [alunoEditando, setAlunoEditando] = useState<Aluno | null>(null);
  const [turmaEditando, setTurmaEditando] = useState<Horario | null>(null);
  const fecharAluno = useCallback(() => setAlunoEditando(null), []);
  const fecharTurma = useCallback(() => setTurmaEditando(null), []);
  const turmas = horarios.filter((horario) => horario.ativo);
  const [horarioId, setHorarioId] = useState(turmas[0] ? String(turmas[0].id) : "");
  const turma = turmas.find((horario) => String(horario.id) === horarioId) ?? null;
  const presentes = matriculas.filter(
    (matricula) => matricula.ativo && String(matricula.horario) === horarioId,
  );

  async function marcar(id: number, presente: boolean) {
    setErro("");
    try {
      await registrarPresenca(id, presente);
      router.refresh();
    } catch (error) {
      setErro(error instanceof Error ? error.message : "Não foi possível registrar a frequência.");
    }
  }

  if (turmas.length === 0) {
    return <p className="empty">Nenhuma turma cadastrada ainda.</p>;
  }

  return (
    <div className="presenca">
      <div className="presenca-turma">
        <label>
          Turma
          <select value={horarioId} onChange={(event) => setHorarioId(event.target.value)}>
            {turmas.map((item) => (
              <option key={item.id} value={item.id}>
                {rotuloTurma(item.dia_semana, item.esporte_nome, item.hora_inicio, item.hora_fim)}
              </option>
            ))}
          </select>
        </label>
        {turma ? (
          <>
            <p className="presenca-professor">Professor: {turma.professor_nome}</p>
            <button type="button" className="presenca-editar" onClick={() => setTurmaEditando(turma)}>
              Editar turma
            </button>
          </>
        ) : null}
      </div>
      <div className="presenca-lista">
        <h2>O aluno esteve presente?</h2>
        {erro ? <p className="error" role="alert">{erro}</p> : null}
        {presentes.length === 0 ? (
          <p className="empty">Nenhum aluno matriculado nesta turma.</p>
        ) : (
          <ul>
            {presentes.map((matricula) => {
              const aluno = alunos.find((item) => item.id === matricula.aluno) ?? null;
              return (
                <li key={matricula.id}>
                  <button
                    type="button"
                    className="presenca-nome"
                    onClick={() => {
                      if (aluno) {
                        setAlunoEditando(aluno);
                      }
                    }}
                    disabled={aluno === null}
                    aria-label={`Editar aluno ${matricula.aluno_nome}`}
                  >
                    {matricula.aluno_nome}
                  </button>
                  <div className="presenca-marca" role="group" aria-label={`Presença de ${matricula.aluno_nome}`}>
                    <button
                      type="button"
                      className={matricula.presente_hoje === true ? "marcado presente" : undefined}
                      onClick={() => void marcar(matricula.id, true)}
                      aria-pressed={matricula.presente_hoje === true}
                      aria-label={`Marcar ${matricula.aluno_nome} como presente`}
                    >
                      ✓
                    </button>
                    <button
                      type="button"
                      className={matricula.presente_hoje === false ? "marcado ausente" : undefined}
                      onClick={() => void marcar(matricula.id, false)}
                      aria-pressed={matricula.presente_hoje === false}
                      aria-label={`Marcar ${matricula.aluno_nome} como ausente`}
                    >
                      ✕
                    </button>
                  </div>
                </li>
              );
            })}
          </ul>
        )}
      </div>
      <FormModal titulo="Editar Aluno" aberto={alunoEditando !== null} onFechar={fecharAluno}>
        {alunoEditando ? <AlunoForm key={alunoEditando.id} aluno={alunoEditando} /> : null}
      </FormModal>
      <FormModal titulo="Editar Turma" aberto={turmaEditando !== null} onFechar={fecharTurma}>
        {turmaEditando ? (
          <HorarioForm
            key={turmaEditando.id}
            horario={turmaEditando}
            esportes={esportes}
            professores={professores}
            alunos={alunos}
            matriculas={matriculas}
          />
        ) : null}
      </FormModal>
    </div>
  );
}
