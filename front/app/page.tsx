import { ItemBoard } from "@/components/item-board";
import { getHealth, getHello, listItems } from "@/lib/api";
import type { Item } from "@/lib/types";

export default async function HomePage() {
  let health = "indisponível";
  let hello = "";
  let items: Item[] = [];
  let error = "";

  try {
    const [healthResponse, helloResponse, itemResponse] = await Promise.all([
      getHealth(),
      getHello(),
      listItems(),
    ]);
    health = healthResponse.status;
    hello = helloResponse.mensagem;
    items = itemResponse;
  } catch {
    error = "Não foi possível falar com a API.";
  }

  return (
    <ItemBoard
      initialHealth={health}
      initialHello={hello}
      initialItems={items}
      initialError={error}
    />
  );
}
