<template>
    <div class="explore-page">
        <Navbar />

        <div class="explore-container">
            <button @click="router.push('/explore')" class="btn-back-link">
                <i class="fas fa-chevron-left"></i> Back to Explore
            </button>

            <div class="page-tabs">
                <button class="tab-btn" :class="{ active: activeTab === 'places' }" @click="activeTab = 'places'">
                    <i class="fas fa-heart"></i> Favorite Places
                </button>
                <button class="tab-btn" :class="{ active: activeTab === 'trips' }" @click="activeTab = 'trips'">
                    <i class="fas fa-route"></i> My Saved Trips
                </button>
            </div>

            <div v-if="activeTab === 'places'">
                <div class="results-info">
                    <h2>My Favorites <span class="count-badge">{{ favorites.length }} places</span></h2>
                </div>

                <div v-if="loading" class="loading-state">
                    <div class="spinner"></div>
                    <p>Loading your favorites...</p>
                </div>

                <div v-else class="places-grid">
                    <div v-for="fav in favorites" :key="fav.id" class="modern-card"
                        @click="goToDetail(fav.place.id)">
                        
                        <div class="card-media">
                            <img :src="getCoverImage(fav.place.image_url)"
                                :alt="fav.place.name" @error="handleImgError" />
                            <button class="btn-heart active" @click.stop="toggleHeart(fav.place.id)">
                                <i class="fas fa-heart"></i>
                            </button>
                        </div>

                        <div class="card-details">
                            <h3>{{ fav.place.name }}</h3>
                            <p class="description">{{ fav.place.description }}</p>

                            <div class="card-footer">
                                <div class="rating">
                                    <i class="fas fa-star"></i>
                                    <span>{{ fav.place.rating_avg || '0.0' }}</span>
                                </div>
                                <span class="view-link">View Details <i class="fas fa-arrow-right"></i></span>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-if="!loading && favorites.length === 0" class="empty-state">
                    <i class="fas fa-heart-broken" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                    <p>You haven't saved any favorites yet. Explore and tap the heart icon!</p>
                    <button @click="router.push('/explore')" class="btn-explore-now">Explore Places</button>
                </div>
            </div>

            <div v-else>
                <div class="results-info">
                    <h2>Saved Itineraries <span class="count-badge">{{ itineraries.length }} plans</span></h2>
                </div>

                <div v-if="loading" class="loading-state">
                    <div class="spinner"></div>
                    <p>Loading your trips...</p>
                </div>

                <div v-else class="trips-grid">
                    <div v-for="itinerary in itineraries" :key="itinerary.id" class="itinerary-modern-card"
                         @click="viewItinerary(itinerary.id)">
                        <div class="itinerary-card-header">
                            <div class="icon-wrap">
                                <i class="fas fa-map-marked-alt"></i>
                            </div>
                            <div class="title-wrap">
                                <h3>{{ itinerary.title }}</h3>
                                <p>{{ itinerary.days }} Days • {{ formatDate(itinerary.created_at) }}</p>
                            </div>
                            <button class="btn-delete" @click.stop="deleteItinerary(itinerary.id)">
                                <i class="fas fa-trash-alt"></i>
                            </button>
                        </div>
                        <div class="itinerary-card-content">
                            <div class="preview-line">
                                <div v-for="day in itinerary.days" :key="day" class="day-bubble">
                                    D{{ day }}
                                </div>
                            </div>
                            <div class="itinerary-footer">
                                <span>{{ itinerary.items.length }} Locations added</span>
                                <span class="view-link">View Plan <i class="fas fa-chevron-right"></i></span>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-if="!loading && itineraries.length === 0" class="empty-state">
                    <i class="fas fa-suitcase-rolling" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                    <p>You haven't created any trip plans yet. Use our AI Trip Planner!</p>
                    <button @click="router.push('/trip-planner')" class="btn-explore-now">Plan a Trip</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import { favoriteRepository } from '@/repositories/favoriteRepository'
import { userRepository } from '@/repositories/userRepository'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { user } = useAuth()
const favorites = ref([])
const itineraries = ref([])
const loading = ref(true)
const activeTab = ref('places') // 'places' or 'trips'

const fetchData = async () => {
    loading.value = true
    try {
        if (!user.value) {
            router.push('/login')
            return
        }
        
        const [favRes, itRes] = await Promise.all([
            favoriteRepository.getUserFavorites(user.value.id),
            userRepository.getItineraries(user.value.id)
        ])
        
        favorites.value = favRes.data
        itineraries.value = itRes.data
    } catch (err) {
        console.error("Error fetching data:", err)
    } finally {
        loading.value = false
    }
}

const viewItinerary = (id) => {
    router.push({ name: 'TripPlanner', query: { id: id }})
}

