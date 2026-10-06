import { DadosPainel } from "@/components/dados-painel";
import { PageHeader } from "@/components/page-header";
import { montarPainel } from "@/lib/dados";
import {
  listAlunos,
  listEsportes,
  listHorarios,
  listMatriculas,
  listParticipacoes,
  listProfessores,
} from "@/lib/gestao-api";

export default async function DadosPage() {
  let erro = "";
  let painel: ReturnType<typeof montarPainel> | null = null;
  try {
    const [alunos, professores, esportes, horarios, matriculas, participacoes] = await Promise.all([
      listAlunos(),
      listProfessores(),
      listEsportes(),
      listHorarios(),
      listMatriculas(),
      listParticipacoes(),
    ]);
    painel = montarPainel({ alunos, professores, esportes, horarios, matriculas, participacoes });
  } catch {
    erro = "Não foi possível falar com a API.";
  }

  return (
    <main className="page wide">
      <PageHeader title="Dados" description="Frequência, faltas do dia e ocupação das turmas." />
      {erro ? <p className="error" role="alert">{erro}</p> : null}
      {painel ? <DadosPainel painel={painel} /> : null}
    </main>
  );
}
