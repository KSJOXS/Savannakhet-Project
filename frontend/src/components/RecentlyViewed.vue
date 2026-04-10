<template>
    <div class="recently-viewed-section" v-if="recentPlaces.length > 0">
        <h2 class="section-title">{{ t('recentlyViewed.title') }}</h2>
        <div class="recent-grid">
            <div v-for="place in recentPlaces" :key="place.id" class="recent-card" @click="goToDetail(place.id)">
                <div class="img-container">
                    <img :src="getCoverImage(place)" :alt="place.name" />
                    <button class="btn-heart" @click.stop="toggleHeart(place.id)" :class="{ active: isFavorite(place.id) }">
                        <i :class="isFavorite(place.id) ? 'fas fa-heart' : 'far fa-heart'"></i>
                    </button>
                </div>
                <div class="info-container">
                    <h4 class="truncate-text" :title="place.name">{{ place.name }}</h4>
                    <div class="rating-row">
                        <span class="rating-num">{{ place.rating_avg ? parseFloat(place.rating_avg).toFixed(1) : 'New' }}</span>
                        <div class="bubbles">
                            <i v-for="s in 5" :key="s" :class="[(place.rating_avg || 0) >= s ? 'fas' : 'far', 'fa-circle']"></i>
                        </div>
                    </div>
                    <p class="category-name">{{ getCategoryName(place.category_id) }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
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
        
        // Map places preserving order of rvIds
        recentPlaces.value = rvIds
            .map(id => resPlaces.data.find(p => p.id === id))
            .filter(p => p !== undefined)

        if (user.value) {
            const favRes = await favoriteRepository.getUserFavorites(user.value.id)
            favoriteIds.value = favRes.data.map(f => f.place_id)
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
    let url = ''
    if (place.images && place.images.length > 0) {
        url = place.images[0].image_url || place.images[0].url || place.images[0]
    } else if (place.image_url) {
        try {
            if (place.image_url.startsWith('[')) {
                url = JSON.parse(place.image_url)[0]
            } else {
                url = place.image_url
            }
        } catch (e) { url = place.image_url }
    }
    if (!url) return 'https://via.placeholder.com/300x250?text=No+Image'
    return url.startsWith('http') ? url : `http://localhost:8000/${url.replace(/^\//,'')}`
}

const isFavorite = (id) => favoriteIds.value.includes(id)

const toggleHeart = async (id) => {
    if (!user.value) return router.push('/login')
    try {
        const res = await favoriteRepository.toggleFavorite(user.value.id, id)
        if (res.data.status === 'added') {
            favoriteIds.value.push(id)
            const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            await axios.post(`${backendUrl}/api/interactions/`, {
                place_id: id, rating: 5, comment: "Liked", interaction_type: 'like'
            }).catch(()=>{});
        }
        else favoriteIds.value = favoriteIds.value.filter(fid => fid !== id)
    } catch (e) { console.error(e) }
}

const goToDetail = (id) => {
    router.push(`/places/${id}`).then(() => {
        window.location.reload()
    })
}

onMounted(fetchData)
</script>

<style scoped>
.recently-viewed-section {
    max-width: 1200px;
    margin: 40px auto 60px;
    padding: 0 20px;
    font-family: 'Inter', sans-serif;
}

.section-title {
    font-size: 1.6rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 20px;
}

.recent-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
}

.recent-card {
    background: transparent;
    cursor: pointer;
    transition: transform 0.2s ease;
    display: flex;
    flex-direction: column;
}

.recent-card:hover {
    transform: translateY(-2px);
}

.img-container {
    position: relative;
    width: 100%;
    aspect-ratio: 1 / 1;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 12px;
}

.img-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.recent-card:hover .img-container img {
    transform: scale(1.05);
}

.btn-heart {
    position: absolute;
    top: 12px;
    right: 12px;
    background: white;
    border: none;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    font-size: 1rem;
    color: #94a3b8;
    transition: 0.2s;
    z-index: 10;
}

.btn-heart:hover {
    transform: scale(1.1);
}

.btn-heart.active {
    color: #ef4444;
}

.info-container {
    padding: 0 4px;
}

.info-container h4 {
    margin: 0 0 6px 0;
    font-size: 1.05rem;
    font-weight: 800;
    color: #0f172a;
}

.truncate-text {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.rating-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
    font-size: 0.85rem;
}

.rating-num {
    font-weight: 700;
    color: #334155;
}

.bubbles i {
    color: #00aa6c;
    font-size: 0.75rem;
    margin-right: 2px;
}

.category-name {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0;
    line-height: 1.4;
}

@media (max-width: 1024px) {
    .recent-grid { grid-template-columns: repeat(3, 1fr); }
}

@media (max-width: 768px) {
    .recent-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 480px) {
    .recent-grid {
        display: flex;
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        gap: 16px;
        padding-bottom: 10px;
    }
    .recent-card {
        min-width: 240px;
        scroll-snap-align: start;
    }
}
</style>
