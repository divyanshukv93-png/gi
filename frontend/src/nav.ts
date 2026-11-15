import { LayoutDashboard, Wheat, ScanSearch, Thermometer, Warehouse, BarChart3, TrendingUp, Store, BadgeCheck, Bot, FileText, Settings } from 'lucide-react'
import type { Role } from './contexts/RoleContext'
const all: Role[] = ['farmer','seller','buyer','admin']
export const NAV = [
  { key:'overview', path:'/', icon:LayoutDashboard, roles:all },
  { key:'grainHealth', path:'/grain-health', icon:Wheat, roles:['farmer','seller','admin'] as Role[] },
  { key:'diseaseDetection', path:'/disease-detection', icon:ScanSearch, roles:['farmer','seller','admin'] as Role[] },
  { key:'environment', path:'/environment', icon:Thermometer, roles:['farmer','seller','admin'] as Role[] },
  { key:'storage', path:'/storage', icon:Warehouse, roles:['farmer','seller','admin'] as Role[] },
  { key:'market', path:'/market', icon:BarChart3, roles:all },
  { key:'supplyDemand', path:'/supply-demand', icon:TrendingUp, roles:all },
  { key:'marketplace', path:'/marketplace', icon:Store, roles:all },
  { key:'certificates', path:'/certificates', icon:BadgeCheck, roles:all },
  { key:'assistant', path:'/assistant', icon:Bot, roles:all },
  { key:'reports', path:'/reports', icon:FileText, roles:all },
  { key:'settings', path:'/settings', icon:Settings, roles:all },
]
