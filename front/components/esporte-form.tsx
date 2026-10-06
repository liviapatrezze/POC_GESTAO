"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { useFecharCadastro } from "@/components/cadastro-modal";
import { createForm, updateForm } from "@/lib/gestao-api";
import type { Esporte } from "@/lib/gestao-types";

export function EsporteForm({ esporte }: { esporte?: Esporte }) {
  const router = useRouter();
  const fechar = useFecharCadastro();
  const [erro, setErro] = useState("");
  const [pending, setPending] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const imagem = data.get("imagem");
    if (!(imagem instanceof File) || imagem.size === 0) {
      data.delete("imagem");
    }
    setPending(true);
    setErro("");
    try {
      if (esporte) {
        await updateForm(`/api/esportes/${esporte.id}/`, data);
      } else {
        await createForm("/api/esportes/", data);
      }
      if (fechar) {
        fechar();
      } else {
        router.push("/esportes");
      }
      router.refresh();
    } catch (error) {
      setErro(error instanceof Error ? error.message : "Não foi possível salvar o esporte.");
      setPending(false);
    }
  }

  return (
    <form className="form-grid" onSubmit={handleSubmit} aria-busy={pending}>
      {erro ? <p className="error span-2" role="alert">{erro}</p> : null}
      <label>
        Nome
        <input name="nome" required maxLength={100} defaultValue={esporte?.nome ?? ""} />
      </label>
      <label>
        Categoria
        <input name="categoria" maxLength={100} defaultValue={esporte?.categoria ?? ""} />
      </label>
      <label className="span-2">
        Descrição
        <textarea name="descricao" rows={4} defaultValue={esporte?.descricao ?? ""} />
      </label>
      <label className="span-2">
        Imagem
        <input name="imagem" type="file" accept="image/*" />
      </label>
      <button type="submit" disabled={pending}>
        {pending ? "Salvando..." : esporte ? "Salvar" : "Cadastrar esporte"}
      </button>
    </form>
  );
}
