import { BrowserRouter, Route, Routes } from 'react-router-dom'
import AppShell from './layouts/AppShell'
import Overview from './pages/Overview'
import ModulePage from './pages/ModulePage'
import Marketplace from './pages/Marketplace'
import Certificates from './pages/Certificates'
import { NAV } from './nav'
import Login from './pages/Login'
import { useAuth } from './contexts/RoleContext'
export default function App() {
  const { user, loading } = useAuth()
  if (loading) return <p className="p-8 text-sm">Loading…</p>
  if (!user) return <Login />
  return <BrowserRouter><Routes><Route element={<AppShell />}>
    <Route index element={<Overview />} />
    <Route path="/marketplace" element={<Marketplace />} />
    <Route path="/certificates" element={<Certificates />} />
    {NAV.filter(n => !['/','/marketplace','/certificates'].includes(n.path)).map(n => <Route key={n.key} path={n.path} element={<ModulePage navKey={n.key} />} />)}
  </Route></Routes></BrowserRouter>
}
