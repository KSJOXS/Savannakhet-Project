<template>
    <div class="restaurants-page">
        <Navbar />

        <div class="restaurant-header">
            <div class="header-container">
                <h1>Restaurants in Savannakhet</h1>
                <p class="subtitle">Explore the best places to eat, drink, and relax.</p>

                <div class="quick-filters" v-if="restaurantCategories.length > 0">
                    <button 
                        v-for="cat in restaurantCategories.slice(0, 6)" 
                        :key="cat.id"
                        class="filter-pill"
                        @click="toggleCategory(cat.name.toLowerCase())"
                        :class="{ active: selectedCategories.includes(cat.name.toLowerCase()) }"
                    >
                        <i :class="getIconForRestaurant(cat.name)"></i> {{ cat.name }}
                    </button>
                </div>
            </div>
        </div>

        <div class="main-layout">
            <aside class="filter-sidebar">
                <div class="map-preview" @click="showMapModal = true">
                    <img src="https://images.unsplash.com/photo-1524661135-423995f22d0b?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"
                        alt="Map View" />
                    <button class="btn-view-map"><i class="fas fa-map"></i> View on map</button>
                </div>

                <div class="filter-group">
                    <h3>Establishment Type</h3>
                    <label v-for="cat in restaurantCategories" :key="'sidebar-'+cat.id" class="filter-checkbox">
                        <input type="checkbox" :value="cat.name.toLowerCase()" v-model="selectedCategories" />
                        <span>{{ cat.name }}</span>
                    </label>
                </div>

                <div class="filter-divider"></div>

                <div class="filter-group">
                    <h3>Meals</h3>
                    <label class="filter-checkbox"><input type="checkbox" /> <span>Breakfast</span></label>
                    <label class="filter-checkbox"><input type="checkbox" /> <span>Lunch</span></label>
                    <label class="filter-checkbox"><input type="checkbox" /> <span>Dinner</span></label>
                </div>
            </aside>

            <main class="restaurant-list-area">
                <div class="list-header">
                    <h2>{{ filteredRestaurants.length }} restaurants found</h2>
                    <div class="sort-by">
                        <span>Sort by:</span>
                        <select>
                            <option>Highest Rated</option>
                            <option>Most Reviewed</option>
                        </select>
                    </div>
                </div>

                <div v-if="loading" class="loading-box">
                    <div class="spinner"></div>
                    <p>Finding the best food...</p>
                </div>

                <div v-else-if="filteredRestaurants.length === 0" class="empty-box">
                    <i class="fas fa-utensils"></i>
                    <p>No restaurants found. Try clearing your filters or check back later.</p>
                </div>

                <div class="restaurants-grid">
                    <div v-for="(place, index) in filteredRestaurants" :key="place.id"
                        class="restaurant-card" @click="goToDetail(place.id)">

                        <div class="card-img-wrapper">
                            <img :src="getCoverImage(place)" :alt="place.name" />
                            <button class="btn-heart" :class="{ active: isFavorite(place.id) }"
                                @click.stop="toggleHeart(place.id)">
                                <i class="fas fa-heart"></i>
                            </button>
                        </div>

                        <div class="card-info">
                            <span class="category-tag">{{ getCategoryName(place.category_id) }}</span>
                            <h3 class="place-name">{{ place.name }}</h3>
                            <div class="rating-row">
                                <span class="bubbles">
                                    <i v-for="s in 5" :key="s"
                                        :class="[(place.rating_avg || 0) >= s ? 'fas' : 'far', 'fa-circle']"></i>
                                </span>
                                <span class="review-count">{{ place.rating_avg || '0.0' }}</span>
                            </div>

                            <div class="review-snippet">
                                <p>{{ place.description || "Experience the authentic flavors of Savannakhet." }}</p>
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
        
        <SectionDivider icon="fas fa-utensils" />

        <MapOverlay 
            :is-open="showMapModal" 
            :places="places" 
            :categories="categories"
            initial-filter="restaurant"
            title="Restaurants" 
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
import axios from 'axios'

const router = useRouter()
const { user } = useAuth()
const { t } = useI18n()
const places = ref([])
const categories = ref([])
const favoriteIds = ref([])
const loading = ref(true)
const selectedCategories = ref([])
const showMapModal = ref(false)

// --- API DATA FETCHING ---
const fetchData = async () => {
    loading.value = true
    try {
        const [resPlaces, resCats] = await Promise.all([
            placeRepository.getAll(),
            categoryRepository.getAll()
        ])

        places.value = resPlaces.data
        categories.value = resCats.data

        // Fetch favorites asynchronously to not block UI rendering
        if (user.value) {
            favoriteRepository.getUserFavorites(user.value.id)
                .then(favRes => {
                    favoriteIds.value = favRes.data.map(f => f.place_id)
                })
                .catch(err => console.error("Error fetching favorites:", err))
        }
    } catch (err) {
        console.error("Error fetching places:", err)
    } finally {
        loading.value = false
    }
}

