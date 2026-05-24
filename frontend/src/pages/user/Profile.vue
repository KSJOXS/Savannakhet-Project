<template>
    <div class="profile-page">
        <Navbar />

        <div class="profile-container">
            <!-- Sidebar: User Info & Navigation -->
            <aside class="profile-sidebar">
                <div class="user-info-card">
                    <div class="avatar-section">
                        <div class="avatar-wrapper" :class="{ 'is-editing': isEditing }" @click="isEditing && triggerImageUpload()">
                            <div class="avatar-inner">
                                <img :src="currentProfileImage" alt="Profile Avatar" class="avatar-img" />
                                <div v-if="isEditing" class="avatar-overlay">
                                    <i class="fas fa-camera"></i>
                                </div>
                            </div>
                        </div>
                        <h3 class="user-name">{{ form.username || 'User' }}</h3>
                        <p class="user-email">{{ form.email }}</p>
                        
                        <input 
                            type="file" 
                            ref="fileInput" 
                            class="hidden-input" 
                            accept="image/jpeg,image/png,image/webp" 
                            @change="onImageSelected" 
                            style="display: none;"
                        />
                    </div>

                    <nav class="profile-nav">
                        <button 
                            class="nav-item" 
                            :class="{ active: activeTab === 'settings' }"
                            @click="switchTab('settings')"
                        >
                            <i class="fas fa-cog"></i> <span>{{ t('auth.settings') }}</span>
                        </button>
                        <button 
                            class="nav-item" 
                            :class="{ active: activeTab === 'reviews' }"
                            @click="switchTab('reviews')"
                        >
                            <i class="fas fa-history"></i> <span>{{ t('auth.review_history') }}</span>
                        </button>
                        <button 
                            class="nav-item" 
                            :class="{ active: activeTab === 'places' }"
                            @click="switchTab('places')"
                        >
                            <i class="fas fa-map-marked-alt"></i> <span>{{ t('auth.my_places') }}</span>
                        </button>
                        <button 
                            class="nav-item" 
                            :class="{ active: activeTab === 'trips' }"
                            @click="switchTab('trips')"
                        >
                            <i class="fas fa-route"></i> <span>{{ t('auth.saved_trips') }}</span>
                        </button>
                    </nav>

                    <div class="sidebar-footer">
                        <button class="btn-back-home" @click="router.push('/')">
                            <i class="fas fa-arrow-left"></i> {{ t('nav.home', 'Back to Home') }}
                        </button>
                        <button class="btn-logout-alt" @click="handleLogout">
                            <i class="fas fa-sign-out-alt"></i> {{ t('auth.sign_out') }}
                        </button>
                    </div>
                </div>
            </aside>

            <!-- Main Content Area -->
            <main class="profile-main-content">
                <div v-if="loading" class="loading-state">
                    <div class="spinner"></div>
                    <p>{{ t('auth.loading_profile') }}</p>
                </div>

                <div v-else class="content-card">
                    <!-- Header inside card -->
                    <div class="content-header">
                        <h2>{{ tabTitle }}</h2>
                        <p>{{ tabSubtitle }}</p>
                    </div>

                    <!-- TAB: Settings -->
                    <div v-if="activeTab === 'settings'" class="tab-pane fade-in">
                        <form @submit.prevent="handleUpdate" class="profile-form">
                            <div class="form-grid">
                                <div class="input-group">
                                    <label>{{ t('auth.username') }}</label>
                                    <div class="input-wrapper">
                                        <i class="fas fa-user"></i>
                                        <input v-model="form.username" type="text" :placeholder="t('auth.username')" :disabled="!isEditing" />
                                    </div>
                                </div>
                                
                                <div class="input-group">
                                    <label>{{ t('auth.email') }}</label>
                                    <div class="input-wrapper">
                                        <i class="fas fa-envelope"></i>
                                        <input v-model="form.email" type="email" :placeholder="t('auth.email')" :disabled="!isEditing" />
                                    </div>
                                </div>

                                <div class="input-group full-width">
                                    <label>{{ t('auth.new_password') }} <span class="hint">({{ t('common.optional', 'optional') }})</span></label>
                                    <div class="input-wrapper">
                                        <i class="fas fa-lock"></i>
                                        <input v-model="form.password" type="password" placeholder="••••••••" :disabled="!isEditing" />
                                    </div>
                                </div>

                                <div class="input-group full-width">
                                    <label>{{ t('auth.interests') }}</label>
                                    <p class="hint">{{ t('auth.interests_hint') }}</p>
                                    <div class="interests-tags">
                                        <div v-for="interest in availableInterests" :key="interest.id" 
                                            class="interest-tag"
                                            :class="{ 
                                                'active': form.preferences.includes(interest.id),
                                                'editing': isEditing 
                                            }"
                                            @click="isEditing && toggleInterest(interest.id)"
                                        >
                                            <i :class="interest.icon"></i>
                                            <span>{{ t(interest.key) }}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="form-actions">
                                <transition name="fade">
                                    <p v-if="successMsg" class="success-msg"><i class="fas fa-check-circle"></i> {{ successMsg }}</p>
                                </transition>
                                <transition name="fade">
                                    <p v-if="errorMsg" class="error-msg"><i class="fas fa-exclamation-circle"></i> {{ errorMsg }}</p>
                                </transition>

                                <div v-if="isEditing" class="btn-group-profile">
                                    <button type="button" class="btn-cancel-action" @click="cancelEdit">{{ t('auth.cancel') }}</button>
                                    <button type="submit" class="btn-save-action" :disabled="saving">
                                        <i class="fas fa-save"></i> {{ saving ? t('auth.saving') : t('auth.save_changes') }}
                                    </button>
                                </div>
                                <div v-else class="btn-group-profile">
                                    <button type="button" class="btn-edit-action" @click="isEditing = true">
                                        <i class="fas fa-edit"></i> {{ t('auth.edit_profile') }}
                                    </button>
                                </div>
                            </div>
                        </form>
                    </div>

                    <!-- TAB: Review History -->
                    <div v-if="activeTab === 'reviews'" class="tab-pane fade-in">
                        <div class="stats-row-modern">
                            <div class="stat-card-modern">
                                <div class="stat-icon post-icon"><i class="fas fa-paper-plane"></i></div>
                                <div class="stat-info">
                                    <span class="stat-value">{{ userReviews.length }}</span>
                                    <span class="stat-label">{{ t('auth.total_posts') }}</span>
                                </div>
                            </div>
                            <div class="stat-card-modern">
                                <div class="stat-icon rating-icon"><i class="fas fa-star"></i></div>
                                <div class="stat-info">
                                    <span class="stat-value">{{ averageRating }}</span>
                                    <span class="stat-label">{{ t('auth.avg_rating') }}</span>
                                </div>
                            </div>
                            <div class="stat-card-modern">
                                <div class="stat-icon place-icon"><i class="fas fa-map-marker-alt"></i></div>
                                <div class="stat-info">
                                    <span class="stat-value">{{ userPlaces.length }}</span>
                                    <span class="stat-label">{{ t('auth.places_added') }}</span>
                                </div>
                            </div>
                        </div>

                        <div v-if="userReviews.length === 0" class="empty-state">
                            <div class="empty-illustration">
                                <i class="fas fa-comments"></i>
                            </div>
                            <p>{{ t('auth.no_experiences') }}</p>
                            <router-link to="/community" class="btn-primary-gradient">{{ t('auth.explore_community') }}</router-link>
                        </div>
                        
                        <div v-else class="social-feed-modern">
                            <div v-for="review in userReviews" :key="review.id" class="post-card-modern">
                                <div class="post-card-header">
                                    <div class="post-place-info">
                                        <router-link :to="`/places/${review.place_id}`" class="post-place-name">
                                            {{ review.place_name }}
                                        </router-link>
                                        <span class="post-timestamp"><i class="far fa-clock"></i> {{ formatDate(review.visited_at) }}</span>
                                    </div>
                                    <div class="post-rating">
                                        <i class="fas fa-star"></i> {{ review.rating }}
                                    </div>
                                </div>
                                <div class="post-card-body">
                                    <p class="post-comment">{{ review.comment_text }}</p>
                                    
                                    <div v-if="review.images && review.images.length > 0" class="post-gallery">
                                        <div v-for="(img, idx) in review.images" :key="idx" class="gallery-item" @click="openLightbox(review.images, idx)">
                                            <img :src="getImageUrl(img)" loading="lazy" />
                                        </div>
                                    </div>
                                </div>
                                <div class="post-card-footer">
                                    <div class="post-engagement">
                                        <span class="engagement-item">
                                            <i class="fas fa-heart"></i> {{ review.liked_by?.length || 0 }}
                                        </span>
                                    </div>
                                    <router-link :to="`/places/${review.place_id}`" class="btn-text-link">
                                        {{ t('auth.view_place') }} <i class="fas fa-arrow-right"></i>
                                    </router-link>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- TAB: Places -->
                    <div v-if="activeTab === 'places'" class="tab-pane fade-in">
                        <div v-if="userPlaces.length === 0" class="empty-state">
                            <div class="empty-illustration">
                                <i class="fas fa-map-signs"></i>
                            </div>
                            <p>{{ t('auth.no_places') }}</p>
                            <router-link to="/submit-place" class="btn-primary-gradient">{{ t('auth.submit_first_place') }}</router-link>
                        </div>
                        <div v-else class="places-grid-modern">
                            <div v-for="place in userPlaces" :key="place.id" class="place-card-modern">
                                <div class="place-card-image">
                                    <img :src="getPlaceImage(place.image_url)" alt="place" />
                                    <div class="status-pill" :class="place.status">
                                        {{ place.status.charAt(0).toUpperCase() + place.status.slice(1) }}
                                    </div>
                                </div>
                                <div class="place-card-content">
                                    <router-link :to="`/places/${place.id}`" class="place-title-link">
                                        <h4>{{ place.name }}</h4>
                                    </router-link>
                                    <p class="place-desc">{{ truncate(place.description, 80) }}</p>
                                    <div class="place-footer">
                                        <router-link :to="`/places/${place.id}`" class="btn-view-modern">
                                            {{ t('auth.view_details') }}
                                        </router-link>
                                        <div class="place-actions">
                                            <button @click="router.push(`/submit-place/${place.id}`)" class="btn-action-edit" :title="t('submit.edit')">
                                                <i class="fas fa-edit"></i>
                                            </button>
                                            <button @click="deletePlace(place.id)" class="btn-action-delete" :title="t('submit.delete')">
                                                <i class="fas fa-trash"></i>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- TAB: Trips -->
                    <div v-if="activeTab === 'trips'" class="tab-pane fade-in">
                        <div v-if="userItineraries.length === 0" class="empty-state">
                            <div class="empty-illustration">
                                <i class="fas fa-suitcase-rolling"></i>
                            </div>
                            <p>{{ t('auth.empty_bucket_list') }}</p>
                            <router-link to="/trip-planner" class="btn-primary-gradient">{{ t('auth.start_planning') }}</router-link>
                        </div>

                        <div v-else class="trips-list-modern">
                            <div v-for="itinerary in userItineraries" :key="itinerary.id" class="trip-card-modern">
                                <div class="trip-card-icon">
                                    <i class="fas fa-route"></i>
                                </div>
                                <div class="trip-card-main">
                                    <div class="trip-info">
                                        <h4>{{ itinerary.title }}</h4>
                                        <div class="trip-meta">
                                            <span class="meta-item"><i class="fas fa-calendar-day"></i> {{ itinerary.days }} {{ t('tripPlanner.days') }}</span>
                                            <span class="meta-separator">•</span>
                                            <span class="meta-item"><i class="far fa-calendar-alt"></i> {{ formatDate(itinerary.created_at) }}</span>
                                        </div>
                                    </div>
                                    <div class="trip-actions">
                                        <button class="btn-action-icon view" @click="openItineraryModal(itinerary)" :title="t('auth.view_plan')">
                                            <i class="fas fa-eye"></i>
                                        </button>
                                        <button class="btn-action-icon delete" @click="confirmDeleteItinerary(itinerary.id)" :title="t('auth.delete_plan')">
                                            <i class="fas fa-trash-alt"></i>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>

        <!-- Itinerary Modal -->
        <div v-if="selectedItinerary" class="modal-overlay" @click="closeItineraryModal">
            <div class="modal-content itinerary-modal-modern" @click.stop>
                <div class="modal-header-modern">
                    <div class="modal-title-group">
                        <h2>{{ selectedItinerary.title }}</h2>
                        <div class="itinerary-meta-pills">
                            <span class="pill"><i class="fas fa-calendar-alt"></i> {{ selectedItinerary.days }} {{ t('tripPlanner.days') }}</span>
                            <span class="pill"><i class="fas fa-clock"></i> {{ formatDate(selectedItinerary.created_at) }}</span>
                        </div>
                    </div>
                    <button class="btn-close-modern" @click="closeItineraryModal"><i class="fas fa-times"></i></button>
                </div>
                <div class="modal-body-modern">
                    <div class="timeline-modern">
                        <div class="day-group" v-for="day in selectedItinerary.days" :key="day">
                            <h3 class="day-label">{{ t('tripPlanner.day') }} {{ day }}</h3>
                            <div class="timeline-items">
                                <div class="timeline-entry" v-for="item in selectedItinerary.items.filter(i => i.day === day)" :key="item.id">
                                    <div class="entry-time">
                                        <span class="time-text">{{ item.time }}</span>
                                        <div class="time-indicator"></div>
                                    </div>
                                    <div class="entry-content">
                                        <div class="slot-type">
                                            <i :class="getSlotIcon(item.time_slot)"></i>
                                            {{ t('tripPlanner.' + item.time_slot.toLowerCase()) }}
                                        </div>
                                        <div class="place-preview-card" @click="handlePlaceClick(item.place_id)">
                                            <img :src="getPlaceImage(item.place?.image_url)" alt="place" class="preview-img" />
                                            <div class="preview-info">
                                                <h5>{{ item.place?.name || t('auth.unknown_place') }}</h5>
                                                <div class="preview-rating">
                                                    <i class="fas fa-star"></i> {{ item.place?.rating_avg || '0.0' }}
                                                </div>
                                            </div>
                                            <i class="fas fa-chevron-right"></i>
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
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import { userRepository } from '@/repositories/userRepository'
import { placeRepository } from '@/repositories/placeRepository'
import { useAuth } from '@/composables/useAuth'
import { useI18n } from '@/composables/useI18n'

