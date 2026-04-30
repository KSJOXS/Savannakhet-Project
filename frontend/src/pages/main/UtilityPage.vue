<template>
  <div class="currency-converter-card">
    <div class="header">
      <h3><i class="fas fa-exchange-alt"></i> แปลงสกุลเงิน (Currency)</h3>
      <span class="live-badge" :class="{ 'is-custom': isCustom }">
        <i class="fas fa-circle"></i> {{ isCustom ? 'Custom Rate' : 'Live Rate' }}
      </span>
    </div>

    <div v-if="isLoading" class="loading-state">
      <i class="fas fa-spinner fa-spin"></i> กำลังดึงเรทเงินล่าสุดจากตลาดโลก...
    </div>

    <div v-else class="converter-body">
      <p class="last-update" v-if="!isCustom">อัปเดตล่าสุด: {{ lastUpdateDate }}</p>
      <p class="last-update text-custom" v-else>คุณกำลังกำหนดเรทแลกเปลี่ยนเอง</p>

      <div class="input-group">
        <label>จำนวนเงิน (Amount)</label>
        <div class="amount-input">
          <input type="number" v-model="amount" min="0" placeholder="กรอกจำนวนเงิน..." />
        </div>
      </div>

      <div class="currency-selectors">
        <div class="select-group">
          <label>จาก (From)</label>
          <select v-model="fromCurrency">
            <option v-for="curr in currencyList" :key="curr.code" :value="curr.code">
              {{ curr.name }}
            </option>
          </select>
        </div>

        <button class="btn-swap" @click="swapCurrencies" title="สลับสกุลเงิน">
          <i class="fas fa-exchange-alt"></i>
        </button>

        <div class="select-group">
          <label>เป็น (To)</label>
          <select v-model="toCurrency">
            <option v-for="curr in currencyList" :key="curr.code" :value="curr.code">
              {{ curr.name }}
            </option>
          </select>
        </div>
      </div>

      <div class="input-group rate-edit-group">
        <div class="rate-header">
          <label>เรทแลกเปลี่ยนปัจจุบัน</label>
          <button v-if="isCustom" @click="resetToLiveRate" class="btn-reset-rate">
            <i class="fas fa-sync-alt"></i> ใช้เรทตลาดโลก
          </button>
        </div>
        <div class="custom-rate-input">
          <span class="rate-prefix">1 {{ fromCurrency }} =</span>
          <input type="number" step="any" :value="currentRateValue" @input="onRateInput" />
          <span class="rate-suffix">{{ toCurrency }}</span>
        </div>
      </div>

      <div class="result-box">
        <span class="result-amount">{{ convertedAmount }}</span>
        <span class="result-currency">{{ toCurrency }}</span>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'

// 🌟 แก้ไขตรงนี้: เปลี่ยนจาก 100000 เป็นค่าว่าง ('') 🌟
const amount = ref('')
const fromCurrency = ref('LAK')
const toCurrency = ref('THB')
const rates = ref({})
const isLoading = ref(true)
const lastUpdateDate = ref('')

const currencyList = [
  { code: 'LAK', name: '🇱🇦 กีบลาว (LAK)' },
  { code: 'THB', name: '🇹🇭 บาทไทย (THB)' },
  { code: 'VND', name: '🇻🇳 ดองเวียดนาม (VND)' },
  { code: 'USD', name: '🇺🇸 ดอลลาร์สหรัฐ (USD)' },
  { code: 'EUR', name: '🇪🇺 ยูโร (EUR)' },
  { code: 'JPY', name: '🇯🇵 เยนญี่ปุ่น (JPY)' },
  { code: 'KRW', name: '🇰🇷 วอนเกาหลี (KRW)' },
  { code: 'CNY', name: '🇨🇳 หยวนจีน (CNY)' },
  { code: 'GBP', name: '🇬🇧 ปอนด์อังกฤษ (GBP)' },
  { code: 'SGD', name: '🇸🇬 ดอลลาร์สิงคโปร์ (SGD)' }
]

const currentRateValue = ref(0)
const isCustom = ref(false)

const fetchLiveRates = async () => {
  try {
    isLoading.value = true
    const response = await fetch('https://open.er-api.com/v6/latest/USD')
    const data = await response.json()

    if (data && data.rates) {
      rates.value = data.rates
      const date = new Date(data.time_last_update_utc)
      lastUpdateDate.value = date.toLocaleString('th-TH', { dateStyle: 'medium', timeStyle: 'short' })
      updateRateValueFromAPI()
    }
  } catch (error) {
    console.error('Failed to fetch exchange rates:', error)
    rates.value = { USD: 1, THB: 36.5, LAK: 21500, VND: 25400 }
    lastUpdateDate.value = 'Offline Mode'
    updateRateValueFromAPI()
  } finally {
    isLoading.value = false
  }
}

