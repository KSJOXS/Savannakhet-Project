<template>
  <div class="utility-card">
    <div class="card-header">
      <span class="icon">🚌</span>
      <h3>การเดินทาง</h3>
    </div>
    <div class="transport-grid">
      <div v-for="item in transports" :key="item.id" class="transport-card">
        <div class="transport-info">
          <span class="type">{{ item.type }}</span>
          <div class="detail-row">
            <span class="price-label">ราคาประเมิน:</span>
            <span class="price">{{ item.price }}</span>
          </div>
          <div class="detail-row">
            <span class="contact-label">ติดต่อ:</span>
            <span class="contact">{{ item.contact }}</span>
          </div>
        </div>
        <div class="transport-status">
          <span class="status-dot"></span>
          ใช้งานได้
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import utilityRepository from "@/repositories/utilityRepository";

const transports = ref([]);

onMounted(async () => {
  try {
    const response = await utilityRepository.getTransports();
    transports.value = response.data;
  } catch (error) {
    console.error("Error fetching transports:", error);
  }
});
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

.transport-grid {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.transport-card {
  padding: 18px;
  border-radius: 12px;
  background: #ffffff;
  border: 1px solid #f1f3f5;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  transition: all 0.3s;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.02);
}
.transport-card:hover {
  border-color: #2ecc71;
  background: #f9fffb;
}
.transport-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.type {
  font-weight: 700;
  color: #2c3e50;
  font-size: 1.05rem;
}
.detail-row {
  display: flex;
  gap: 8px;
  font-size: 0.9rem;
}
.price-label,
.contact-label {
  color: #95a5a6;
  min-width: 80px;
}
.price {
  color: #27ae60;
  font-weight: 600;
}
.contact {
  color: #34495e;
}
.transport-status {
  font-size: 0.75rem;
  color: #2ecc71;
  background: #eafaf1;
  padding: 4px 10px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: 600;
}
.status-dot {
  width: 6px;
  height: 6px;
  background: #2ecc71;
  border-radius: 50%;
}
</style>