const { t, locale } = useI18n()
const router = useRouter()
const route = useRoute()
const { user, logout } = useAuth()

const loading = ref(true)
const saving = ref(false)
const isEditing = ref(false)
const successMsg = ref('')
const errorMsg = ref('')

const activeTab = ref('settings')
const userReviews = ref([])
const userPlaces = ref([])
const userItineraries = ref([])
const selectedItinerary = ref(null)

const tabTitle = computed(() => {
    switch (activeTab.value) {
        case 'settings': return t('auth.settings')
        case 'reviews': return t('auth.my_review_history')
        case 'places': return t('auth.places_i_added')
        case 'trips': return t('auth.my_saved_trips')
        default: return t('auth.profile_tab')
    }
})

const tabSubtitle = computed(() => {
    switch (activeTab.value) {
        case 'settings': return t('auth.manage_settings')
        case 'reviews': return t('auth.review_history_subtitle')
        case 'places': return t('auth.places_subtitle')
        case 'trips': return t('auth.trips_subtitle')
        default: return ''
    }
})

const availableInterests = [
    { id: 'nature', key: 'auth.interest_nature', icon: 'fas fa-mountain' },
    { id: 'culture', key: 'auth.interest_culture', icon: 'fas fa-vihara' },
    { id: 'cafe', key: 'auth.interest_cafe', icon: 'fas fa-coffee' },
    { id: 'local_food', key: 'auth.interest_local_food', icon: 'fas fa-bowl-food' },
    { id: 'landmark', key: 'auth.interest_landmark', icon: 'fas fa-camera' },
    { id: 'chill', key: 'auth.interest_chill', icon: 'fas fa-walking' }
]

