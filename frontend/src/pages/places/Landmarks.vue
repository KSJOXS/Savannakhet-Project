<template>
    <div class="landmarks-page">
        <Navbar />

        <!-- Hero Header -->
        <div class="landmarks-header">
            <div class="header-container">
                <div class="header-content-flex">
                    <div class="text-zone">
                        <div class="header-badge">
                            <i class="fas fa-gopuram"></i>
                            <span>{{ t('landmarks.badge') }}</span>
                        </div>
                        <h1>{{ t('landmarks.title') }}</h1>
                        <p class="subtitle">{{ t('landmarks.subtitle') }}</p>
                        <div class="header-stats">
                            <div class="stat-item">
                                <span class="stat-num">{{ filteredLandmarks.length }}</span>
                                <span class="stat-label">{{ t('landmarks.sitesLabel') }}</span>
                            </div>
                            <div class="stat-divider"></div>
                            <div class="stat-item">
                                <span class="stat-num">{{ landmarkCategories.length }}</span>
                                <span class="stat-label">{{ t('landmarks.categoriesLabel') }}</span>
                            </div>
                        </div>
                    </div>
                    <div class="icon-zone">
                        <i class="fas fa-landmark"></i>
                    </div>
                </div>

                <div class="quick-filters">
                    <button
                        class="filter-pill"
                        :class="{ active: selectedCategories.length === 0 }"
                        @click="selectedCategories = []"
                    >
                        <i class="fas fa-th-large"></i> {{ t('landmarks.all') }}
                    </button>
                    <button
                        v-for="cat in landmarkCategories"
                        :key="cat.id"
                        class="filter-pill"
                        @click="toggleCategory(cat.name.toLowerCase())"
                        :class="{ active: selectedCategories.includes(cat.name.toLowerCase()) }"
                    >
                        <i :class="getIconForLandmark(cat.name)"></i> {{ cat.name }}
                    </button>
                </div>
            </div>
        </div>

        <!-- Main Layout -->
        <div class="main-layout">
            <!-- Sidebar -->
            <aside class="filter-sidebar">
                <div class="map-preview" @click="showMapModal = true">
                    <img
                        src="https://images.unsplash.com/photo-1524661135-423995f22d0b?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"
                        alt="Map View"
                    />
                    <button class="btn-view-map">
                        <i class="fas fa-map-marked-alt"></i> {{ t('landmarks.viewOnMap') }}
                    </button>
                </div>

                <div class="filter-group">
                    <h3>{{ t('landmarks.filterCategory') }}</h3>
                    <label v-for="cat in landmarkCategories" :key="'sidebar-' + cat.id" class="filter-checkbox">
                        <input type="checkbox" :value="cat.name.toLowerCase()" v-model="selectedCategories" />
                        <span>{{ cat.name }}</span>
                    </label>
                </div>

                <div class="filter-divider"></div>

                <div class="filter-group">
                    <h3>{{ t('landmarks.goodFor') }}</h3>
                    <label class="filter-checkbox"><input type="checkbox" /> <span>{{ t('landmarks.historyLovers') }}</span></label>
                    <label class="filter-checkbox"><input type="checkbox" /> <span>{{ t('landmarks.families') }}</span></label>
                    <label class="filter-checkbox"><input type="checkbox" /> <span>{{ t('landmarks.photography') }}</span></label>
                    <label class="filter-checkbox"><input type="checkbox" /> <span>{{ t('landmarks.spiritual') }}</span></label>
                </div>
            </aside>

            <main class="landmarks-list-area">
                <div class="list-header">
                    <h2>
                        <span class="count-badge">{{ filteredLandmarks.length }}</span>
                        {{ filteredLandmarks.length !== 1 ? t('landmarks.foundLabelPlural') : t('landmarks.foundLabel') }} {{ t('landmarks.found') }}
                    </h2>
                    <div class="sort-by">
                        <span>{{ t('landmarks.sortBy') }}</span>
                        <select v-model="sortBy">
                            <option value="default">{{ t('landmarks.sortDefault') }}</option>
                            <option value="name">{{ t('landmarks.sortName') }}</option>
                            <option value="rating">{{ t('landmarks.sortRating') }}</option>
                        </select>
                    </div>
                </div>

                <!-- Loading -->
                <div v-if="loading" class="loading-box">
                    <div class="spinner"></div>
                    <p>{{ t('landmarks.loading') }}</p>
                </div>

                <!-- Empty -->
                <div v-else-if="filteredLandmarks.length === 0" class="empty-box">
                    <i class="fas fa-gopuram"></i>
                    <p>{{ t('landmarks.noResults') }}</p>
                    <button @click="selectedCategories = []" class="btn-details" style="margin-top: 15px;">
                        {{ t('landmarks.clearFilters') }}
                    </button>
                </div>

                <!-- Cards Grid -->
                <div v-else class="landmarks-grid">
                    <div
                        class="landmark-card"
                        v-for="(place, index) in sortedLandmarks"
                        :key="place.id"
                        @click="goToDetail(place.id)"
                    >
                        <div class="card-img-wrapper">
                            <img :src="getCoverImage(place)" :alt="place.name" @error="handleImgError" />
                            <div class="card-rank-badge">#{{ index + 1 }}</div>
                            <button
                                class="btn-heart"
                                :class="{ active: isFavorite(place.id) }"
                                @click.stop="toggleHeart(place.id)"
                            >
                                <i class="fas fa-heart"></i>
                            </button>
                        </div>

                        <div class="card-info">
                            <span class="category-tag">{{ getCategoryName(place.category_id) }}</span>
                            <h3 class="place-name">{{ place.name }}</h3>
                            <div class="rating-row">
                                <span class="bubbles">
                                    <i v-for="s in 5" :key="s" :class="[(place.rating_avg || 0) >= s ? 'fas' : 'far', 'fa-circle']"></i>
                                </span>
                                <span class="review-count">{{ place.rating_avg || '0.0' }}</span>
                            </div>
                            <div class="description-snippet">
                                <p>{{ place.description || t('landmarks.defaultDesc') }}</p>
                            </div>
                            <div class="card-footer">
                                <span class="location-tag">✨ {{ t('landmarks.verified') }}</span>
                                <span class="btn-details">{{ t('landmarks.openGuide') }} →</span>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
        
        <SectionDivider icon="fas fa-monument" />

        <MapOverlay
            :is-open="showMapModal"
            :places="places"
            :categories="categories"
            initial-filter="landmark"
            title="Landmarks & Heritage"
            @close="showMapModal = false"
        />

        <RecentlyViewed />
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { placeRepository } from '@/repositories/placeRepository'
import { categoryRepository } from '@/repositories/categoryRepository'
import { favoriteRepository } from '@/repositories/favoriteRepository'
import { useAuth } from '@/composables/useAuth'
import { useI18n } from '@/composables/useI18n'
import Navbar from '@/components/Navbar.vue'
import MapOverlay from '@/components/MapOverlay.vue'
import SectionDivider from '@/components/SectionDivider.vue'
import RecentlyViewed from '@/components/RecentlyViewed.vue'

