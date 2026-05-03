<template>
    <div class="profile-page">
        <Navbar />
        
        <div class="profile-container">
            <div class="profile-card">
                <div class="profile-header">
                    <h2>⚙️ Account Settings</h2>
                    <p>View and update your personal information</p>
                </div>
                
                <div v-if="loading" class="loading-state">
                    <div class="spinner"></div>
                    <p>Loading your profile...</p>
                </div>
                
                <!-- TAB: Settings -->
                <form v-if="!loading && activeTab === 'settings'" @submit.prevent="handleUpdate" class="profile-form">
                    
                    <div class="avatar-section">
                        <div class="avatar-wrapper" :class="{ 'is-editing': isEditing }" @click="isEditing && triggerImageUpload()">
                            <img :src="currentProfileImage" alt="Profile Avatar" class="avatar-img" />
                            <div v-if="isEditing" class="avatar-overlay">
                                <i class="fas fa-camera"></i>
                            </div>
                        </div>
                        <p v-if="isEditing" class="avatar-hint">Click the image to change</p>
                        
                        <input 
                            type="file" 
                            ref="fileInput" 
                            class="hidden-input" 
                            accept="image/jpeg,image/png,image/webp" 
                            @change="onImageSelected" 
                        />
                    </div>

                    <div class="input-group">
                        <label>Username</label>
                        <input v-model="form.username" type="text" placeholder="Username" :disabled="!isEditing" />
                    </div>
                    
                    <div class="input-group">
                        <label>Email Address</label>
                        <input v-model="form.email" type="email" placeholder="Email address" :disabled="!isEditing" />
                    </div>
                    
                    <div class="input-group" v-if="isEditing">
                        <label>New Password <span style="color:#94a3b8; font-weight:400;">(optional)</span></label>
                        <input v-model="form.password" type="password" placeholder="Leave blank to keep current" />
                    </div>
                    
                    <div class="form-actions">
                        <p v-if="successMsg" class="success-msg">{{ successMsg }}</p>
                        <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

                        <div class="btn-group-profile">
                            <button v-if="!isEditing" type="button" class="btn-edit" @click="isEditing = true">
                                <i class="fas fa-edit"></i> Edit Profile
                            </button>
                            
                            <template v-else>
                                <button type="button" class="btn-cancel" @click="cancelEdit" :disabled="saving">
                                    Cancel
                                </button>
                                <button type="submit" class="btn-save" :disabled="saving">
                                    <i class="fas fa-save"></i> {{ saving ? 'Saving...' : 'Save Changes' }}
                                </button>
                            </template>
                        </div>
                    </div>
                </form>

                <!-- TAB: Social History (formerly Reviews) -->
                <div v-if="!loading && activeTab === 'reviews'" class="history-section fade-in">
                    <div class="stats-row">
                        <div class="stat-card">
                            <span class="stat-value">{{ userReviews.length }}</span>
                            <span class="stat-label">Total Posts</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-value">{{ averageRating }}</span>
                            <span class="stat-label">Avg Rating</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-value">{{ userPlaces.length }}</span>
                            <span class="stat-label">Places Submitted</span>
                        </div>
                    </div>

                    <div v-if="userReviews.length === 0" class="empty-history">
                        <div class="empty-icon-wrap"><i class="fas fa-comment-slash"></i></div>
                        <p>You haven't shared any experiences yet.</p>
                        <router-link to="/community" class="btn-primary-outline">Go to Community</router-link>
                    </div>
                    
                    <div v-else class="social-history-feed">
                        <div v-for="review in userReviews" :key="review.id" class="social-post-card">
                            <div class="post-header">
                                <div class="place-info">
                                    <router-link :to="`/places/${review.place_id}`" class="place-name-link">
                                        {{ review.place_name }}
                                    </router-link>
                                    <span class="post-date">{{ formatDate(review.visited_at) }}</span>
                                </div>
                                <div class="rating-badge">
                                    <i class="fas fa-star"></i> {{ review.rating }}
                                </div>
                            </div>
                            <div class="post-body">
                                <p class="post-text">{{ review.comment_text }}</p>
                                
                                <div v-if="review.images && review.images.length > 0" class="post-images-grid">
                                    <div v-for="(img, idx) in review.images" :key="idx" class="img-thumb" @click="openLightbox(review.images, idx)">
                                        <img :src="getImageUrl(img)" />
                                    </div>
                                </div>
                            </div>
                            <div class="post-footer">
                                <span class="likes-count"><i class="fas fa-heart text-danger"></i> {{ review.liked_by?.length || 0 }} likes</span>
                                <button class="btn-view-place" @click="$router.push(`/places/${review.place_id}`)">View Place</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- TAB: Places -->
                <div v-if="!loading && activeTab === 'places'" class="history-section fade-in">
                    <div class="section-header">
                        <h3><i class="fas fa-map-marked-alt text-primary"></i> Places You Added</h3>
                        <p class="text-muted">Locations you have contributed to the directory.</p>
                    </div>
                    <div v-if="userPlaces.length === 0" class="empty-history">
                        <div class="empty-icon-wrap"><i class="fas fa-map-signs"></i></div>
                        <p>You haven't submitted any places yet.</p>
                        <router-link to="/submit-place" class="btn-primary-action mt-3">Submit a Place</router-link>
                    </div>
                    <div v-else class="place-grid">
                        <div v-for="place in userPlaces" :key="place.id" class="history-card">
                            <div class="card-img-wrapper">
                                <img :src="getPlaceImage(place.image_url)" alt="place" class="history-card-img" />
                                <div class="status-badge" :class="place.status">
                                    {{ place.status === 'pending' ? '⏳ Pending' : (place.status === 'approved' ? '✅ Approved' : '❌ Rejected') }}
                                </div>
                            </div>
                            <div class="history-card-body">
                                <router-link :to="`/places/${place.id}`" class="place-link">
                                    <h4>{{ place.name }}</h4>
                                </router-link>
                                <p class="desc-text">{{ truncate(place.description, 70) }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- TAB: Trips -->
                <div v-if="!loading && activeTab === 'trips'" class="history-section fade-in">
                    <div class="section-header">
                        <h3><i class="fas fa-route text-success"></i> Your Saved Trips</h3>
                        <p class="text-muted">Personalized travel plans you have saved.</p>
                    </div>
                    
                    <div v-if="userItineraries.length === 0" class="empty-history">
                        <div class="empty-icon-wrap"><i class="fas fa-suitcase-rolling"></i></div>
                        <p>You haven't saved any trip plans yet.</p>
                        <router-link to="/trip-planner" class="btn-primary-action mt-3">Plan a New Trip</router-link>
                    </div>

                    <div v-else class="itinerary-list">
                        <div v-for="itinerary in userItineraries" :key="itinerary.id" class="itinerary-card">
                            <div class="itinerary-card-header">
                                <div>
                                    <h4>{{ itinerary.title }}</h4>
                                    <span class="itinerary-meta">
                                        <i class="fas fa-calendar-day"></i> {{ itinerary.days }} Days 
                                        <span class="dot">•</span> 
                                        <i class="fas fa-clock"></i> {{ formatDate(itinerary.created_at) }}
                                    </span>
                                </div>
                                <button class="btn-delete-itinerary" @click="confirmDeleteItinerary(itinerary.id)" title="Delete Plan">
                                    <i class="fas fa-trash-alt"></i>
                                </button>
                            </div>
                            
                            <div class="itinerary-card-body">
                                <div class="itinerary-items-preview">
                                    <div v-for="day in itinerary.days" :key="day" class="day-preview">
                                        <span class="day-num">Day {{ day }}</span>
                                        <div class="day-dots">
                                            <div v-for="item in itinerary.items.filter(i => i.day === day)" :key="item.id" 
                                                 class="item-dot" :title="item.time_slot"></div>
                                        </div>
                                    </div>
                                </div>
                                <router-link :to="{ name: 'TripPlanner', query: { id: itinerary.id }}" class="btn-view-itinerary">
                                    View Full Plan <i class="fas fa-chevron-right"></i>
                                </router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import { userRepository } from '@/repositories/userRepository'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const route = useRoute()
const { user } = useAuth()
const loading = ref(true)
const saving = ref(false)
const isEditing = ref(false)
const successMsg = ref('')
const errorMsg = ref('')

const activeTab = ref('settings')
const userReviews = ref([])
const userPlaces = ref([])
const userItineraries = ref([])

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
    profile_image: ''
})

