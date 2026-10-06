"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { useFecharCadastro } from "@/components/cadastro-modal";
import { createForm, updateForm } from "@/lib/gestao-api";
import { ESTADOS, type Aluno } from "@/lib/gestao-types";

export function AlunoForm({ aluno }: { aluno?: Aluno }) {
  const router = useRouter();
  const fechar = useFecharCadastro();
  const [erro, setErro] = useState("");
  const [pending, setPending] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const data = new FormData(form);
    const nascimento = String(data.get("data_nascimento") ?? "");
    if (!nascimento) {
      data.delete("data_nascimento");
    }
    const imagem = data.get("imagem");
    if (!(imagem instanceof File) || imagem.size === 0) {
      data.delete("imagem");
    }
    setPending(true);
    setErro("");
    try {
      if (aluno) {
        await updateForm(`/api/alunos/${aluno.id}/`, data);
      } else {
        await createForm("/api/alunos/", data);
      }
      if (fechar) {
        fechar();
      } else {
        router.push("/alunos");
      }
      router.refresh();
    } catch (error) {
      setErro(error instanceof Error ? error.message : "Não foi possível salvar o aluno.");
      setPending(false);
    }
  }

  return (
    <form className="form-grid" onSubmit={handleSubmit} aria-busy={pending}>
      {erro ? <p className="error span-2" role="alert">{erro}</p> : null}
      <label className="span-2">
        Nome completo
        <input name="nome" required maxLength={150} defaultValue={aluno?.nome ?? ""} />
      </label>
      <label>
        CPF
        <input name="cpf" required maxLength={14} placeholder="000.000.000-00" defaultValue={aluno?.cpf ?? ""} />
      </label>
      <label>
        Telefone
        <input name="telefone" maxLength={15} placeholder="(00) 00000-0000" defaultValue={aluno?.telefone ?? ""} />
      </label>
      <label className="span-2">
        E-mail
        <input name="email" type="email" maxLength={254} defaultValue={aluno?.email ?? ""} />
      </label>
      <label>
        Data de nascimento
        <input name="data_nascimento" type="date" defaultValue={aluno?.data_nascimento ?? ""} />
      </label>
      <label>
        Endereço
        <input name="endereco" required maxLength={200} defaultValue={aluno?.endereco ?? ""} />
      </label>
      <label>
        Número
        <input name="numero" required maxLength={10} defaultValue={aluno?.numero ?? ""} />
      </label>
      <label>
        Bairro
        <input name="bairro" maxLength={100} defaultValue={aluno?.bairro ?? ""} />
      </label>
      <label>
        Cidade
        <input name="cidade" maxLength={100} defaultValue={aluno?.cidade ?? ""} />
      </label>
      <label>
        Estado
        <select name="estado" required defaultValue={aluno?.estado ?? ""}>
          <option value="" disabled>
            Selecione
          </option>
          {ESTADOS.map((estado) => (
            <option key={estado} value={estado}>
              {estado}
            </option>
          ))}
        </select>
      </label>
      <label className="span-2">
        Foto do aluno
        <input name="imagem" type="file" accept="image/*" />
      </label>
      <button type="submit" disabled={pending}>
        {pending ? "Salvando..." : aluno ? "Salvar" : "Cadastrar aluno"}
      </button>
    </form>
  );
}
