"use client";

import type { Item } from "@/lib/types";

type ItemListProps = {
  items: Item[];
  onDelete: (id: number) => Promise<void>;
};

export function ItemList({ items, onDelete }: ItemListProps) {
  if (items.length === 0) {
    return <p className="empty">Nenhum item ainda.</p>;
  }

  return (
    <ul className="item-list">
      {items.map((item) => (
        <li key={item.id}>
          <div>
            <strong>{item.titulo}</strong>
            {item.descricao ? <p>{item.descricao}</p> : null}
            <time dateTime={item.criado_em}>
              {new Date(item.criado_em).toLocaleString("pt-BR")}
            </time>
          </div>
          <button type="button" onClick={() => void onDelete(item.id)} aria-label={`Excluir ${item.titulo}`}>
            Excluir
          </button>
        </li>
      ))}
    </ul>
  );
}
