<template>
    <div class="explore-page">
        <Navbar />

        <div class="explore-container">
            <div class="explore-layout">
                <aside class="sidebar">
                    <div class="filter-card">
                        <div class="filter-header">
                            <h3>ค้นหาอัจฉริยะ</h3>
                            <p>ระบุความต้องการของคุณ</p>
                        </div>

                        <div class="filter-group">
                            <label>ชื่อสถานที่</label>
                            <div class="input-with-icon">
                                <i class="fas fa-search"></i>
                                <input v-model="searchQuery" type="text" placeholder="เช่น วัด, ถ้ำ, ร้านอาหาร..." />
                            </div>
                        </div>

                        <div class="filter-group">
                            <label>ประเภทสถานที่</label>
                            <div class="category-grid">
                                <button :class="['cat-btn', { active: !selectedCategory }]"
                                    @click="filterByCategory(null)">
                                    ทั้งหมด
                                </button>
                                <button v-for="cat in categories" :key="cat.id"
                                    :class="['cat-btn', { active: selectedCategory === cat.id }]"
                                    @click="filterByCategory(cat.id)">
                                    {{ cat.name }}
                                </button>
                            </div>
                        </div>

                        <button @click="resetFilters" class="btn-clear">
                            ล้างค่าทั้งหมด
                        </button>
                    </div>
                </aside>

                <main class="content-area">
                    <div class="results-info">
                        <h2>ผลการค้นหา <span class="count-badge">{{ filteredPlaces.length }} สถานที่</span></h2>
                    </div>

                    <div v-if="loading" class="loading-state">
                        <div class="spinner"></div>
                        <p>กำลังค้นหาสถานที่...</p>
                    </div>

                    <div v-else class="places-grid">
                        <div v-for="place in filteredPlaces" :key="place.id" class="modern-card"
                            @click="goToDetail(place.id)">
                            <div class="card-media">
                                <img :src="place.image_url || 'https://via.placeholder.com/400x300?text=Savannakhet'"
                                    :alt="place.name" />
                                <div class="category-tag">{{ getCategoryName(place.category_id) }}</div>
                            </div>

                            <div class="card-details">
                                <h3>{{ place.name }}</h3>
                                <p class="description">{{ place.description }}</p>

                                <div class="card-footer">
                                    <div class="rating">
                                        <i class="fas fa-star"></i>
                                        <span>{{ place.rating_avg || '0.0' }}</span>
                                    </div>
                                    <span class="view-link">รายละเอียด</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div v-if="!loading && filteredPlaces.length === 0" class="empty-state">
                        <i class="fas fa-map-marked-alt"></i>
                        <p>ไม่พบสถานที่ที่คุณต้องการ ลองเปลี่ยนคำค้นหาดูนะครับ</p>
                    </div>
                </main>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'

const router = useRouter()
const places = ref([])
const categories = ref([])
const loading = ref(true)
const searchQuery = ref('')
const selectedCategory = ref(null)

const fetchData = async () => {
    loading.value = true
    try {
        const [resPlaces, resCats] = await Promise.all([
            axios.get('http://127.0.0.1:8000/places'),
            axios.get('http://127.0.0.1:8000/categories')
        ])
        places.value = resPlaces.data
        categories.value = resCats.data
    } catch (err) {
        console.error("API Error:", err)
    } finally {
        loading.value = false
    }
}

const filteredPlaces = computed(() => {
    return places.value.filter(p => {
        const matchesSearch = p.name.toLowerCase().includes(searchQuery.value.toLowerCase())
        const matchesCat = !selectedCategory.value || p.category_id === selectedCategory.value
        return matchesSearch && matchesCat
    })
})

const filterByCategory = (id) => selectedCategory.value = id
const resetFilters = () => {
    searchQuery.value = ''
    selectedCategory.value = null
}

const getCategoryName = (id) => {
    const cat = categories.value.find(c => c.id === id)
    return cat ? cat.name : 'ทั่วไป'
}