// 📸 คำนวณรูปภาพที่จะแสดง (ถ้าเลือกรูปใหม่โชว์ Preview / ถ้าไม่มีใช้รูปจำลองจากชื่อ)
const currentProfileImage = computed(() => {
    if (imagePreview.value) return imagePreview.value;
    
    if (form.value.profile_image) {
        const url = form.value.profile_image;
        if (url.startsWith('http') || url.startsWith('data:')) return url;
        return `http://localhost:8000/${url.startsWith('/') ? url.slice(1) : url}`;
    }
    
    // รูปภาพ Default แบบ Generate จากชื่อ
    return `https://ui-avatars.com/api/?name=${form.value.username || 'User'}&background=3498db&color=fff&size=150`;
})

// 📸 สั่งคลิก Input File
const triggerImageUpload = () => {
    fileInput.value.click()
}

// 📸 จัดการเมื่อผู้ใช้เลือกไฟล์
const onImageSelected = (e) => {
    const file = e.target.files[0];
    if (file) {
        selectedFile.value = file;
        imagePreview.value = URL.createObjectURL(file);
    }
}

const cancelEdit = () => {
    isEditing.value = false
    form.value = { ...originalData.value, password: '' }
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
        form.value.profile_image = res.data.profile_image // ดึงรูปโปรไฟล์มาเก็บ
        originalData.value = { 
            username: res.data.username, 
            email: res.data.email, 
            profile_image: res.data.profile_image 
        }
        
        // Fetch history parallelly
        const [reviewsRes, placesRes, itinerariesRes] = await Promise.all([
            userRepository.getUserReviews(user.value.id),
            userRepository.getUserPlaces(user.value.id),
            userRepository.getItineraries(user.value.id)
        ])
        userReviews.value = reviewsRes.data.map(r => ({
            ...r,
            images: r.images || [],
            liked_by: r.liked_by || []
        }))
        userPlaces.value = placesRes.data
        userItineraries.value = itinerariesRes.data
        
    } catch (err) {
        console.error("Error fetching profile:", err)
        errorMsg.value = "ไม่สามารถดึงข้อมูลโปรไฟล์ได้"
    } finally {
        loading.value = false
    }
}

