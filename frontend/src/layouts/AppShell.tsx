import { useState } from 'react'
import { NavLink, Outlet } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { Menu, X, Sprout } from 'lucide-react'
import { NAV } from '../nav'
import { useAuth } from '../contexts/RoleContext'
const LANGS = [['en','English'],['hi','हिन्दी']]
export default function AppShell() {
  const { t, i18n } = useTranslation()
  const { user, role, logout } = useAuth()
  const [open, setOpen] = useState(false)
  const sel = 'rounded-lg border border-sand-300 bg-white px-2 py-1.5 text-sm'
  return (
    <div className="min-h-screen lg:grid lg:grid-cols-[264px_1fr]">
      <aside className={`${open ? 'block' : 'hidden'} fixed inset-0 z-30 overflow-y-auto bg-forest-900 p-5 text-forest-100 lg:static lg:block`}>
        <div className="mb-6 flex items-center justify-between">
          <div className="flex items-center gap-2"><Sprout className="h-6 w-6 text-olive-100" /><span className="font-display text-xl text-white">Grain Intelligence</span></div>
          <button className="lg:hidden" aria-label="Close menu" onClick={() => setOpen(false)}><X /></button>
        </div>
        <nav className="space-y-1">
          {NAV.filter(n => n.roles.includes(role)).map(n => (
            <NavLink key={n.key} to={n.path} end={n.path === '/'} onClick={() => setOpen(false)}
              className={({ isActive }) => `flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors ${isActive ? 'bg-forest-700 text-white' : 'hover:bg-forest-700/50'}`}>
              <n.icon className="h-4 w-4" />{t(`nav.${n.key}`)}
            </NavLink>
          ))}
        </nav>
        <p className="mt-8 text-xs text-forest-100/70">{t('tagline')}</p>
      </aside>
      <div className="min-w-0">
        <header className="flex items-center justify-between gap-3 border-b border-sand-300/70 bg-white px-4 py-3 lg:px-8">
          <button className="lg:hidden" aria-label="Open menu" onClick={() => setOpen(true)}><Menu /></button>
          <div className="ml-auto flex items-center gap-3">
            <span className="hidden text-sm text-ink/70 sm:inline">{user?.email} · {role}</span>
            <button onClick={logout} className={sel}>Log out</button>
            <label className="flex items-center gap-2 text-sm"><span className="sr-only">{t('language')}</span>
              <select className={sel} value={i18n.language} onChange={e => { i18n.changeLanguage(e.target.value); localStorage.setItem('lang', e.target.value) }}>{LANGS.map(([c, n]) => <option key={c} value={c}>{n}</option>)}</select></label>
          </div>
        </header>
        <main className="p-4 lg:p-8"><Outlet /></main>
      </div>
    </div>
  )
}
