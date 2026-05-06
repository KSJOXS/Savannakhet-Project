<template>
    <div class="recently-viewed-section" v-if="recentPlaces.length > 0">
        <div class="section-header">
            <h2 class="section-title">
                <i class="fas fa-history title-icon"></i>
                {{ t('recentlyViewed.title') }}
            </h2>
            <button class="btn-clear-all" @click="clearHistory" v-if="recentPlaces.length > 0">
                {{ t('common.clear') || 'Clear' }}
            </button>
        </div>

        <div class="recent-scroll-container">
            <div class="recent-grid">
                <div v-for="place in recentPlaces" :key="place.id" class="recent-card" @click="goToDetail(place.id)">
                    <div class="img-wrapper">
                        <img :src="getCoverImage(place)" :alt="place.name" @error="handleImgError" />
                        <span class="category-badge">{{ getCategoryName(place.category_id) }}</span>
                        <div class="img-overlay"></div>
                        <button class="btn-heart" @click.stop="toggleHeart(place.id)" :class="{ active: isFavorite(place.id) }">
                            <i :class="isFavorite(place.id) ? 'fas fa-heart' : 'far fa-heart'"></i>
                        </button>
                    </div>
                    
                    <div class="card-content">
                        <span class="viewed-label">PREVIOUSLY VISITED</span>
                        <h4 class="place-name" :title="place.name">{{ place.name }}</h4>
                        <div class="rating-bar">
                            <div class="stars">
                                <i v-for="s in 5" :key="s" 
                                   :class="[getStarClass(place.rating_avg, s), 'fa-star']"></i>
                            </div>
                            <span class="rating-text">{{ place.rating_avg ? parseFloat(place.rating_avg).toFixed(1) : '0.0' }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { placeRepository } from '@/repositories/placeRepository'
import { categoryRepository } from '@/repositories/categoryRepository'
import { favoriteRepository } from '@/repositories/favoriteRepository'
import { useI18n } from '@/composables/useI18n'
import axios from 'axios'

const { t } = useI18n()
const router = useRouter()
const recentPlaces = ref([])
const categories = ref([])
const favoriteIds = ref([])
const user = ref(JSON.parse(localStorage.getItem('user')))

const fetchData = async () => {
    try {
        const [resPlaces, resCats] = await Promise.all([
            placeRepository.getAll(),
            categoryRepository.getAll()
        ])
        categories.value = resCats.data

        let rvIds = JSON.parse(localStorage.getItem('recently_viewed') || '[]')
        
        // Map places preserving order of rvIds, limit to 8
        recentPlaces.value = rvIds
            .map(id => resPlaces.data.find(p => p.id === id))
            .filter(p => p !== undefined)
            .slice(0, 8)

        if (user.value) {
            try {
                const favRes = await favoriteRepository.getUserFavorites(user.value.id)
                favoriteIds.value = favRes.data.map(f => f.place_id)
            } catch (favErr) {
                console.warn("Could not fetch favorites:", favErr)
            }
        }
    } catch (err) {
        console.error("Error fetching recently viewed:", err)
    }
}

const getCategoryName = (id) => {
    const cat = categories.value.find(c => c.id === id)
    return cat ? cat.name : 'Attraction'
}

const getCoverImage = (place) => {
    const noImageUrl = 'https://images.unsplash.com/photo-1540611025311-01df3cef54b5?q=80&w=800'
    let url = ''
    
    if (place.images && Array.isArray(place.images) && place.images.length > 0) {
        url = place.images[0].image_url || place.images[0].url || place.images[0]
    } else if (place.image_url) {
        try {
            if (typeof place.image_url === 'string' && place.image_url.trim().startsWith('[')) {
                const parsed = JSON.parse(place.image_url)
                url = parsed[0]
            } else {
                url = place.image_url
            }
        } catch (e) { url = place.image_url }
    }

    if (!url) return noImageUrl
    
    if (url.startsWith('http')) return url
    
    const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    return `${backendUrl}${url.startsWith('/') ? '' : '/'}${url}`
}

const handleImgError = (e) => {
    e.target.src = 'https://images.unsplash.com/photo-1540611025311-01df3cef54b5?q=80&w=800'
}

const getStarClass = (rating, star) => {
    const r = parseFloat(rating) || 0
    if (r >= star) return 'fas'
    if (r >= star - 0.5) return 'fas fa-star-half-alt'
    return 'far'
}

const isFavorite = (id) => favoriteIds.value.includes(id)

const toggleHeart = async (id) => {
    if (!user.value) return router.push('/login')
    try {
        const res = await favoriteRepository.toggleFavorite(user.value.id, id)
        if (res.data.status === 'added') {
            favoriteIds.value.push(id)
            const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
            await axios.post(`${backendUrl}/api/interactions/`, {
                place_id: id, rating: 5, comment: "Liked", interaction_type: 'like'
            }).catch(()=>{});
        }
        else favoriteIds.value = favoriteIds.value.filter(fid => fid !== id)
    } catch (e) { console.error(e) }
}

const goToDetail = (id) => {
    router.push(`/places/${id}`)
}

const clearHistory = () => {
    localStorage.removeItem('recently_viewed')
    recentPlaces.value = []
}

onMounted(fetchData)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:wght@700;800;900&display=swap');

.recently-viewed-section {
    max-width: 1400px;
    margin: 80px auto;
    padding: 0 40px;
    font-family: 'Inter', sans-serif;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.section-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #0f172a;
    font-family: 'Playfair Display', serif;
    display: flex;
    align-items: center;
    gap: 15px;
    margin: 0;
}

.title-icon {
    color: #000;
    font-size: 1.5rem;
}

.btn-clear-all {
    background: none;
    border: none;
    color: #64748b;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: color 0.2s;
}

.btn-clear-all:hover {
    color: #ef4444;
}

.recent-scroll-container {
    overflow-x: auto;
    padding-bottom: 15px;
    scrollbar-width: thin;
    scrollbar-color: #e2e8f0 transparent;
}

.recent-scroll-container::-webkit-scrollbar {
    height: 6px;
}

.recent-scroll-container::-webkit-scrollbar-thumb {
    background: #e2e8f0;
    border-radius: 10px;
}

.recent-grid {
    display: flex;
    gap: 24px;
    padding: 4px;
}

.recent-card {
    flex: 0 0 320px;
    position: relative;
    background: #0f172a;
    border-radius: 4px;
    overflow: hidden;
    height: 400px;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    border: none;
}

.recent-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.5);
}

