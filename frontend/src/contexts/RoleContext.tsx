import { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { api, getToken, setToken } from '../services/api'
export type Role = 'farmer' | 'seller' | 'buyer' | 'admin'
export type User = { id: number; email: string; role: Role; language: string }
type Auth = { user: User | null; role: Role; loading: boolean; login: (e: string, p: string) => Promise<void>; register: (e: string, p: string, r: Role) => Promise<void>; logout: () => void }
const Ctx = createContext<Auth>(null as unknown as Auth)
export const RoleProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(!!getToken())
  useEffect(() => { if (getToken()) api.get('/auth/me').then(r => setUser(r.data)).catch(() => setToken(null)).finally(() => setLoading(false)) }, [])
  const login = async (email: string, password: string) => {
    const r = await api.post('/auth/login', new URLSearchParams({ username: email, password }))
    setToken(r.data.access_token); setUser((await api.get('/auth/me')).data)
  }
  const register = async (email: string, password: string, role: Role) => { await api.post('/auth/register', { email, password, role }); await login(email, password) }
  const logout = () => { setToken(null); setUser(null) }
  return <Ctx.Provider value={{ user, role: user?.role ?? 'buyer', loading, login, register, logout }}>{children}</Ctx.Provider>
}
export const useAuth = () => useContext(Ctx)
export const useRole = useAuth
