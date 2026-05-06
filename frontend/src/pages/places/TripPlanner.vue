<template>
    <div class="trip-planner-page">
        <Navbar />

        <div class="planner-header">
            <div class="header-container">
                <div class="text-zone">
                    <div class="header-badge">
                        <i class="fas fa-magic"></i>
                        <span>{{ t('tripPlanner.badge') }}</span>
                    </div>
                    <h1>{{ t('tripPlanner.title') }}</h1>
                    <p class="subtitle">{{ t('tripPlanner.subtitle') }}</p>
                </div>
            </div>
        </div>

        <div class="planner-container">
            <!-- Input Form -->
            <div class="search-bar-wrapper" v-if="!itinerary">
                <div class="search-bar">
                    <!-- Interests Section -->
                    <div class="search-section" @click.stop="showInterestDropdown = !showInterestDropdown; showDaysDropdown = false">
                        <div class="section-content">
                            <div class="section-label">{{ t('tripPlanner.interests') }}</div>
                            <div class="section-value" :class="{ 'has-value': selectedPreferences.length > 0 }">
                                {{ selectedPreferencesText }}
                            </div>
                        </div>
                        
                        <!-- Dropdown -->
                        <div class="dropdown-menu" v-if="showInterestDropdown" @click.stop>
                            <div class="dropdown-header">{{ t('tripPlanner.selectInterests') }}</div>
                            <div class="pref-list">
                                <div class="pref-item" 
                                     v-for="pref in availablePreferences" 
                                     :key="pref.id"
                                     :class="{ active: selectedPreferences.includes(pref.id) }"
                                     @click="togglePreference(pref.id)">
                                    <i :class="pref.icon"></i>
                                    <span>{{ pref.label }}</span>
                                    <i class="fas fa-check check-icon" v-if="selectedPreferences.includes(pref.id)"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="divider"></div>
                    
                    <!-- Days Section -->
                    <div class="search-section" @click.stop="showDaysDropdown = !showDaysDropdown; showInterestDropdown = false">
                        <div class="section-content">
                            <div class="section-label">{{ t('tripPlanner.duration') }}</div>
                            <div class="section-value has-value">
                                {{ days }} {{ days === 1 ? t('tripPlanner.day') : t('tripPlanner.days') }}
                            </div>
                        </div>
                        
                        <!-- Dropdown -->
                        <div class="dropdown-menu days-dropdown" v-if="showDaysDropdown" @click.stop>
                            <div class="day-item" v-for="d in 5" :key="d" :class="{active: days === d}" @click="days = d; showDaysDropdown = false">
                                {{ d }} {{ d === 1 ? t('tripPlanner.day') : t('tripPlanner.days') }}
                            </div>
                        </div>
                    </div>
                    
                    <!-- Generate Button -->
                    <div class="search-action">
                        <button class="btn-generate-bar" @click="generateItinerary" :disabled="loading">
                            <i class="fas fa-spinner fa-spin" v-if="loading"></i>
                            <span v-else>{{ t('tripPlanner.generate') }}</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Itinerary Result -->
            <div class="itinerary-result" v-else>
                <div class="result-header">
                    <h2>{{ t('tripPlanner.yourItinerary', { days }) }}</h2>
                    <div class="action-buttons">
                        <button v-if="user" class="btn-save" @click="saveItinerary" :disabled="saving">
                            <i class="fas fa-spinner fa-spin" v-if="saving"></i>
                            <i class="fas fa-bookmark" v-else></i>
                            {{ saving ? t('tripPlanner.saving') : t('tripPlanner.saveToTrips') }}
                        </button>
                        <button class="btn-outline" @click="resetPlanner">
                            <i class="fas fa-redo"></i> {{ t('tripPlanner.planAnother') }}
                        </button>
                    </div>
                </div>

                <div v-if="saveSuccess" class="save-success-alert">
                    <i class="fas fa-check-circle"></i>
                    <span>{{ t('tripPlanner.saveSuccess') }}</span>
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
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

const availablePreferences = [
    { id: 'nature', label: 'Nature', icon: 'fas fa-tree' },
    { id: 'culture', label: 'Culture & Temple', icon: 'fas fa-vihara' },
    { id: 'local_food', label: 'Local Food', icon: 'fas fa-utensils' },
    { id: 'cafe', label: 'Cafe & Sweets', icon: 'fas fa-coffee' },
    { id: 'landmark', label: 'Landmarks', icon: 'fas fa-camera' },
    { id: 'chill', label: 'Chill & Nightlife', icon: 'fas fa-glass-cheers' }
]
const selectedPreferences = ref([])

const togglePreference = (id) => {
    const index = selectedPreferences.value.indexOf(id)
    if (index > -1) {
        selectedPreferences.value.splice(index, 1)
    } else {
        selectedPreferences.value.push(id)
    }
}

const showInterestDropdown = ref(false)
const showDaysDropdown = ref(false)

const closeDropdowns = () => {
    showInterestDropdown.value = false
    showDaysDropdown.value = false
}

onMounted(() => {
    document.addEventListener('click', closeDropdowns)
})

onUnmounted(() => {
    document.removeEventListener('click', closeDropdowns)
})

