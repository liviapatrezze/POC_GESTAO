"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { useFecharCadastro } from "@/components/cadastro-modal";
import { createJson, patchMatricula, updateJson } from "@/lib/gestao-api";
import type { Aluno, Esporte, Horario, Matricula, Professor } from "@/lib/gestao-types";

const DIAS = [
  { value: "SEG", label: "Segunda" },
  { value: "TER", label: "Terça" },
  { value: "QUA", label: "Quarta" },
  { value: "QUI", label: "Quinta" },
  { value: "SEX", label: "Sexta" },
  { value: "SAB", label: "Sábado" },
  { value: "DOM", label: "Domingo" },
] as const;

type Dia = (typeof DIAS)[number]["value"];

type HorarioFormProps = {
  esportes: Esporte[];
  professores: Professor[];
  alunos?: Aluno[];
  matriculas?: Matricula[];
  horario?: Horario;
};

async function matricularAlunos(horarioId: number, alunoIds: number[], alunos: Aluno[]): Promise<string[]> {
  const falhas: string[] = [];
  for (const alunoId of alunoIds) {
    const nome = alunos.find((aluno) => aluno.id === alunoId)?.nome ?? "Aluno";
    try {
      await createJson("/api/matriculas/", { aluno: alunoId, horario: horarioId });
    } catch (error) {
      const mensagem = error instanceof Error ? error.message : "Não foi possível matricular o aluno.";
      falhas.push(`${nome}: ${mensagem}`);
    }
  }
  return falhas;
}

async function sincronizarAlunos(
  horarioId: number,
  alunoIds: number[],
  matriculas: Matricula[],
  alunos: Aluno[],
): Promise<string[]> {
  const daTurma = matriculas.filter((item) => item.horario === horarioId);
  const falhas: string[] = [];
  for (const alunoId of alunoIds) {
    const nome = alunos.find((aluno) => aluno.id === alunoId)?.nome ?? "Aluno";
    const atual = daTurma.find((item) => item.aluno === alunoId);
    try {
      if (!atual) {
        await createJson("/api/matriculas/", { aluno: alunoId, horario: horarioId });
      } else if (!atual.ativo) {
        await patchMatricula(atual.id, true);
      }
    } catch (error) {
      const mensagem = error instanceof Error ? error.message : "Não foi possível matricular o aluno.";
      falhas.push(`${nome}: ${mensagem}`);
    }
  }
  for (const atual of daTurma) {
    if (!atual.ativo || alunoIds.includes(atual.aluno)) {
      continue;
    }
    try {
      await patchMatricula(atual.id, false);
    } catch (error) {
      const mensagem = error instanceof Error ? error.message : "Não foi possível remover o aluno.";
      falhas.push(`${atual.aluno_nome}: ${mensagem}`);
    }
  }
  return falhas;
}

function alunosIniciais(horario: Horario | undefined, matriculas: Matricula[]): number[] {
  if (!horario) {
    return [];
  }
  return matriculas.filter((item) => item.horario === horario.id && item.ativo).map((item) => item.aluno);
}

function diaInicial(horario: Horario | undefined): Dia[] {
  if (!horario) {
    return [];
  }
  const encontrado = DIAS.find((dia) => dia.value === horario.dia_semana);
  return encontrado ? [encontrado.value] : [];
}

