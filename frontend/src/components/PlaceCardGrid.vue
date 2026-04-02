<template>
    <div class="grid">
        <div v-for="place in places" :key="place.id" class="card">
            <img :src="place.image_url || 'https://via.placeholder.com/300x200'" class="place-img">

            <div class="card-body">
                <h3>{{ place.name }}</h3>
                <p>{{ place.description }}</p>

                <div class="footer">
                    <span class="rating">⭐ {{ place.rating_avg || '0.0' }}</span>
                    <button class="btn-detail">ดูข้อมูล</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
// รับข้อมูลจากตัวแม่ (RecommendList.vue ในโฟลเดอร์ pages)
defineProps(['places', 'loading'])
</script>

<style scoped>
/* ใส่ Style ตามใจชอบครับ */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
}

.card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.place-img {
    width: 100%;
    height: 180px;
    object-fit: cover;
}

.card-body {
    padding: 15px;
}

.rating {
    font-weight: bold;
    color: #f1c40f;
}
</style>