import { CadastroModal } from "@/components/cadastro-modal";
import { EsportesLista } from "@/components/esportes-lista";
import { EsporteForm } from "@/components/esporte-form";
import { PageHeader } from "@/components/page-header";
import { listEsportes } from "@/lib/gestao-api";

export default async function EsportesPage() {
  let erro = "";
  let esportes: Awaited<ReturnType<typeof listEsportes>> = [];
  try {
    esportes = await listEsportes();
  } catch {
    erro = "Não foi possível falar com a API.";
  }

  return (
    <main className="page wide">
      <PageHeader
        title="Esportes"
        description="Modalidades cadastradas."
        action={
          <CadastroModal titulo="Cadastrar Esporte" rotulo="Cadastrar Esporte">
            <EsporteForm />
          </CadastroModal>
        }
      />
      {erro ? <p className="error" role="alert">{erro}</p> : null}
      {esportes.length === 0 ? (
        <p className="empty">Nenhum esporte cadastrado ainda.</p>
      ) : (
        <EsportesLista esportes={esportes} />
      )}
    </main>
  );
}
