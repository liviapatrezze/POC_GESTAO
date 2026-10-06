"use client";

import { useCallback, useState } from "react";
import { useRouter } from "next/navigation";
import { FormModal } from "@/components/cadastro-modal";
import { MatriculaForm } from "@/components/matricula-form";
import { patchMatricula } from "@/lib/gestao-api";
import type { Aluno, Esporte, Horario, Matricula } from "@/lib/gestao-types";

type MatriculaTabelaProps = {
  matriculas: Matricula[];
  alunos: Aluno[];
  esportes: Esporte[];
  horarios: Horario[];
};

export function MatriculaTabela({ matriculas, alunos, esportes, horarios }: MatriculaTabelaProps) {
  const router = useRouter();
  const [erro, setErro] = useState("");
  const [editando, setEditando] = useState<Matricula | null>(null);
  const fechar = useCallback(() => setEditando(null), []);

  async function alterar(matricula: Matricula) {
    setErro("");
    try {
      await patchMatricula(matricula.id, !matricula.ativo);
      router.refresh();
    } catch (error) {
      setErro(error instanceof Error ? error.message : "Não foi possível alterar a matrícula.");
    }
  }

  if (matriculas.length === 0) {
    return <p className="empty">Nenhuma matrícula cadastrada.</p>;
  }

  return (
    <>
      {erro ? <p className="error" role="alert">{erro}</p> : null}
      <table className="data">
        <thead>
          <tr>
            <th scope="col">Aluno</th>
            <th scope="col">Esporte</th>
            <th scope="col">Professor</th>
            <th scope="col">Horário</th>
            <th scope="col">Status</th>
            <th scope="col">
              <span className="sr-only">Ações</span>
            </th>
          </tr>
        </thead>
        <tbody>
          {matriculas.map((matricula) => (
            <tr key={matricula.id} className="clicavel" onClick={() => setEditando(matricula)}>
              <td>
                <button
                  type="button"
                  className="celula-editar"
                  aria-label={`Editar matrícula de ${matricula.aluno_nome}`}
                  onClick={() => setEditando(matricula)}
                >
                  {matricula.aluno_nome}
                </button>
              </td>
              <td>{matricula.esporte}</td>
              <td>{matricula.professor}</td>
              <td>
                {matricula.dia_semana_display} · {matricula.hora_inicio.slice(0, 5)} às{" "}
                {matricula.hora_fim.slice(0, 5)}
              </td>
              <td>{matricula.ativo ? "Ativa" : "Inativa"}</td>
              <td>
                <button
                  type="button"
                  onClick={(event) => {
                    event.stopPropagation();
                    void alterar(matricula);
                  }}
                >
                  {matricula.ativo ? "Inativar" : "Ativar"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <FormModal titulo="Editar Matrícula" aberto={editando !== null} onFechar={fechar}>
        {editando ? (
          <MatriculaForm
            key={editando.id}
            matricula={editando}
            alunos={alunos}
            esportes={esportes}
            horarios={horarios}
          />
        ) : null}
      </FormModal>
    </>
  );
}
