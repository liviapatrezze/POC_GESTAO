import { EsporteForm } from "@/components/esporte-form";
import { PageHeader } from "@/components/page-header";

export default function NovoEsportePage() {
  return (
    <main className="page">
      <PageHeader title="Novo esporte" actionHref="/esportes" actionLabel="Voltar" />
      <EsporteForm />
    </main>
  );
}
