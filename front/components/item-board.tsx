"use client";

import { useState } from "react";
import { ItemForm } from "@/components/item-form";
import { ItemList } from "@/components/item-list";
import { createItem, deleteItem, listItems } from "@/lib/api";
import type { Item } from "@/lib/types";

type ItemBoardProps = {
  initialHealth: string;
  initialItems: Item[];
  initialError: string;
};

export function ItemBoard({
  initialHealth,
  initialItems,
  initialError,
}: ItemBoardProps) {
  const [items, setItems] = useState(initialItems);
  const [error, setError] = useState(initialError);

  async function refreshItems() {
    const nextItems = await listItems();
    setItems(nextItems);
    setError("");
  }

  async function handleCreate(titulo: string, descricao: string) {
    try {
      await createItem({ titulo, descricao });
      await refreshItems();
    } catch (caught) {
      setError("Não foi possível criar o item.");
      throw caught;
    }
  }

  async function handleDelete(id: number) {
    try {
      await deleteItem(id);
      await refreshItems();
    } catch {
      setError("Não foi possível excluir o item.");
    }
  }

  return (
    <main className="page">
      <header>
        <h1>POC Gestão</h1>
        <p>
          API: <span className="health">{initialHealth}</span>
        </p>
      </header>
      {error ? <p className="error">{error}</p> : null}
      <section>
        <h2>Novo item</h2>
        <ItemForm onCreate={handleCreate} />
      </section>
      <section>
        <h2>Itens</h2>
        <ItemList items={items} onDelete={handleDelete} />
      </section>
    </main>
  );
}
