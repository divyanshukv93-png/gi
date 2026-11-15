import type { CertSource } from '../../services/mock'
const m: Record<CertSource | 'none', [string, string]> = {
  lab_certified: ['Lab certified', 'bg-forest-100 text-forest-700'],
  human_verified: ['Human verified', 'bg-olive-100 text-olive-700'],
  ai_assessment: ['AI assessment, unverified', 'bg-amber-100 text-amber-800'],
  none: ['No certificate', 'bg-sand-100 text-ink'],
}
export const CertBadge = ({ source }: { source?: CertSource }) => {
  const [label, cls] = m[source ?? 'none']
  return <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${cls}`}>{label}</span>
}
