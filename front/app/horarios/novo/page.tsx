import { HorarioForm } from "@/components/horario-form";
import { PageHeader } from "@/components/page-header";
import { listAlunos, listEsportes, listProfessores } from "@/lib/gestao-api";

export default async function NovoHorarioPage() {
  let erro = "";
  let alunos: Awaited<ReturnType<typeof listAlunos>> = [];
  let esportes: Awaited<ReturnType<typeof listEsportes>> = [];
  let professores: Awaited<ReturnType<typeof listProfessores>> = [];
  try {
    [alunos, esportes, professores] = await Promise.all([listAlunos(), listEsportes(), listProfessores()]);
  } catch {
    erro = "Não foi possível carregar esportes e professores.";
  }

  return (
    <main className="page">
      <PageHeader title="Cadastro de Turmas" actionHref="/horarios" actionLabel="Voltar" />
      {erro ? (
        <p className="error" role="alert">{erro}</p>
      ) : (
        <HorarioForm esportes={esportes} professores={professores} alunos={alunos} />
      )}
    </main>
  );
}
