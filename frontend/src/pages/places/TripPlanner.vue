<template>
    <div class="trip-planner-page">
        <Navbar />

        <div class="planner-header">
            <div class="header-container">
                <div class="text-zone">
                    <div class="header-badge">
                        <i class="fas fa-magic"></i>
                        <span>AI Powered Itinerary</span>
                    </div>
                    <h1>Smart Trip Planner</h1>
                    <p class="subtitle">Let us organize your perfect trip to Savannakhet based on your lifestyle.</p>
                </div>
            </div>
        </div>

        <div class="planner-container">
            <!-- Input Form -->
            <div class="planner-card setup-card" v-if="!itinerary">
                <h2>How many days do you want to travel?</h2>
                <div class="days-selector">
                    <div class="day-option" :class="{ active: days === 1 }" @click="days = 1">
                        <span class="num">1</span>
                        <span class="text">Day</span>
                    </div>
                    <div class="day-option" :class="{ active: days === 2 }" @click="days = 2">
                        <span class="num">2</span>
                        <span class="text">Days</span>
                    </div>
                    <div class="day-option" :class="{ active: days === 3 }" @click="days = 3">
                        <span class="num">3</span>
                        <span class="text">Days</span>
                    </div>
                </div>

                <button class="btn-generate" @click="generateItinerary" :disabled="loading">
                    <i class="fas fa-spinner fa-spin" v-if="loading"></i>
                    <i class="fas fa-magic" v-else></i>
                    {{ loading ? 'Creating your perfect trip...' : 'Generate My Itinerary' }}
                </button>
            </div>

            <!-- Itinerary Result -->
            <div class="itinerary-result" v-else>
                <div class="result-header">
                    <h2>Your {{ days }}-Day Savannakhet Itinerary</h2>
                    <div class="action-buttons">
                        <button v-if="user" class="btn-save" @click="saveItinerary" :disabled="saving">
                            <i class="fas fa-spinner fa-spin" v-if="saving"></i>
                            <i class="fas fa-bookmark" v-else></i>
                            {{ saving ? 'Saving...' : 'Save to My Trips' }}
                        </button>
                        <button class="btn-outline" @click="resetPlanner">
                            <i class="fas fa-redo"></i> Plan Another Trip
                        </button>
                    </div>
                </div>

                <div v-if="saveSuccess" class="save-success-alert">
                    <i class="fas fa-check-circle"></i>
                    <span>Itinerary saved successfully! You can find it in your profile.</span>
                </div>

                <div class="timeline-container">
                    <div class="day-section" v-for="(plan, dayLabel) in itinerary" :key="dayLabel">
                        <div class="day-header">
                            <h3>{{ dayLabel }}</h3>
                        </div>

                        <div class="timeline">
                            <div class="timeline-item" v-for="(slot, index) in plan" :key="index">
                                <div class="time-marker">
                                    <span class="time">{{ slot.time }}</span>
                                    <div class="marker-dot"></div>
                                    <div class="marker-line" v-if="index !== plan.length - 1"></div>
                                </div>
                                
                                <div class="timeline-content">
                                    <div class="slot-label">
                                        <i v-if="slot.time_slot === 'Morning'" class="fas fa-sun" style="color: #f59e0b;"></i>
                                        <i v-else-if="slot.time_slot === 'Afternoon'" class="fas fa-cloud-sun" style="color: #f97316;"></i>
                                        <i v-else class="fas fa-moon" style="color: #6366f1;"></i>
                                        {{ slot.time_slot }}
                                    </div>
                                    
                                    <div class="place-card" @click="goToDetail(slot.place.id)">
                                        <div class="place-img">
                                            <img :src="getCoverImage(slot.place.image_url)" :alt="slot.place.name" @error="handleImgError" />
                                            <div class="match-badge" v-if="slot.is_preferred">🔥 Perfect Match</div>
                                        </div>
                                        <div class="place-info">
                                            <h4>{{ slot.place.name }}</h4>
                                            <div class="rating-cat">
                                                <span class="rating"><i class="fas fa-star" style="color: #f59e0b;"></i> {{ slot.place.rating_avg || 'New' }}</span>
                                                <span class="dot">•</span>
                                                <span class="cat">{{ slot.category_name }}</span>
                                            </div>
                                            <p class="desc">{{ slot.place.description }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <SectionDivider icon="fas fa-map-marked-alt" />
        <RecentlyViewed />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import Navbar from '@/components/Navbar.vue'
import SectionDivider from '@/components/SectionDivider.vue'
import RecentlyViewed from '@/components/RecentlyViewed.vue'
import api from '@/services/api'

const router = useRouter()
const route = useRoute()
const { user } = useAuth()
const days = ref(2)
const loading = ref(false)
const saving = ref(false)
const saveSuccess = ref(false)
const itinerary = ref(null)

const generateItinerary = async () => {
    loading.value = true
    try {
        const payload = { days: days.value }
        if (user.value) {
            payload.user_id = user.value.id
        }
        
        const response = await api.post('/api/itinerary/generate', payload)
        itinerary.value = response.data
    } catch (error) {
        console.error("Error generating itinerary:", error)
        alert("Failed to generate itinerary. Please try again.")
    } finally {
        loading.value = false
    }
}

const resetPlanner = () => {
    itinerary.value = null
    saveSuccess.value = false
    if (route.query.id) {
        router.push('/trip-planner')
    }
}

const saveItinerary = async () => {
    if (!user.value) {
        router.push('/login')
        return
    }

    saving.value = true
    try {
        const items = []
        // Convert itinerary object into flat array for saving
        Object.entries(itinerary.value).forEach(([dayLabel, plan]) => {
            const dayNum = parseInt(dayLabel.replace('Day ', ''))
            plan.forEach(slot => {
                items.push({
                    day: dayNum,
                    time_slot: slot.time_slot,
                    time: slot.time,
                    place_id: slot.place.id
                })
            })
        })

        const payload = {
            user_id: user.value.id,
            title: `My ${days.value}-Day Trip to Savannakhet`,
            days: days.value,
            items: items
        }

        await api.post('/api/itinerary/save', payload)
        saveSuccess.value = true
        setTimeout(() => {
            saveSuccess.value = false
        }, 5000)
    } catch (error) {
        console.error("Error saving itinerary:", error)
        alert("Failed to save itinerary. Please try again.")
    } finally {
        saving.value = false
    }
}

const goToDetail = (id) => {
    router.push(`/places/${id}`)
}

const loadSavedItinerary = async (id) => {
    loading.value = true
    try {
        const response = await api.get(`/api/itinerary/user/${user.value.id}`)
        const saved = response.data.find(it => it.id === parseInt(id))
        if (saved) {
            days.value = saved.days
            const formatted = {}
            for (let d = 1; d <= saved.days; d++) {
                formatted[`Day ${d}`] = []
            }
            
            saved.items.forEach(item => {
                if (item.place) {
                    formatted[`Day ${item.day}`].push({
                        time_slot: item.time_slot,
                        time: item.time,
                        place: item.place,
                        category_name: item.place.category_name || "Place",
                        is_preferred: false
                    })
                }
            })
            itinerary.value = formatted
        }
    } catch (error) {
        console.error("Error loading saved itinerary:", error)
        alert("Could not load the saved trip.")
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    if (route.query.id && user.value) {
        loadSavedItinerary(route.query.id)
    }
})

const getCoverImage = (imgData) => {
    const noImageUrl = 'https://via.placeholder.com/400x300?text=No+Image'
    if (!imgData) return noImageUrl
    
    let urls = []
    if (typeof imgData === 'string' && imgData.trim().startsWith('[')) {
        try { urls = JSON.parse(imgData) } catch (e) { urls = [imgData.replace(/^\["?|"?\]$/g, '').replace(/\\"/g, '')] }
    } else {
        urls = [imgData]
    }
    
    if (urls.length === 0) return noImageUrl
    const url = urls[0]
    
    if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) return url
    return `http://localhost:8000${url.startsWith('/') ? '' : '/'}${url}`
}

const handleImgError = (e) => {
    e.target.src = 'https://via.placeholder.com/400x300?text=Image+Not+Found'
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

.trip-planner-page {
    background-color: #f8fafc;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    color: #0f172a;
}

.planner-header {
    background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%);
    padding: 60px 20px 40px;
    border-bottom: 1px solid #bbf7d0;
    text-align: center;
}

.header-container {
    max-width: 800px;
    margin: 0 auto;
}

.header-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #dcfce7;
    color: #166534;
    padding: 6px 16px;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 700;
    margin-bottom: 15px;
    border: 1px solid #bbf7d0;
}

.header-container h1 {
    font-size: 2.8rem;
    font-weight: 900;
    color: #14532d;
    margin: 0 0 10px;
    letter-spacing: -1px;
}

.subtitle {
    font-size: 1.1rem;
    color: #166534;
    opacity: 0.8;
}

.planner-container {
    max-width: 800px;
    margin: 40px auto;
    padding: 0 20px;
}

/* Setup Card */
.setup-card {
    background: white;
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.05);
    text-align: center;
    border: 1px solid #e2e8f0;
}

.setup-card h2 {
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: 30px;
}

.days-selector {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-bottom: 40px;
}

.day-option {
    width: 100px;
    height: 100px;
    border: 2px solid #e2e8f0;
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
    background: #f8fafc;
}

.day-option:hover {
    border-color: #22c55e;
    background: #f0fdf4;
}

.day-option.active {
    border-color: #22c55e;
    background: #22c55e;
    color: white;
    box-shadow: 0 8px 20px rgba(34, 197, 94, 0.3);
}

.day-option .num {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
}

.day-option .text {
    font-size: 0.9rem;
    font-weight: 600;
    margin-top: 5px;
}

.btn-generate {
    background: #0f172a;
    color: white;
    border: none;
    padding: 16px 32px;
    border-radius: 50px;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
}

.btn-generate:hover {
    background: #1e293b;
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.2);
}

