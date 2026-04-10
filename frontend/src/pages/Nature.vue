<template>
    <div class="nature-page">
        <Navbar />

        <div class="nature-header">
            <div class="header-container">
                <div class="header-content-flex">
                    <div class="text-zone">
                        <h1>Nature & Parks in Savannakhet</h1>
                        <p class="subtitle">Discover serene landscapes, lush forests, and outdoor adventures.</p>
                    </div>
                    <div class="icon-zone">
                        <i class="fas fa-tree"></i>
                    </div>
                </div>

                <div class="quick-filters">
                    <button class="filter-pill" @click="toggleCategory('waterfall')"
                        :class="{ active: selectedCategories.includes('waterfall') }">
                        <i class="fas fa-water"></i> Waterfalls
                    </button>
                    <button class="filter-pill" @click="toggleCategory('cave')"
                        :class="{ active: selectedCategories.includes('cave') }">
                        <i class="fas fa-mountain"></i> Caves
                    </button>
                    <button class="filter-pill" @click="toggleCategory('forest')"
                        :class="{ active: selectedCategories.includes('forest') }">
                        <i class="fas fa-leaf"></i> Forests
                    </button>
                </div>
            </div>
        </div>

        <div class="main-layout">
            <aside class="filter-sidebar">
                <div class="map-preview" @click="openGeneralMap">
                    <img src="https://images.unsplash.com/photo-1524661135-423995f22d0b?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"
                        alt="Map View" />
                    <button class="btn-view-map"><i class="fas fa-map"></i> View on map</button>
                </div>

                <div class="filter-group">
                    <h3>Category</h3>
                    <label class="filter-checkbox">
                        <input type="checkbox" value="nature" v-model="selectedCategories" />
                        <span>Nature & Parks</span>
                    </label>
                    <label class="filter-checkbox">
                        <input type="checkbox" value="waterfall" v-model="selectedCategories" />
                        <span>Waterfalls</span>
                    </label>
                    <label class="filter-checkbox">
                        <input type="checkbox" value="cave" v-model="selectedCategories" />
                        <span>Caves</span>
                    </label>
                    <label class="filter-checkbox">
                        <input type="checkbox" value="forest" v-model="selectedCategories" />
                        <span>Forests</span>
                    </label>
                </div>

                <div class="filter-divider"></div>

                <div class="filter-group">
                    <h3>Good for</h3>
                    <label class="filter-checkbox"><input type="checkbox" /> <span>Adventure</span></label>
                    <label class="filter-checkbox"><input type="checkbox" /> <span>Families</span></label>
                    <label class="filter-checkbox"><input type="checkbox" /> <span>Relaxing</span></label>
                </div>
            </aside>

            <main class="nature-list-area">
                <div class="list-header">
                    <h2>{{ filteredNature.length }} nature spots found</h2>
                    <div class="sort-by">
                        <span>Sort by:</span>
                        <select>
                            <option>Traveler Ranked</option>
                            <option>Distance</option>
                        </select>
                    </div>
                </div>

                <div v-if="loading" class="loading-box">
                    <div class="spinner"></div>
                    <p>Loading nature's beauty...</p>
                </div>

                <div v-else-if="filteredNature.length === 0" class="empty-box">
                    <i class="fas fa-seedling"></i>
                    <p>No nature spots found matching your filter.</p>
                    <button @click="selectedCategories = []" class="btn-details" style="margin-top: 15px;">Clear
                        Filters</button>
                </div>

                <div v-else>
                    <div class="nature-card" v-for="(place, index) in filteredNature" :key="place.id"
                        @click="goToDetail(place.id)">

                        <div class="card-img-wrapper">
                            <img :src="getCoverImage(place)" :alt="place.name" @error="handleImgError" />
                            <button class="btn-heart" :class="{ active: isFavorite(place.id) }"
                                @click.stop="toggleHeart(place.id)">
                                <i class="fas fa-heart"></i>
                            </button>
                        </div>

                        <div class="card-info">
                            <h3 class="place-name">{{ index + 1 }}. {{ place.name }}</h3>

                            <div class="rating-row">
                                <span class="bubbles">
                                    <i v-for="s in 5" :key="s"
                                        :class="[(place.rating_avg || 0) >= s ? 'fas' : 'far', 'fa-circle']"></i>
                                </span>
                                <span class="review-count">{{ place.rating_avg || '0.0' }} Rating</span>
                            </div>

                            <div class="category-row">
                                <span class="cat-label"><i class="fas fa-leaf"></i> {{
                                    getCategoryName(place.category_id) }}</span>
                                <span class="divider">•</span>
                                <span>Savannakhet Province</span>
                            </div>

                            <div class="description-snippet">
                                <p>{{ place.description || `Explore the untouched beauty of this natural wonder in
                                    Savannakhet.` }}</p>
                            </div>

                            <div class="card-footer">
                                <button class="btn-contact" @click.stop="handleContact(place)">
                                    <i class="fas fa-phone-alt"></i> Contact
                                </button>
                                <button class="btn-details">View Details</button>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { placeRepository } from '@/repositories/placeRepository'
