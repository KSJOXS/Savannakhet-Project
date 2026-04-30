<template>
  <div class="utility-card">
    <div class="card-header">
      <span class="icon">🗣️</span>
      <h3>ประโยคพื้นฐาน</h3>
    </div>
    <div class="phrase-list">
      <div v-for="phrase in phrases" :key="phrase.id" class="phrase-item">
        <div class="phrase-content">
          <span class="thai">{{ phrase.thai_text }}</span>
          <span class="lao">{{ phrase.lao_text }}</span>
          <span class="pronunciation">{{ phrase.pronunciation }}</span>
        </div>
        <button @click="speak(phrase.lao_text)" class="speak-btn" title="ฟังเสียง">
          <span class="btn-icon">🔊</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import utilityRepository from '@/repositories/utilityRepository';

const phrases = ref([]);

onMounted(async () => {
  try {
    const response = await utilityRepository.getPhrases();
    phrases.value = response.data;
  } catch (error) {
    console.error("Error fetching phrases:", error);
  }
});

const speak = (text) => {
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text);
    // พยายามหาเสียงภาษาไทยถ้าภาษาลาวไม่มี เพราะสำเนียงใกล้กัน
    utterance.lang = 'lo-LA';
    
    // ตรวจสอบว่ามีเสียงโหลดมาหรือยัง
    const voices = window.speechSynthesis.getVoices();
    const laoVoice = voices.find(v => v.lang.includes('lo'));
    const thaiVoice = voices.find(v => v.lang.includes('th'));
    
    if (laoVoice) utterance.voice = laoVoice;
    else if (thaiVoice) utterance.voice = thaiVoice;
    
    window.speechSynthesis.speak(utterance);
  } else {
    alert("ขออภัย เบราว์เซอร์ของคุณไม่รองรับการอ่านออกเสียง");
  }
};
</script>

<style scoped>
.utility-card {
  background: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  margin-bottom: 20px;
}
.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}
.card-header h3 { margin: 0; color: #2c3e50; font-size: 1.2rem; }
.icon { font-size: 1.5rem; }

.phrase-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.phrase-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f8fbff;
  border-radius: 12px;
  border: 1px solid #eef2f7;
  transition: transform 0.2s;
}
.phrase-item:active {
  transform: scale(0.98);
}
.phrase-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.thai {
  font-weight: 600;
  color: #34495e;
  font-size: 1rem;
}
.lao {
  font-size: 1.1rem;
  color: #3498db;
  font-weight: bold;
}
.pronunciation {
  font-size: 0.85rem;
  color: #95a5a6;
  font-style: italic;
}
.speak-btn {
  background: white;
  border: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-radius: 50%;
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}
.speak-btn:hover {
  background: #3498db;
}
.speak-btn:hover .btn-icon {
  filter: brightness(0) invert(1);
}
.btn-icon {
  font-size: 1.2rem;
}
</style>
