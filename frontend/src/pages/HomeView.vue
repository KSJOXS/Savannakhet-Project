<template>
    <div class="home-page">
        <Navbar />

        <header class="hero">
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <div class="badge-new">NEW: AI Recommendation System</div>
                <h1>ค้นพบสะวันนะเขต</h1>
                <p>สัมผัสประสบการณ์การท่องเที่ยวในลาวใต้ ด้วยระบบแนะนำอัจฉริยะ GNN</p>
                <button @click="router.push('/explore')" class="btn-start">
                    <i class="fas fa-rocket"></i> เริ่มต้นสำรวจเลย
                </button>
            </div>
        </header>

        <section class="featured-section">
            <div class="container">
                <div class="section-header">
                    <div>
                        <h2>สถานที่น่าสนใจ</h2>
                        <p>คัดสรรมาเพื่อคุณโดยเฉพาะ</p>
                    </div>
                    <button @click="router.push('/explore')" class="btn-view-all">ดูทั้งหมด →</button>
                </div>

                <div v-if="loading" class="featured-grid">
                    <div v-for="i in 3" :key="i" class="placeholder-card">
                        <div class="skeleton-img"></div>
                        <div class="skeleton-body">
                            <div class="skeleton-title"></div>
                            <div class="skeleton-text"></div>
                        </div>
                    </div>
                </div>

                <div v-else class="featured-grid">
                    <div v-for="place in featuredPlaces" :key="place.id" class="place-card"
                        @click="router.push(`/explore`)">
                        <div class="card-img-wrapper">
                            <img :src="place.image_url || 'https://via.placeholder.com/400x300?text=Savannakhet'"
                                alt="place">
                            <span class="card-tag">{{ getCategoryName(place.category_id) }}</span>
                        </div>
                        <div class="card-body">
                            <h3>{{ place.name }}</h3>
                            <p class="desc">{{ place.description }}</p>
                            <div class="card-footer">
                                <span class="rating">⭐ {{ place.rating_avg || '0.0' }}</span>
                                <span class="btn-detail">ดูข้อมูล</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <footer class="simple-footer">
            <p>&copy; 2026 Savannakhet Smart Travel Project - GNN Recommendation</p>
        </footer>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Navbar from '../components/Navbar.vue'

const router = useRouter()
const featuredPlaces = ref([])
const categories = ref([])
const loading = ref(true)

const fetchData = async () => {
    try {
        // ดึงข้อมูลสถานที่และหมวดหมู่พร้อมกัน
        const [resPlaces, resCats] = await Promise.all([
            axios.get('http://127.0.0.1:8000/places'),
            axios.get('http://127.0.0.1:8000/categories')
        ])
        // สุ่มหรือเลือกเฉพาะ 3 ที่แรกมาโชว์หน้า Home
        featuredPlaces.value = resPlaces.data.slice(0, 3)
        categories.value = resCats.data
    } catch (error) {
        console.error("Error fetching home data:", error)
    } finally {
        loading.value = false
    }
}

const getCategoryName = (id) => {
    const cat = categories.value.find(c => c.id === id)
    return cat ? cat.name : 'ทั่วไป'
}

onMounted(fetchData)
</script>

<style scoped>
/* 📌 Hero Styles */
.hero {
    position: relative;
    background: url('https://images.unsplash.com/photo-1540611025311-01df3cef54b5?q=80&w=2070') center/cover;
    height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: white;
}

.hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(52, 152, 219, 0.8), rgba(44, 62, 80, 0.9));
}

.hero-content {
    position: relative;
    z-index: 1;
    max-width: 800px;
    padding: 0 20px;
}

.badge-new {
    background: rgba(255, 255, 255, 0.2);
    padding: 5px 15px;
    border-radius: 50px;
    display: inline-block;
    margin-bottom: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 1px;
}

.hero-content h1 {
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 15px;
    line-height: 1.2;
}

.hero-content p {
    font-size: 1.2rem;
    opacity: 0.9;
    margin-bottom: 30px;
}

.btn-start {
    background: #3498db;
    color: white;
    border: none;
    padding: 15px 40px;
    border-radius: 50px;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    transition: 0.3s;
}

.btn-start:hover {
    background: #2980b9;
    transform: translateY(-5px);
    box-shadow: 0 15px 25px rgba(0, 0, 0, 0.3);
}

/* 📌 Section Styles */
.featured-section {
    padding: 80px 20px;
    max-width: 1200px;
    margin: 0 auto;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 40px;
}

.section-header h2 {
    font-size: 2rem;
    color: #2c3e50;
    margin: 0;
}

.btn-view-all {
    background: none;
    border: none;
    color: #3498db;
    font-weight: 700;
    cursor: pointer;
}

/* 📌 Grid & Card Styles */
.featured-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
}

.place-card {
    background: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    transition: 0.3s;
    cursor: pointer;
}

.place-card:hover {
    transform: translateY(-10px);
}

.card-img-wrapper {
    position: relative;
    height: 230px;
}

.card-img-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.card-tag {
    position: absolute;
    top: 15px;
    left: 15px;
    background: #3498db;
    color: white;
    padding: 5px 15px;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: bold;
}

.card-body {
    padding: 25px;
}

.card-body h3 {
    margin: 0 0 10px;
    color: #2c3e50;
}

.desc {
    color: #7f8c8d;
    font-size: 0.9rem;
    line-height: 1.6;
    height: 45px;
    overflow: hidden;
    margin-bottom: 20px;
}

.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 15px;
    border-top: 1px solid #f1f5f9;
}

.rating {
    color: #f1c40f;
    font-weight: bold;
}

.btn-detail {
    color: #3498db;
    font-weight: bold;
    font-size: 0.9rem;
}

/* 📌 Skeleton Animation */
.skeleton-img {
    width: 100%;
    height: 230px;
    background: #eee;
}

.skeleton-title {
    width: 60%;
    height: 20px;
    background: #eee;
    margin-bottom: 10px;
}

.skeleton-text {
    width: 100%;
    height: 15px;
    background: #f5f5f5;
}

.simple-footer {
    text-align: center;
    padding: 40px;
    color: #95a5a6;
    border-top: 1px solid #eee;
}
</style>