<template>
    <div class="explore-page">
        <Navbar />

        <div class="hero-section" :style="{ backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.6)), url(${heroImages[currentHeroIndex]})` }">
            <div class="hero-content">
                <h1>Book traveler-backed things to do</h1>
                <p>Discover top attractions, amazing food, and the best experiences in Savannakhet.</p>
                
                <div class="hero-search-container">
                    <div class="hero-search-box" :class="{ 'dropdown-open': isSearchFocused }">
                        <i class="fas fa-search"></i>
                        <input 
                            v-model="searchQuery" 
                            type="text" 
                            placeholder="Search by destination, place, or category..." 
                            @focus="isSearchFocused = true"
                            @keyup.enter="executeSearch"
                        />
                        <button class="btn-search-hero" @click="executeSearch">Search</button>
                    </div>

                    <div v-if="isSearchFocused" class="search-overlay" @click="isSearchFocused = false"></div>

                    <div v-if="isSearchFocused" class="search-dropdown">
                        <div class="dropdown-item" @click="executeSearch">
                            <div class="icon-box"><i class="fas fa-location-arrow"></i></div>
                            <div class="item-text">
                                <strong>Nearby</strong>
                            </div>
                        </div>

                        <div class="dropdown-divider"></div>

                        <div class="dropdown-group" v-if="topRatedPlaces.length > 0">
                            <h4>Popular Destinations</h4>
                            <div v-for="place in topRatedPlaces.slice(0, 3)" :key="'dd-'+place.id" class="dropdown-item" @click="goToDetail(place.id)">
                                <img :src="getCoverImage(place)" class="dropdown-img" :alt="place.name" />
                                <div class="item-text">
                                    <strong>{{ place.name }}</strong>
                                    <small>{{ getCategoryName(place.category_id) }}, Savannakhet</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="hero-dots">
                <span v-for="(_, idx) in heroImages" :key="'hero-dot-'+idx" 
                      :class="['dot', { active: currentHeroIndex === idx }]" 
                      @click="currentHeroIndex = idx">
                </span>
            </div>
        </div>

        <div class="main-container">
            <section v-if="recommendedPlaces.length > 0" class="horizontal-section">
                <div class="section-header">
                    <h2>✨ Recommended for you</h2>
                    <p>Browsing Savannakhet? We think you'll like these based on your activity.</p>
                </div>
                <div class="carousel-container">
                    <div v-for="place in recommendedPlaces" :key="'rec-'+place.id" class="ta-card ai-card" @click="goToDetail(place.id)">
                        <div class="card-img-wrapper">
                            <img :src="getCoverImage(place)" :alt="place.name" />
                            
                            <div class="slider-arrows" v-if="getPlaceImagesArray(place).length > 1">
                                <button class="arrow-btn left" @click.stop="prevImage(place.id, place)"><i class="fas fa-chevron-left"></i></button>
                                <button class="arrow-btn right" @click.stop="nextImage(place.id, place)"><i class="fas fa-chevron-right"></i></button>
                            </div>
                            <div class="slider-dots" v-if="getPlaceImagesArray(place).length > 1">
                                <span v-for="(_, idx) in getPlaceImagesArray(place)" :key="idx" :class="['dot', { active: (currentImageIndices[place.id] || 0) === idx }]"></span>
                            </div>

                            <button v-if="!user || user.role !== 'admin'" class="btn-heart" :class="{ active: isFavorite(place.id) }" @click.stop="toggleHeart(place.id)">
                                <i class="fas fa-heart"></i>
                            </button>
                        </div>
                        <div class="card-info">
                            <h3 class="truncate">{{ place.name }}</h3>
                            <div class="rating-row">
                                <span class="bubbles"><i class="fas fa-circle"></i><i class="fas fa-circle"></i><i class="fas fa-circle"></i><i class="fas fa-circle"></i><i class="fas fa-circle-half-stroke"></i></span>
                                <span class="rating-num">{{ place.rating_avg || '0.0' }}</span>
                            </div>
                            <p class="cat-text"><i class="fas fa-map-marker-alt"></i> {{ getCategoryName(place.category_id) }}</p>
                        </div>
                    </div>
                </div>
            </section>

            <section v-if="topRatedPlaces.length > 0" class="horizontal-section">
                <div class="section-header">
                    <h2>🏆 Top Rated Places</h2>
                    <p>Highly rated by fellow travelers</p>
                </div>
                <div class="carousel-container">
                    <div v-for="place in topRatedPlaces" :key="'top-'+place.id" class="ta-card" @click="goToDetail(place.id)">
                        <div class="card-img-wrapper">
                            <img :src="getCoverImage(place)" :alt="place.name" />
                            <div class="rank-badge">Top Rated</div>

                            <div class="slider-arrows" v-if="getPlaceImagesArray(place).length > 1">
                                <button class="arrow-btn left" @click.stop="prevImage(place.id, place)"><i class="fas fa-chevron-left"></i></button>
                                <button class="arrow-btn right" @click.stop="nextImage(place.id, place)"><i class="fas fa-chevron-right"></i></button>
                            </div>
                            <div class="slider-dots" v-if="getPlaceImagesArray(place).length > 1">
                                <span v-for="(_, idx) in getPlaceImagesArray(place)" :key="idx" :class="['dot', { active: (currentImageIndices[place.id] || 0) === idx }]"></span>
                            </div>

                            <button v-if="!user || user.role !== 'admin'" class="btn-heart" :class="{ active: isFavorite(place.id) }" @click.stop="toggleHeart(place.id)">
                                <i class="fas fa-heart"></i>
                            </button>
                        </div>
                        <div class="card-info">
                            <h3 class="truncate">{{ place.name }}</h3>
                            <div class="rating-row">
                                <i class="fas fa-star" style="color: #f59e0b;"></i>
                                <span class="rating-num">{{ place.rating_avg || '0.0' }}</span>
                            </div>
                            <p class="cat-text"><i class="fas fa-map-marker-alt"></i> {{ getCategoryName(place.category_id) }}</p>
                        </div>
                    </div>
                </div>
            </section>

            <section v-if="foodPlaces.length > 0" class="horizontal-section">
                <div class="section-header"><h2>🍽️ Restaurants & Cafes</h2></div>
                <div class="carousel-container">
                    <div v-for="place in foodPlaces" :key="'food-'+place.id" class="ta-card" @click="goToDetail(place.id)">
                        <div class="card-img-wrapper">
                            <img :src="getCoverImage(place)" :alt="place.name" />
                            <div class="slider-arrows" v-if="getPlaceImagesArray(place).length > 1">
                                <button class="arrow-btn left" @click.stop="prevImage(place.id, place)"><i class="fas fa-chevron-left"></i></button>
                                <button class="arrow-btn right" @click.stop="nextImage(place.id, place)"><i class="fas fa-chevron-right"></i></button>
                            </div>
                            <div class="slider-dots" v-if="getPlaceImagesArray(place).length > 1">
                                <span v-for="(_, idx) in getPlaceImagesArray(place)" :key="idx" :class="['dot', { active: (currentImageIndices[place.id] || 0) === idx }]"></span>
                            </div>
                            <button v-if="!user || user.role !== 'admin'" class="btn-heart" :class="{ active: isFavorite(place.id) }" @click.stop="toggleHeart(place.id)">
                                <i class="fas fa-heart"></i>
                            </button>
                        </div>
                        <div class="card-info"><h3 class="truncate">{{ place.name }}</h3><p class="cat-text"><i class="fas fa-map-marker-alt"></i> {{ getCategoryName(place.category_id) }}</p></div>
                    </div>
                </div>
            </section>

            <section v-if="naturePlaces.length > 0" class="horizontal-section">
                <div class="section-header"><h2>🌿 Nature</h2></div>
                <div class="carousel-container">
                    <div v-for="place in naturePlaces" :key="'nat-'+place.id" class="ta-card" @click="goToDetail(place.id)">
                        <div class="card-img-wrapper">
                            <img :src="getCoverImage(place)" :alt="place.name" />
                            <div class="slider-arrows" v-if="getPlaceImagesArray(place).length > 1">
                                <button class="arrow-btn left" @click.stop="prevImage(place.id, place)"><i class="fas fa-chevron-left"></i></button>
                                <button class="arrow-btn right" @click.stop="nextImage(place.id, place)"><i class="fas fa-chevron-right"></i></button>
                            </div>
                            <div class="slider-dots" v-if="getPlaceImagesArray(place).length > 1">
                                <span v-for="(_, idx) in getPlaceImagesArray(place)" :key="idx" :class="['dot', { active: (currentImageIndices[place.id] || 0) === idx }]"></span>
                            </div>
                            <button v-if="!user || user.role !== 'admin'" class="btn-heart" :class="{ active: isFavorite(place.id) }" @click.stop="toggleHeart(place.id)">
                                <i class="fas fa-heart"></i>
                            </button>
                        </div>
                        <div class="card-info"><h3 class="truncate">{{ place.name }}</h3><p class="cat-text"><i class="fas fa-map-marker-alt"></i> {{ getCategoryName(place.category_id) }}</p></div>
                    </div>
                </div>
            </section>

            <section v-if="landmarkPlaces.length > 0" class="horizontal-section">
                <div class="section-header"><h2>📸 Landmarks & Points of Interest</h2></div>
                <div class="carousel-container">
                    <div v-for="place in landmarkPlaces" :key="'lan-'+place.id" class="ta-card" @click="goToDetail(place.id)">
                        <div class="card-img-wrapper">
                            <img :src="getCoverImage(place)" :alt="place.name" />
                            <div class="slider-arrows" v-if="getPlaceImagesArray(place).length > 1">
                                <button class="arrow-btn left" @click.stop="prevImage(place.id, place)"><i class="fas fa-chevron-left"></i></button>
                                <button class="arrow-btn right" @click.stop="nextImage(place.id, place)"><i class="fas fa-chevron-right"></i></button>
                            </div>
                            <div class="slider-dots" v-if="getPlaceImagesArray(place).length > 1">
                                <span v-for="(_, idx) in getPlaceImagesArray(place)" :key="idx" :class="['dot', { active: (currentImageIndices[place.id] || 0) === idx }]"></span>
                            </div>
                            <button v-if="!user || user.role !== 'admin'" class="btn-heart" :class="{ active: isFavorite(place.id) }" @click.stop="toggleHeart(place.id)">
                                <i class="fas fa-heart"></i>
                            </button>
                        </div>
                        <div class="card-info"><h3 class="truncate">{{ place.name }}</h3><p class="cat-text"><i class="fas fa-map-marker-alt"></i> {{ getCategoryName(place.category_id) }}</p></div>
                    </div>
                </div>
            </section>

            <section v-if="religiousPlaces.length > 0" class="horizontal-section">
                <div class="section-header"><h2>⛩️ Religious & Sacred Sites</h2></div>
                <div class="carousel-container">
                    <div v-for="place in religiousPlaces" :key="'rel-'+place.id" class="ta-card" @click="goToDetail(place.id)">
                        <div class="card-img-wrapper">
                            <img :src="getCoverImage(place)" :alt="place.name" />
                            <div class="slider-arrows" v-if="getPlaceImagesArray(place).length > 1">
                                <button class="arrow-btn left" @click.stop="prevImage(place.id, place)"><i class="fas fa-chevron-left"></i></button>
                                <button class="arrow-btn right" @click.stop="nextImage(place.id, place)"><i class="fas fa-chevron-right"></i></button>
                            </div>
                            <div class="slider-dots" v-if="getPlaceImagesArray(place).length > 1">
                                <span v-for="(_, idx) in getPlaceImagesArray(place)" :key="idx" :class="['dot', { active: (currentImageIndices[place.id] || 0) === idx }]"></span>
                            </div>
                            <button v-if="!user || user.role !== 'admin'" class="btn-heart" :class="{ active: isFavorite(place.id) }" @click.stop="toggleHeart(place.id)">
                                <i class="fas fa-heart"></i>
                            </button>
                        </div>
                        <div class="card-info"><h3 class="truncate">{{ place.name }}</h3><p class="cat-text"><i class="fas fa-map-marker-alt"></i> {{ getCategoryName(place.category_id) }}</p></div>
                    </div>
                </div>
            </section>

            <section class="explore-all-section" ref="exploreAllSection">
                <div class="section-header mt-50">
                    <h2>🔍 Explore All Places</h2>
                </div>
                <div class="explore-layout">
                    <aside class="sidebar">
                        <div class="filter-card">
                            <h3>Filters</h3>
                            <div class="filter-group mt-15">
                                <div class="input-with-icon">
                                    <i class="fas fa-search"></i>
                                    <input v-model="searchQuery" type="text" placeholder="Search..." />
                                </div>
                            </div>
                            <div class="filter-group">
                                <h4>Categories</h4>
                                <div class="category-list">
                                    <button :class="['cat-pill', { active: !selectedCategory }]" @click="filterByCategory(null)">All</button>
                                    <button v-for="cat in categories" :key="cat.id"
                                        :class="['cat-pill', { active: selectedCategory === cat.id }]"
                                        @click="filterByCategory(cat.id)">
                                        {{ cat.name }}
                                    </button>
                                </div>
                            </div>
                            <button @click="resetFilters" class="btn-clear">Clear Filters</button>
                        </div>
                    </aside>

                    <main class="content-area">
                        <div class="results-bar">
                            <span>Found <strong>{{ filteredPlaces.length }}</strong> places</span>
                        </div>

                        <div v-if="loading" class="loading-state">
                            <div class="spinner"></div><p>Searching...</p>
                        </div>

                        <div v-else class="places-grid">
                            <div v-for="place in filteredPlaces" :key="place.id" class="ta-card list-card" @click="goToDetail(place.id)">
                                <div class="card-img-wrapper">
                                    <img :src="getCoverImage(place)" :alt="place.name" />
                                    
                                    <div class="slider-arrows" v-if="getPlaceImagesArray(place).length > 1">
                                        <button class="arrow-btn left" @click.stop="prevImage(place.id, place)"><i class="fas fa-chevron-left"></i></button>
                                        <button class="arrow-btn right" @click.stop="nextImage(place.id, place)"><i class="fas fa-chevron-right"></i></button>
                                    </div>
                                    <div class="slider-dots" v-if="getPlaceImagesArray(place).length > 1">
                                        <span v-for="(_, idx) in getPlaceImagesArray(place)" :key="idx" :class="['dot', { active: (currentImageIndices[place.id] || 0) === idx }]"></span>
                                    </div>

                                    <button v-if="!user || user.role !== 'admin'" class="btn-heart" :class="{ active: isFavorite(place.id) }" @click.stop="toggleHeart(place.id)">
                                        <i class="fas fa-heart"></i>
                                    </button>
                                </div>
                                <div class="card-info">
                                    <h3>{{ place.name }}</h3>
                                    <div class="rating-row mb-10">
                                        <i class="fas fa-star" style="color: #f59e0b;"></i>
                                        <span class="rating-num">{{ place.rating_avg || '0.0' }}</span>
                                        <span class="cat-text" style="margin-left: 10px;">• <i class="fas fa-map-marker-alt"></i> {{ getCategoryName(place.category_id) }}</span>
                                    </div>
                                    <p class="description">{{ place.description }}</p>
                                </div>
                            </div>
                        </div>

                        <div v-if="!loading && filteredPlaces.length === 0" class="empty-state">
                            <i class="fas fa-map-marked-alt"></i>
                            <p>No places found. Try adjusting your search.</p>
                        </div>
                    </main>
                </div>
            </section>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { placeRepository } from '@/repositories/placeRepository'
