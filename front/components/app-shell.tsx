"use client";

import type { ReactNode } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

const ITENS = [
  { href: "/alunos", label: "Alunos" },
  { href: "/professores", label: "Professores" },
  { href: "/frequencia", label: "Turmas e Presenças" },
  { href: "/dados", label: "Dados" },
];

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="home-frame">
      <a className="pular" href="#conteudo">
        Ir para o conteúdo
      </a>
      <header className="home-header">
        <Link href="/" className="home-logo" aria-label="Sportbridge, início">
          <img src="/logo-sportbridge.png" alt="" />
        </Link>
        <p className="home-titulo">POC Sistema Gestão</p>
      </header>
      <div className="home-body">
        <nav className="home-side" aria-label="Principal">
          {ITENS.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={pathname === item.href ? "home-action active" : "home-action"}
              aria-current={pathname === item.href ? "page" : undefined}
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="home-main" id="conteudo" tabIndex={-1}>
          {children}
        </div>
      </div>
      <footer className="home-footer" aria-hidden="true">
        <img src="/logo-sportbridge-clara.png" alt="" />
      </footer>
    </div>
  );
}