const handleUpdate = async () => {
    saving.value = true
    successMsg.value = ''
    errorMsg.value = ''
    
    // 📦 ใช้ FormData เพราะมีการอัปโหลดไฟล์รูปภาพ
    const formData = new FormData()
    if (form.value.username) formData.append('username', form.value.username)
    if (form.value.email) formData.append('email', form.value.email)
    if (form.value.password) formData.append('password', form.value.password)
    
    // แนบไฟล์รูปถ้ามีการเลือกรูปใหม่
    if (selectedFile.value) {
        formData.append('profile_image', selectedFile.value)
    }
    
    try {
        // 🚨 หมายเหตุ: Backend ของคุณต้องรองรับการรับค่าแบบ form-data ใน Endpoint นี้นะครับ
        const res = await userRepository.updateProfile(user.value.id, formData)
        successMsg.value = "Profile updated successfully!"
        
        // Update local storage
        const currentData = JSON.parse(localStorage.getItem('user') || '{}')
        currentData.username = res.data.username
        currentData.profile_image = res.data.profile_image // อัปเดตรูปใหม่ใน LocalStorage
        localStorage.setItem('user', JSON.stringify(currentData))
        
        // Update user state
        user.value.username = res.data.username 
        if (res.data.profile_image) user.value.profile_image = res.data.profile_image
        
        // Update form state
        form.value.profile_image = res.data.profile_image
        originalData.value = { ...form.value }
        
        isEditing.value = false
        form.value.password = ''
        selectedFile.value = null
        imagePreview.value = null
    } catch (err) {
        errorMsg.value = err.response?.data?.detail || "Something went wrong. Please try again."
    } finally {
        saving.value = false
    }
}

const getPlaceImage = (imageString) => {
    try {
        if (!imageString || imageString === '[]') return '/placeholder-image.jpg'
        const images = JSON.parse(imageString)
        if (images.length > 0) {
            return `http://localhost:8000${images[0]}`
        }
    } catch (e) {
        // อาจเป็น string เปล่าๆ ไม่ใช่ JSON
        if (imageString && !imageString.includes('[')) return `http://localhost:8000${imageString}`
    }
    return '/placeholder-image.jpg'
}

