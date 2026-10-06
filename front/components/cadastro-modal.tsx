"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useId,
  useRef,
  useState,
  type ReactNode,
} from "react";

const FecharCadastro = createContext<(() => void) | null>(null);

const SELETOR_FOCO =
  'a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), select:not([disabled]), textarea:not([disabled])';

export function useFecharCadastro() {
  return useContext(FecharCadastro);
}

function focaveis(dialog: HTMLElement) {
  return [...dialog.querySelectorAll<HTMLElement>(SELETOR_FOCO)].filter(
    (elemento) => elemento.getClientRects().length > 0,
  );
}

type CadastroModalProps = {
  titulo: string;
  rotulo: string;
  children: ReactNode;
};

type FormModalProps = {
  titulo: string;
  aberto: boolean;
  onFechar: () => void;
  children: ReactNode;
};

export function FormModal({ titulo, aberto, onFechar, children }: FormModalProps) {
  const tituloId = useId();
  const dialogRef = useRef<HTMLDivElement>(null);
  const origemRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!aberto) {
      return;
    }
    const origem = document.activeElement;
    origemRef.current = origem instanceof HTMLElement ? origem : null;
    dialogRef.current?.focus();

    function aoTeclar(event: KeyboardEvent) {
      const dialog = dialogRef.current;
      if (event.key === "Escape") {
        event.preventDefault();
        onFechar();
        return;
      }
      if (event.key !== "Tab" || !dialog) {
        return;
      }
      const itens = focaveis(dialog);
      if (itens.length === 0) {
        event.preventDefault();
        return;
      }
      const primeiro = itens[0];
      const ultimo = itens[itens.length - 1];
      const atual = document.activeElement;
      if (event.shiftKey && (atual === primeiro || atual === dialog)) {
        event.preventDefault();
        ultimo.focus();
      } else if (!event.shiftKey && atual === ultimo) {
        event.preventDefault();
        primeiro.focus();
      }
    }

    window.addEventListener("keydown", aoTeclar);
    return () => {
      window.removeEventListener("keydown", aoTeclar);
      const origemAtual = origemRef.current;
      if (origemAtual && document.contains(origemAtual)) {
        origemAtual.focus();
      }
    };
  }, [aberto, onFechar]);

  if (!aberto) {
    return null;
  }

  return (
    <div className="modal-fundo" onClick={onFechar}>
      <div
        ref={dialogRef}
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby={tituloId}
        tabIndex={-1}
        onClick={(event) => event.stopPropagation()}
      >
        <div className="modal-topo">
          <h2 id={tituloId}>{titulo}</h2>
          <button type="button" className="modal-fechar" onClick={onFechar} aria-label="Fechar">
            ✕
          </button>
        </div>
        <FecharCadastro.Provider value={onFechar}>{children}</FecharCadastro.Provider>
      </div>
    </div>
  );
}

export function CadastroModal({ titulo, rotulo, children }: CadastroModalProps) {
  const [aberto, setAberto] = useState(false);
  const fechar = useCallback(() => setAberto(false), []);

  return (
    <>
      <button
        type="button"
        className="text-button"
        aria-haspopup="dialog"
        aria-expanded={aberto}
        onClick={() => setAberto(true)}
      >
        {rotulo}
      </button>
      <FormModal titulo={titulo} aberto={aberto} onFechar={fechar}>
        {children}
      </FormModal>
    </>
  );
}
