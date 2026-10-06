"use client";

import { useCallback, useState } from "react";
import { FormModal } from "@/components/cadastro-modal";
import { HorarioForm } from "@/components/horario-form";
import type { Aluno, Esporte, Horario, Matricula, Professor } from "@/lib/gestao-types";

type HorariosListaProps = {
  horarios: Horario[];
  esportes: Esporte[];
  professores: Professor[];
  alunos: Aluno[];
  matriculas: Matricula[];
};

export function HorariosLista({ horarios, esportes, professores, alunos, matriculas }: HorariosListaProps) {
  const [editando, setEditando] = useState<Horario | null>(null);
  const fechar = useCallback(() => setEditando(null), []);

  return (
    <>
      <table className="data">
        <thead>
          <tr>
            <th scope="col">Esporte</th>
            <th scope="col">Professor</th>
            <th scope="col">Dia</th>
            <th scope="col">Início</th>
            <th scope="col">Fim</th>
          </tr>
        </thead>
        <tbody>
          {horarios.map((horario) => (
            <tr key={horario.id} className="clicavel" onClick={() => setEditando(horario)}>
              <td>
                <button
                  type="button"
                  className="celula-editar"
                  aria-label={`Editar turma de ${horario.esporte_nome}, ${horario.dia_semana_display}`}
                  onClick={() => setEditando(horario)}
                >
                  {horario.esporte_nome}
                </button>
              </td>
              <td>{horario.professor_nome}</td>
              <td>{horario.dia_semana_display}</td>
              <td>{horario.hora_inicio.slice(0, 5)}</td>
              <td>{horario.hora_fim.slice(0, 5)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <FormModal titulo="Editar Turma" aberto={editando !== null} onFechar={fechar}>
        {editando ? (
          <HorarioForm
            key={editando.id}
            horario={editando}
            esportes={esportes}
            professores={professores}
            alunos={alunos}
            matriculas={matriculas}
          />
        ) : null}
      </FormModal>
    </>
  );
}