const parsePreferences = (prefs) => {
    if (!prefs) return []
    if (Array.isArray(prefs)) return prefs
    if (typeof prefs === 'string') {
        try {
            const parsed = JSON.parse(prefs)
            return Array.isArray(parsed) ? parsed : []
        } catch (e) {
            return prefs.split(',').filter(p => p.trim())
        }
    }
    return []
}

const toggleInterest = (id) => {
    if (!Array.isArray(form.value.preferences)) form.value.preferences = []
    const index = form.value.preferences.indexOf(id)
    if (index === -1) form.value.preferences.push(id)
    else form.value.preferences.splice(index, 1)
}

const switchTab = (tab) => {
    activeTab.value = tab
    router.push({ query: { tab } })
}

const openItineraryModal = (itinerary) => {
    selectedItinerary.value = itinerary
    document.body.style.overflow = 'hidden'
}

const closeItineraryModal = () => {
    selectedItinerary.value = null
    document.body.style.overflow = ''
}

const handlePlaceClick = (placeId) => {
    document.body.style.overflow = ''
    router.push(`/places/${placeId}`)
}

const getSlotIcon = (slot) => {
    if (slot === 'Morning') return 'fas fa-sun text-warning'
    if (slot === 'Afternoon') return 'fas fa-cloud-sun text-orange'
    return 'fas fa-moon text-indigo'
}

