"use client";

import { useCallback, useState } from "react";
import { AlunoForm } from "@/components/aluno-form";
import { FormModal } from "@/components/cadastro-modal";
import { PessoaFaixa } from "@/components/pessoa-faixa";
import type { Aluno } from "@/lib/gestao-types";

type AlunoItem = {
  aluno: Aluno;
  etiquetas: string[];
};

export function AlunosLista({ itens }: { itens: AlunoItem[] }) {
  const [editando, setEditando] = useState<Aluno | null>(null);
  const fechar = useCallback(() => setEditando(null), []);

  return (
    <>
      <div className="faixa-lista">
        {itens.map((item) => (
          <PessoaFaixa
            key={item.aluno.id}
            nome={item.aluno.nome}
            imagem={item.aluno.imagem}
            etiquetas={item.etiquetas}
            onClick={() => setEditando(item.aluno)}
          />
        ))}
      </div>
      <FormModal titulo="Editar Aluno" aberto={editando !== null} onFechar={fechar}>
        {editando ? <AlunoForm key={editando.id} aluno={editando} /> : null}
      </FormModal>
    </>
  );
}
