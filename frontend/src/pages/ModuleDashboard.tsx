import { useState } from 'react'
import { api, errMsg } from '../services/api'
import { Bar, BarChart, CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { Card } from '../components/ui/Card'
import { ProvenanceBadge, Source } from '../components/domain/ProvenanceBadge'
export type Cfg = { source: Source; note?: string; upload?: boolean
  stats?: [string, string][]; bullets?: { title: string; items: string[] }
  chart?: { title: string; kind: 'line' | 'bar'; x: string; series: string[]; data: Record<string, string | number>[] }
  table?: { title: string; cols: string[]; rows: string[][] } }
const COLORS = ['#2F6B4F', '#B7791F', '#7A8450']
export default function ModuleDashboard({ title, cfg }: { title: string; cfg: Cfg }) {
  const [img, setImg] = useState<string>()
  const [inspection, setInspection] = useState<any>()
  const [uploadError, setUploadError] = useState('')
  const [uploading, setUploading] = useState(false)
  const c = cfg.chart
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-2"><h1 className="text-3xl">{title}</h1><ProvenanceBadge source={cfg.source} /></div>
      {cfg.note && <p className="rounded-lg bg-amber-50 p-3 text-sm text-amber-900">{cfg.note}</p>}
      {cfg.stats && <div className="grid grid-cols-2 gap-4 xl:grid-cols-4">{cfg.stats.map(([k, v]) => <Card key={k}><p className="text-sm text-ink/70">{k}</p><p className="mt-1 font-display text-2xl text-forest-900">{v}</p></Card>)}</div>}
      {cfg.upload && <Card title="Upload a grain image">
        <input type="file" accept="image/jpeg,image/png" onChange={async e => { const f=e.target.files?.[0]; if(!f)return; if(f.size>8*1024*1024){setUploadError('Image must be 8 MB or smaller.');return} setImg(URL.createObjectURL(f));setInspection(undefined);setUploadError('');setUploading(true);const form=new FormData();form.append('file',f);form.append('grain_type','Wheat');try{const r=await api.post('/disease-detection/analyze',form);setInspection(r.data)}catch(err){setUploadError(errMsg(err))}finally{setUploading(false)} }} className="text-sm" />
        {img && <img src={img} alt="Uploaded grain" className="mt-4 max-h-64 rounded-lg" />}
        {uploading&&<p className="mt-2 text-sm">Checking image…</p>}{uploadError&&<p role="alert" className="mt-2 text-sm text-red-700">{uploadError}</p>}{inspection&&<div className="mt-3 rounded-lg bg-amber-50 p-3 text-sm text-amber-900"><p className="font-semibold">Image checks completed · {inspection.mode}</p><p>{inspection.message}</p><p className="mt-1">Image usable for future model analysis: {inspection.image_checks.usable?'Yes':'No'}</p></div>}
      </Card>}
      {c && <Card title={c.title}><div className="h-72"><ResponsiveContainer>
        {c.kind === 'line' ? <LineChart data={c.data}><CartesianGrid stroke="#E2D9BF" strokeDasharray="3 3" /><XAxis dataKey={c.x} fontSize={12} /><YAxis fontSize={12} /><Tooltip /><Legend />{c.series.map((s, i) => <Line key={s} dataKey={s} stroke={COLORS[i]} strokeWidth={2} dot={false} />)}</LineChart>
        : <BarChart data={c.data}><CartesianGrid stroke="#E2D9BF" strokeDasharray="3 3" /><XAxis dataKey={c.x} fontSize={12} /><YAxis fontSize={12} /><Tooltip /><Legend />{c.series.map((s, i) => <Bar key={s} dataKey={s} fill={COLORS[i]} radius={[4, 4, 0, 0]} />)}</BarChart>}
      </ResponsiveContainer></div></Card>}
      {cfg.table && <Card title={cfg.table.title}><div className="overflow-x-auto"><table className="w-full text-left text-sm"><thead><tr className="border-b border-sand-300 text-ink/70">{cfg.table.cols.map(h => <th key={h} className="py-2 pr-4 font-medium">{h}</th>)}</tr></thead>
        <tbody>{cfg.table.rows.map((r, i) => <tr key={i} className="border-b border-sand-100">{r.map((v, j) => <td key={j} className="py-2 pr-4">{v}</td>)}</tr>)}</tbody></table></div></Card>}
      {cfg.bullets && <Card title={cfg.bullets.title}><ul className="list-disc space-y-1 pl-5 text-sm">{cfg.bullets.items.map(i => <li key={i}>{i}</li>)}</ul></Card>}
    </div>
  )
}