const averageRating = computed(() => {
    if (userReviews.value.length === 0) return '0.0'
    const sum = userReviews.value.reduce((acc, r) => acc + r.rating, 0)
    return (sum / userReviews.value.length).toFixed(1)
})

const originalData = ref({})
const fileInput = ref(null)
const selectedFile = ref(null)
const imagePreview = ref(null)

const form = ref({
    username: '',
    email: '',
    password: '',
    profile_image: '',
    preferences: []
})

const currentProfileImage = computed(() => {
    if (imagePreview.value) return imagePreview.value
    if (form.value.profile_image) {
        const url = form.value.profile_image
        if (url.startsWith('http') || url.startsWith('data:')) return url
        return `http://localhost:8000/${url.startsWith('/') ? url.slice(1) : url}`
    }
    return `https://ui-avatars.com/api/?name=${form.value.username || 'User'}&background=3b82f6&color=fff&size=150`
})

const triggerImageUpload = () => fileInput.value.click()

const onImageSelected = (e) => {
    const file = e.target.files[0]
    if (file) {
        selectedFile.value = file
        imagePreview.value = URL.createObjectURL(file)
    }
}

const cancelEdit = () => {
    isEditing.value = false
    form.value = { 
        ...originalData.value, 
        preferences: originalData.value.preferences ? [...originalData.value.preferences] : [],
        password: '' 
    }
    selectedFile.value = null
    imagePreview.value = null
    errorMsg.value = ''
    successMsg.value = ''
}

const fetchProfile = async () => {
    if (!user.value) {
        router.push('/login')
        return
    }
    
    loading.value = true
    try {
        const res = await userRepository.getProfile(user.value.id)
        form.value.username = res.data.username
        form.value.email = res.data.email
        form.value.profile_image = res.data.profile_image
        form.value.preferences = parsePreferences(res.data.preferences)
        
        originalData.value = { 
            username: res.data.username, 
            email: res.data.email, 
            profile_image: res.data.profile_image,
            preferences: [...form.value.preferences]
        }
        
        loading.value = false
        fetchHistory(user.value.id)
    } catch (err) {
        console.error("Error fetching profile:", err)
        errorMsg.value = t('auth.load_error')
    } finally {
        loading.value = false
    }
}