const router = useRouter()
const { user } = useAuth()
const { t } = useI18n()
const places = ref([])
const categories = ref([])
const favoriteIds = ref([])
const loading = ref(true)
const selectedCategories = ref([])
const showMapModal = ref(false)
const sortBy = ref('default')

// --- Filter / Category Logic ---
const toggleCategory = (cat) => {
    cat = cat.toLowerCase()
    if (selectedCategories.value.includes(cat)) {
        selectedCategories.value = selectedCategories.value.filter(c => c !== cat)
    } else {
        selectedCategories.value.push(cat)
    }
}

const landmarkCategories = computed(() => {
    return categories.value.filter(c => c.parent_type === 'landmark')
})

const getIconForLandmark = (name) => {
    if (!name) return 'fas fa-landmark'
    name = name.toLowerCase()
    if (name.includes('temple') || name.includes('wat') || name.includes('pagoda')) return 'fas fa-place-of-worship'
    if (name.includes('museum')) return 'fas fa-university'
    if (name.includes('monument') || name.includes('statue')) return 'fas fa-monument'
    if (name.includes('colonial') || name.includes('church')) return 'fas fa-church'
    if (name.includes('market') || name.includes('street')) return 'fas fa-store'
    if (name.includes('palace') || name.includes('house')) return 'fas fa-home'
    return 'fas fa-landmark'
}

// --- Fetch Data ---
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
        console.error('Error fetching data:', err)
        loading.value = false
    }
}

