import { useEffect, useState } from 'react'
import { Card } from '../components/ui/Card'
import { api, errMsg } from '../services/api'
import { useAuth } from '../contexts/RoleContext'
type Listing={id:number;seller_id:number;grain:string;quantity_tonnes:number;location:string;price_per_quintal:number}
type Cert={id:number;listing_id:number;certificate_type:string;status:string;issued_at:string;notes:string}
const field='rounded-lg border border-sand-300 bg-white px-3 py-2 text-sm'
export default function Certificates(){
 const {role,user}=useAuth(); const userId=user?.id; const [rows,setRows]=useState<Cert[]>([]); const [listings,setListings]=useState<Listing[]>([]); const [listing,setListing]=useState('');  const [notes,setNotes]=useState(''); const [error,setError]=useState(''); const [busy,setBusy]=useState(false)
 const load=()=>api.get('/certificates').then(r=>setRows(r.data)).catch(e=>setError(errMsg(e)))
 useEffect(()=>{load(); if(['seller','farmer','admin'].includes(role)) api.get('/marketplace/listings').then(r=>setListings(r.data)).catch(()=>{})},[role])
 const issue=async()=>{setError('');setBusy(true);try{await api.post('/certificates',{listing_id:Number(listing),certificate_type:'seller_declaration',notes});setNotes('');await load()}catch(e){setError(errMsg(e))}finally{setBusy(false)}}
 const download=async(id:number)=>{try{const r=await api.get(`/certificates/${id}/pdf`,{responseType:'blob'});const url=URL.createObjectURL(r.data);const a=document.createElement('a');a.href=url;a.download=`grain-record-${id}.pdf`;a.click();URL.revokeObjectURL(url)}catch(e){setError(errMsg(e))}}
 return <div className="space-y-6"><div><h1 className="text-3xl">Quality records</h1><p className="mt-1 text-sm text-ink/60">Traceable records for marketplace listings. A seller declaration is not an independent laboratory certificate.</p></div>
 {['seller','farmer','admin'].includes(role)&&<Card title="Issue a record"><div className="grid gap-3 md:grid-cols-2"><select className={field} value={listing} onChange={e=>setListing(e.target.value)}><option value="">Select your listing</option>{listings.filter(l=>role==='admin'||l.seller_id===userId).map(l=><option key={l.id} value={l.id}>#{l.id} · {l.grain} · {l.location}</option>)}</select><p className="text-sm text-ink/70">Record type: Seller declaration</p><input className={`${field} md:col-span-2`} placeholder="Notes (optional)" value={notes} onChange={e=>setNotes(e.target.value)}/><button disabled={!listing||busy} onClick={issue} className="rounded-lg bg-forest-700 px-4 py-2 text-sm text-white disabled:opacity-50">{busy?'Issuing…':'Issue record'}</button></div></Card>}
 {error&&<p role="alert" className="text-sm text-red-700">{error}</p>}
 <Card title="Your records">{rows.length===0?<p className="text-sm text-ink/60">No records found.</p>:<div className="space-y-3">{rows.map(c=><div key={c.id} className="flex flex-wrap items-center justify-between gap-3 border-b border-sand-200 pb-3"><div><p className="font-medium">Record #{c.id} · Listing #{c.listing_id}</p><p className="text-sm text-ink/60">{c.certificate_type.replace(/_/g,' ')} · {new Date(c.issued_at).toLocaleString()}</p>{c.notes&&<p className="text-sm">{c.notes}</p>}</div><button onClick={()=>download(c.id)} className="rounded-lg border border-sand-300 px-3 py-2 text-sm">Download PDF</button></div>)}</div>}</Card></div>
}