const fetchHistory = async (userId) => {
    try {
        const [reviewsRes, placesRes, itinerariesRes] = await Promise.allSettled([
            userRepository.getUserReviews(userId),
            userRepository.getUserPlaces(userId),
            userRepository.getItineraries(userId)
        ])
        
        if (reviewsRes.status === 'fulfilled') {
            userReviews.value = reviewsRes.value.data.map(r => ({
                ...r,
                images: r.images || [],
                liked_by: r.liked_by || []
            }))
        }
        if (placesRes.status === 'fulfilled') userPlaces.value = placesRes.value.data
        if (itinerariesRes.status === 'fulfilled') userItineraries.value = itinerariesRes.value.data
    } catch (historyErr) {
        console.warn("Could not load history data:", historyErr)
    }
}

const deletePlace = async (id) => {
    if (!confirm(t('auth.delete_place_confirm'))) return
    
    try {
        await userRepository.deleteUserPlace(id) // We should check if this exists or use placeRepository.delete
        // If userRepository doesn't have it, we might need to add it or use admin route if allowed
        userPlaces.value = userPlaces.value.filter(p => p.id !== id)
        successMsg.value = "Place deleted successfully."
    } catch (err) {
        console.error("Error deleting place:", err)
        // Fallback to placeRepository.delete if user specific one is missing
        try {
            await placeRepository.delete(id)
            userPlaces.value = userPlaces.value.filter(p => p.id !== id)
            successMsg.value = t('auth.delete_place_success')
        } catch(e) {
            errorMsg.value = t('auth.delete_place_error')
        }
    }
}

const handleUpdate = async () => {
    saving.value = true
    successMsg.value = ''
    errorMsg.value = ''
    
    const formData = new FormData()
    if (form.value.username) formData.append('username', form.value.username)
    if (form.value.email) formData.append('email', form.value.email)
    if (form.value.password) formData.append('password', form.value.password)
    if (selectedFile.value) formData.append('profile_image', selectedFile.value)
    formData.append('preferences', JSON.stringify(form.value.preferences))

    try {
        const res = await userRepository.updateProfile(user.value.id, formData)
        successMsg.value = t('auth.profile_updated')
        
        const currentData = JSON.parse(localStorage.getItem('user') || '{}')
        currentData.username = res.data.username
        currentData.profile_image = res.data.profile_image
        localStorage.setItem('user', JSON.stringify(currentData))
        
        user.value.username = res.data.username 
        if (res.data.profile_image) user.value.profile_image = res.data.profile_image
        
        isEditing.value = false
        form.value.password = ''
        selectedFile.value = null
        imagePreview.value = null

        await fetchProfile()
    } catch (err) {
        errorMsg.value = err.response?.data?.detail || "Something went wrong. Please try again."
    } finally {
        saving.value = false
    }
}

const handleLogout = () => {
    if (confirm(t('auth.sign_out_confirm'))) {
        logout()
        router.push('/')
    }
}

const getPlaceImage = (imageString) => {
    if (!imageString || imageString === '[]') return '/placeholder-image.jpg'
    
    let url = ''
    try {
        const images = JSON.parse(imageString)
        if (Array.isArray(images) && images.length > 0) {
            url = images[0]
        } else {
            url = imageString
        }
    } catch (e) {
        url = imageString
    }

    if (!url) return '/placeholder-image.jpg'
    if (url.startsWith('http') || url.startsWith('data:')) return url
    return `http://localhost:8000${url.startsWith('/') ? '' : '/'}${url}`
}

const truncate = (text, length) => {
    if (!text) return ''
    return text.length > length ? text.substring(0, length) + '...' : text
}

const formatDate = (dateString) => {
    if (!dateString) return ''
    const options = { year: 'numeric', month: 'short', day: 'numeric' }
    const langMap = { en: 'en-US', th: 'th-TH', la: 'lo-LA', vi: 'vi-VN' }
    return new Date(dateString).toLocaleDateString(langMap[locale.value] || 'en-US', options)
}

const getImageUrl = (url) => {
    if (!url) return ''
    if (url.startsWith('http') || url.startsWith('data:')) return url
    return `http://localhost:8000/${url.startsWith('/') ? url.slice(1) : url}`
}

watch(() => route.query.tab, (newTab) => {
    if (newTab) activeTab.value = newTab
})

const confirmDeleteItinerary = async (id) => {
    if (confirm(t('auth.delete_trip_confirm'))) {
        try {
            await userRepository.deleteItinerary(id)
            userItineraries.value = userItineraries.value.filter(it => it.id !== id)
        } catch (err) {
            alert(t('auth.delete_trip_error'))
        }
    }
}

onMounted(() => {
    activeTab.value = route.query.tab || 'settings'
    fetchProfile()
})

onUnmounted(() => {
    document.body.style.overflow = ''
})
</script>

<style scoped>
.profile-page {
    background-color: #f8fafc;
    min-height: 100vh;
    padding-bottom: 50px;
}

