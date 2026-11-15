import { ReactNode } from 'react'
export const Card = ({ title, action, children, className = '' }: { title?: string; action?: ReactNode; children: ReactNode; className?: string }) => (
  <section className={`rounded-xl border border-sand-300/70 bg-white p-5 ${className}`}>
    {(title || action) && <header className="mb-4 flex items-center justify-between gap-3"><h3 className="text-lg">{title}</h3>{action}</header>}
    {children}
  </section>
)
