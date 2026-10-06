import { CadastroModal } from "@/components/cadastro-modal";
import { PageHeader } from "@/components/page-header";
import { ProfessorForm } from "@/components/professor-form";
import { ProfessoresLista } from "@/components/professores-lista";
import { listHorarios, listProfessores } from "@/lib/gestao-api";
import { etiquetaFaixa } from "@/lib/turma";

export default async function ProfessoresPage() {
  let erro = "";
  let professores: Awaited<ReturnType<typeof listProfessores>> = [];
  let horarios: Awaited<ReturnType<typeof listHorarios>> = [];
  try {
    [professores, horarios] = await Promise.all([listProfessores(), listHorarios()]);
  } catch {
    erro = "Não foi possível falar com a API.";
  }

  const etiquetas = new Map<number, string[]>();
  for (const horario of horarios) {
    if (!horario.ativo) {
      continue;
    }
    const etiqueta = etiquetaFaixa(horario.esporte_nome, horario.hora_inicio, horario.hora_fim);
    const atuais = etiquetas.get(horario.professor) ?? [];
    if (!atuais.includes(etiqueta)) {
      atuais.push(etiqueta);
    }
    etiquetas.set(horario.professor, atuais);
  }

  return (
    <main className="page wide">
      <PageHeader
        title="Professores"
        action={
          <CadastroModal titulo="Cadastrar Professor" rotulo="Cadastrar Professor">
            <ProfessorForm />
          </CadastroModal>
        }
      />
      {erro ? <p className="error" role="alert">{erro}</p> : null}
      {professores.length === 0 ? (
        <p className="empty">Nenhum professor cadastrado ainda.</p>
      ) : (
        <ProfessoresLista
          itens={professores.map((professor) => ({
            professor,
            etiquetas: etiquetas.get(professor.id) ?? [],
          }))}
        />
      )}
    </main>
  );
}