.profile-container {
    max-width: 100%;
    margin: 0;
    padding: 0 30px 0 0;
    display: grid;
    grid-template-columns: 320px 1fr;
    gap: 40px;
    align-items: start;
}

/* Sidebar Styles */
.profile-sidebar {
    position: sticky;
    top: 100px;
}

.user-info-card {
    background: white;
    border-radius: 0 24px 24px 0;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    border: 1px solid rgba(0,0,0,0.05);
    border-left: none;
    min-height: calc(100vh - 200px);
}

.avatar-section {
    text-align: center;
    margin-bottom: 30px;
}

.avatar-wrapper {
    position: relative;
    width: 140px;
    height: 140px;
    margin: 0 auto 20px;
    border-radius: 50%;
    padding: 6px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    box-shadow: 0 15px 35px rgba(37, 99, 235, 0.2);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.avatar-inner {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    border: 4px solid white;
    overflow: hidden;
    background: #f1f5f9;
    position: relative;
}

.avatar-wrapper.is-editing {
    cursor: pointer;
}

.avatar-wrapper.is-editing:hover {
    transform: scale(1.05);
}

.avatar-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-overlay {
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.5rem;
    opacity: 0;
    transition: opacity 0.3s;
}

.avatar-wrapper.is-editing:hover .avatar-overlay {
    opacity: 1;
}

.user-name {
    font-size: 1.4rem;
    font-weight: 800;
    color: #1e293b;
    margin: 0;
}

.user-email {
    font-size: 0.9rem;
    color: #64748b;
    margin: 5px 0 0;
}

.profile-nav {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 30px;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 14px 20px;
    border: none;
    background: transparent;
    border-radius: 16px;
    color: #64748b;
    font-weight: 700;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    text-align: left;
    position: relative;
}

.nav-item:hover {
    background: #f8fafc;
    color: #1e293b;
    padding-left: 25px;
}

.nav-item.active {
    background: #eff6ff;
    color: #2563eb;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08);
}

.nav-item.active::before {
    content: '';
    position: absolute;
    left: 0;
    top: 20%;
    bottom: 20%;
    width: 4px;
    background: #2563eb;
    border-radius: 0 4px 4px 0;
}

.nav-item i {
    width: 20px;
    font-size: 1.1rem;
}

.sidebar-footer {
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid #f1f5f9;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.btn-back-home {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 10px;
    background: #f1f5f9;
    color: #334155;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
}

.btn-back-home:hover {
    background: #e2e8f0;
    color: #0f172a;
}

.btn-logout-alt {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 10px;
    background: #fff1f2;
    color: #e11d48;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
}

.btn-logout-alt:hover {
    background: #ffe4e6;
}

/* Main Content Styles */
.profile-main-content {
    min-height: 600px;
    max-width: 1200px;
}

.content-card {
    background: transparent;
    padding: 40px 0 40px 40px;
}

.content-header {
    margin-bottom: 35px;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 20px;
}

.content-header h2 {
    font-size: 1.8rem;
    font-weight: 800;
    color: #1e293b;
    margin: 0 0 5px;
}

.content-header p {
    color: #64748b;
    margin: 0;
}

/* Form Styles */
.profile-form {
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.form-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 20px;
    width: 100%;
}

@media (min-width: 850px) {
    .form-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 30px;
    }
    .full-width {
        grid-column: span 2;
    }
}

.input-group {
    width: 100%;
    min-width: 0;
    display: flex;
    flex-direction: column;
}

.full-width {
    width: 100%;
}

.input-group label {
    display: block;
    font-weight: 700;
    color: #334155;
    margin-bottom: 8px;
    font-size: 0.9rem;
}

.input-wrapper {
    position: relative;
}

.input-wrapper i {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: #94a3b8;
}

.input-wrapper input {
    width: 100%;
    max-width: 100%;
    padding: 12px 15px 12px 45px;
    border: 1.5px solid #e2e8f0;
    border-radius: 12px;
    font-size: 1rem;
    transition: all 0.2s;
    box-sizing: border-box;
    display: block;
    margin: 0;
}

.input-wrapper input:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
    outline: none;
}

.input-wrapper input:disabled {
    background: #f8fafc;
    color: #64748b;
    cursor: not-allowed;
}

.hint {
    font-weight: 400;
    color: #94a3b8;
    font-size: 0.8rem;
}

/* Interests Tags */
.interests-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 15px;
}

.interest-tag {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 18px;
    background: #f1f5f9;
    border-radius: 50px;
    color: #475569;
    font-weight: 600;
    font-size: 0.9rem;
    transition: 0.2s;
    border: 1.5px solid transparent;
}

.interest-tag.active {
    background: #eff6ff;
    color: #1d4ed8;
    border-color: #bfdbfe;
}

.interest-tag.editing {
    cursor: pointer;
}

.interest-tag.editing:hover {
    transform: translateY(-2px);
}

.interest-tag.editing.active:hover {
    background: #fee2e2;
    color: #b91c1c;
    border-color: #fecaca;
}

