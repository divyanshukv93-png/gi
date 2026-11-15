import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
const nav = (o: string[]) => Object.fromEntries(['overview','grainHealth','diseaseDetection','environment','storage','market','supplyDemand','marketplace','certificates','assistant','reports','settings'].map((k, i) => [k, o[i]]))
const resources = {
  en: { translation: { tagline: 'Smart Grain. Safe Storage. Secure Future.', language: 'Language', role: 'Demo role',
    nav: nav(['Overview','Grain Health','Disease Detection','Environmental Monitoring','Storage Intelligence','Market Intelligence','Supply & Demand','Marketplace','Quality Certificates','AI Assistant','Reports','Settings']) } },
  hi: { translation: { tagline: 'स्मार्ट अनाज। सुरक्षित भंडारण। सुरक्षित भविष्य।', language: 'भाषा', role: 'डेमो भूमिका',
    nav: nav(['अवलोकन','अनाज स्वास्थ्य','रोग पहचान','पर्यावरण निगरानी','भंडारण बुद्धिमत्ता','बाज़ार जानकारी','आपूर्ति और मांग','मार्केटप्लेस','गुणवत्ता प्रमाणपत्र','एआई सहायक','रिपोर्ट','सेटिंग्स']) } },
}
i18n.use(initReactI18next).init({ resources, lng: localStorage.getItem('lang') || 'en', fallbackLng: 'en', interpolation: { escapeValue: false } })
export default i18n
