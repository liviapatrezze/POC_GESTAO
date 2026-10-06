"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { useFecharCadastro } from "@/components/cadastro-modal";
import { createForm, updateForm } from "@/lib/gestao-api";
import type { Professor } from "@/lib/gestao-types";

export function ProfessorForm({ professor }: { professor?: Professor }) {
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
      if (professor) {
        await updateForm(`/api/professores/${professor.id}/`, data);
      } else {
        await createForm("/api/professores/", data);
      }
      if (fechar) {
        fechar();
      } else {
        router.push("/professores");
      }
      router.refresh();
    } catch (error) {
      setErro(error instanceof Error ? error.message : "Não foi possível salvar o professor.");
      setPending(false);
    }
  }

  return (
    <form className="form-grid" onSubmit={handleSubmit} aria-busy={pending}>
      {erro ? <p className="error span-2" role="alert">{erro}</p> : null}
      <label className="span-2">
        Nome
        <input name="nome" required maxLength={150} defaultValue={professor?.nome ?? ""} />
      </label>
      <label>
        CPF
        <input name="cpf" required maxLength={14} placeholder="000.000.000-00" defaultValue={professor?.cpf ?? ""} />
      </label>
      <label>
        Telefone
        <input name="telefone" maxLength={15} placeholder="(00) 00000-0000" defaultValue={professor?.telefone ?? ""} />
      </label>
      <label className="span-2">
        E-mail
        <input name="email" type="email" defaultValue={professor?.email ?? ""} />
      </label>
      <label className="span-2">
        Foto
        <input name="imagem" type="file" accept="image/*" />
      </label>
      <button type="submit" disabled={pending}>
        {pending ? "Salvando..." : professor ? "Salvar" : "Cadastrar professor"}
      </button>
    </form>
  );
}