import { categoryRepository } from '@/repositories/categoryRepository'
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'
import { favoriteRepository } from '@/repositories/favoriteRepository'
import { useAuth } from '@/composables/useAuth'
import axios from 'axios'

const router = useRouter()
const { user } = useAuth()
const places = ref([])
const categories = ref([])
const loading = ref(true)
const searchQuery = ref('')
const selectedCategory = ref(null)
const favoriteIds = ref([])
const recommendedPlaces = ref([])

// 🔍 State สำหรับ Search Dropdown
const isSearchFocused = ref(false)

// 🏞️ ข้อมูลสำหรับ Hero Slider
const heroImages = [
    'https://images.unsplash.com/photo-1540202404-b711c0729ea2?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80',
    'https://images.unsplash.com/photo-1528181304800-259b08848526?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80',
    'https://images.unsplash.com/photo-1518509562904-e7ef99cdcc86?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80'
]
const currentHeroIndex = ref(0)
let heroInterval = null

// 📍 ตัวแปรสำหรับเลื่อนหน้าจอไปยังผลการค้นหา
const exploreAllSection = ref(null)
const executeSearch = () => {
    isSearchFocused.value = false; // ปิด dropdown
    if (exploreAllSection.value) {
        exploreAllSection.value.scrollIntoView({ behavior: 'smooth' })
    }
}

