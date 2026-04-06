<template>
    <div class="explore-page">
        <Navbar />

        <div class="explore-container">
            <div class="explore-layout">
                <aside class="sidebar">
                    <div class="filter-card">
                        <div class="filter-header">
                            <h3>Smart Search</h3>
                            <p>Filter places by your preference</p>
                        </div>

                        <div class="filter-group">
                            <label>Place Name</label>
                            <div class="input-with-icon">
                                <i class="fas fa-search"></i>
                                <input v-model="searchQuery" type="text" placeholder="e.g. Temple, Cave, Restaurant..." />
                            </div>
                        </div>

                        <div class="filter-group">
                            <label>Category</label>
                            <div class="category-grid">
                                <button :class="['cat-btn', { active: !selectedCategory }]"
                                    @click="filterByCategory(null)">
                                    All
                                </button>
                                <button v-for="cat in categories" :key="cat.id"
                                    :class="['cat-btn', { active: selectedCategory === cat.id }]"
                                    @click="filterByCategory(cat.id)">
                                    {{ cat.name }}
                                </button>
                            </div>
                        </div>

                        <button @click="resetFilters" class="btn-clear">
                            Clear Filters
                        </button>
                    </div>
                </aside>

                <main class="content-area">
                    <div class="results-info">
                        <h2>Search Results <span class="count-badge">{{ filteredPlaces.length }} places</span></h2>
                    </div>

                    <div v-if="loading" class="loading-state">
                        <div class="spinner"></div>
                        <p>Finding places...</p>
                    </div>

                    <div v-else class="places-grid">
                        <div v-for="place in filteredPlaces" :key="place.id" class="modern-card"
                            @click="goToDetail(place.id)">
                            <div class="card-media">
                                <img :src="getCoverImage(place)" :alt="place.name" />
                                
                                <div class="category-tag">{{ getCategoryName(place.category_id) }}</div>
                                <button v-if="user && user.role !== 'admin'" :class="['btn-heart', { active: isFavorite(place.id) }]" 
                                    @click.stop="toggleHeart(place.id)">
                                    <i class="fas fa-heart"></i>
                                </button>
                            </div>

                            <div class="card-details">
                                <h3>{{ place.name }}</h3>
                                <p class="description">{{ place.description }}</p>

                                <div class="card-footer">
                                    <div class="rating">
                                        <i class="fas fa-star"></i>
                                        <span>{{ place.rating_avg || '0.0' }}</span>
                                    </div>
                                <span class="view-link">View Details <i class="fas fa-arrow-right"></i></span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div v-if="!loading && filteredPlaces.length === 0" class="empty-state">
                        <i class="fas fa-map-marked-alt"></i>
                        <p>No places found. Try a different search term.</p>
                    </div>
                </main>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { placeRepository } from '@/repositories/placeRepository'
import { categoryRepository } from '@/repositories/categoryRepository'
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'

import { favoriteRepository } from '@/repositories/favoriteRepository'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { user } = useAuth()
const places = ref([])
const categories = ref([])
const loading = ref(true)
const searchQuery = ref('')
const selectedCategory = ref(null)
const favoriteIds = ref([])

// 📷 เพิ่มฟังก์ชันจัดการปกรูปภาพ
const getCoverImage = (place) => {
    // กำหนด SVG กรณีไม่มีรูป
    const noImageUrl = 'data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22400%22%20height%3D%22300%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20fill%3D%22%23e2e8f0%22%2F%3E%3Ctext%20x%3D%2250%25%22%20y%3D%2250%25%22%20fill%3D%22%2364748b%22%20font-family%3D%22sans-serif%22%20font-size%3D%2220%22%20text-anchor%3D%22middle%22%20dy%3D%22.3em%22%3ENo%20Image%3C%2Ftext%3E%3C%2Fsvg%3E';

    let targetUrl = null;

    // 1. ถ้ามีหลายรูปใน array (ดึงรูปแรกมาโชว์)
    if (place.images && Array.isArray(place.images) && place.images.length > 0) {
        targetUrl = place.images[0].image_url || place.images[0].url || place.images[0];
    } 
    // 2. ถ้ามีรูปเดียว
    else if (place.image_url) {
        targetUrl = place.image_url;
    }

    if (!targetUrl) return noImageUrl;

    // ดักจับ JSON Array ซ้อน String (แบบเดียวกับที่แก้ในหน้า Detail)
    if (typeof targetUrl === 'string' && targetUrl.trim().startsWith('[')) {
        try {
            const parsed = JSON.parse(targetUrl);
            if (Array.isArray(parsed) && parsed.length > 0) {
                targetUrl = parsed[0];
            }
        } catch (e) {
            targetUrl = targetUrl.replace(/^\["?|"?\]$/g, '').replace(/\\"/g, '');
        }
    }

    // จัดการ URL ให้สมบูรณ์
    if (targetUrl.startsWith('http://') || targetUrl.startsWith('https://') || targetUrl.startsWith('data:')) {
        return targetUrl;
    }

    return `http://localhost:8000${targetUrl.startsWith('/') ? '' : '/'}${targetUrl}`;
}

const fetchData = async () => {
    loading.value = true
    try {
        const [resPlaces, resCats] = await Promise.all([
            placeRepository.getAll(),
            categoryRepository.getAll()
        ])
        places.value = resPlaces.data
        categories.value = resCats.data

        if (user.value && user.value.role !== 'admin') {
            const favRes = await favoriteRepository.getUserFavorites(user.value.id)
            favoriteIds.value = favRes.data.map(f => f.place_id)
        }
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
    return cat ? cat.name : 'General'
}

const goToDetail = (id) => {
    const userData = localStorage.getItem('user')
    if (!userData) {
        router.push('/login')
    } else {
        router.push(`/places/${id}`)
    }
}

const isFavorite = (id) => favoriteIds.value.includes(id)

const toggleHeart = async (placeId) => {
    try {
        const res = await favoriteRepository.toggleFavorite(user.value.id, placeId)
        if (res.data.status === 'added') {
            favoriteIds.value.push(placeId)
        } else {
            favoriteIds.value = favoriteIds.value.filter(id => id !== placeId)
        }
    } catch (err) {
        console.error("Failed to toggle favorite:", err)
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
    font-size: 1.15rem;
    font-weight: 800;
    color: #1e293b;
    margin: 0;
}

.filter-header p {
    font-size: 0.82rem;
    color: #64748b;
    margin-bottom: 18px;
    margin-top: 4px;
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
    grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
    gap: 24px;
}

.modern-card {
    background: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    cursor: pointer;
    border: 1px solid rgba(255,255,255,0.8);
}

.modern-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.18);
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

.btn-heart {
    position: absolute;
    top: 12px;
    right: 12px;
    background: rgba(255,255,255,0.9);
    border: none;
    border-radius: 50%;
    width: 35px;
    height: 35px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    transition: 0.2s;
    color: #94a3b8;
    z-index: 10;
}

.btn-heart.active {
    color: #ef4444;
}

.btn-heart:hover {
    transform: scale(1.1);
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
    line-height: 1.55;
    margin-bottom: 14px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    min-height: 2.7em;
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
    font-size: 0.82rem;
    display: flex;
    align-items: center;
    gap: 4px;
    transition: 0.2s;
}

.modern-card:hover .view-link {
    color: #2980b9;
    gap: 7px;
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