const truncate = (text, length) => {
    if (!text) return ''
    return text.length > length ? text.substring(0, length) + '...' : text
}

const formatDate = (dateString) => {
    if (!dateString) return ''
    const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }
    return new Date(dateString).toLocaleDateString('en-US', options)
}

const getImageUrl = (url) => {
    if (!url) return '';
    if (url.startsWith('http') || url.startsWith('data:')) return url;
    return `http://localhost:8000/${url.startsWith('/') ? url.slice(1) : url}`;
}

watch(() => route.query.tab, (newTab) => {
    activeTab.value = newTab || 'settings'
})

const confirmDeleteItinerary = async (id) => {
    if (confirm("Are you sure you want to delete this trip plan?")) {
        try {
            await userRepository.deleteItinerary(id)
            userItineraries.value = userItineraries.value.filter(it => it.id !== id)
        } catch (err) {
            console.error("Error deleting itinerary:", err)
            alert("Failed to delete itinerary.")
        }
    }
}

onMounted(() => {
    activeTab.value = route.query.tab || 'settings'
    fetchProfile()
})
</script>

<style scoped>
.profile-page {
    background: linear-gradient(135deg, #1e5799 0%, #2989d8 50%, #207cca 100%) !important;
    min-height: 100vh;
    width: 100%;
}

.profile-container {
    max-width: 600px;
    margin: 60px auto;
    padding: 0 20px;
}

.profile-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.2);
}

.profile-header {
    text-align: center;
    margin-bottom: 30px;
}

.profile-header h2 {
    color: #1e293b;
    margin: 0 0 10px;
    font-size: 1.8rem;
}

.profile-header p {
    color: #64748b;
    font-size: 0.95rem;
}

/* 📸 Avatar Styles */
.avatar-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 25px;
}

.avatar-wrapper {
    position: relative;
    width: 110px;
    height: 110px;
    border-radius: 50%;
    overflow: hidden;
    border: 4px solid white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: 0.3s;
}

.avatar-wrapper.is-editing {
    cursor: pointer;
}

.avatar-wrapper.is-editing:hover {
    box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
    transform: translateY(-2px);
}

.avatar-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-overlay {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-size: 1.8rem;
    opacity: 0;
    transition: 0.3s;
}

.avatar-wrapper.is-editing:hover .avatar-overlay {
    opacity: 1;
}

.avatar-hint {
    font-size: 0.8rem;
    color: #94a3b8;
    margin-top: 10px;
}

.hidden-input {
    display: none;
}

/* Form Styles */
.profile-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.input-group label {
    display: block;
    font-weight: 700;
    color: #334155;
    margin-bottom: 8px;
    font-size: 0.9rem;
}

.input-group input {
    width: 100%;
    padding: 12px 15px;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    background: #f8fafc;
    color: #1e293b;
    transition: 0.3s;
    box-sizing: border-box;
}

.input-group input:disabled {
    background: #e2e8f0;
    color: #64748b;
    cursor: not-allowed;
    border-color: #cbd5e1;
}

.input-group input:focus {
    border-color: #3498db;
    outline: none;
    background: white;
}

.btn-group-profile {
    display: flex;
    gap: 15px;
    margin-top: 10px;
}

.btn-edit, .btn-cancel, .btn-save {
    flex: 1;
    padding: 12px;
    border-radius: 50px;
    border: none;
    font-weight: bold;
    font-size: 1rem;
    cursor: pointer;
    transition: 0.3s;
    color: white;
}

.btn-edit {
    background: #f59e0b;
}

.btn-edit:hover {
    background: #d97706;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(245, 158, 11, 0.3);
}

.btn-cancel {
    background: #94a3b8;
}

.btn-cancel:hover {
    background: #64748b;
}

.btn-save {
    background: #3498db;
    margin-top: 10px;
}

.btn-save:hover:not(:disabled) {
    background: #2980b9;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
}

.btn-save:disabled {
    background: #94a3b8;
    cursor: not-allowed;
}

