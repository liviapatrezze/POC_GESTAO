import type { ContagemEsporte, PainelDados, SemanaFrequencia } from "@/lib/dados";

function rotuloSemanas(semanas: SemanaFrequencia[]): string {
  if (semanas.length === 0) {
    return "Sem chamadas registradas.";
  }
  const ultima = semanas[semanas.length - 1];
  const abaixo = semanas.filter((semana) => semana.percentual < 75).length;
  const semanasAbaixo = abaixo === 1 ? "1 semana abaixo de 75%." : `${abaixo} semanas abaixo de 75%.`;
  return `Frequência semanal de ${semanas[0]?.rotulo} até ${ultima?.rotulo}. A última semana está em ${ultima?.percentual}%. ${semanasAbaixo}`;
}

function GraficoSemanas({ semanas }: { semanas: SemanaFrequencia[] }) {
  if (semanas.length === 0) {
    return <p className="empty">Sem chamadas registradas.</p>;
  }

  const largura = 720;
  const altura = 240;
  const margemEsquerda = 36;
  const margemBaixo = 28;
  const areaLargura = largura - margemEsquerda - 12;
  const areaAltura = altura - 16 - margemBaixo;
  const passo = areaLargura / semanas.length;
  const barra = Math.min(26, passo * 0.62);

  return (
    <svg className="grafico grafico-semanas" viewBox={`0 0 ${largura} ${altura}`} role="img" aria-label={rotuloSemanas(semanas)}>
      <defs>
        <pattern id="barra-baixa-semana" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <rect width="8" height="8" fill="#c25200" />
          <line x1="0" y1="0" x2="0" y2="8" stroke="#ffffff" strokeWidth="3" />
        </pattern>
      </defs>
      {[0, 25, 50, 75, 100].map((marca) => {
        const y = 16 + areaAltura - (marca / 100) * areaAltura;
        return (
          <g key={marca}>
            <line className={marca === 75 ? "grafico-meta" : "grafico-guia"} x1={margemEsquerda} x2={largura - 12} y1={y} y2={y} />
            <text className="grafico-eixo" x={0} y={y + 4}>
              {marca}
            </text>
          </g>
        );
      })}
      {semanas.map((semana, indice) => {
        const alturaBarra = Math.max((semana.percentual / 100) * areaAltura, semana.registros > 0 ? 2 : 0);
        const x = margemEsquerda + indice * passo + (passo - barra) / 2;
        const y = 16 + areaAltura - alturaBarra;
        return (
          <g key={semana.inicio} aria-label={`${semana.rotulo}: ${semana.percentual}% (${semana.presentes} de ${semana.registros})`}>
            <rect
              className={semana.percentual < 75 ? "grafico-barra baixa" : "grafico-barra"}
              x={x}
              y={y}
              width={barra}
              height={alturaBarra}
              rx={6}
            />
            <text className="grafico-eixo" x={x + barra / 2} y={altura - 8} textAnchor="middle">
              {semana.rotulo}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

function GraficoEsportes({ esportes }: { esportes: ContagemEsporte[] }) {
  if (esportes.length === 0) {
    return <p className="empty">Nenhum esporte ativo.</p>;
  }
  const maximo = Math.max(...esportes.map((esporte) => esporte.alunos), 1);
  const altura = esportes.length * 36 + 8;
  const resumo = esportes.map((esporte) => `${esporte.nome} ${esporte.alunos}`).join(", ");

  return (
    <svg className="grafico" viewBox={`0 0 460 ${altura}`} role="img" aria-label={`Alunos por esporte: ${resumo}.`}>
      {esportes.map((esporte, indice) => {
        const y = indice * 36 + 6;
        const comprimento = Math.max((esporte.alunos / maximo) * 220, esporte.alunos > 0 ? 8 : 0);
        return (
          <g key={esporte.id} aria-label={`${esporte.nome}: ${esporte.alunos} alunos em ${esporte.turmas} turmas`}>
            <text className="grafico-nome" x={0} y={y + 16}>
              {esporte.nome}
            </text>
            <rect className="grafico-barra" x={128} y={y + 4} width={comprimento} height={16} rx={8} />
            <text className="grafico-valor" x={136 + comprimento} y={y + 16}>
              {esporte.alunos}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

function GraficoHoje({ painel }: { painel: PainelDados }) {
  const partes = [
    { nome: "Presentes", valor: painel.resumo.presentesHoje, classe: "grafico-barra" },
    { nome: "Ausentes", valor: painel.resumo.ausentesHoje, classe: "grafico-barra baixa" },
    { nome: "Sem chamada", valor: painel.resumo.semRegistroHoje, classe: "grafico-barra neutra" },
  ];
  const total = partes.reduce((soma, parte) => soma + parte.valor, 0);
  if (total === 0) {
    return <p className="empty">Nenhuma matrícula ativa hoje.</p>;
  }

  let inicio = 0;
  const fatias = partes.map((parte) => {
    const largura = (parte.valor / total) * 100;
    const fatia = { ...parte, inicio, largura };
    inicio += largura;
    return fatia;
  });

  return (
    <div>
      <svg
        className="grafico grafico-hoje"
        viewBox="0 0 320 28"
        role="img"
        aria-label={partes.map((parte) => `${parte.nome} ${parte.valor}`).join(", ")}
      >
        <defs>
          <pattern id="barra-baixa-hoje" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <rect width="8" height="8" fill="#c25200" />
            <line x1="0" y1="0" x2="0" y2="8" stroke="#ffffff" strokeWidth="3" />
          </pattern>
          <clipPath id="chamada-hoje">
            <rect width="320" height="28" rx="10" />
          </clipPath>
        </defs>
        <g clipPath="url(#chamada-hoje)">
          {fatias.map((fatia) =>
            fatia.largura > 0 ? (
              <rect
                key={fatia.nome}
                className={fatia.classe}
                x={(fatia.inicio / 100) * 320}
                y={0}
                width={(fatia.largura / 100) * 320}
                height={28}
              />
            ) : null,
          )}
        </g>
      </svg>
      <ul className="grafico-legenda">
        {partes.map((parte) => (
          <li key={parte.nome}>
            <span className={parte.classe} />
            {parte.nome}
            <strong>{parte.valor}</strong>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function DadosGraficos({ painel }: { painel: PainelDados }) {
  return (
    <div className="dados-graficos">
      <section className="dados-card dados-card-largo">
        <h2>Frequência por semana</h2>
        <p className="dados-nota">
          Percentual de presença nas chamadas da semana. A linha tracejada marca 75%. Semanas abaixo disso aparecem
          listradas.
        </p>
        <GraficoSemanas semanas={painel.semanas} />
      </section>
      <section className="dados-card">
        <h2>Alunos por esporte</h2>
        <GraficoEsportes esportes={painel.esportes} />
      </section>
      <section className="dados-card">
        <h2>Chamada de hoje</h2>
        <GraficoHoje painel={painel} />
      </section>
    </div>
  );
}
