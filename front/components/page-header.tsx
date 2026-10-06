import type { ReactNode } from "react";
import Link from "next/link";

type PageHeaderProps = {
  title: string;
  description?: string;
  actionHref?: string;
  actionLabel?: string;
  action?: ReactNode;
};

export function PageHeader({ title, description, actionHref, actionLabel, action }: PageHeaderProps) {
  return (
    <div className="page-header">
      <div>
        <h1>{title}</h1>
        {description ? <p>{description}</p> : null}
      </div>
      {action ? action : null}
      {!action && actionHref && actionLabel ? (
        <Link className="text-button" href={actionHref}>
          {actionLabel}
        </Link>
      ) : null}
    </div>
  );
}