const goToDetail = (id) => {
    const userData = localStorage.getItem('user')
    if (!userData) {
        router.push('/login')
    } else {
        router.push(`/places/${id}`)
    }
}

onMounted(fetchData)
</script>

<style scoped>
/* 📌 ปรับพื้นหลังให้เป็น Gradient น้ำเงินเข้มเหมือนหน้า Home */
.explore-page {
    background: linear-gradient(135deg, #1e5799 0%, #2989d8 50%, #207cca 100%) !important;
    min-height: 100vh;
    width: 100%;
}

.explore-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 40px 20px;
}

.explore-layout {
    display: grid;
    grid-template-columns: 320px 1fr;
    /* แยกฝั่ง Sidebar และ Content */
    gap: 30px;
}

/* 📌 Sidebar Styling */
.sidebar {
    position: sticky;
    top: 100px;
    height: fit-content;
}

.filter-card {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    padding: 25px;
    border-radius: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.filter-header h3 {
    font-size: 1.3rem;
    font-weight: 800;
    color: #1e293b;
    margin: 0;
}

.filter-header p {
    font-size: 0.85rem;
    color: #64748b;
    margin-bottom: 20px;
}

.filter-group {
    margin-bottom: 20px;
}

.filter-group label {
    display: block;
    font-weight: 700;
    font-size: 0.85rem;
    color: #475569;
    margin-bottom: 8px;
}

.input-with-icon {
    position: relative;
    display: flex;
    align-items: center;
}

.input-with-icon i {
    position: absolute;
    left: 15px;
    color: #94a3b8;
}

.input-with-icon input {
    width: 100%;
    padding: 12px 15px 12px 40px;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    background: #f8fafc;
}

.category-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.cat-btn {
    padding: 8px 14px;
    border-radius: 50px;
    border: 1px solid #e2e8f0;
    background: white;
    color: #64748b;
    font-weight: 600;
    font-size: 0.8rem;
    cursor: pointer;
}

.cat-btn.active {
    background: #3498db;
    color: white;
    border-color: #3498db;
}

.btn-clear {
    width: 100%;
    padding: 12px;
    background: none;
    border: 1px dashed #cbd5e1;
    border-radius: 12px;
    color: #94a3b8;
    font-weight: 700;
    cursor: pointer;
}

/* 📌 Content & Grid Styling - ปรับให้โชว์หลายคอลัมน์เหมือนเดิม */
.results-info h2 {
    font-size: 1.8rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 30px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.count-badge {
    color: #ffd700;
}

.places-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    /* ทำให้โชว์ 3 อันในแถวเดียวถ้าจอกว้าง */
    gap: 25px;
}

.modern-card {
    background: white;
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    transition: 0.3s ease;
    cursor: pointer;
}

.modern-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
}

.card-media {
    position: relative;
    height: 200px;
    background: #eee;
}

.card-media img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.category-tag {
    position: absolute;
    top: 12px;
    left: 12px;
    background: #3498db;
    color: white;
    padding: 4px 12px;
    border-radius: 50px;
    font-size: 0.7rem;
    font-weight: 800;
}

.card-details {
    padding: 20px;
}

.card-details h3 {
    margin: 0 0 8px;
    font-size: 1.15rem;
    color: #1e293b;
}

.description {
    color: #64748b;
    font-size: 0.85rem;
    line-height: 1.5;
    margin-bottom: 15px;
    height: 40px;
    overflow: hidden;
}

.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #f1f5f9;
    padding-top: 15px;
}

.rating {
    color: #f59e0b;
    font-weight: 800;
    font-size: 0.9rem;
}

.view-link {
    color: #3498db;
    font-weight: 700;
    font-size: 0.85rem;
}

/* 📌 States */
.loading-state,
.empty-state {
    text-align: center;
    padding: 100px 0;
    color: white;
}

.spinner {
    border: 4px solid rgba(255, 255, 255, 0.3);
    border-top: 4px solid #fff;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}
</style>