.btn-generate:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
}

/* Itinerary Result */
.result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}

.result-header h2 {
    font-size: 1.8rem;
    font-weight: 800;
    margin: 0;
}

.action-buttons {
    display: flex;
    gap: 12px;
}

.btn-save {
    background: #22c55e;
    color: white;
    border: none;
    padding: 10px 24px;
    border-radius: 50px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
    display: flex;
    align-items: center;
    gap: 8px;
}

.btn-save:hover {
    background: #16a34a;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
}

.btn-save:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.btn-outline {
    background: transparent;
    border: 2px solid #e2e8f0;
    padding: 10px 20px;
    border-radius: 50px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
    display: flex;
    align-items: center;
    gap: 8px;
}

.save-success-alert {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #166534;
    padding: 15px 20px;
    border-radius: 12px;
    margin-bottom: 25px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 600;
    animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}

.btn-outline:hover {
    border-color: #0f172a;
    background: #f1f5f9;
}

/* Timeline */
.timeline-container {
    background: white;
    border-radius: 24px;
    padding: 40px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.05);
    border: 1px solid #e2e8f0;
}

.day-section {
    margin-bottom: 50px;
}

.day-section:last-child {
    margin-bottom: 0;
}

.day-header h3 {
    font-size: 1.5rem;
    font-weight: 900;
    color: #22c55e;
    margin: 0 0 25px;
    padding-bottom: 15px;
    border-bottom: 2px dashed #e2e8f0;
}