.success-msg { color: #10b981; text-align: center; margin-bottom: 10px; font-weight: bold; }
.error-msg { color: #ef4444; text-align: center; margin-bottom: 10px; font-weight: bold; }
.loading-state { text-align: center; padding: 40px 0; color: #64748b; }

.spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 0 auto 15px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Social History Feed Styles */
.social-history-feed {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.social-post-card {
    background: #f8fafc;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #e2e8f0;
    transition: 0.3s;
}

.social-post-card:hover {
    border-color: #3b82f6;
    background: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.post-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 15px;
    align-items: center;
}

.place-tag {
    background: #e0f2fe;
    color: #0369a1;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 700;
    text-decoration: none;
}

/* 📊 Stats Row */
.stats-row {
    display: flex;
    gap: 15px;
    margin-bottom: 30px;
}

.stat-card {
    flex: 1;
    background: #f8fafc;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    border: 1px solid #e2e8f0;
}

.stat-value {
    display: block;
    font-size: 1.5rem;
    font-weight: 800;
    color: #1e293b;
}

.stat-label {
    font-size: 0.8rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* 📱 Social History Feed */
.social-history-feed {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.social-post-card {
    background: white;
    border: 1px solid #eef2f6;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 10px;
    transition: 0.3s;
}

.social-post-card:hover {
    box-shadow: 0 8px 25px rgba(0,0,0,0.05);
    transform: translateY(-2px);
}

.post-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 15px;
}

.place-name-link {
    display: block;
    font-weight: 700;
    color: #1e293b;
    font-size: 1.1rem;
    text-decoration: none;
}

.place-name-link:hover {
    color: #3498db;
}

.post-date {
    font-size: 0.8rem;
    color: #94a3b8;
}

.rating-badge {
    background: #fef9c3;
    color: #854d0e;
    padding: 4px 10px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 5px;
}

.post-text {
    color: #334155;
    line-height: 1.6;
    margin-bottom: 15px;
}

.post-images-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 10px;
    margin-bottom: 15px;
}

.img-thumb {
    aspect-ratio: 1;
    border-radius: 10px;
    overflow: hidden;
    cursor: pointer;
}

.img-thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.post-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 15px;
    border-top: 1px solid #f1f5f9;
}

.likes-count {
    font-size: 0.9rem;
    color: #64748b;
    font-weight: 600;
}

.btn-view-place {
    background: #eff6ff;
    color: #1d4ed8;
    border: none;
    padding: 6px 15px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
    transition: 0.2s;
}

.btn-view-place:hover {
    background: #dbeafe;
}

.history-section {
    padding: 10px 0;
}

.history-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    overflow: hidden;
    transition: 0.3s;
    display: flex;
    flex-direction: column;
}

.history-card:hover {
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    transform: translateY(-4px);
    border-color: #cbd5e1;
}

.card-img-wrapper {
    position: relative;
    height: 160px;
    width: 100%;
}

.history-card-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.rating-badge {
    position: absolute;
    bottom: 10px;
    left: 10px;
    background: rgba(0,0,0,0.7);
    color: #fcd34d;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    backdrop-filter: blur(4px);
}

.status-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    backdrop-filter: blur(4px);
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}
.status-badge.approved { background: rgba(16, 185, 129, 0.9); color: white; }
.status-badge.pending { background: rgba(245, 158, 11, 0.9); color: white; }
.status-badge.rejected { background: rgba(239, 68, 68, 0.9); color: white; }

.history-card-body {
    padding: 18px;
    flex: 1;
    display: flex;
    flex-direction: column;
}

.place-link {
    text-decoration: none;
    color: #0f172a;
}

.place-link h4 {
    margin: 0 0 10px 0;
    font-size: 1.15rem;
    transition: 0.2s;
    line-height: 1.3;
}

.place-link:hover h4 {
    color: #3b82f6;
}

.comment-text {
    margin: 0 0 15px 0;
    font-size: 0.9rem;
    color: #475569;
    line-height: 1.5;
    flex: 1;
}

.quote-icon {
    color: #cbd5e1;
    font-size: 0.8rem;
    margin-right: 4px;
}

.card-footer-info {
    margin-top: auto;
    padding-top: 12px;
    border-top: 1px dashed #e2e8f0;
}

.date-text {
    color: #94a3b8;
    font-size: 0.8rem;
    font-weight: 500;
}

.desc-text {
    margin: 0;
    font-size: 0.9rem;
    color: #64748b;
    line-height: 1.5;
}

.fade-in {
    animation: fadeIn 0.4s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 600px) {
    .profile-card { padding: 25px; }
    .review-grid, .place-grid { grid-template-columns: 1fr; }
}
</style>