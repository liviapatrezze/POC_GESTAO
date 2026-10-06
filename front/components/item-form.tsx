"use client";

import { FormEvent, useState } from "react";

type ItemFormProps = {
  onCreate: (titulo: string, descricao: string) => Promise<void>;
};

export function ItemForm({ onCreate }: ItemFormProps) {
  const [titulo, setTitulo] = useState("");
  const [descricao, setDescricao] = useState("");
  const [pending, setPending] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!titulo.trim()) {
      return;
    }
    setPending(true);
    try {
      await onCreate(titulo.trim(), descricao.trim());
      setTitulo("");
      setDescricao("");
    } catch {
      return;
    } finally {
      setPending(false);
    }
  }

  return (
    <form className="item-form" onSubmit={handleSubmit} aria-busy={pending}>
      <label>
        Título
        <input
          name="titulo"
          value={titulo}
          onChange={(event) => setTitulo(event.target.value)}
          required
          maxLength={200}
        />
      </label>
      <label>
        Descrição
        <textarea
          name="descricao"
          value={descricao}
          onChange={(event) => setDescricao(event.target.value)}
          rows={3}
        />
      </label>
      <button type="submit" disabled={pending}>
        {pending ? "Salvando..." : "Adicionar"}
      </button>
    </form>
  );
}