export function HorarioForm({
  esportes,
  professores,
  alunos = [],
  matriculas = [],
  horario,
}: HorarioFormProps) {
  const router = useRouter();
  const fechar = useFecharCadastro();
  const [erro, setErro] = useState("");
  const [pending, setPending] = useState(false);
  const [dias, setDias] = useState<Dia[]>(() => diaInicial(horario));
  const [alunosMarcados, setAlunosMarcados] = useState<number[]>(() => alunosIniciais(horario, matriculas));
  const todos = dias.length === DIAS.length;
  const alunosVisiveis = alunos.filter((aluno) => aluno.ativo || alunosMarcados.includes(aluno.id));
  const todosAlunos =
    alunosVisiveis.length > 0 && alunosVisiveis.every((aluno) => alunosMarcados.includes(aluno.id));
  const esportesVisiveis = esportes.filter((esporte) => esporte.ativo || esporte.id === horario?.esporte);
  const professoresVisiveis = professores.filter(
    (professor) => professor.ativo || professor.id === horario?.professor,
  );

  function marcarTodos(marcado: boolean) {
    setDias(marcado ? DIAS.map((dia) => dia.value) : []);
  }

  function marcarTodosAlunos(marcado: boolean) {
    setAlunosMarcados(marcado ? alunosVisiveis.map((aluno) => aluno.id) : []);
  }

  function marcarAluno(alunoId: number, marcado: boolean) {
    setAlunosMarcados((atual) => {
      if (marcado) {
        return atual.includes(alunoId) ? atual : [...atual, alunoId];
      }
      return atual.filter((item) => item !== alunoId);
    });
  }

  function marcarDia(dia: Dia, marcado: boolean) {
    if (horario) {
      setDias(marcado ? [dia] : []);
      return;
    }
    setDias((atual) => {
      if (marcado) {
        return atual.includes(dia) ? atual : [...atual, dia];
      }
      return atual.filter((item) => item !== dia);
    });
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    if (dias.length === 0) {
      setErro("Selecione ao menos um dia da semana.");
      return;
    }
    if (horario) {
      if (dias.length !== 1) {
        setErro("Escolha um dia da semana.");
        return;
      }
      setPending(true);
      setErro("");
      try {
        await updateJson(`/api/horarios/${horario.id}/`, {
          esporte: Number(data.get("esporte")),
          professor: Number(data.get("professor")),
          dia_semana: dias[0],
          hora_inicio: String(data.get("hora_inicio")),
          hora_fim: String(data.get("hora_fim")),
        });
        const matriculasFalhas = await sincronizarAlunos(horario.id, alunosMarcados, matriculas, alunosVisiveis);
        if (matriculasFalhas.length > 0) {
          setErro(matriculasFalhas.join(" "));
          setPending(false);
          return;
        }
        if (fechar) {
          fechar();
        } else {
          router.push("/horarios");
        }
        router.refresh();
      } catch (error) {
        setErro(error instanceof Error ? error.message : "Não foi possível salvar a turma.");
        setPending(false);
      }
      return;
    }
    setPending(true);
    setErro("");
    const falhas: string[] = [];
    for (const dia of dias) {
      const nome = DIAS.find((item) => item.value === dia)?.label ?? dia;
      try {
        const criada = await createJson<Horario>("/api/horarios/", {
          esporte: Number(data.get("esporte")),
          professor: Number(data.get("professor")),
          dia_semana: dia,
          hora_inicio: String(data.get("hora_inicio")),
          hora_fim: String(data.get("hora_fim")),
        });
        const matriculasFalhas = await matricularAlunos(criada.id, alunosMarcados, alunosVisiveis);
        if (matriculasFalhas.length > 0) {
          falhas.push(`${nome}: ${matriculasFalhas.join(" ")}`);
        }
      } catch (error) {
        const mensagem = error instanceof Error ? error.message : "Não foi possível cadastrar a turma.";
        falhas.push(`${nome}: ${mensagem}`);
      }
    }
    if (falhas.length > 0) {
      setErro(falhas.join(" "));
      setPending(false);
      return;
    }
    if (fechar) {
      fechar();
    } else {
      router.push("/horarios");
    }
    router.refresh();
  }

  return (
    <form className="turma-form" onSubmit={handleSubmit} aria-busy={pending}>
      {erro ? <p className="error" role="alert">{erro}</p> : null}
      <div className="form-grid">
        <label>
          Esporte
          <select name="esporte" required defaultValue={horario ? String(horario.esporte) : ""}>
            <option value="" disabled>
              Selecione
            </option>
            {esportesVisiveis.map((esporte) => (
              <option key={esporte.id} value={esporte.id}>
                {esporte.nome}
              </option>
            ))}
          </select>
        </label>
        <label>
          Professor
          <select name="professor" required defaultValue={horario ? String(horario.professor) : ""}>
            <option value="" disabled>
              Selecione
            </option>
            {professoresVisiveis.map((professor) => (
              <option key={professor.id} value={professor.id}>
                {professor.nome}
              </option>
            ))}
          </select>
        </label>
      </div>
      <fieldset className="dias">
        <legend>Dia da semana</legend>
        <div className="dias-opcoes">
          {horario ? null : (
            <label className="check-line">
              <input
                type="checkbox"
                checked={todos}
                onChange={(event) => marcarTodos(event.target.checked)}
              />
              Todos os dias
            </label>
          )}
          {DIAS.map((dia) => (
            <label key={dia.value} className="check-line">
              <input
                type="checkbox"
                checked={dias.includes(dia.value)}
                onChange={(event) => marcarDia(dia.value, event.target.checked)}
              />
              {dia.label}
            </label>
          ))}
        </div>
      </fieldset>
      <div className="turma-horas">
        <label>
          Hora início
          <input name="hora_inicio" type="time" required defaultValue={horario?.hora_inicio.slice(0, 5) ?? ""} />
        </label>
        <span>Até</span>
        <label>
          Hora final
          <input name="hora_fim" type="time" required defaultValue={horario?.hora_fim.slice(0, 5) ?? ""} />
        </label>
      </div>
      <fieldset className="dias">
        <legend>Alunos</legend>
        {alunosVisiveis.length === 0 ? (
          <p className="empty">Nenhum aluno cadastrado.</p>
        ) : (
          <div className="alunos-opcoes">
            <label className="check-line">
              <input
                type="checkbox"
                checked={todosAlunos}
                onChange={(event) => marcarTodosAlunos(event.target.checked)}
              />
              Todos
            </label>
            {alunosVisiveis.map((aluno) => (
              <label key={aluno.id} className="check-line">
                <input
                  type="checkbox"
                  checked={alunosMarcados.includes(aluno.id)}
                  onChange={(event) => marcarAluno(aluno.id, event.target.checked)}
                />
                {aluno.nome}
              </label>
            ))}
          </div>
        )}
      </fieldset>
      <div className="form-actions-end">
        <button type="submit" disabled={pending}>
          {pending ? "Salvando..." : horario ? "Salvar" : "Cadastrar"}
        </button>
      </div>
    </form>
  );
}
