import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { Card } from '../components/ui/Card'
import { ProvenanceBadge } from '../components/domain/ProvenanceBadge'
import { RiskPill } from '../components/domain/RiskPill'
import { demoOverview } from '../services/mock'
export default function Overview() {
  const d = demoOverview
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-2"><h1 className="text-3xl">Overview</h1><ProvenanceBadge source="demo" /></div>
      <div className="grid grid-cols-2 gap-4 xl:grid-cols-4">
        {d.stats.map(s => <Card key={s.label}><p className="text-sm text-ink/70">{s.label}</p><p className="mt-1 font-display text-3xl text-forest-900">{s.value}</p></Card>)}
      </div>
      <div className="grid gap-6 xl:grid-cols-3">
        <Card title="Warehouse humidity, last 12 hours (%)" className="xl:col-span-2">
          <div className="h-64"><ResponsiveContainer><AreaChart data={d.humidity}>
            <CartesianGrid stroke="#E2D9BF" strokeDasharray="3 3" /><XAxis dataKey="t" fontSize={12} /><YAxis domain={[40, 90]} fontSize={12} /><Tooltip />
            <Area dataKey="rh" stroke="#2F6B4F" fill="#D6E5DB" strokeWidth={2} /></AreaChart></ResponsiveContainer></div>
        </Card>
        <Card title="Batches needing attention">
          <ul className="space-y-3">{d.batches.map(b => <li key={b.id} className="flex items-center justify-between text-sm"><span>{b.id} · {b.grain}</span><RiskPill level={b.risk} /></li>)}</ul>
        </Card>
      </div>
    </div>
  )
}
