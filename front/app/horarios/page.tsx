import { CadastroModal } from "@/components/cadastro-modal";
import { HorarioForm } from "@/components/horario-form";
import { HorariosLista } from "@/components/horarios-lista";
import { PageHeader } from "@/components/page-header";
import { listAlunos, listEsportes, listHorarios, listMatriculas, listProfessores } from "@/lib/gestao-api";

export default async function HorariosPage() {
  let erro = "";
  let horarios: Awaited<ReturnType<typeof listHorarios>> = [];
  let alunos: Awaited<ReturnType<typeof listAlunos>> = [];
  let matriculas: Awaited<ReturnType<typeof listMatriculas>> = [];
  let esportes: Awaited<ReturnType<typeof listEsportes>> = [];
  let professores: Awaited<ReturnType<typeof listProfessores>> = [];
  try {
    [horarios, alunos, matriculas, esportes, professores] = await Promise.all([
      listHorarios(),
      listAlunos(),
      listMatriculas(),
      listEsportes(),
      listProfessores(),
    ]);
  } catch {
    erro = "Não foi possível falar com a API.";
  }

  return (
    <main className="page wide">
      <PageHeader
        title="Horários"
        description="Programação semanal das aulas."
        action={
          <CadastroModal titulo="Cadastrar Turmas" rotulo="Cadastrar Turmas">
            <HorarioForm esportes={esportes} professores={professores} alunos={alunos} />
          </CadastroModal>
        }
      />
      {erro ? <p className="error" role="alert">{erro}</p> : null}
      {horarios.length === 0 ? (
        <p className="empty">Nenhum horário cadastrado ainda.</p>
      ) : (
        <HorariosLista
          horarios={horarios}
          esportes={esportes}
          professores={professores}
          alunos={alunos}
          matriculas={matriculas}
        />
      )}
    </main>
  );
}