const currentImageIndices = ref({}) 

const getPlaceImagesArray = (place) => {
    const noImageUrl = 'data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22400%22%20height%3D%22300%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20fill%3D%22%23e2e8f0%22%2F%3E%3Ctext%20x%3D%2250%25%22%20y%3D%2250%25%22%20fill%3D%22%2364748b%22%20font-family%3D%22sans-serif%22%20font-size%3D%2220%22%20text-anchor%3D%22middle%22%20dy%3D%22.3em%22%3ENo%20Image%3C%2Ftext%3E%3C%2Fsvg%3E';
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
        if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) return url;
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

const filterByCategoryKeywords = (keywords) => {
    return places.value.filter(p => {
        const cat = categories.value.find(c => c.id === p.category_id);
        if (!cat) return false;
        const catName = cat.name.toLowerCase();
        return keywords.some(kw => catName.includes(kw.toLowerCase()));
    });
};

const foodPlaces = computed(() => filterByCategoryKeywords(['restaurant', 'coffee', 'cafe', 'food', 'ร้านอาหาร', 'คาเฟ่', 'กาแฟ', 'ของกิน']));
const naturePlaces = computed(() => filterByCategoryKeywords(['nature', 'ธรรมชาติ']));
const marketPlaces = computed(() => filterByCategoryKeywords(['market', 'walking street', 'ตลาด', 'ถนนคนเดิน']));
const landmarkPlaces = computed(() => filterByCategoryKeywords(['landmark', 'point of interest', 'สถานที่สำคัญ', 'จุดที่น่าสนใจ']));
const historicPlaces = computed(() => filterByCategoryKeywords(['historic', 'history', 'ประวัติศาสตร์']));
const sciencePlaces = computed(() => filterByCategoryKeywords(['science', 'museum', 'วิทยาศาสตร์', 'พิพิธภัณฑ์']));
const parkPlaces = computed(() => filterByCategoryKeywords(['park', 'สวน']));
const religiousPlaces = computed(() => filterByCategoryKeywords(['religious', 'sacred', 'temple', 'ศาสนา', 'ศักดิ์สิทธิ์', 'วัด']));

