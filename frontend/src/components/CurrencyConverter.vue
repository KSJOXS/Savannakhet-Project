<template>
  <div class="utility-card">
    <div class="card-header">
      <span class="icon">💰</span>
      <h3>คำนวณค่าเงิน</h3>
    </div>
    <div class="converter-grid">
      <div class="input-group">
        <label>LAK (กีบ)</label>
        <div class="input-wrapper">
          <input
            type="number"
            v-model="lakAmount"
            @input="convertFromLak"
            placeholder="ระบุเงินกีบ"
          />
          <span class="unit">LAK</span>
        </div>
      </div>
      <div class="swap-icon">⇅</div>
      <div class="input-group">
        <label>THB (บาท)</label>
        <div class="input-wrapper">
          <input
            type="number"
            v-model="thbAmount"
            @input="convertFromThb"
            placeholder="ระบุเงินบาท"
          />
          <span class="unit">THB</span>
        </div>
      </div>
    </div>
    <p class="rate-info">
      เรทโดยประมาณ: 1 THB ≈ {{ Math.round(1 / rates.THB) || 650 }} LAK
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import utilityRepository from "@/repositories/utilityRepository";

const lakAmount = ref(0);
const thbAmount = ref(0);
const rates = ref({ THB: 0.0015 });

onMounted(async () => {
  try {
    const response = await utilityRepository.getExchangeRates();
    rates.value = response.data.rates;
  } catch (error) {
    console.error("Error fetching rates:", error);
  }
});

const convertFromLak = () => {
  thbAmount.value = (lakAmount.value * rates.value.THB).toFixed(2);
};

const convertFromThb = () => {
  lakAmount.value = Math.round(thbAmount.value / rates.value.THB);
};
</script>

<style scoped>
.utility-card {
  background: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;
}
.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}
.card-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.2rem;
}
.icon {
  font-size: 1.5rem;
}

.converter-grid {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.input-group {
  display: flex;
  flex-direction: column;
}
.input-group label {
  font-size: 0.85rem;
  color: #7f8c8d;
  margin-bottom: 6px;
  font-weight: 500;
}
.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}
.input-group input {
  width: 100%;
  padding: 12px 15px;
  padding-right: 60px;
  border: 2px solid #edf2f7;
  border-radius: 10px;
  font-size: 1.1rem;
  transition: border-color 0.2s;
  outline: none;
}
.input-group input:focus {
  border-color: #3498db;
}
.unit {
  position: absolute;
  right: 15px;
  color: #95a5a6;
  font-weight: bold;
  font-size: 0.9rem;
}
.swap-icon {
  text-align: center;
  color: #3498db;
  font-size: 1.5rem;
  font-weight: bold;
  margin: -5px 0;
}
.rate-info {
  font-size: 0.8rem;
  color: #bdc3c7;
  margin-top: 15px;
  text-align: center;
  border-top: 1px solid #f8f9fa;
  padding-top: 10px;
}
</style>