const selectedPreferencesText = computed(() => {
    if (selectedPreferences.value.length === 0) return 'Any Interests'
    if (selectedPreferences.value.length === 1) {
        return availablePreferences.find(p => p.id === selectedPreferences.value[0]).label
    }
    return `${selectedPreferences.value.length} Selected`
})

const generateItinerary = async () => {
    loading.value = true
    try {
        const payload = { 
            days: days.value,
            preferences: selectedPreferences.value.length > 0 ? selectedPreferences.value : null
        }
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
    const noImageUrl = 'https://images.unsplash.com/photo-1540611025311-01df3cef54b5?q=80&w=800'
    if (!imgData) return noImageUrl
    
    let urls = []
    if (typeof imgData === 'string' && imgData.trim().startsWith('[')) {
        try { urls = JSON.parse(imgData) } catch (e) { urls = [imgData.replace(/^\["?|"?\]$/g, '').replace(/\\"/g, '')] }
    } else {
        urls = [imgData]
    }
    
    if (urls.length === 0) return noImageUrl
    const url = urls[0]
    
    if (url.startsWith('http')) return url
    const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    return `${backendUrl}${url.startsWith('/') ? '' : '/'}${url}`
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
    background: linear-gradient(135deg, #f8fafc 0%, #eff6ff 100%);
    padding: 80px 20px 60px;
    text-align: center;
    border-bottom: 1px solid #e2e8f0;
}

.header-container {
    max-width: 800px;
    margin: 0 auto;
}

.header-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #dbeafe;
    color: #2563eb;
    padding: 8px 20px;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 800;
    margin-bottom: 20px;
    border: 1px solid #bfdbfe;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.header-container h1 {
    font-size: 3.5rem;
    font-weight: 900;
    color: #0f172a;
    margin: 0 0 15px;
    letter-spacing: -2px;
    line-height: 1.1;
}

.subtitle {
    font-size: 1.2rem;
    color: #475569;
    max-width: 600px;
    margin: 0 auto;
    font-weight: 500;
    line-height: 1.6;
}

.planner-container {
    max-width: 800px;
    margin: 40px auto;
    padding: 0 20px;
}

/* Setup Bar Style */
.search-bar-wrapper {
    display: flex;
    justify-content: center;
    margin-bottom: 40px;
}

.search-bar {
    display: flex;
    align-items: center;
    background: white;
    border-radius: 24px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.04);
    border: 1px solid #e2e8f0;
    padding: 12px;
    width: 100%;
    max-width: 680px;
    position: relative;
    transition: all 0.3s ease;
}

.search-bar:focus-within {
    border-color: #3b82f6;
    box-shadow: 0 15px 50px rgba(59, 130, 246, 0.1);
}

.search-section {
    flex: 1;
    padding: 10px 25px;
    cursor: pointer;
    border-radius: 40px;
    transition: 0.2s;
    position: relative;
}

.search-section:hover {
    background: #f1f5f9;
}

.section-label {
    font-size: 0.75rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 4px;
    letter-spacing: 0.5px;
}

.section-value {
    font-size: 0.95rem;
    color: #94a3b8;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.section-value.has-value {
    color: #0f172a;
    font-weight: 600;
}

.divider {
    width: 1px;
    height: 40px;
    background: #e2e8f0;
    margin: 0 5px;
}

.search-action {
    padding-left: 10px;
}

.btn-generate-bar {
    background: #2563eb;
    color: white;
    border: none;
    padding: 14px 34px;
    border-radius: 16px;
    font-size: 1rem;
    font-weight: 800;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2);
}

.btn-generate-bar:hover {
    background: #1d4ed8;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(37, 99, 235, 0.3);
}

.btn-generate-bar:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
}

/* Dropdowns */
.dropdown-menu {
    position: absolute;
    top: 100%;
    left: 0;
    margin-top: 15px;
    background: white;
    border-radius: 24px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    border: 1px solid #e2e8f0;
    width: 350px;
    z-index: 100;
    padding: 20px;
    cursor: default;
}

.days-dropdown {
    width: 200px;
    left: auto;
    right: 0;
}

.dropdown-header {
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 15px;
    font-size: 1.1rem;
}

.pref-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.pref-item {
    display: flex;
    align-items: center;
    padding: 12px 15px;
    border-radius: 12px;
    cursor: pointer;
    transition: 0.2s;
    font-weight: 600;
    color: #475569;
}

.pref-item i:first-child {
    width: 30px;
    font-size: 1.2rem;
    color: #94a3b8;
}

.pref-item:hover {
    background: #f8fafc;
}

.pref-item.active {
    background: #eff6ff;
    color: #3b82f6;
}

.pref-item.active i:first-child {
    color: #3b82f6;
}

.check-icon {
    margin-left: auto;
    color: #3b82f6;
}

.day-item {
    padding: 12px 20px;
    border-radius: 12px;
    cursor: pointer;
    transition: 0.2s;
    font-weight: 600;
    color: #475569;
    text-align: center;
    margin-bottom: 5px;
}

.day-item:hover {
    background: #f1f5f9;
}

.day-item.active {
    background: #22c55e;
    color: white;
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
