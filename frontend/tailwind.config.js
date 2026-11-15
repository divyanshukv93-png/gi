export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: { extend: {
    colors: { forest: { 50:'#EEF4F0',100:'#D6E5DB',500:'#2F6B4F',700:'#1F4D3A',900:'#12301F' },
      olive: { 100:'#ECEED9',500:'#7A8450',700:'#565F34' }, sand: { 100:'#F1ECDD',300:'#E2D9BF' },
      paper:'#F8F7F2', ink:'#23272A', risk: { low:'#2F6B4F', mid:'#B7791F', high:'#B23A2E' } },
    fontFamily: { display: ['Fraunces','Georgia','serif'], sans: ['"Public Sans"','system-ui','sans-serif'] },
    borderRadius: { xl: '14px' } } },
}
