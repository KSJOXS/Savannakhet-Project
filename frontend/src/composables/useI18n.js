import { ref, computed } from 'vue'
import { messages, supportedLocales } from '@/i18n/index.js'

// Global reactive locale — shared across all components
const currentLocale = ref(localStorage.getItem('lang') || 'en')

export function useI18n() {
  const setLocale = (code) => {
    if (messages[code]) {
      currentLocale.value = code
      localStorage.setItem('lang', code)
    }
  }

  /**
   * Translate a dot-notation key, e.g. t('nav.home') → 'Home'
   */
  const t = (key) => {
    const parts = key.split('.')
    let result = messages[currentLocale.value]
    for (const part of parts) {
      if (result && typeof result === 'object') {
        result = result[part]
      } else {
        return key // fallback: return the key itself
      }
    }
    return result ?? key
  }

  const locale = computed(() => currentLocale.value)

  return { t, setLocale, locale, supportedLocales }
}