.timeline {
    padding-left: 10px;
}

.timeline-item {
    display: flex;
    gap: 30px;
    position: relative;
    margin-bottom: 30px;
}

.timeline-item:last-child {
    margin-bottom: 0;
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
    font-size: 1.1rem;
    color: #0f172a;
    margin-bottom: 8px;
    background: #f1f5f9;
    padding: 4px 8px;
    border-radius: 8px;
}

.marker-dot {
    width: 16px;
    height: 16px;
    background: white;
    border: 4px solid #22c55e;
    border-radius: 50%;
    z-index: 2;
}

.marker-line {
    position: absolute;
    top: 45px;
    bottom: -40px;
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
    font-size: 0.9rem;
    font-weight: 700;
    color: #64748b;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Place Card */
.place-card {
    display: flex;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    overflow: hidden;
    cursor: pointer;
    transition: 0.2s;
}

.place-card:hover {
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    transform: translateY(-3px);
    border-color: #cbd5e1;
}

.place-img {
    width: 140px;
    flex-shrink: 0;
    position: relative;
}

.place-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.match-badge {
    position: absolute;
    top: 8px;
    left: 8px;
    background: #f59e0b;
    color: white;
    font-size: 0.7rem;
    font-weight: 800;
    padding: 4px 8px;
    border-radius: 6px;
}

.place-info {
    padding: 15px;
}

.place-info h4 {
    margin: 0 0 5px;
    font-size: 1.1rem;
    font-weight: 800;
}

.rating-cat {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.85rem;
    color: #64748b;
    margin-bottom: 8px;
}

.dot {
    color: #cbd5e1;
}

.desc {
    margin: 0;
    font-size: 0.85rem;
    color: #475569;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

@media (max-width: 640px) {
    .place-card {
        flex-direction: column;
    }
    .place-img {
        width: 100%;
        height: 140px;
    }
    .timeline-item {
        gap: 15px;
    }
    .time-marker {
        width: 50px;
    }
}
</style>