/* Button Actions */
.btn-group-profile {
    display: flex;
    gap: 15px;
    margin-top: 20px;
}

.btn-edit-action {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 25px;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 50px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.3s;
}

.btn-edit-action:hover {
    background: #2563eb;
    box-shadow: 0 5px 15px rgba(37, 99, 235, 0.3);
}

.btn-save-action {
    flex: 1;
    padding: 12px;
    background: #10b981;
    color: white;
    border: none;
    border-radius: 50px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.3s;
}

.btn-save-action:hover {
    background: #059669;
}

.btn-cancel-action {
    padding: 12px 25px;
    background: #f1f5f9;
    color: #475569;
    border: none;
    border-radius: 50px;
    font-weight: 700;
    cursor: pointer;
}

/* Stats Row Modern */
.stats-row-modern {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 40px;
}

.stat-card-modern {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 25px;
    background: #f8fafc;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
}

.stat-icon {
    width: 50px;
    height: 50px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
}

.post-icon { background: #e0f2fe; color: #0284c7; }
.rating-icon { background: #fef9c3; color: #ca8a04; }
.place-icon { background: #f0fdf4; color: #16a34a; }

.stat-value {
    display: block;
    font-size: 1.6rem;
    font-weight: 800;
    color: #1e293b;
    line-height: 1.2;
}

.stat-label {
    font-size: 0.8rem;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Social Feed Modern */
.social-feed-modern {
    display: flex;
    flex-direction: column;
    gap: 25px;
}

.post-card-modern {
    background: white;
    border: 1px solid #f1f5f9;
    border-radius: 20px;
    padding: 25px;
    transition: 0.3s;
}

.post-card-modern:hover {
    box-shadow: 0 15px 40px rgba(0,0,0,0.06);
    transform: translateY(-5px);
}

.post-card-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 15px;
}

.post-place-name {
    display: block;
    font-size: 1.2rem;
    font-weight: 800;
    color: #1e293b;
    text-decoration: none;
    margin-bottom: 4px;
}

.post-timestamp {
    font-size: 0.85rem;
    color: #94a3b8;
}

.post-rating {
    background: #fefce8;
    color: #854d0e;
    padding: 5px 12px;
    border-radius: 50px;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 6px;
    height: fit-content;
}

.post-comment {
    color: #334155;
    line-height: 1.6;
    margin-bottom: 20px;
}

.post-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 12px;
}

.gallery-item {
    aspect-ratio: 1;
    border-radius: 12px;
    overflow: hidden;
    cursor: pointer;
}

.gallery-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: 0.3s;
}

.gallery-item:hover img {
    transform: scale(1.1);
}

.post-card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #f1f5f9;
}

.post-engagement {
    display: flex;
    gap: 15px;
}

