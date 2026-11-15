export const RiskPill = ({ level }: { level: 'low' | 'mid' | 'high' }) => {
  const m = { low:['Low risk','bg-forest-100 text-forest-700'], mid:['Watch','bg-amber-100 text-amber-800'], high:['High risk','bg-red-100 text-red-800'] }[level]
  return <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${m[1]}`}>{m[0]}</span>
}
