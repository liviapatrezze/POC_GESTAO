import { CadastroModal } from "@/components/cadastro-modal";
import { FrequenciaTabela } from "@/components/frequencia-tabela";
import { HorarioForm } from "@/components/horario-form";
import { PageHeader } from "@/components/page-header";
import { listAlunos, listEsportes, listHorarios, listMatriculas, listProfessores } from "@/lib/gestao-api";

export default async function FrequenciaPage() {
  let erro = "";
  let horarios: Awaited<ReturnType<typeof listHorarios>> = [];
  let matriculas: Awaited<ReturnType<typeof listMatriculas>> = [];
  let alunos: Awaited<ReturnType<typeof listAlunos>> = [];
  let esportes: Awaited<ReturnType<typeof listEsportes>> = [];
  let professores: Awaited<ReturnType<typeof listProfessores>> = [];
  try {
    [horarios, matriculas, alunos, esportes, professores] = await Promise.all([
      listHorarios(),
      listMatriculas(),
      listAlunos(),
      listEsportes(),
      listProfessores(),
    ]);
  } catch {
    erro = "Não foi possível falar com a API.";
  }

  return (
    <main className="page wide">
      <PageHeader
        title="Turmas e Presenças"
        action={
          <CadastroModal titulo="Cadastrar Turmas" rotulo="Cadastrar Turmas">
            <HorarioForm esportes={esportes} professores={professores} alunos={alunos} />
          </CadastroModal>
        }
      />
      {erro ? (
        <p className="error" role="alert">{erro}</p>
      ) : (
        <FrequenciaTabela
          horarios={horarios}
          matriculas={matriculas}
          alunos={alunos}
          esportes={esportes}
          professores={professores}
        />
      )}
    </main>
  );
}