.engagement-item {
    color: #64748b;
    font-weight: 600;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

.engagement-item i {
    color: #ef4444;
}

.btn-text-link {
    color: #2563eb;
    font-weight: 700;
    text-decoration: none;
    font-size: 0.9rem;
}

/* Places Grid Modern */
.places-grid-modern {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 25px;
}

.place-card-modern {
    background: white;
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid #f1f5f9;
    transition: 0.3s;
}

.place-card-modern:hover {
    box-shadow: 0 15px 40px rgba(0,0,0,0.08);
    transform: translateY(-8px);
}

.place-card-image {
    position: relative;
    height: 180px;
}

.place-card-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.status-pill {
    position: absolute;
    top: 15px;
    right: 15px;
    padding: 6px 14px;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 800;
    color: white;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.status-pill.approved { background: #10b981; }
.status-pill.pending { background: #f59e0b; }
.status-pill.rejected { background: #ef4444; }

.place-card-content {
    padding: 20px;
}

.place-title-link {
    text-decoration: none;
}

.place-title-link h4 {
    font-size: 1.2rem;
    font-weight: 800;
    color: #1e293b;
    margin: 0 0 10px;
}

.place-desc {
    font-size: 0.9rem;
    color: #64748b;
    line-height: 1.5;
    margin-bottom: 20px;
}

.place-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: auto;
}

.place-actions {
    display: flex;
    gap: 8px;
}

.btn-action-edit, .btn-action-delete {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: 0.2s;
    font-size: 0.85rem;
}

.btn-action-edit {
    color: #3b82f6;
}

.btn-action-edit:hover {
    background: #eff6ff;
    border-color: #3b82f6;
}

.btn-action-delete {
    color: #ef4444;
}

.btn-action-delete:hover {
    background: #fef2f2;
    border-color: #ef4444;
}

.btn-view-modern {
    flex: 1;
    margin-right: 10px;
    padding: 8px;
    background: #f1f5f9;
    color: #475569;
    border-radius: 8px;
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 600;
    text-align: center;
    transition: 0.2s;
}

.btn-view-modern:hover {
    background: #e2e8f0;
    color: #1e293b;
}

/* Trips List Modern */
.trips-list-modern {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.trip-card-modern {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 20px;
    background: #f8fafc;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
    transition: 0.2s;
}

.trip-card-modern:hover {
    background: white;
    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    border-color: #3b82f6;
}

.trip-card-icon {
    width: 50px;
    height: 50px;
    background: #f0fdf4;
    color: #16a34a;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
}

.trip-card-main {
    flex: 1;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.trip-info h4 {
    margin: 0 0 5px;
    font-size: 1.1rem;
    font-weight: 800;
    color: #1e293b;
}

.trip-meta {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.85rem;
    color: #94a3b8;
    font-weight: 600;
}

.meta-separator { opacity: 0.5; }

.trip-actions {
    display: flex;
    gap: 10px;
}

.btn-action-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: 0.2s;
}

.btn-action-icon.view { background: #eff6ff; color: #2563eb; }
.btn-action-icon.delete { background: #fff1f2; color: #e11d48; }

.btn-action-icon:hover { transform: scale(1.1); }

/* Empty States */
.empty-state {
    text-align: center;
    padding: 80px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.empty-illustration {
    width: 120px;
    height: 120px;
    background: #f8fafc;
    border-radius: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3.5rem;
    color: #cbd5e1;
    margin-bottom: 30px;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.02);
}

.empty-state p {
    color: #64748b;
    font-size: 1.1rem;
    font-weight: 500;
    margin-bottom: 30px;
    max-width: 300px;
}

.btn-primary-gradient {
    display: inline-block;
    padding: 12px 30px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    text-decoration: none;
    border-radius: 50px;
    font-weight: 700;
    box-shadow: 0 10px 20px rgba(37, 99, 235, 0.2);
}

/* Modals */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(8px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 2000;
    padding: 20px;
}

.itinerary-modal-modern {
    background: white;
    width: 100%;
    max-width: 700px;
    max-height: 90vh;
    border-radius: 30px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    animation: zoomIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes zoomIn {
    from { opacity: 0; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1); }
}

.modal-header-modern {
    padding: 30px;
    background: #f8fafc;
    border-bottom: 1px solid #f1f5f9;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.modal-title-group h2 {
    margin: 0 0 10px;
    font-size: 1.5rem;
    font-weight: 800;
}

.itinerary-meta-pills {
    display: flex;
    gap: 10px;
}

.pill {
    padding: 5px 12px;
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 700;
    color: #64748b;
    display: flex;
    align-items: center;
    gap: 6px;
}

.btn-close-modern {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: none;
    background: white;
    color: #64748b;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.modal-body-modern {
    padding: 30px;
    overflow-y: auto;
}

.timeline-modern {
    display: flex;
    flex-direction: column;
    gap: 40px;
}

.day-label {
    font-size: 1.2rem;
    font-weight: 800;
    color: #16a34a;
    margin: 0 0 20px;
    padding-bottom: 10px;
    border-bottom: 2px dashed #e2e8f0;
}

.timeline-items {
    padding-left: 10px;
}

.timeline-entry {
    display: flex;
    gap: 25px;
    margin-bottom: 25px;
}

.entry-time {
    width: 70px;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
}

.time-text {
    font-weight: 800;
    font-size: 0.9rem;
    background: #f1f5f9;
    padding: 4px 10px;
    border-radius: 8px;
    margin-bottom: 10px;
}

.time-indicator {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: white;
    border: 3px solid #3b82f6;
    z-index: 2;
}

.entry-time::after {
    content: '';
    position: absolute;
    top: 40px;
    bottom: -30px;
    left: 50%;
    transform: translateX(-50%);
    width: 2px;
    background: #e2e8f0;
}

.timeline-entry:last-child .entry-time::after { display: none; }

.entry-content { flex: 1; }

.slot-type {
    font-size: 0.8rem;
    font-weight: 700;
    color: #94a3b8;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.place-preview-card {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 12px;
    background: white;
    border: 1.5px solid #f1f5f9;
    border-radius: 16px;
    cursor: pointer;
    transition: 0.2s;
}

.place-preview-card:hover {
    border-color: #3b82f6;
    background: #f8fbff;
    transform: translateX(5px);
}

.preview-img {
    width: 100px;
    height: 80px;
    border-radius: 14px;
    object-fit: cover;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.preview-info h5 {
    margin: 0 0 4px;
    font-size: 1rem;
}

.preview-rating {
    font-size: 0.85rem;
    color: #ca8a04;
    font-weight: 800;
}

.preview-info i { color: #facc15; }

/* Utilities */
.fade-in { animation: fadeIn 0.4s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

.loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 400px;
}

.spinner {
    width: 50px;
    height: 50px;
    border: 5px solid #f1f5f9;
    border-top-color: #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 20px;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* Mobile Responsiveness */
@media (max-width: 900px) {
    .profile-container {
        grid-template-columns: 1fr;
        margin-top: -50px;
    }
    .profile-sidebar {
        position: static;
    }
    .stats-row-modern {
        grid-template-columns: 1fr;
    }
    .form-grid {
        grid-template-columns: 1fr;
    }
    .full-width {
        grid-column: span 1;
    }
}
</style>