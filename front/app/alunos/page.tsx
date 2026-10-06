import { AlunoForm } from "@/components/aluno-form";
import { AlunosLista } from "@/components/alunos-lista";
import { CadastroModal } from "@/components/cadastro-modal";
import { PageHeader } from "@/components/page-header";
import { listAlunos, listMatriculas } from "@/lib/gestao-api";
import { etiquetaFaixa } from "@/lib/turma";

export default async function AlunosPage() {
  let erro = "";
  let alunos: Awaited<ReturnType<typeof listAlunos>> = [];
  let matriculas: Awaited<ReturnType<typeof listMatriculas>> = [];
  try {
    [alunos, matriculas] = await Promise.all([listAlunos(), listMatriculas()]);
  } catch {
    erro = "Não foi possível falar com a API.";
  }

  const etiquetas = new Map<number, string[]>();
  for (const matricula of matriculas) {
    if (!matricula.ativo) {
      continue;
    }
    const etiqueta = etiquetaFaixa(matricula.esporte, matricula.hora_inicio, matricula.hora_fim);
    const atuais = etiquetas.get(matricula.aluno) ?? [];
    if (!atuais.includes(etiqueta)) {
      atuais.push(etiqueta);
    }
    etiquetas.set(matricula.aluno, atuais);
  }

  return (
    <main className="page wide">
      <PageHeader
        title="Alunos"
        action={
          <CadastroModal titulo="Cadastrar Aluno" rotulo="Cadastrar Aluno">
            <AlunoForm />
          </CadastroModal>
        }
      />
      {erro ? <p className="error" role="alert">{erro}</p> : null}
      {alunos.length === 0 ? (
        <p className="empty">Nenhum aluno cadastrado ainda.</p>
      ) : (
        <AlunosLista
          itens={alunos.map((aluno) => ({
            aluno,
            etiquetas: etiquetas.get(aluno.id) ?? [],
          }))}
        />
      )}
    </main>
  );
}
