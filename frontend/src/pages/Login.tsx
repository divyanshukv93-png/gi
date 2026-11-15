import { FormEvent, useState } from 'react'
import { Sprout } from 'lucide-react'
import { Role, useAuth } from '../contexts/RoleContext'
import { errMsg } from '../services/api'
const input = 'w-full rounded-lg border border-sand-300 bg-white px-3 py-2 text-sm'
export default function Login() {
  const { login, register } = useAuth()
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const [email, setEmail] = useState(''); const [password, setPassword] = useState(''); const [role, setRole] = useState<Role>('farmer')
  const [error, setError] = useState(''); const [busy, setBusy] = useState(false)
  const submit = async (e: FormEvent) => { e.preventDefault(); setBusy(true); setError('')
    try { mode === 'login' ? await login(email, password) : await register(email, password, role) } catch (x) { setError(errMsg(x)) } finally { setBusy(false) } }
  return (
    <div className="flex min-h-screen items-center justify-center bg-forest-50 p-4">
      <form onSubmit={submit} className="w-full max-w-sm space-y-4 rounded-xl border border-sand-300 bg-white p-6">
        <div className="flex items-center gap-2"><Sprout className="h-6 w-6 text-forest-700" /><h1 className="text-2xl">Grain Intelligence</h1></div>
        <p className="text-sm text-ink/70">Smart Grain. Safe Storage. Secure Future.</p>
        <label className="block text-sm">Email<input className={input} type="email" required value={email} onChange={e => setEmail(e.target.value)} /></label>
        <label className="block text-sm">Password<input className={input} type="password" required minLength={8} value={password} onChange={e => setPassword(e.target.value)} /></label>
        {mode === 'register' && <label className="block text-sm">I am a<select className={input} value={role} onChange={e => setRole(e.target.value as Role)}><option value="farmer">Farmer</option><option value="seller">Seller</option><option value="buyer">Buyer</option></select></label>}
        {error && <p role="alert" className="text-sm text-red-700">{error}</p>}
        <button disabled={busy} className="w-full rounded-lg bg-forest-700 py-2 text-sm font-medium text-white hover:bg-forest-900 disabled:opacity-60">{busy ? 'Please wait…' : mode === 'login' ? 'Log in' : 'Create account'}</button>
        <button type="button" className="w-full text-sm text-forest-700 underline" onClick={() => { setMode(mode === 'login' ? 'register' : 'login'); setError('') }}>{mode === 'login' ? 'New here? Create an account' : 'Have an account? Log in'}</button>
      </form>
    </div>
  )
}