// --- Filtered & Sorted ---
const filteredLandmarks = computed(() => {
    let spots = places.value.filter(p => {
        const cat = categories.value.find(c => c.id == p.category_id)
        if (!cat) return false
        return cat.parent_type === 'landmark'
    })

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

const sortedLandmarks = computed(() => {
    const list = [...filteredLandmarks.value]
    if (sortBy.value === 'name') return list.sort((a, b) => a.name.localeCompare(b.name))
    if (sortBy.value === 'rating') return list.sort((a, b) => (b.rating_avg || 0) - (a.rating_avg || 0))
    return list
})

// --- Image Carousel ---
const currentImageIndices = ref({})

const getPlaceImagesArray = (place) => {
    const noImageUrl = 'data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22400%22%20height%3D%22300%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20fill%3D%22%23e2e8f0%22%2F%3E%3Ctext%20x%3D%2250%25%22%20y%3D%2250%25%22%20fill%3D%22%2364748b%22%20font-family%3D%22sans-serif%22%20font-size%3D%2220%22%20text-anchor%3D%22middle%22%20dy%3D%22.3em%22%3ENo%20Image%3C%2Ftext%3E%3C%2Fsvg%3E'
    let urls = []

    if (place.images && Array.isArray(place.images) && place.images.length > 0) {
        urls = place.images.map(img => img.image_url || img.url || img)
    } else if (place.image_url) {
        if (typeof place.image_url === 'string' && place.image_url.trim().startsWith('[')) {
            try { urls = JSON.parse(place.image_url) } catch (e) { urls = [place.image_url.replace(/^\[\"?|\"?\]$/g, '').replace(/\\"/g, '')] }
        } else {
            urls = [place.image_url]
        }
    }

    if (urls.length === 0) return [noImageUrl]

    return urls.map(url => {
        if (!url) return noImageUrl
        if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) return url
        return `http://localhost:8000${url.startsWith('/') ? '' : '/'}${url}`
    })
}

const getCoverImage = (place) => {
    const images = getPlaceImagesArray(place)
    const index = currentImageIndices.value[place.id] || 0
    return images[index] || images[0]
}

const nextImage = (placeId, place) => {
    const images = getPlaceImagesArray(place)
    if (images.length <= 1) return
    const currentIdx = currentImageIndices.value[placeId] || 0
    currentImageIndices.value[placeId] = (currentIdx + 1) % images.length
}

const prevImage = (placeId, place) => {
    const images = getPlaceImagesArray(place)
    if (images.length <= 1) return
    const currentIdx = currentImageIndices.value[placeId] || 0
    currentImageIndices.value[placeId] = currentIdx === 0 ? images.length - 1 : currentIdx - 1
}

const handleImgError = (e) => {
    e.target.src = 'https://via.placeholder.com/600x400?text=Image+Not+Found'
}

const getCategoryName = (id) => {
    const cat = categories.value.find(c => c.id == id)
    return cat ? cat.name : 'Landmark'
}

// --- Favorites ---
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
const handleContact = (place) => alert(`Contact for ${place.name}`)

onMounted(fetchData)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:wght@700;800;900&display=swap');

.landmarks-page {
    background-color: #faf9f6;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    color: #1e293b;
}

/* ===== HERO HEADER ===== */
.landmarks-header {
    background: linear-gradient(135deg, #ede9fe 0%, #fdf4ff 50%, #ffffff 100%);
    padding: 48px 20px 36px;
    border-bottom: 1px solid #ddd6fe;
    position: relative;
    overflow: hidden;
}

.landmarks-header::before {
    content: '';
    position: absolute;
    top: -60px;
    right: -60px;
    width: 300px;
    height: 300px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(139, 92, 246, 0.08) 0%, transparent 70%);
    pointer-events: none;
}

.header-container {
    max-width: 1200px;
    margin: 0 auto;
}

.header-content-flex {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
}

.header-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(139, 92, 246, 0.1);
    border: 1px solid rgba(139, 92, 246, 0.25);
    color: #7c3aed;
    padding: 5px 14px;
    border-radius: 50px;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
}

.header-badge i {
    font-size: 0.85rem;
}

.header-container h1 {
    font-size: 2.6rem;
    font-weight: 900;
    margin: 0 0 8px;
    color: #1e1b4b;
    letter-spacing: -1.5px;
    line-height: 1.1;
}

.subtitle {
    color: #5b21b6;
    font-size: 1.05rem;
    margin: 0 0 20px;
    font-weight: 500;
    max-width: 480px;
    line-height: 1.6;
}

.header-stats {
    display: flex;
    align-items: center;
    gap: 20px;
}

.stat-item {
    text-align: center;
}

.stat-num {
    display: block;
    font-size: 1.6rem;
    font-weight: 900;
    color: #7c3aed;
    line-height: 1;
}

.stat-label {
    font-size: 0.78rem;
    color: #7c3aed;
    font-weight: 600;
    opacity: 0.7;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stat-divider {
    width: 1px;
    height: 30px;
    background: rgba(139, 92, 246, 0.3);
}

.icon-zone {
    font-size: 5rem;
    color: #a78bfa;
    opacity: 0.5;
    line-height: 1;
}

/* Quick Filters */
.quick-filters {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.filter-pill {
    background: white;
    border: 1.5px solid #ddd6fe;
    padding: 9px 20px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.88rem;
    color: #4c1d95;
    cursor: pointer;
    transition: 0.2s;
    display: flex;
    align-items: center;
    gap: 7px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

.filter-pill:hover {
    border-color: #7c3aed;
    background: #f5f3ff;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15);
}

.filter-pill.active {
    border-color: #7c3aed;
    background: #7c3aed;
    color: white;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
    transform: translateY(-2px);
}

.filter-pill i {
    font-size: 0.9rem;
}

/* ===== MAIN LAYOUT ===== */
.main-layout {
    max-width: 1200px;
    margin: 30px auto;
    padding: 0 20px;
    display: grid;
    grid-template-columns: 260px 1fr;
    gap: 30px;
}

/* ===== SIDEBAR ===== */
.map-preview {
    position: relative;
    border-radius: 14px;
    overflow: hidden;
    height: 130px;
    border: 1px solid #ddd6fe;
    cursor: pointer;
    margin-bottom: 25px;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.1);
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
    border: 1.5px solid #7c3aed;
    color: #7c3aed;
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
    font-size: 1rem;
    font-weight: 800;
    margin: 0 0 14px;
    color: #1e1b4b;
}

.filter-checkbox {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 11px;
    cursor: pointer;
    font-size: 0.9rem;
    color: #475569;
    transition: color 0.15s;
}

.filter-checkbox:hover {
    color: #7c3aed;
}

.filter-checkbox input[type="checkbox"] {
    width: 18px;
    height: 18px;
    cursor: pointer;
    accent-color: #7c3aed;
}

.filter-divider {
    height: 1px;
    background: #ede9fe;
    margin: 22px 0;
}

/* ===== LIST AREA ===== */
.list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 22px;
}

.list-header h2 {
    font-size: 1.45rem;
    font-weight: 800;
    margin: 0;
    color: #1e1b4b;
    display: flex;
    align-items: center;
    gap: 10px;
}

.count-badge {
    background: #7c3aed;
    color: white;
    font-size: 0.95rem;
    font-weight: 800;
    padding: 2px 12px;
    border-radius: 50px;
}

.sort-by {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.88rem;
    font-weight: 600;
    color: #475569;
}

.sort-by select {
    padding: 8px 14px;
    border: 1.5px solid #ddd6fe;
    border-radius: 8px;
    font-weight: 600;
    outline: none;
    cursor: pointer;
    background: white;
    color: #1e1b4b;
    transition: border-color 0.2s;
}

.sort-by select:focus {
    border-color: #7c3aed;
}

/* ===== LANDMARK CARD ===== */
.landmarks-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 30px;
}

.landmark-card {
    position: relative;
    background: #0f172a;
    border-radius: 4px;
    overflow: hidden;
    height: 500px;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    border: none;
    display: flex;
    flex-direction: column;
}

.landmark-card:hover {
    transform: translateY(-5px) scale(1.01);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.card-img-wrapper {
    position: absolute;
    inset: 0;
    height: 100%;
    overflow: hidden;
    z-index: 0;
}

.card-img-wrapper::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, 
        rgba(0,0,0,0) 0%, 
        rgba(0,0,0,0.2) 40%, 
        rgba(0,0,0,0.8) 80%, 
        rgba(0,0,0,0.95) 100%);
    z-index: 1;
}