// 🍽️ กรองเฉพาะร้านอาหารและคาเฟ่
const filteredRestaurants = computed(() => {
    let results = places.value.filter(p => {
        const cat = categories.value.find(c => c.id == p.category_id)
        const pType = cat?.parent_type?.toLowerCase() || ''
        return ['restaurant', 'cafe', 'local_food'].includes(pType)
    })

    if (selectedCategories.value.length > 0) {
        results = results.filter(p => {
            const cat = categories.value.find(c => c.id === p.category_id)
            return cat && selectedCategories.value.includes(cat.name.toLowerCase())
        })
    }
    return results
})

const restaurantCategories = computed(() => {
    return categories.value.filter(c => {
        const pType = c.parent_type?.toLowerCase() || ''
        return ['restaurant', 'cafe', 'local_food'].includes(pType)
    })
})

const toggleCategory = (name) => {
    name = name.toLowerCase()
    if (selectedCategories.value.includes(name)) {
        selectedCategories.value = selectedCategories.value.filter(c => c !== name)
    } else {
        selectedCategories.value.push(name)
    }
}

const getIconForRestaurant = (name) => {
    name = name.toLowerCase()
    if (name.includes('coffee') || name.includes('cafe')) return 'fas fa-mug-hot'
    if (name.includes('breakfast')) return 'fas fa-coffee'
    if (name.includes('lunch')) return 'fas fa-hamburger'
    if (name.includes('dinner')) return 'fas fa-utensils'
    if (name.includes('bar') || name.includes('pub')) return 'fas fa-wine-glass-alt'
    if (name.includes('street')) return 'fas fa-pizza-slice'
    return 'fas fa-utensils'
}

// --- Image Carousel Logic ---
const currentImageIndices = ref({}) 

