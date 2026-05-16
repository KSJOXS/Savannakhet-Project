<template>
    <div class="hotels-page">
        <Navbar />

        <div class="hotel-search-header">
            <div class="search-container">
                <h1>{{ t('hotels.title') }}</h1>
                
                <div class="booking-bar">
                    <div class="booking-input destination">
                        <i class="fas fa-map-marker-alt"></i>
                        <div class="input-content">
                            <label>{{ t('hotels.whereTo') }}</label>
                            <input type="text" :value="t('hotels.savannakhetLaos')" readonly />
                        </div>
                    </div>
                    
                    <div class="booking-divider"></div>
                    
                    <div class="booking-divider"></div>
                    
                    <div class="booking-input budget" @click.stop="showBudgetDropdown = !showBudgetDropdown">
                        <i class="fas fa-wallet"></i>
                        <div class="input-content">
                            <label>{{ t('hotels.budget') }}</label>
                            <div class="input-value">{{ selectedBudgetText }}</div>
                        </div>

                        <div class="dropdown-menu budget-dropdown" v-if="showBudgetDropdown" @click.stop>
                            <div class="dropdown-item" v-for="b in budgets" :key="b.id" 
                                :class="{ active: selectedBudget === b.id }"
                                @click="selectedBudget = b.id; showBudgetDropdown = false">
                                {{ b.label }}
                            </div>
                        </div>
                    </div>
                    
                    <button class="btn-update-search">{{ t('hotels.update') }}</button>
                </div>
            </div>
        </div>

        <div class="main-layout">
            <aside class="filter-sidebar">
                <div class="map-preview" @click="showMapModal = true">
                    <img src="https://images.unsplash.com/photo-1524661135-423995f22d0b?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80" alt="Map View" />
                    <button class="btn-view-map"><i class="fas fa-map"></i> {{ t('common.viewOnMap') }}</button>
                </div>

                <div class="filter-group">
                    <h3>Property Type</h3>
                    <label v-for="cat in hotelCategories" :key="'sidebar-'+cat.id" class="filter-checkbox">
                        <input type="checkbox" :value="cat.name.toLowerCase()" v-model="selectedCategories" />
                        <span>{{ cat.name }}</span>
                    </label>
                </div>
            </aside>

            <main class="hotel-list-area">
                <div class="list-header">
                    <h2>{{ filteredHotels.length }} properties in Savannakhet</h2>
                    <div class="sort-by">
                        <span>Sort by:</span>
                        <select>
                            <option>Traveler Ranked</option>
                            <option>Price (Low to High)</option>
                            <option>Distance</option>
                        </select>
                    </div>
                </div>

                <div v-if="loading" class="loading-box">
                    <div class="spinner"></div>
                    <p>Finding comfort for you...</p>
                </div>

                <div v-else-if="filteredHotels.length === 0" class="empty-box">
                    <i class="fas fa-bed"></i>
                    <p>No hotels found matching your search.</p>
                </div>

                <div class="hotels-grid">
                    <div class="hotel-card" v-for="(hotel, index) in filteredHotels" :key="hotel.id" @click="goToDetail(hotel.id)">
                        
                        <div class="card-img-wrapper">
                            <img :src="getCoverImage(hotel)" :alt="hotel.name" />
                            <button class="btn-heart" :class="{ active: isFavorite(hotel.id) }" @click.stop="toggleHeart(hotel.id)">
                                <i class="fas fa-heart"></i>
                            </button>
                        </div>

                        <div class="card-info">
                            <span class="category-tag">{{ getCategoryName(hotel.category_id) }}</span>
                            <h3 class="place-name">{{ hotel.name }}</h3>
                            
                            <div class="rating-row">
                                <span class="bubbles">
                                    <i v-for="s in 5" :key="s" :class="[(hotel.rating_avg || 0) >= s ? 'fas' : 'far', 'fa-circle']"></i>
                                </span>
                                <span class="review-count">{{ hotel.rating_avg || '0.0' }}</span>
                            </div>

                            <p class="description">
                                {{ hotel.description || 'Experience comfort and luxury in the heart of Savannakhet.' }}
                            </p>

                            <div class="card-footer">
                                <span class="location-tag">✨ {{ t('landmarks.verified') }}</span>
                                <span class="btn-details">{{ t('landmarks.openGuide') }} →</span>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
        
        <SectionDivider icon="fas fa-bed" />

        <MapOverlay 
            :is-open="showMapModal" 
            :places="places" 
            :categories="categories"
            initial-filter="hotel"
            title="Hotels" 
            @close="showMapModal = false" 
        />

        <RecentlyViewed />
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
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

