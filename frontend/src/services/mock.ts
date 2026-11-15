// DEMO DATA ONLY. Replaced by real API calls in the backend-integration phase.
export const demoOverview = {
  stats: [{ label:'Batches monitored', value:'12' }, { label:'High-risk batches', value:'2' }, { label:'Avg humidity', value:'64%' }, { label:'Active listings', value:'5' }],
  humidity: Array.from({ length: 12 }, (_, i) => ({ t: `${i * 2}:00`, rh: 58 + Math.round(8 * Math.sin(i / 2) + i / 2) })),
  batches: [{ id:'B-1042', grain:'Wheat', risk:'high' as const }, { id:'B-1038', grain:'Rice', risk:'mid' as const }, { id:'B-1027', grain:'Maize', risk:'low' as const }],
}

// DEMO marketplace data. Certificate sourceType decides whether it may show as "verified".
export type CertSource = 'ai_assessment' | 'human_verified' | 'lab_certified'
export const demoCertificates = [
  { id:'GI-C-0001', batchId:'B-1027', grain:'Maize', grade:'A', moisture:12.8, defects:'No visible defects detected', date:'2026-11-02', method:'Image inspection + sensor log', sourceType:'lab_certified' as CertSource, storage:'Dry store, avg 24°C / 58% RH for 21 days' },
  { id:'GI-C-0002', batchId:'B-1038', grain:'Rice', grade:'B', moisture:13.9, defects:'Minor discoloration (3% of kernels)', date:'2026-11-06', method:'Image inspection', sourceType:'human_verified' as CertSource, storage:'Warehouse, avg 27°C / 66% RH for 40 days' },
  { id:'GI-C-0003', batchId:'B-1042', grain:'Wheat', grade:'B', moisture:14.6, defects:'Possible mould spots flagged for review', date:'2026-11-10', method:'Demo model inference', sourceType:'ai_assessment' as CertSource, storage:'Silo, humidity above 75% for 6 days' },
]
export const demoListings = [
  { id:'L-201', grain:'Maize', qty:'40 t', price:2150, seller:'Kisan Agro Co-op', location:'Karnal, Haryana', grade:'A', moisture:12.8, inspected:'2026-11-02', certId:'GI-C-0001' },
  { id:'L-202', grain:'Rice', qty:'25 t', price:3400, seller:'Sharma Traders', location:'Ludhiana, Punjab', grade:'B', moisture:13.9, inspected:'2026-11-06', certId:'GI-C-0002' },
  { id:'L-203', grain:'Wheat', qty:'60 t', price:2475, seller:'Bhumi Farms', location:'Hisar, Haryana', grade:'B', moisture:14.6, inspected:'2026-11-10', certId:'GI-C-0003' },
  { id:'L-204', grain:'Wheat', qty:'15 t', price:2510, seller:'Gill Storage', location:'Bathinda, Punjab', grade:'—', moisture:null as number | null, inspected:'—', certId:'' },
]
