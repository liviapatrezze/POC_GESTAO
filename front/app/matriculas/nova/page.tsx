import { MatriculaForm } from "@/components/matricula-form";
import { PageHeader } from "@/components/page-header";
import { listAlunos, listEsportes, listHorarios } from "@/lib/gestao-api";

export default async function NovaMatriculaPage() {
  let erro = "";
  let alunos: Awaited<ReturnType<typeof listAlunos>> = [];
  let esportes: Awaited<ReturnType<typeof listEsportes>> = [];
  let horarios: Awaited<ReturnType<typeof listHorarios>> = [];
  try {
    [alunos, esportes, horarios] = await Promise.all([
      listAlunos(),
      listEsportes(),
      listHorarios(),
    ]);
  } catch {
    erro = "Não foi possível carregar os dados da matrícula.";
  }

  return (
    <main className="page">
      <PageHeader title="Nova matrícula" actionHref="/matriculas" actionLabel="Voltar" />
      {erro ? (
        <p className="error" role="alert">{erro}</p>
      ) : (
        <MatriculaForm alunos={alunos} esportes={esportes} horarios={horarios} />
      )}
    </main>
  );
}
