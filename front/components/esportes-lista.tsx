"use client";

import { useCallback, useState } from "react";
import { FormModal } from "@/components/cadastro-modal";
import { EsporteForm } from "@/components/esporte-form";
import type { Esporte } from "@/lib/gestao-types";

export function EsportesLista({ esportes }: { esportes: Esporte[] }) {
  const [editando, setEditando] = useState<Esporte | null>(null);
  const fechar = useCallback(() => setEditando(null), []);

  return (
    <>
      <ul className="cards">
        {esportes.map((esporte) => (
          <li key={esporte.id}>
            <button type="button" className="card" onClick={() => setEditando(esporte)}>
              {esporte.imagem ? <img src={esporte.imagem} alt="" /> : <span className="sem-imagem">Sem imagem</span>}
              <strong>{esporte.nome}</strong>
              <span>{esporte.categoria || "Sem categoria"}</span>
              {esporte.descricao ? <span>{esporte.descricao}</span> : null}
            </button>
          </li>
        ))}
      </ul>
      <FormModal titulo="Editar Esporte" aberto={editando !== null} onFechar={fechar}>
        {editando ? <EsporteForm key={editando.id} esporte={editando} /> : null}
      </FormModal>
    </>
  );
}