const topRatedPlaces = computed(() => {
    return [...places.value].sort((a, b) => (parseFloat(b.rating_avg) || 0) - (parseFloat(a.rating_avg) || 0)).slice(0, 8);
})

const fetchData = async () => {
    loading.value = true
    try {
        const [resPlaces, resCats] = await Promise.all([placeRepository.getAll(), categoryRepository.getAll()])
        places.value = resPlaces.data
        categories.value = resCats.data

        if (user.value && user.value.role !== 'admin') {
            try {
                const favRes = await favoriteRepository.getUserFavorites(user.value.id)
                favoriteIds.value = favRes.data.map(f => f.place_id)
            } catch (err) { console.warn("Cannot fetch favorites", err) }

            try {
                const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
                const aiRes = await axios.get(`${backendUrl}/api/recommendations/${user.value.id}?top_k=8`);
                if (aiRes.data.status === 'success') {
                    recommendedPlaces.value = aiRes.data.recommended_place_ids
                        .map(id => places.value.find(p => p.id === id))
                        .filter(p => p !== undefined);
                }
            } catch (aiErr) { console.warn("AI Not ready", aiErr); }
        }
    } catch (err) { console.error("API Error:", err) } finally { loading.value = false }
}

const filteredPlaces = computed(() => {
    return places.value.filter(p => {
        const matchesSearch = p.name.toLowerCase().includes(searchQuery.value.toLowerCase())
        const matchesCat = !selectedCategory.value || p.category_id === selectedCategory.value
        return matchesSearch && matchesCat
    })
})