const apiExchangeRate = computed(() => {
  if (!rates.value[fromCurrency.value] || !rates.value[toCurrency.value]) return 0
  const fromRateToUSD = rates.value[fromCurrency.value]
  const toRateToUSD = rates.value[toCurrency.value]
  return (1 / fromRateToUSD) * toRateToUSD
})

const updateRateValueFromAPI = () => {
  if (!isCustom.value && apiExchangeRate.value) {
    const rate = apiExchangeRate.value
    currentRateValue.value = rate < 0.01 ? Number(rate.toFixed(5)) : Number(rate.toFixed(3))
  }
}

watch([fromCurrency, toCurrency], () => {
  isCustom.value = false
  updateRateValueFromAPI()
})

watch(apiExchangeRate, () => {
  updateRateValueFromAPI()
})

const onRateInput = (e) => {
  isCustom.value = true
  currentRateValue.value = parseFloat(e.target.value) || 0
}

const resetToLiveRate = () => {
  isCustom.value = false
  updateRateValueFromAPI()
}

const swapCurrencies = () => {
  const temp = fromCurrency.value
  fromCurrency.value = toCurrency.value
  toCurrency.value = temp
}

const convertedAmount = computed(() => {
  // 🌟 ถ้าค่า amount เป็นค่าว่าง (ยังไม่พิมพ์) ให้โชว์ 0.00
  if (!amount.value || isNaN(amount.value) || !currentRateValue.value) return '0.00'
  const result = amount.value * currentRateValue.value

  return new Intl.NumberFormat('th-TH', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(result)
})

onMounted(() => {
  fetchLiveRates()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.currency-converter-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  padding: 24px;
  font-family: 'Inter', sans-serif;
  max-width: 500px;
  margin: 0 auto;
  border: 1px solid #f1f5f9;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 15px;
}

.header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #0f172a;
  display: flex;
  align-items: center;
  gap: 10px;
}

.header h3 i {
  color: #00aa6c;
}

.live-badge {
  font-size: 0.75rem;
  font-weight: 700;
  color: #ef4444;
  background: #fef2f2;
  padding: 4px 10px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s;
}

.live-badge.is-custom {
  color: #f59e0b;
  background: #fef3c7;
}

.live-badge i {
  font-size: 0.5rem;
}

.live-badge:not(.is-custom) i {
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% {
    opacity: 1;
  }

  50% {
    opacity: 0.3;
  }

  100% {
    opacity: 1;
  }
}

.loading-state {
  text-align: center;
  padding: 40px 0;
  color: #64748b;
  font-weight: 500;
}

.last-update {
  font-size: 0.8rem;
  color: #94a3b8;
  margin: 0 0 15px;
  text-align: right;
}

.text-custom {
  color: #f59e0b;
  font-weight: 600;
}

.input-group label,
.select-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 8px;
}

.amount-input input {
  width: 100%;
  padding: 14px 16px;
  font-size: 1.2rem;
  font-weight: 700;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  color: #0f172a;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.amount-input input:focus {
  border-color: #00aa6c;
}

.currency-selectors {
  display: flex;
  align-items: flex-end;
  gap: 15px;
  margin: 20px 0;
}

.select-group {
  flex: 1;
}

.select-group select {
  width: 100%;
  padding: 12px;
  font-size: 1rem;
  font-weight: 600;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  background: white;
  color: #0f172a;
  outline: none;
  cursor: pointer;
}

.btn-swap {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: #f1f5f9;
  border: none;
  color: #00aa6c;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-swap:hover {
  background: #00aa6c;
  color: white;
  transform: rotate(180deg);
}

.rate-edit-group {
  margin-bottom: 20px;
  background: #f8fafc;
  padding: 15px;
  border-radius: 12px;
  border: 1px dashed #cbd5e1;
}

.rate-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.rate-header label {
  margin: 0;
  color: #0f172a;
}

.btn-reset-rate {
  background: none;
  border: none;
  color: #3b82f6;
  font-size: 0.75rem;
  font-weight: 700;
  cursor: pointer;
  padding: 0;
}

.btn-reset-rate:hover {
  text-decoration: underline;
}

.custom-rate-input {
  display: flex;
  align-items: center;
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 8px 12px;
}

.custom-rate-input input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 1.1rem;
  font-weight: 700;
  color: #00aa6c;
  text-align: center;
  outline: none;
  min-width: 50px;
}

.rate-prefix,
.rate-suffix {
  font-size: 0.9rem;
  font-weight: 600;
  color: #64748b;
}

.result-box {
  background: #0f172a;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
}

.result-amount {
  font-size: 2.5rem;
  font-weight: 800;
  color: #22c55e;
  word-break: break-all;
}

.result-currency {
  font-size: 1.2rem;
  font-weight: 600;
  color: white;
  margin-left: 10px;
}
</style>