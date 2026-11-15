import type { Cfg } from './ModuleDashboard'
const hrs = Array.from({ length: 12 }, (_, i) => `${i * 2}:00`)
const months = ['Jan','Feb','Mar','Apr','May','Jun']
// All values below are DEMO / SIMULATED / PREDICTED placeholders, never real statistics.
export const MODULES: Record<string, Cfg> = {
  grainHealth: { source: 'demo', stats: [['Batches', '12'], ['Healthy', '9'], ['Watch', '2'], ['High risk', '1']],
    table: { title: 'Batches', cols: ['Batch', 'Grain', 'Moisture', 'Status'], rows: [['B-1027', 'Maize', '12.8%', 'Healthy'], ['B-1038', 'Rice', '13.9%', 'Watch'], ['B-1042', 'Wheat', '14.6%', 'High risk']] } },
  diseaseDetection: { source: 'demo', upload: true, note: 'Demo model mode: image upload only. No disease or defect results are produced until a trained model is connected.',
    table: { title: 'Inspection history', cols: ['Date', 'Batch', 'Result', 'Mode'], rows: [['No inspections yet', '', '', '']] } },
  environment: { source: 'simulated', note: 'Simulated sensor feed. Physical ESP32 readings will be labelled "Live" once MQTT is connected.',
    stats: [['Temperature', '27.4 °C'], ['Humidity', '66 %'], ['Grain moisture', '13.2 %'], ['Sensors online', '4 / 5']],
    chart: { title: 'Temperature and humidity, last 24 h', kind: 'line', x: 't', series: ['temp', 'rh'], data: hrs.map((t, i) => ({ t, temp: +(25 + 3 * Math.sin(i / 2)).toFixed(1), rh: Math.round(62 + 6 * Math.cos(i / 3)) })) },
    table: { title: 'Alert history', cols: ['Time', 'Alert', 'Severity'], rows: [['08:00', 'Humidity above 70%', 'Watch'], ['14:00', 'Sensor 5 offline', 'Warning']] } },
  storage: { source: 'predicted', note: 'Preliminary risk estimate only. It is not a food-safety guarantee; confirm by inspection before sale or consumption.',
    stats: [['Estimated safe period', '~38 days'], ['Uncertainty range', '28–50 days'], ['Storage health', '72 / 100'], ['Risk', 'Watch']],
    chart: { title: 'Projected grain moisture (%)', kind: 'line', x: 'week', series: ['moisture'], data: [1,2,3,4,5,6].map(w => ({ week: `W${w}`, moisture: +(13.2 + w * 0.25).toFixed(2) })) },
    bullets: { title: 'Suggested actions', items: ['Improve ventilation to bring humidity down', 'Re-measure moisture within 7 days', 'Inspect for mould before listing the batch'] } },
  market: { source: 'demo', note: 'Illustrative layout only. Real mandi prices and production data will come from AGMARKNET, data.gov.in and FAOSTAT imports, with source and date shown.',
    chart: { title: 'Price by mandi (illustrative index)', kind: 'bar', x: 'mandi', series: ['index'], data: ['Mandi A', 'Mandi B', 'Mandi C', 'Mandi D'].map((mandi, i) => ({ mandi, index: 96 + i * 3 })) },
    table: { title: 'Datasets', cols: ['Source', 'Status'], rows: [['AGMARKNET', 'Not imported'], ['data.gov.in', 'Not imported'], ['FAOSTAT', 'Not imported']] } },
  supplyDemand: { source: 'predicted', note: 'Demo forecast curves. Real forecasts need imported history and time-based validation.',
    chart: { title: 'Supply vs demand (index, next 6 months)', kind: 'line', x: 'm', series: ['supply', 'demand'], data: months.map((m, i) => ({ m, supply: 100 + i * 2, demand: 98 + i * 4 })) },
    bullets: { title: 'Signals', items: ['Demand rising faster than supply in this demo series: possible shortage later in the window'] } },
  assistant: { source: 'demo', note: 'The chat connects to Ollama and Gemini in the backend phase. Nothing is sent from this page yet.',
    bullets: { title: 'Questions it will answer', items: ['What is the health status of my wheat batch?', 'How long can my rice stay in current conditions?', 'Which batches are high risk?', 'Explain my quality certificate'] } },
  reports: { source: 'demo', table: { title: 'Report types', cols: ['Report', 'Status'], rows: [['Batch quality report (PDF)', 'Needs backend'], ['Storage risk report (PDF)', 'Needs backend'], ['Market summary (PDF)', 'Needs backend']] } },
  settings: { source: 'demo', bullets: { title: 'Planned settings', items: ['Profile and language preference (saved to account)', 'Alert thresholds', 'Notification channels'] } },
}
