"use client";

import { useCallback, useState } from "react";
import { FormModal } from "@/components/cadastro-modal";
import { PessoaFaixa } from "@/components/pessoa-faixa";
import { ProfessorForm } from "@/components/professor-form";
import type { Professor } from "@/lib/gestao-types";

type ProfessorItem = {
  professor: Professor;
  etiquetas: string[];
};

export function ProfessoresLista({ itens }: { itens: ProfessorItem[] }) {
  const [editando, setEditando] = useState<Professor | null>(null);
  const fechar = useCallback(() => setEditando(null), []);

  return (
    <>
      <div className="faixa-lista">
        {itens.map((item) => (
          <PessoaFaixa
            key={item.professor.id}
            nome={item.professor.nome}
            imagem={item.professor.imagem}
            etiquetas={item.etiquetas}
            onClick={() => setEditando(item.professor)}
          />
        ))}
      </div>
      <FormModal titulo="Editar Professor" aberto={editando !== null} onFechar={fechar}>
        {editando ? <ProfessorForm key={editando.id} professor={editando} /> : null}
      </FormModal>
    </>
  );
}