.card-img-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
}

/* Rank Badge */
.card-rank-badge {
    position: absolute;
    top: 14px;
    left: 14px;
    background: #7c3aed;
    color: white;
    font-size: 0.78rem;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 50px;
    letter-spacing: 0.5px;
    box-shadow: 0 2px 8px rgba(124, 58, 237, 0.4);
    z-index: 2;
}

/* Slider */
.slider-arrows { opacity: 0; transition: opacity 0.2s ease; }
.card-img-wrapper:hover .slider-arrows { opacity: 1; }
.arrow-btn {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(255,255,255,0.9);
    border: none;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: #1e293b;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    z-index: 5;
    transition: 0.2s;
}
.arrow-btn:hover { background: white; transform: translateY(-50%) scale(1.1); }
.arrow-btn.left { left: 8px; }
.arrow-btn.right { right: 8px; }
.slider-dots { position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%); display: flex; gap: 4px; z-index: 5; }
.dot { width: 6px; height: 6px; background: rgba(255,255,255,0.6); border-radius: 50%; transition: 0.2s; }
.dot.active { background: white; transform: scale(1.3); }

/* Heart */
.btn-heart {
    position: absolute;
    top: 14px;
    right: 14px;
    background: rgba(255,255,255,0.92);
    border: none;
    width: 38px;
    height: 38px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: #94a3b8;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    transition: 0.2s;
    z-index: 2;
}
.btn-heart.active { color: #ef4444; }
.btn-heart:hover { transform: scale(1.1); background: white; }

/* Card Info */
.card-info {
    position: relative;
    z-index: 2;
    padding: 30px 24px;
    margin-top: auto;
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
}

.category-tag {
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.65rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

.place-name {
    font-size: 2.2rem;
    font-weight: 800;
    font-family: 'Playfair Display', serif;
    color: white;
    letter-spacing: -0.5px;
    line-height: 1.1;
    margin: 0 0 10px;
}

.landmark-card:hover .place-name {
    color: #7c3aed;
    text-decoration: underline;
}

.rating-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
}

.bubbles i {
    color: #7c3aed;
    font-size: 0.85rem;
    margin-right: 2px;
}

.review-count {
    font-size: 0.88rem;
    color: #64748b;
    font-weight: 600;
    text-decoration: underline;
}

.category-row {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.88rem;
    color: #64748b;
    margin-bottom: 14px;
}

.cat-label {
    font-weight: 700;
    color: #7c3aed;
    background: #f5f3ff;
    padding: 4px 10px;
    border-radius: 5px;
    display: flex;
    align-items: center;
    gap: 5px;
}

.divider { color: #cbd5e1; }

.description-snippet {
    font-size: 0.88rem;
    color: #64748b;
    line-height: 1.65;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* Footer Buttons */
.card-footer {
    margin-top: auto;
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    padding-top: 12px;
}

.btn-contact {
    background: white;
    color: #1e293b;
    border: 1.5px solid #ddd6fe;
    padding: 10px 20px;
    border-radius: 25px;
    font-weight: 700;
    font-size: 0.88rem;
    cursor: pointer;
    transition: 0.2s;
    display: flex;
    align-items: center;
    gap: 6px;
}

.btn-contact:hover {
    border-color: #7c3aed;
    color: #7c3aed;
    background: #f5f3ff;
}

.btn-details {
    background: #7c3aed;
    color: white;
    border: none;
    padding: 10px 24px;
    border-radius: 25px;
    font-weight: 700;
    font-size: 0.88rem;
    cursor: pointer;
    transition: 0.2s;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.btn-details:hover {
    background: #6d28d9;
    box-shadow: 0 6px 16px rgba(124, 58, 237, 0.4);
    transform: translateY(-1px);
}

/* ===== LOADING / EMPTY ===== */
.loading-box,
.empty-box {
    text-align: center;
    padding: 80px 40px;
    background: white;
    border-radius: 18px;
    border: 1px solid #ede9fe;
}

.spinner {
    border: 4px solid #ede9fe;
    border-top: 4px solid #7c3aed;
    border-radius: 50%;
    width: 45px;
    height: 45px;
    animation: spin 0.9s linear infinite;
    margin: 0 auto 20px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.empty-box i {
    font-size: 3.5rem;
    color: #c4b5fd;
    margin-bottom: 20px;
    display: block;
}

.empty-box p {
    color: #64748b;
    font-size: 1.05rem;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 1100px) {
    .landmark-card {
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

@media (max-width: 600px) {
    .landmarks-header {
        padding: 32px 16px 24px;
    }
    .header-container h1 {
        font-size: 1.6rem;
    }
    .icon-zone {
        display: none;
    }
}
</style>
