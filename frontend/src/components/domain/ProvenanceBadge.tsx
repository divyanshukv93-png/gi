export type Source = 'live' | 'historical' | 'simulated' | 'predicted' | 'demo'
const style: Record<Source, string> = { live:'bg-forest-100 text-forest-700', historical:'bg-sand-100 text-ink', simulated:'bg-olive-100 text-olive-700', predicted:'bg-sky-100 text-sky-800', demo:'bg-amber-100 text-amber-800' }
export const ProvenanceBadge = ({ source }: { source: Source }) => (
  <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${style[source]}`}>{source === 'demo' ? 'Demo data' : source[0].toUpperCase() + source.slice(1)}</span>
)