const deleteItinerary = async (id) => {
    if (confirm("Delete this trip plan?")) {
        try {
            await userRepository.deleteItinerary(id)
            itineraries.value = itineraries.value.filter(it => it.id !== id)
        } catch (err) {
            console.error(err)
        }
    }
}

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', { 
        year: 'numeric', month: 'short', day: 'numeric' 
    })
}

const getCoverImage = (imgData) => {
    const noImageUrl = 'https://via.placeholder.com/400x300?text=Savannakhet'
    if (!imgData) return noImageUrl
    
    let urls = []
    if (typeof imgData === 'string' && imgData.trim().startsWith('[')) {
        try { urls = JSON.parse(imgData) } catch (e) { urls = [imgData] }
    } else {
        urls = [imgData]
    }
    
    const url = urls[0]
    if (!url) return noImageUrl
    if (url.startsWith('http') || url.startsWith('data:')) return url
    return `http://localhost:8000${url.startsWith('/') ? '' : '/'}${url}`
}

const handleImgError = (e) => {
    e.target.src = 'https://via.placeholder.com/400x300?text=Image+Not+Found'
}

const goToDetail = (id) => {
    router.push(`/places/${id}`)
}

const toggleHeart = async (placeId) => {
    if (!user.value) return
    try {
        await favoriteRepository.toggleFavorite(user.value.id, placeId)
        fetchData()
    } catch (err) {
        console.error(err)
    }
}

onMounted(fetchData)
</script>

<style scoped>
.explore-page {
    background: linear-gradient(135deg, #1e5799 0%, #2989d8 50%, #207cca 100%) !important;
    min-height: 100vh;
    width: 100%;
}

.btn-back-link {
    background: rgba(255, 255, 255, 0.2);
    border: none;
    color: white;
    padding: 10px 20px;
    border-radius: 50px;
    cursor: pointer;
    margin-bottom: 25px;
    font-weight: 600;
    transition: 0.3s;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.btn-back-link:hover {
    background: rgba(255, 255, 255, 0.35);
    transform: translateX(-5px);
}

.explore-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px 20px;
}

.results-info h2 {
    font-size: 1.8rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 30px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.page-tabs {
    display: flex;
    gap: 15px;
    margin-bottom: 40px;
    background: rgba(255, 255, 255, 0.15);
    padding: 8px;
    border-radius: 60px;
    width: fit-content;
}

.tab-btn {
    padding: 12px 25px;
    border-radius: 50px;
    border: none;
    background: transparent;
    color: white;
    font-weight: 700;
    cursor: pointer;
    transition: 0.3s;
    display: flex;
    align-items: center;
    gap: 10px;
}

.tab-btn.active {
    background: white;
    color: #207cca;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.tab-btn:hover:not(.active) {
    background: rgba(255, 255, 255, 0.1);
}

.trips-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 25px;
}

.itinerary-modern-card {
    background: white;
    border-radius: 20px;
    padding: 25px;
    cursor: pointer;
    transition: 0.3s;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.itinerary-modern-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.18);
}

.itinerary-card-header {
    display: flex;
    gap: 15px;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 1px dashed #e2e8f0;
}

.icon-wrap {
    width: 45px;
    height: 45px;
    background: #f0fdf4;
    color: #10b981;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
}

.title-wrap h3 {
    margin: 0;
    font-size: 1.15rem;
    color: #1e293b;
}

.title-wrap p {
    margin: 3px 0 0;
    font-size: 0.85rem;
    color: #64748b;
}

.btn-delete {
    margin-left: auto;
    background: #fee2e2;
    color: #ef4444;
    border: none;
    width: 35px;
    height: 35px;
    border-radius: 50%;
    cursor: pointer;
    transition: 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn-delete:hover {
    background: #ef4444;
    color: white;
}

.itinerary-card-content {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.preview-line {
    display: flex;
    gap: 8px;
}

.day-bubble {
    background: #f1f5f9;
    color: #475569;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 800;
}

.itinerary-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #64748b;
    font-size: 0.85rem;
    font-weight: 600;
}

@media (max-width: 600px) {
    .page-tabs { width: 100%; justify-content: center; }
    .trips-grid { grid-template-columns: 1fr; }
}

.count-badge {
    color: #ffd700;
}

.places-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 25px;
}

.modern-card {
    background: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
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

.btn-heart {
    position: absolute;
    top: 15px;
    right: 15px;
    background: rgba(255,255,255,0.9);
    border: none;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    transition: 0.2s;
    color: #94a3b8;
}

.btn-heart.active {
    color: #ef4444; /* red heart */
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
    gap: 7px;
}

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

.btn-explore-now {
    margin-top: 20px;
    padding: 12px 24px;
    background: #3498db;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 50px;
    cursor: pointer;
    transition: 0.3s;
}

.btn-explore-now:hover {
    background: #2980b9;
    transform: scale(1.05);
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