.img-wrapper {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
}

.img-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s ease;
}

.recent-card:hover .img-wrapper img {
    transform: scale(1.1);
}

.img-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, 
        rgba(0,0,0,0) 0%, 
        rgba(0,0,0,0.2) 40%, 
        rgba(0,0,0,0.7) 80%, 
        rgba(0,0,0,0.9) 100%);
    z-index: 1;
}

.btn-heart {
    position: absolute;
    top: 15px;
    right: 15px;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(8px);
    border: none;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    color: #94a3b8;
    transition: all 0.3s;
    z-index: 5;
}

.btn-heart:hover {
    transform: scale(1.2);
    background: white;
    color: #ef4444;
}

.btn-heart.active {
    color: #ef4444;
    background: white;
}

.category-badge {
    position: absolute;
    bottom: 15px;
    left: 15px;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(8px);
    color: #1e293b;
    padding: 5px 12px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.card-content {
    position: relative;
    z-index: 2;
    padding: 24px;
    margin-top: auto;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    pointer-events: none;
}

.place-name {
    margin: 0 0 5px 0;
    font-size: 1.8rem;
    font-weight: 800;
    font-family: 'Playfair Display', serif;
    color: white;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.2;
}

.rating-bar {
    display: flex;
    align-items: center;
    gap: 10px;
}

.stars {
    color: #f59e0b;
    font-size: 0.9rem;
    display: flex;
    gap: 2px;
}

.rating-text {
    font-size: 0.9rem;
    font-weight: 800;
    color: rgba(255, 255, 255, 0.7);
}

.viewed-label {
    color: rgba(255, 255, 255, 0.5);
    font-size: 0.6rem;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 5px;
}

.category-badge {
    position: absolute;
    top: 24px;
    left: 24px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    color: white;
    padding: 6px 14px;
    border-radius: 4px;
    font-size: 0.65rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    z-index: 5;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

@media (max-width: 768px) {
    .recent-card {
        flex: 0 0 240px;
    }
    .section-title {
        font-size: 1.3rem;
    }
}
</style>