import { categoryRepository } from '@/repositories/categoryRepository'
import { favoriteRepository } from '@/repositories/favoriteRepository'
import { useAuth } from '@/composables/useAuth'
import Navbar from '../components/Navbar.vue'

const router = useRouter()
const { user } = useAuth()
const places = ref([])
const categories = ref([])
const favoriteIds = ref([])
const loading = ref(true)
const selectedCategories = ref([])

const toggleCategory = (cat) => {
    if (selectedCategories.value.includes(cat)) {
        selectedCategories.value = selectedCategories.value.filter(c => c !== cat)
    } else {
        selectedCategories.value.push(cat)
    }
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
        loading.value = false

        if (user.value) {
            favoriteRepository.getUserFavorites(user.value.id)
                .then(favRes => {
                    favoriteIds.value = favRes.data.map(f => f.place_id)
                })
        }
    } catch (err) {
        console.error("Error fetching data:", err)
        loading.value = false
    }
}

const filteredNature = computed(() => {
    let spots = places.value.filter(p => {
        const cat = categories.value.find(c => c.id == p.category_id)
        if (!cat) return false
        const name = cat.name.toLowerCase()
        return name.includes('nature') || name.includes('park') ||
            name.includes('waterfall') || name.includes('cave') ||
            name.includes('forest') || name.includes('ธรรมชาติ')
    })

    if (spots.length === 0 && places.value.length > 0) {
        spots = places.value;
    }

    if (selectedCategories.value.length > 0) {
        return spots.filter(p => {
            const cat = categories.value.find(c => c.id == p.category_id)
            if (!cat) return false
            const name = cat.name.toLowerCase()
            return selectedCategories.value.some(sel => name.includes(sel))
        })
    }
    return spots
})

