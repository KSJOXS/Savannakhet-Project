<template>
    <div class="explore-page">
        <Navbar />

        <div class="explore-container">
            <button @click="router.back()" class="btn-back-link">
                <i class="fas fa-chevron-left"></i> Back
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
                         @click="viewItinerary(itinerary)">
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

        <!-- Itinerary Modal -->
        <div v-if="selectedItinerary" class="modal-overlay" @click="closeItineraryModal">
            <div class="modal-content itinerary-modal" @click.stop>
                <div class="modal-header">
                    <h2>{{ selectedItinerary.title }}</h2>
                    <button class="btn-close" @click="closeItineraryModal"><i class="fas fa-times"></i></button>
                </div>
                <div class="modal-body">
                    <div class="itinerary-meta-large">
                        <span class="meta-pill"><i class="fas fa-calendar-day"></i> {{ selectedItinerary.days }} Days</span>
                        <span class="meta-pill"><i class="fas fa-clock"></i> {{ formatDate(selectedItinerary.created_at) }}</span>
                    </div>
                    
                    <div class="timeline-container-mini">
                        <div class="day-section" v-for="day in selectedItinerary.days" :key="day">
                            <h3 class="day-heading">Day {{ day }}</h3>
                            <div class="timeline">
                                <div class="timeline-item" v-for="item in selectedItinerary.items.filter(i => i.day === day)" :key="item.id">
                                    <div class="time-marker">
                                        <span class="time">{{ item.time }}</span>
                                        <div class="marker-dot"></div>
                                        <div class="marker-line"></div>
                                    </div>
                                    
                                    <div class="timeline-content">
                                        <div class="slot-label">
                                            <i v-if="item.time_slot === 'Morning'" class="fas fa-sun text-warning"></i>
                                            <i v-else-if="item.time_slot === 'Afternoon'" class="fas fa-cloud-sun text-orange"></i>
                                            <i v-else class="fas fa-moon text-indigo"></i>
                                            {{ item.time_slot }}
                                        </div>
                                        
                                        <div class="place-card-mini" @click="$router.push(`/places/${item.place_id}`)">
                                            <div class="place-img-mini">
                                                <img :src="getCoverImage(item.place?.image_url)" alt="place" />
                                            </div>
                                            <div class="place-info-mini">
                                                <h4>{{ item.place?.name || 'Unknown Place' }}</h4>
                                                <div class="rating-mini">
                                                    <i class="fas fa-star text-warning"></i> {{ item.place?.rating_avg || 'New' }}
                                                </div>
                                            </div>
                                            <i class="fas fa-chevron-right arrow-icon"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
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
const selectedItinerary = ref(null)

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

const viewItinerary = (itinerary) => {
    selectedItinerary.value = itinerary
    document.body.style.overflow = 'hidden' // Prevent scrolling
}

const closeItineraryModal = () => {
    selectedItinerary.value = null
    document.body.style.overflow = ''
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
    return `http://127.0.0.1:8000${url.startsWith('/') ? '' : '/'}${url}`
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

/* Modal Styles */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(4px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    padding: 20px;
}

.modal-content.itinerary-modal {
    background: white;
    width: 100%;
    max-width: 600px;
    max-height: 85vh;
    border-radius: 24px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 20px 50px rgba(0,0,0,0.2);
    animation: slideUp 0.3s ease-out;
    overflow: hidden;
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 25px;
    border-bottom: 1px solid #e2e8f0;
    background: #f8fafc;
    color: #1e293b;
}

.modal-header h2 {
    margin: 0;
    font-size: 1.4rem;
    color: #0f172a;
    font-weight: 800;
    text-shadow: none;
}

.btn-close {
    background: #e2e8f0;
    border: none;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: #64748b;
    transition: 0.2s;
}

.btn-close:hover {
    background: #cbd5e1;
    color: #0f172a;
}

.modal-body {
    padding: 25px;
    overflow-y: auto;
    flex: 1;
    color: #1e293b;
}

.itinerary-meta-large {
    display: flex;
    gap: 10px;
    margin-bottom: 30px;
}

.meta-pill {
    background: #f1f5f9;
    color: #475569;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Timeline Mini */
.timeline-container-mini {
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.day-heading {
    font-size: 1.2rem;
    color: #22c55e;
    font-weight: 800;
    margin: 0 0 15px;
    padding-bottom: 10px;
    border-bottom: 2px dashed #e2e8f0;
    text-shadow: none;
}

.timeline {
    padding-left: 5px;
}

.timeline-item {
    display: flex;
    gap: 20px;
    position: relative;
    margin-bottom: 20px;
}

.timeline-item:last-child {
    margin-bottom: 0;
}

.timeline-item:last-child .marker-line {
    display: none;
}

.time-marker {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 60px;
    flex-shrink: 0;
    position: relative;
}

.time {
    font-weight: 800;
    font-size: 0.95rem;
    color: #0f172a;
    background: #f1f5f9;
    padding: 4px 8px;
    border-radius: 8px;
    margin-bottom: 8px;
}

.marker-dot {
    width: 14px;
    height: 14px;
    background: white;
    border: 3px solid #3b82f6;
    border-radius: 50%;
    z-index: 2;
}

.marker-line {
    position: absolute;
    top: 40px;
    bottom: -30px;
    left: 50%;
    transform: translateX(-50%);
    width: 2px;
    background: #e2e8f0;
    z-index: 1;
}

.timeline-content {
    flex: 1;
    padding-top: 5px;
}

.slot-label {
    font-size: 0.85rem;
    font-weight: 700;
    color: #64748b;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.text-warning { color: #f59e0b; }
.text-orange { color: #f97316; }
.text-indigo { color: #6366f1; }

.place-card-mini {
    display: flex;
    align-items: center;
    gap: 15px;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 10px;
    cursor: pointer;
    transition: 0.2s;
}

.place-card-mini:hover {
    border-color: #3b82f6;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
    transform: translateX(4px);
}

.place-img-mini {
    width: 60px;
    height: 60px;
    border-radius: 8px;
    overflow: hidden;
    flex-shrink: 0;
}

.place-img-mini img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.place-info-mini {
    flex: 1;
}

.place-info-mini h4 {
    margin: 0 0 4px;
    font-size: 1rem;
    color: #1e293b;
    text-shadow: none;
}

.rating-mini {
    font-size: 0.85rem;
    color: #64748b;
    font-weight: 600;
}

.arrow-icon {
    color: #cbd5e1;
    font-size: 1.2rem;
    margin-right: 10px;
}

.place-card-mini:hover .arrow-icon {
    color: #3b82f6;
}
</style>
