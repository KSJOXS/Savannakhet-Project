import en from './locales/en.js'
import la from './locales/la.js'
import vi from './locales/vi.js'

export const messages = { en, la, vi }

export const supportedLocales = [
  { code: 'en', label: 'English', flag: '🇬🇧' },
  { code: 'la', label: 'ລາວ',    flag: '🇱🇦' },
  { code: 'vi', label: 'Việt',   flag: '🇻🇳' },
]