// 🛠️ แก้ไข BUG รูปภาพไม่ขึ้น
const getCoverImage = (place) => {
    let url = place.image_url;
    if (!url || url === '[]' || url === '') return 'https://via.placeholder.com/600x400?text=No+Image';

    // 1. ถ้าเป็น JSON Array ["url"] ให้แกะออกมา
    if (typeof url === 'string' && url.startsWith('[')) {
        try {
            const arr = JSON.parse(url);
            if (Array.isArray(arr) && arr.length > 0) {
                url = arr[0];
            }
        } catch (e) {
            url = url.replace(/[\[\]"]/g, ''); // ถ้า Parse พัง ให้ล้างเครื่องหมายทิ้ง
        }
    }

    // 2. ถ้าเป็น Base64 (data:image...) ให้ส่งคืนไปตรงๆ เลย
    if (url.startsWith('data:')) {
        return url;
    }

    // 3. ถ้าเป็น URL สมบูรณ์ (http...) ให้ส่งคืนไปเลย
    if (url.startsWith('http')) {
        return url;
    }

    // 4. ถ้าเป็น Path ในเครื่อง ให้เติม localhost:8000
    const cleanPath = url.startsWith('/') ? url.slice(1) : url;
    return `http://localhost:8000/${cleanPath}`;
}

const handleImgError = (e) => {
    e.target.src = 'https://via.placeholder.com/600x400?text=Image+Not+Found';
}

const getCategoryName = (id) => {
    const cat = categories.value.find(c => c.id == id)
    return cat ? cat.name : 'Nature'
}

const isFavorite = (id) => favoriteIds.value.includes(id)

const toggleHeart = async (placeId) => {
    if (!user.value) return router.push('/login')
    try {
        const res = await favoriteRepository.toggleFavorite(user.value.id, placeId)
        if (res.data.status === 'added') {
            favoriteIds.value.push(placeId)
        } else {
            favoriteIds.value = favoriteIds.value.filter(id => id !== placeId)
        }
    } catch (err) { console.error(err) }
}

const goToDetail = (id) => router.push(`/places/${id}`)
const openGeneralMap = () => window.open('https://www.google.com/maps', '_blank')
const handleContact = (place) => alert(`Contact for ${place.name}`)

onMounted(fetchData)
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

.nature-page {
    background-color: #f7f9fa;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    color: #1e293b;
}

.nature-header {
    background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 100%);
    padding: 40px 20px;
    border-bottom: 1px solid #c8e6c9;
}

.header-container {
    max-width: 1200px;
    margin: 0 auto;
}

.header-content-flex {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.header-container h1 {
    font-size: 2.5rem;
    font-weight: 900;
    margin: 0 0 5px;
    color: #1b5e20;
    letter-spacing: -1px;
}

.subtitle {
    color: #388e3c;
    font-size: 1.1rem;
    margin: 0;
    font-weight: 500;
}

.icon-zone {
    font-size: 3.5rem;
    color: #81c784;
    opacity: 0.7;
}

.quick-filters {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.filter-pill {
    background: white;
    border: 1px solid #a5d6a7;
    padding: 10px 22px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.9rem;
    color: #1b5e20;
    cursor: pointer;
    transition: 0.2s;
    display: flex;
    align-items: center;
    gap: 8px;
}

.filter-pill:hover,
.filter-pill.active {
    border-color: #2e7d32;
    background: #e8f5e9;
    transform: translateY(-2px);
}

.filter-pill i {
    color: #66bb6a;
    font-size: 1.1rem;
}

.main-layout {
    max-width: 1200px;
    margin: 30px auto;
    padding: 0 20px;
    display: grid;
    grid-template-columns: 260px 1fr;
    gap: 30px;
}

.map-preview {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    height: 130px;
    border: 1px solid #cbd5e1;
    cursor: pointer;
    margin-bottom: 25px;
}

.map-preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.btn-view-map {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    border: 1px solid #000;
    padding: 10px 18px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    pointer-events: none;
}

.filter-group h3 {
    font-size: 1.05rem;
    font-weight: 800;
    margin: 0 0 15px;
    color: #000;
}

.filter-checkbox {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
    cursor: pointer;
    font-size: 0.95rem;
    color: #475569;
}

.filter-checkbox input[type="checkbox"] {
    width: 19px;
    height: 19px;
    cursor: pointer;
    accent-color: #2e7d32;
}

.filter-divider {
    height: 1px;
    background: #e0e0e0;
    margin: 25px 0;
}

.list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.list-header h2 {
    font-size: 1.5rem;
    font-weight: 800;
    margin: 0;
    color: #000;
}

.sort-by {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.9rem;
    font-weight: 600;
}

.sort-by select {
    padding: 9px 15px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-weight: 600;
    outline: none;
    cursor: pointer;
    background: white;
}

.nature-card {
    display: flex;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 25px;
    transition: 0.3s;
    cursor: pointer;
    height: 260px;
}

.nature-card:hover {
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    transform: translateY(-5px);
}

.card-img-wrapper {
    width: 320px;
    position: relative;
    flex-shrink: 0;
}

.card-img-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.btn-heart {
    position: absolute;
    top: 15px;
    right: 15px;
    background: rgba(255, 255, 255, 0.9);
    border: none;
    width: 38px;
    height: 38px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: #94a3b8;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    transition: 0.2s;
    z-index: 2;
}

.btn-heart.active {
    color: #ef4444;
}

.btn-heart:hover {
    transform: scale(1.1);
    background: white;
}

.card-info {
    flex: 1;
    padding: 25px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.place-name {
    font-size: 1.5rem;
    font-weight: 800;
    color: #000;
    margin: 0 0 8px;
    transition: 0.2s;
}

.nature-card:hover .place-name {
    color: #2e7d32;
    text-decoration: underline;
}

.rating-row {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
}

.bubbles i {
    color: #00aa6c;
    font-size: 0.9rem;
    margin-right: 3px;
}

.review-count {
    font-size: 0.9rem;
    color: #475569;
    margin-left: 10px;
    font-weight: 600;
    text-decoration: underline;
}

.category-row {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.9rem;
    color: #64748b;
    margin-bottom: 15px;
}

.cat-label {
    font-weight: 600;
    color: #388e3c;
    background: #e8f5e9;
    padding: 4px 10px;
    border-radius: 4px;
}

.cat-label i {
    margin-right: 5px;
}

.divider {
    color: #cbd5e1;
}

.description-snippet {
    font-size: 0.9rem;
    color: #475569;
    line-height: 1.6;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin-bottom: 15px;
}

.card-footer {
    margin-top: auto;
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}

.btn-contact {
    background: white;
    color: #1e293b;
    border: 1px solid #cbd5e1;
    padding: 10px 20px;
    border-radius: 25px;
    font-weight: 700;
    font-size: 0.9rem;
    cursor: pointer;
    transition: 0.2s;
    display: flex;
    align-items: center;
    gap: 6px;
}

.btn-contact:hover {
    border-color: #000;
    background: #f8fafc;
}

.btn-contact i {
    font-size: 0.85rem;
}

.btn-details {
    background: #000;
    color: white;
    border: none;
    padding: 10px 24px;
    border-radius: 25px;
    font-weight: 700;
    font-size: 0.9rem;
    cursor: pointer;
    transition: 0.2s;
}

.btn-details:hover {
    background: #333;
}

.loading-box,
.empty-box {
    text-align: center;
    padding: 80px;
    background: white;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
}

.spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #2e7d32;
    border-radius: 50%;
    width: 45px;
    height: 45px;
    animation: spin 1s linear infinite;
    margin: 0 auto 25px;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.empty-box i {
    font-size: 3rem;
    color: #a5d6a7;
    margin-bottom: 20px;
}

.empty-box p {
    color: #64748b;
    font-size: 1.1rem;
}

@media (max-width: 1100px) {
    .nature-card {
        height: auto;
        flex-direction: column;
    }

    .card-img-wrapper {
        width: 100%;
        height: 240px;
    }
}

@media (max-width: 992px) {
    .main-layout {
        grid-template-columns: 1fr;
    }

    .filter-sidebar {
        display: none;
    }

    .header-container h1 {
        font-size: 2rem;
    }
}
</style>