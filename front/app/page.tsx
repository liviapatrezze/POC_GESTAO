import { ItemBoard } from "@/components/item-board";
import { getHealth, listItems } from "@/lib/api";
import type { Item } from "@/lib/types";

export default async function HomePage() {
  let health = "indisponível";
  let items: Item[] = [];
  let error = "";

  try {
    const [healthResponse, itemResponse] = await Promise.all([
      getHealth(),
      listItems(),
    ]);
    health = healthResponse.status;
    items = itemResponse;
  } catch {
    error = "Não foi possível falar com a API.";
  }

  return (
    <ItemBoard initialHealth={health} initialItems={items} initialError={error} />
  );
}
