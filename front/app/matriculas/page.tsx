import { CadastroModal } from "@/components/cadastro-modal";
import { MatriculaForm } from "@/components/matricula-form";
import { MatriculaTabela } from "@/components/matricula-tabela";
import { PageHeader } from "@/components/page-header";
import { listAlunos, listEsportes, listHorarios, listMatriculas } from "@/lib/gestao-api";

export default async function MatriculasPage() {
  let erro = "";
  let matriculas: Awaited<ReturnType<typeof listMatriculas>> = [];
  let alunos: Awaited<ReturnType<typeof listAlunos>> = [];
  let esportes: Awaited<ReturnType<typeof listEsportes>> = [];
  let horarios: Awaited<ReturnType<typeof listHorarios>> = [];
  try {
    [matriculas, alunos, esportes, horarios] = await Promise.all([
      listMatriculas(),
      listAlunos(),
      listEsportes(),
      listHorarios(),
    ]);
  } catch {
    erro = "Não foi possível falar com a API.";
  }

  return (
    <main className="page wide">
      <PageHeader
        title="Matrículas"
        description="Alunos vinculados a um horário de aula."
        action={
          <CadastroModal titulo="Matricular" rotulo="Matricular">
            <MatriculaForm alunos={alunos} esportes={esportes} horarios={horarios} />
          </CadastroModal>
        }
      />
      {erro ? <p className="error" role="alert">{erro}</p> : (
        <MatriculaTabela matriculas={matriculas} alunos={alunos} esportes={esportes} horarios={horarios} />
      )}
    </main>
  );
}
