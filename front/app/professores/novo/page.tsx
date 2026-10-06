import { PageHeader } from "@/components/page-header";
import { ProfessorForm } from "@/components/professor-form";

export default function NovoProfessorPage() {
  return (
    <main className="page">
      <PageHeader title="Novo professor" actionHref="/professores" actionLabel="Voltar" />
      <ProfessorForm />
    </main>
  );
}
