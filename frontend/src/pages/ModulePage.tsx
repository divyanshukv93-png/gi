import { useTranslation } from 'react-i18next'
import ModuleDashboard from './ModuleDashboard'
import { MODULES } from './modules'
import Assistant from './Assistant'
import MarketData from './MarketData'
import EnvironmentPage from './EnvironmentPage'
import StoragePage from './StoragePage'
export default function ModulePage({ navKey }: { navKey: string }) {
  const { t } = useTranslation()
  if (navKey === 'assistant') return <Assistant />
  if (navKey === 'market') return <MarketData />
  if (navKey === 'environment') return <EnvironmentPage />
  if (navKey === 'storage') return <StoragePage />
  return <ModuleDashboard title={t(`nav.${navKey}`)} cfg={MODULES[navKey]} />
}
