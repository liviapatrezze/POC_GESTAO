type PessoaFaixaProps = {
  nome: string;
  imagem: string | null;
  etiquetas: string[];
  onClick?: () => void;
};

export function PessoaFaixa({ nome, imagem, etiquetas, onClick }: PessoaFaixaProps) {
  const inicial = nome.trim().charAt(0).toUpperCase() || "?";
  const identidade = (
    <>
      {imagem ? (
        <img className="faixa-foto" src={imagem} alt="" />
      ) : (
        <span className="faixa-foto">{inicial}</span>
      )}
      <strong>{nome}</strong>
    </>
  );
  const etiquetasLista =
    etiquetas.length > 0 ? (
      <ul className="faixa-tags">
        {etiquetas.map((etiqueta) => (
          <li key={etiqueta}>{etiqueta}</li>
        ))}
      </ul>
    ) : null;

  if (!onClick) {
    return (
      <article className="faixa">
        {identidade}
        {etiquetasLista}
      </article>
    );
  }

  return (
    <article className="faixa">
      <button type="button" className="faixa-abrir" onClick={onClick} aria-label={`Editar ${nome}`}>
        {identidade}
      </button>
      {etiquetasLista}
    </article>
  );
}
