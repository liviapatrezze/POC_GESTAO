import { AlunoForm } from "@/components/aluno-form";
import { PageHeader } from "@/components/page-header";

export default function NovoAlunoPage() {
  return (
    <main className="page">
      <PageHeader title="Novo aluno" actionHref="/alunos" actionLabel="Voltar" />
      <AlunoForm />
    </main>
  );
}