const selectedBudget = ref('any')
const showBudgetDropdown = ref(false)

const budgets = computed(() => [
    { id: 'any', label: t('hotels.budgetAny') },
    { id: 'economy', label: t('hotels.budgetEconomy') },
    { id: 'midRange', label: t('hotels.budgetMidRange') },
    { id: 'luxury', label: t('hotels.budgetLuxury') }
])

const selectedBudgetText = computed(() => {
    return budgets.value.find(b => b.id === selectedBudget.value)?.label || t('hotels.budgetAny')
})

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
        console.error("Error fetching hotels:", err)
    } finally {
        loading.value = false
    }
}

const filteredHotels = computed(() => {
    let results = places.value.filter(p => {
        const cat = categories.value.find(c => c.id == p.category_id)
        return cat && cat.parent_type?.toLowerCase() === 'hotel'
    })

    // Budget Filter
    if (selectedBudget.value !== 'any') {
        results = results.filter(p => {
            if (!p.daily_budget) return false
            const budgetLevel = getBudgetLevel(p.daily_budget)
            return budgetLevel === selectedBudget.value
        })
    }

    if (selectedCategories.value.length > 0) {
        results = results.filter(p => {
            const cat = categories.value.find(c => c.id === p.category_id)
            return cat && selectedCategories.value.includes(cat.name.toLowerCase())
        })
    }
    return results
})

const getBudgetLevel = (budgetString) => {
    if (!budgetString) return 'any'
    if (budgetString.toLowerCase().includes('free')) return 'economy'
    
    const numbers = budgetString.match(/\d+(,\d+)*(\.\d+)?/g)
    if (!numbers) return 'any'
    
    let price = parseFloat(numbers[0].replace(/,/g, ''))
    
    // Currency conversion if needed
    if (budgetString.includes('฿')) price = price * 600
    if (budgetString.includes('$')) price = price * 20000

    if (price < 200000) return 'economy'
    if (price <= 600000) return 'midRange'
    return 'luxury'
}

const hotelCategories = computed(() => {
    return categories.value.filter(c => c.parent_type === 'hotel')
})

const getCategoryName = (id) => categories.value.find(c => c.id === id)?.name || 'Accommodation'

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

const isFavorite = (id) => favoriteIds.value.includes(id)
const toggleHeart = async (id) => {
    if (!user.value) return router.push('/login')
    try {
        const res = await favoriteRepository.toggleFavorite(user.value.id, id)
        if (res.data.status === 'added') favoriteIds.value.push(id)
        else favoriteIds.value = favoriteIds.value.filter(fid => fid !== id)
    } catch (e) { console.error(e) }
}

const goToDetail = (id) => router.push(`/places/${id}`)

const closeDropdowns = () => {
    showBudgetDropdown.value = false
}

onMounted(() => {
    fetchData()
    document.addEventListener('click', closeDropdowns)
})