const filterByCategory = (id) => selectedCategory.value = id
const resetFilters = () => { searchQuery.value = ''; selectedCategory.value = null }
const getCategoryName = (id) => categories.value.find(c => c.id === id)?.name || 'General'

const goToDetail = (id) => {
    router.push(`/places/${id}`)
}

const toggleHeart = async (placeId) => {
    if (!user.value) {
        return router.push('/login')
    }

    try {
        const res = await favoriteRepository.toggleFavorite(user.value.id, placeId)
        if (res.data.status === 'added') {
            favoriteIds.value.push(placeId)
            try {
                const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
                await axios.post(`${backendUrl}/api/interactions/`, { place_id: placeId, rating: 5, comment: "Liked", interaction_type: 'like' });
            } catch (aiErr) { }
        } else {
            favoriteIds.value = favoriteIds.value.filter(id => id !== placeId)
        }
    } catch (err) { console.error(err) }
}
const isFavorite = (id) => favoriteIds.value.includes(id)

onMounted(() => {
    fetchData()
    heroInterval = setInterval(() => {
        currentHeroIndex.value = (currentHeroIndex.value + 1) % heroImages.length
    }, 5000)
})

onUnmounted(() => {
    if (heroInterval) clearInterval(heroInterval)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

/* --- ปรับสีพื้นหลังให้ขาวสะอาดแบบ TripAdvisor --- */
.explore-page {
    background-color: #f7f9fa; /* สีเทาอ่อนมากๆ / ขาว */
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    color: #1e293b; /* อักษรสีเข้ม */
}

/* --- 🆕 Hero Banner --- */
.hero-section {
    height: 480px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: white;
    padding: 0 20px;
    position: relative;
    background-size: cover;
    background-position: center;
    transition: background-image 0.8s ease-in-out;
    z-index: 50; /* 🛠️ แก้ไขบั๊กหัวใจทะลุ: ปรับให้ Hero อยู่ชั้นบนสุด */
}

.hero-content {
    width: 100%;
    max-width: 900px;
    z-index: 52;
}

.hero-content h1 { 
    font-size: 3.5rem; 
    font-weight: 900; 
    margin-bottom: 15px; 
    text-shadow: 0 4px 15px rgba(0,0,0,0.6); 
    letter-spacing: -0.5px;
    color: white;
}

.hero-content p { 
    font-size: 1.3rem; 
    margin: 0 auto 40px; 
    opacity: 0.95; 
    text-shadow: 0 2px 8px rgba(0,0,0,0.6); 
    font-weight: 500;
    color: white;
}

/* 🔍 Search Container & Dropdown */
.hero-search-container {
    position: relative;
    max-width: 750px;
    margin: 0 auto;
    z-index: 60; /* ให้อยู่บนสุดเหนือทุกสิ่ง */
}

.hero-search-box {
    position: relative;
    display: flex;
    align-items: center;
    background: white;
    border-radius: 50px;
    padding: 8px 8px 8px 25px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.25);
    z-index: 62;
    transition: 0.3s;
}

.hero-search-box.dropdown-open {
    border-radius: 24px 24px 0 0;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    border-bottom: 1px solid #e2e8f0;
}

.hero-search-box i { font-size: 1.3rem; color: #1e293b; margin-right: 15px; }

.hero-search-box input {
    flex: 1; border: none; font-size: 1.15rem; color: #1e293b; outline: none; background: transparent; font-family: 'Inter', sans-serif;
}
.hero-search-box input::placeholder { color: #94a3b8; font-weight: 500; }

.btn-search-hero {
    background: #000; color: white; border: none; padding: 14px 32px; border-radius: 40px;
    font-size: 1.1rem; font-weight: 700; cursor: pointer; transition: 0.2s;
}
.btn-search-hero:hover { background: #334155; transform: scale(1.02); }

.search-overlay {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 60; background: rgba(0,0,0,0.3);
}

.search-dropdown {
    position: absolute; top: 100%; left: 0; right: 0; background: white; border-radius: 0 0 24px 24px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2); padding: 15px; z-index: 61; text-align: left;
}

.dropdown-item {
    display: flex; align-items: center; padding: 12px; cursor: pointer; border-radius: 12px; transition: 0.2s;
}
.dropdown-item:hover { background: #f1f5f9; }

.icon-box {
    width: 45px; height: 45px; border-radius: 12px; background: #f8fafc; border: 1px solid #e2e8f0;
    display: flex; justify-content: center; align-items: center; color: #1e293b; font-size: 1.1rem; margin-right: 15px;
}

.dropdown-img { width: 45px; height: 45px; border-radius: 12px; object-fit: cover; margin-right: 15px; }

.item-text { display: flex; flex-direction: column; }
.item-text strong { font-size: 1rem; color: #0f172a; font-weight: 700; }
.item-text small { font-size: 0.85rem; color: #64748b; }

.dropdown-divider { height: 1px; background: #e2e8f0; margin: 10px 0; }
.dropdown-group h4 { font-size: 0.85rem; color: #64748b; margin: 0 0 10px 10px; text-transform: uppercase; letter-spacing: 0.5px; }

.hero-dots { position: absolute; bottom: 25px; display: flex; gap: 10px; z-index: 52; }
.hero-dots .dot { width: 10px; height: 10px; background: rgba(255,255,255,0.4); border-radius: 50%; cursor: pointer; transition: 0.3s; }
.hero-dots .dot.active { background: white; transform: scale(1.3); }

@media (max-width: 768px) {
    .hero-content h1 { font-size: 2.2rem; }
    .hero-content p { font-size: 1rem; margin-bottom: 25px;}
    .hero-search-box { padding: 5px 5px 5px 15px; }
    .hero-search-box input { font-size: 0.95rem; }
    .btn-search-hero { padding: 10px 20px; font-size: 0.95rem; }
}

/* --- Main Layout --- */
.main-container { 
    max-width: 1400px; margin: 0 auto; padding: 40px 20px; 
    position: relative; z-index: 10; /* 🛠️ แก้ไขบั๊กหัวใจทะลุ: ให้ส่วนนี้อยู่ล่าง Hero เสมอ */
}

/* --- Horizontal Sections --- */
.horizontal-section { margin-bottom: 50px; }
.section-header { margin-bottom: 20px; }
.section-header h2 { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin: 0 0 5px; }
.section-header p { color: #475569; font-size: 0.95rem; margin: 0; }

.carousel-container { display: flex; overflow-x: auto; gap: 20px; padding-bottom: 20px; scroll-snap-type: x mandatory; scrollbar-width: thin; scrollbar-color: #cbd5e1 transparent; }
.carousel-container::-webkit-scrollbar { height: 8px; }
.carousel-container::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }

/* --- Cards --- */
.ta-card {
    background: white; border-radius: 16px; overflow: hidden; cursor: pointer;
    border: 1px solid #e2e8f0; transition: box-shadow 0.3s, transform 0.3s; flex: 0 0 280px; scroll-snap-align: start;
}
.ta-card:hover { box-shadow: 0 15px 35px rgba(0,0,0,0.1); transform: translateY(-5px); }
.ai-card { border: 2px solid #3498db; box-shadow: 0 4px 15px rgba(52, 152, 219, 0.1); }

.card-img-wrapper { position: relative; height: 190px; }
.card-img-wrapper img { width: 100%; height: 100%; object-fit: cover; transition: 0.3s; }

.rank-badge { position: absolute; top: 10px; left: 10px; background: #000; color: white; padding: 4px 10px; font-size: 0.75rem; font-weight: 800; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.3); }

.slider-arrows { opacity: 0; transition: opacity 0.2s ease-in-out; }
.card-img-wrapper:hover .slider-arrows { opacity: 1; }
.arrow-btn { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(255, 255, 255, 0.85); border: none; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; color: #1e293b; box-shadow: 0 2px 6px rgba(0,0,0,0.2); z-index: 5; transition: 0.2s; }
.arrow-btn:hover { background: white; transform: translateY(-50%) scale(1.1); }
.arrow-btn.left { left: 8px; } .arrow-btn.right { right: 8px; }

.slider-dots { position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%); display: flex; gap: 4px; z-index: 5; }
.dot { width: 6px; height: 6px; background: rgba(255, 255, 255, 0.6); border-radius: 50%; transition: 0.2s; }
.dot.active { background: white; transform: scale(1.3); }

.btn-heart { position: absolute; top: 10px; right: 10px; background: rgba(255,255,255,0.9); border: none; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.2); color: #94a3b8; transition: 0.2s; z-index: 10; }
.btn-heart.active { color: #ef4444; }
.btn-heart:hover { transform: scale(1.1); }

.card-info { padding: 16px; color: #1e293b; }
.card-info h3 { margin: 0 0 6px; font-size: 1.15rem; font-weight: 800; }
.truncate { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.rating-row { display: flex; align-items: center; margin-bottom: 6px; }
.bubbles i { color: #34d399; font-size: 0.8rem; margin-right: 2px; }
.rating-num { font-size: 0.9rem; font-weight: 700; margin-left: 6px; }
.cat-text { font-size: 0.85rem; color: #64748b; margin: 0; }
.cat-text i { color: #3498db; margin-right: 4px; }
.description { font-size: 0.85rem; color: #475569; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; margin-top: 10px; }

/* --- Explore All Section --- */
.mt-50 { margin-top: 50px; scroll-margin-top: 100px; } 
.mb-10 { margin-bottom: 10px; }
.explore-layout { display: grid; grid-template-columns: 300px 1fr; gap: 30px; margin-top: 20px; }

.sidebar { position: sticky; top: 90px; height: fit-content; }
.filter-card { background: white; padding: 25px; border-radius: 16px; border: 1px solid #e2e8f0; color: #1e293b; }
.filter-card h3 { margin: 0; font-size: 1.25rem; font-weight: 800; }
.filter-card h4 { margin: 15px 0 10px; font-size: 0.95rem; font-weight: 700; color: #475569; }
.mt-15 { margin-top: 15px; }

.input-with-icon { position: relative; display: flex; align-items: center; }
.input-with-icon i { position: absolute; left: 12px; color: #94a3b8; }
.input-with-icon input { width: 100%; padding: 10px 10px 10px 35px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.9rem; background: #f8fafc; outline: none; }
.input-with-icon input:focus { border-color: #3498db; }

.category-list { display: flex; flex-wrap: wrap; gap: 8px; }
.cat-pill { padding: 6px 14px; border-radius: 20px; border: 1px solid #cbd5e1; background: white; color: #475569; font-size: 0.85rem; font-weight: 600; cursor: pointer; transition: 0.2s; }
.cat-pill:hover { border-color: #000; color: #000; }
.cat-pill.active { background: #000; color: white; border-color: #000; }

.btn-clear { width: 100%; padding: 12px; margin-top: 20px; background: none; border: 1px solid #cbd5e1; border-radius: 8px; font-weight: 700; color: #1e293b; cursor: pointer; transition: 0.2s; }
.btn-clear:hover { background: #f1f5f9; }

.results-bar { margin-bottom: 20px; font-size: 1.1rem; color: #1e293b;}
.places-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 25px; }
.list-card { flex: none; }
.loading-state, .empty-state { text-align: center; padding: 100px 0; color: #64748b;}
.spinner { border: 4px solid #e2e8f0; border-top: 4px solid #000; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 20px; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

@media (max-width: 992px) { .explore-layout { grid-template-columns: 1fr; } .sidebar { position: relative; top: 0; margin-bottom: 20px; } }
</style>