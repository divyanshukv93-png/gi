import axios from 'axios'
export const api = axios.create({ baseURL: '/api' })
export const getToken = () => localStorage.getItem('token')
export const setToken = (t: string | null) => (t ? localStorage.setItem('token', t) : localStorage.removeItem('token'))
api.interceptors.request.use(c => { const t = getToken(); if (t) c.headers.Authorization = `Bearer ${t}`; return c })
export const errMsg = (e: any): string => {
  const d = e?.response?.data?.detail
  return typeof d === 'string' ? d : e?.response ? 'Please check the details and try again.' : 'Cannot reach the server. Is the API running?'
}