onUnmounted(() => {
    document.removeEventListener('click', closeDropdowns)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:wght@700;800;900&display=swap');

.hotels-page {
    background-color: #faf9f6;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    color: #1e293b;
}

/* --- 1. Booking Header Bar --- */
.hotel-search-header {
    background: white;
    padding: 30px 20px;
    border-bottom: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.02);
}

.search-container {
    max-width: 1200px;
    margin: 0 auto;
}

.search-container h1 {
    font-size: 2rem;
    font-weight: 800;
    margin: 0 0 20px;
    color: #000;
}

.booking-bar {
    display: flex;
    align-items: center;
    background: white;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    padding: 8px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.booking-input {
    display: flex;
    align-items: center;
    padding: 10px 20px;
    flex: 1;
    cursor: pointer;
    border-radius: 8px;
    transition: 0.2s;
}

.booking-input:hover { background: #f8fafc; }
.booking-input i { font-size: 1.4rem; color: #000; margin-right: 15px; }

.input-content { display: flex; flex-direction: column; }
.input-content label { font-size: 0.75rem; font-weight: 700; color: #475569; text-transform: uppercase; margin-bottom: 2px; cursor: pointer;}
.input-content input { border: none; background: transparent; font-size: 1rem; font-weight: 600; color: #000; outline: none; cursor: pointer; width: 100%;}
.input-content input::placeholder { color: #94a3b8; font-weight: 500; }

.booking-divider { width: 1px; height: 40px; background: #e2e8f0; margin: 0 10px; }

.btn-update-search {
    background: #000;
    color: white;
    border: none;
    padding: 15px 30px;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
    margin-left: 10px;
}
.btn-update-search:hover { background: #334155; }

/* Budget Selector Styles */
.booking-input.budget {
    position: relative;
}

.input-value {
    font-size: 1rem;
    font-weight: 600;
    color: #000;
}

.budget-dropdown {
    position: absolute;
    top: calc(100% + 10px);
    left: 0;
    width: 220px;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    z-index: 100;
    padding: 8px;
}

.dropdown-item {
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 500;
    color: #475569;
    transition: 0.2s;
    cursor: pointer;
}

.dropdown-item:hover {
    background: #f1f5f9;
    color: #000;
}

.dropdown-item.active {
    background: #000;
    color: white;
}

/* --- Main Layout --- */
.main-layout {
    max-width: 1200px;
    margin: 30px auto;
    padding: 0 20px;
    display: grid;
    grid-template-columns: 260px 1fr;
    gap: 30px;
}

/* --- 2. Sidebar Filters --- */
.filter-sidebar { height: fit-content; }

.map-preview {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    height: 120px;
    margin-bottom: 25px;
    border: 1px solid #cbd5e1;
    cursor: pointer;
}
.map-preview img { width: 100%; height: 100%; object-fit: cover; }
.btn-view-map {
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    background: white; border: 1px solid #000; padding: 8px 16px; border-radius: 8px;
    font-weight: 700; font-size: 0.85rem; display: flex; align-items: center; gap: 8px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15); pointer-events: none;
}

.filter-group h3 { font-size: 1rem; font-weight: 800; margin: 0 0 15px; color: #000; }
.filter-checkbox { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; cursor: pointer; font-size: 0.95rem; color: #475569;}
.filter-checkbox input[type="checkbox"] { width: 18px; height: 18px; cursor: pointer; accent-color: #000;}
.stars { color: #f59e0b; font-size: 0.85rem; letter-spacing: 2px;}
.filter-divider { height: 1px; background: #cbd5e1; margin: 25px 0; }

/* --- 3. Hotel List Area --- */
.list-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.list-header h2 { font-size: 1.4rem; font-weight: 700; margin: 0; color: #000; }
.sort-by { display: flex; align-items: center; gap: 10px; font-size: 0.9rem; font-weight: 600;}
.sort-by select { padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-weight: 600; outline: none; cursor: pointer;}

/* 🏨 Hotel Card (Horizontal List View) */
.hotels-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 30px;
}

.hotel-card {
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

.hotel-card:hover {
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
.hotel-img-wrapper:hover .slider-arrows { opacity: 1; }
.arrow-btn { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(255, 255, 255, 0.85); border: none; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; color: #1e293b; box-shadow: 0 2px 6px rgba(0,0,0,0.2); z-index: 5; transition: 0.2s; }
.arrow-btn:hover { background: white; transform: translateY(-50%) scale(1.1); }
.arrow-btn.left { left: 8px; } .arrow-btn.right { right: 8px; }

.slider-dots { position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%); display: flex; gap: 4px; z-index: 5; }
.dot { width: 6px; height: 6px; background: rgba(255, 255, 255, 0.6); border-radius: 50%; transition: 0.2s; }
.dot.active { background: white; transform: scale(1.3); }

.btn-heart { position: absolute; top: 15px; right: 15px; background: white; border: none; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 2px 6px rgba(0,0,0,0.2); font-size: 1.1rem; color: #94a3b8; transition: 0.2s; z-index: 50;}
.btn-heart.active { color: #ef4444; }
.btn-heart:hover { transform: scale(1.1); }
.img-counter { position: absolute; bottom: 15px; left: 15px; background: rgba(0,0,0,0.6); color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; display: flex; align-items: center; gap: 6px;}

/* Middle: Details */
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

.description {
    margin: 0 0 15px;
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

.other-deals { width: 100%; border-top: 1px solid #e2e8f0; padding-top: 15px;}
.mini-deal { display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #475569; margin-bottom: 6px;}
.mini-deal strong { color: #000; font-size: 0.9rem;}

/* --- Responsive Design --- */
@media (max-width: 1024px) {
    .main-layout { grid-template-columns: 1fr; }
    .filter-sidebar { display: none; } /* ซ่อน Sidebar ในมือถือ (ในเว็บจริงจะทำเป็นปุ่ม Filter เด้งขึ้นมา) */
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
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
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

</style>
