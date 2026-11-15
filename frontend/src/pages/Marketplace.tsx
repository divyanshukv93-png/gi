import { useCallback, useEffect, useState } from 'react'
import { MapPin, Search } from 'lucide-react'
import { Card } from '../components/ui/Card'
import { CertBadge } from '../components/domain/CertBadge'
import { useAuth } from '../contexts/RoleContext'
import { api, errMsg } from '../services/api'
import type { CertSource } from '../services/mock'
import OrdersPanel from '../components/domain/OrdersPanel'
type L = { id: number; seller_id: number; grain: string; quantity_tonnes: number; price_per_quintal: number; location: string; certificate_source: CertSource | null }
const input = 'rounded-lg border border-sand-300 bg-white px-3 py-2 text-sm'
export default function Marketplace() {
  const { role } = useAuth()
  const [rows, setRows] = useState<L[]>([]); const [err, setErr] = useState(''); const [loading, setLoading] = useState(true)
  const [loc, setLoc] = useState(''); const [grain, setGrain] = useState('All'); const [max, setMax] = useState(''); const [sent, setSent] = useState<number[]>([])
  const [d, setD] = useState({ grain: 'Wheat', qty: '', price: '', location: '' }); const [formErr, setFormErr] = useState('')
  const canSell = role === 'seller' || role === 'farmer'
  const load = useCallback(() => { setLoading(true)
    api.get('/marketplace/listings', { params: { grain: grain === 'All' ? undefined : grain, max_price: max || undefined, location: loc || undefined } })
      .then(r => { setRows(r.data); setErr('') }).catch(e => setErr(errMsg(e))).finally(() => setLoading(false)) }, [grain, max, loc])
  useEffect(() => { const t = setTimeout(load, 300); return () => clearTimeout(t) }, [load])
  const add = async () => { setFormErr('')
    try { await api.post('/marketplace/listings', { grain: d.grain, quantity_tonnes: +d.qty, price_per_quintal: +d.price, location: d.location }); setD({ grain: 'Wheat', qty: '', price: '', location: '' }); load() }
    catch (e) { setFormErr(errMsg(e)) } }
  const inquire = async (id: number) => { try { await api.post('/orders', { listing_id: id, quantity_tonnes: 1 }); setSent(s => [...s, id]) } catch (e) { setErr(errMsg(e)) } }
  return (
    <div className="space-y-6">
      <h1 className="text-3xl">Marketplace</h1>
      {canSell && <Card title="Add a grain listing"><div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
        <select aria-label="Grain" className={input} value={d.grain} onChange={e => setD({ ...d, grain: e.target.value })}>{['Wheat', 'Rice', 'Maize'].map(g => <option key={g}>{g}</option>)}</select>
        <input className={input} placeholder="Quantity (tonnes)" inputMode="decimal" value={d.qty} onChange={e => setD({ ...d, qty: e.target.value })} />
        <input className={input} placeholder="Price (₹/quintal)" inputMode="numeric" value={d.price} onChange={e => setD({ ...d, price: e.target.value })} />
        <input className={input} placeholder="Location" value={d.location} onChange={e => setD({ ...d, location: e.target.value })} />
        <button onClick={add} className="rounded-lg bg-forest-700 px-4 py-2 text-sm font-medium text-white hover:bg-forest-900">Publish listing</button></div>
        {formErr && <p role="alert" className="mt-2 text-sm text-red-700">{formErr}</p>}</Card>}
      <Card><div className="flex flex-wrap gap-3">
        <div className="relative min-w-[200px] flex-1"><Search className="absolute left-3 top-2.5 h-4 w-4 text-ink/50" /><input className={`${input} w-full pl-9`} placeholder="Search by location" value={loc} onChange={e => setLoc(e.target.value)} /></div>
        <select aria-label="Grain filter" className={input} value={grain} onChange={e => setGrain(e.target.value)}>{['All', 'Wheat', 'Rice', 'Maize'].map(g => <option key={g}>{g}</option>)}</select>
        <input className={`${input} w-40`} placeholder="Max ₹/quintal" inputMode="numeric" value={max} onChange={e => setMax(e.target.value.replace(/\D/g, ''))} /></div></Card>
      {err && <p role="alert" className="text-sm text-red-700">{err}</p>}
      {loading ? <p className="text-sm">Loading listings…</p> : rows.length === 0 ? <Card><p className="text-sm">No listings yet{canSell ? '. Publish the first one above.' : ' match these filters.'}</p></Card> :
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">{rows.map(l => (
          <Card key={l.id}>
            <div className="flex items-start justify-between gap-2"><h3 className="text-lg">{l.grain} · {l.quantity_tonnes} t</h3><CertBadge source={l.certificate_source ?? undefined} /></div>
            <p className="mt-1 text-xl font-semibold text-forest-700">₹{l.price_per_quintal.toLocaleString('en-IN')}<span className="text-sm font-normal text-ink/60"> / quintal</span></p>
            <p className="mt-2 flex items-center gap-1 text-sm text-ink/70"><MapPin className="h-3.5 w-3.5" />{l.location}</p>
            <p className="text-xs text-ink/60">Seller #{l.seller_id}</p>
            {role === 'buyer' && <button disabled={sent.includes(l.id)} onClick={() => inquire(l.id)} className="mt-4 rounded-lg bg-forest-700 px-3 py-1.5 text-sm text-white disabled:bg-sand-300 disabled:text-ink">{sent.includes(l.id) ? 'Request sent' : 'Request 1 tonne'}</button>}
          </Card>))}</div>}
      <OrdersPanel key={sent.length} />
    </div>
  )
}