const getPlaceImagesArray = (place) => {
    const noImageUrl = 'https://via.placeholder.com/400x300?text=No+Image';
    let urls = [];
    
    if (place.images && Array.isArray(place.images) && place.images.length > 0) {
        urls = place.images.map(img => img.image_url || img.url || img);
    } else if (place.image_url) { 
        if (typeof place.image_url === 'string' && place.image_url.trim().startsWith('[')) {
            try { urls = JSON.parse(place.image_url); } catch (e) { urls = [place.image_url.replace(/^\["?|"?\]$/g, '').replace(/\\"/g, '')]; }
        } else {
            urls = [place.image_url];
        }
    }
    
    if (urls.length === 0) return [noImageUrl];

    return urls.map(url => {
        if (!url) return noImageUrl;
        if (url.startsWith('https://') || url.startsWith('http://') || url.startsWith('data:')) return url;
        return `http://localhost:8000${url.startsWith('/') ? '' : '/'}${url}`;
    });
}

const getCoverImage = (place) => {
    const images = getPlaceImagesArray(place);
    const index = currentImageIndices.value[place.id] || 0;
    return images[index] || images[0];
}

const nextImage = (placeId, place) => {
    const images = getPlaceImagesArray(place);
    if (images.length <= 1) return;
    const currentIdx = currentImageIndices.value[placeId] || 0;
    currentImageIndices.value[placeId] = (currentIdx + 1) % images.length;
}

const prevImage = (placeId, place) => {
    const images = getPlaceImagesArray(place);
    if (images.length <= 1) return;
    const currentIdx = currentImageIndices.value[placeId] || 0;
    currentImageIndices.value[placeId] = currentIdx === 0 ? images.length - 1 : currentIdx - 1;
}

const getCategoryName = (id) => {
    const cat = categories.value.find(c => c.id === id)
    return cat ? cat.name : 'Restaurant'
}

const isFavorite = (id) => favoriteIds.value.includes(id)

const toggleHeart = async (placeId) => {
    if (!user.value) return router.push('/login')
    try {
        const res = await favoriteRepository.toggleFavorite(user.value.id, placeId)
        if (res.data.status === 'added') {
            favoriteIds.value.push(placeId)
            await axios.post('http://localhost:8000/api/interactions/', {
                place_id: placeId, rating: 5, interaction_type: 'like'
            })
        } else {
            favoriteIds.value = favoriteIds.value.filter(id => id !== placeId)
        }
    } catch (err) { console.error(err) }
}

// นำทางไปหน้า Detail ปกติ (เพราะร้านอาหารใช้ฟอร์แมตข้อมูลเหมือนสถานที่ท่องเที่ยวทั่วไปได้)
const goToDetail = (id) => router.push(`/places/${id}`)

onMounted(fetchData)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:wght@700;800;900&display=swap');

.restaurants-page {
    background-color: #faf9f6;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    color: #1e293b;
}

/* 🍽️ Restaurant Header */
.restaurant-header {
    background: white;
    padding: 30px 20px;
    border-bottom: 1px solid #e2e8f0;
}

.header-container {
    max-width: 1200px;
    margin: 0 auto;
}

.header-container h1 {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 0 0 5px;
    color: #000;
}

.subtitle {
    color: #475569;
    font-size: 1rem;
    margin-bottom: 20px;
}

/* Quick Filters */
.quick-filters {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.filter-pill {
    background: white;
    border: 1px solid #cbd5e1;
    padding: 10px 20px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.9rem;
    color: #1e293b;
    cursor: pointer;
    transition: 0.2s;
    display: flex;
    align-items: center;
    gap: 8px;
}

.filter-pill:hover {
    border-color: #000;
    background: #f8fafc;
}

.filter-pill i {
    color: #64748b;
    font-size: 1.1rem;
}

/* Layout */
.main-layout {
    max-width: 1200px;
    margin: 30px auto;
    padding: 0 20px;
    display: grid;
    grid-template-columns: 260px 1fr;
    gap: 30px;
}

/* Sidebar */
.map-preview {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    height: 120px;
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
    padding: 8px 16px;
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
    width: 18px;
    height: 18px;
    cursor: pointer;
    accent-color: #000;
}

.filter-divider {
    height: 1px;
    background: #cbd5e1;
    margin: 25px 0;
}

/* Main Content */
.list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.list-header h2 {
    font-size: 1.4rem;
    font-weight: 700;
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
    padding: 8px 12px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-weight: 600;
    outline: none;
    cursor: pointer;
}

/* 🍽️ Restaurant Card */
.restaurants-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 30px;
}

.restaurant-card {
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

.restaurant-card:hover {
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

.slider-arrows { opacity: 0; transition: opacity 0.2s ease-in-out; }
.card-img-wrapper:hover .slider-arrows { opacity: 1; }
.arrow-btn { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(255, 255, 255, 0.85); border: none; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; color: #1e293b; box-shadow: 0 2px 6px rgba(0,0,0,0.2); z-index: 5; transition: 0.2s; }
.arrow-btn:hover { background: white; transform: translateY(-50%) scale(1.1); }
.arrow-btn.left { left: 8px; } .arrow-btn.right { right: 8px; }

.slider-dots { position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%); display: flex; gap: 4px; z-index: 5; }
.dot { width: 6px; height: 6px; background: rgba(255, 255, 255, 0.6); border-radius: 50%; transition: 0.2s; }
.dot.active { background: white; transform: scale(1.3); }

.btn-heart {
    position: absolute;
    top: 12px;
    right: 12px;
    background: rgba(255, 255, 255, 0.9);
    border: none;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: #94a3b8;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
    transition: 0.2s;
}

.btn-heart.active {
    color: #ef4444;
}

.btn-heart:hover {
    transform: scale(1.1);
    background: white;
}

/* Info */
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

.restaurant-card:hover .place-name {
    text-decoration: underline;
}

.rating-row {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.bubbles i {
    color: #00aa6c;
    font-size: 0.85rem;
    margin-right: 2px;
}

.review-count {
    font-size: 0.85rem;
    color: #475569;
    margin-left: 10px;
    font-weight: 600;
    text-decoration: underline;
}

.category-price-row {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.85rem;
    color: #475569;
    margin-bottom: 15px;
}

.dot-divider {
    color: #cbd5e1;
}

.price-range {
    font-weight: 600;
    color: #000;
}

.review-snippet {
    margin-bottom: 15px;
}

.review-snippet p {
    margin: 0;
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.7);
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 15px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.location-tag {
    color: rgba(255, 255, 255, 0.5);
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
}

.btn-details {
    color: white;
    font-weight: 800;
    font-size: 0.75rem;
    letter-spacing: 1px;
}

/* States */
.loading-box,
.empty-box {
    text-align: center;
    padding: 60px;
    background: white;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
}

.spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #00aa6c;
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

.empty-box i {
    font-size: 2.5rem;
    color: #cbd5e1;
    margin-bottom: 15px;
}

.empty-box p {
    color: #64748b;
    font-size: 1rem;
}

@media (max-width: 992px) {
    .main-layout {
        grid-template-columns: 1fr;
    }

    .filter-sidebar {
        display: none;
    }

    .restaurant-card {
        flex-direction: column;
        height: auto;
    }

    .card-img-wrapper {
        width: 100%;
        height: 220px;
    }
}
</style>
