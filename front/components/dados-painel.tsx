import { DadosGraficos } from "@/components/dados-graficos";
import type { PainelDados } from "@/lib/dados";
import { textoPercentual, textoPresencas } from "@/lib/dados";

function classeFrequencia(percentual: number | null): string | undefined {
  if (percentual === null) {
    return undefined;
  }
  if (percentual < 75) {
    return "dados-baixa";
  }
  return "dados-ok";
}

export function DadosPainel({ painel }: { painel: PainelDados }) {
  const { resumo } = painel;

  return (
    <div className="dados">
      <ul className="dados-resumo">
        <li>
          <strong>{resumo.alunosAtivos}</strong>
          <span>Alunos ativos</span>
        </li>
        <li>
          <strong>{resumo.professoresAtivos}</strong>
          <span>Professores ativos</span>
        </li>
        <li>
          <strong>{resumo.turmasAtivas}</strong>
          <span>Turmas ativas</span>
        </li>
        <li>
          <strong>{resumo.matriculasAtivas}</strong>
          <span>Matrículas ativas</span>
        </li>
        <li>
          <strong>{resumo.presentesHoje}</strong>
          <span>Presentes hoje</span>
        </li>
        <li>
          <strong>{resumo.ausentesHoje}</strong>
          <span>Ausentes hoje</span>
        </li>
        <li>
          <strong>{resumo.semRegistroHoje}</strong>
          <span>Sem chamada hoje</span>
        </li>
      </ul>

      <DadosGraficos painel={painel} />

      <section className="dados-bloco">
        <h2>Faltas de hoje</h2>
        {painel.ausentesHoje.length === 0 ? (
          <p className="empty">Nenhuma falta registrada hoje.</p>
        ) : (
          <ul className="dados-faltas">
            {painel.ausentesHoje.map((falta) => (
              <li key={falta.id}>
                <strong>{falta.nome}</strong>
                <span>{falta.turma}</span>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="dados-bloco">
        <h2>Frequência dos alunos</h2>
        <p className="dados-nota">Calculada sobre as presenças já registradas. Abaixo de 75% fica em destaque.</p>
        {painel.frequenciaAlunos.length === 0 ? (
          <p className="empty">Nenhum aluno ativo.</p>
        ) : (
          <div className="dados-tabela-wrap">
            <table className="dados-tabela">
              <thead>
                <tr>
                  <th scope="col">Aluno</th>
                  <th scope="col">Turmas</th>
                  <th scope="col">Presenças</th>
                  <th scope="col">Frequência</th>
                </tr>
              </thead>
              <tbody>
                {painel.frequenciaAlunos.map((aluno) => (
                  <tr key={aluno.id}>
                    <td>{aluno.nome}</td>
                    <td>{aluno.turmas}</td>
                    <td>{textoPresencas(aluno.presentes, aluno.registros)}</td>
                    <td className={classeFrequencia(aluno.percentual)}>{textoPercentual(aluno.percentual)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="dados-bloco">
        <h2>Frequência das turmas</h2>
        {painel.frequenciaTurmas.length === 0 ? (
          <p className="empty">Nenhuma turma ativa.</p>
        ) : (
          <div className="dados-tabela-wrap">
            <table className="dados-tabela">
              <thead>
                <tr>
                  <th scope="col">Turma</th>
                  <th scope="col">Professor</th>
                  <th scope="col">Alunos</th>
                  <th scope="col">Presenças</th>
                  <th scope="col">Frequência</th>
                </tr>
              </thead>
              <tbody>
                {painel.frequenciaTurmas.map((turma) => (
                  <tr key={turma.id}>
                    <td>{turma.rotulo}</td>
                    <td>{turma.professor}</td>
                    <td>{turma.matriculados}</td>
                    <td>{textoPresencas(turma.presentes, turma.registros)}</td>
                    <td className={classeFrequencia(turma.percentual)}>{textoPercentual(turma.percentual)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="dados-bloco">
        <h2>Detalhe por esporte</h2>
        {painel.esportes.length === 0 ? (
          <p className="empty">Nenhum esporte ativo.</p>
        ) : (
          <div className="dados-tabela-wrap">
            <table className="dados-tabela compacta">
              <thead>
                <tr>
                  <th scope="col">Esporte</th>
                  <th scope="col">Turmas</th>
                  <th scope="col">Alunos</th>
                </tr>
              </thead>
              <tbody>
                {painel.esportes.map((esporte) => (
                  <tr key={esporte.id}>
                    <td>{esporte.nome}</td>
                    <td>{esporte.turmas}</td>
                    <td>{esporte.alunos}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}
