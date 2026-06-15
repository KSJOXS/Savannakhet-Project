<template>
    <div class="admin-page">
        <div class="header-content">
            <div class="title-section">
                <div class="back-link" @click="router.push('/admin/manage-users')">
                    <i class="fas fa-arrow-left"></i> Back to Users
                </div>
                <h3><i class="fas fa-id-card"></i> User Profile Details</h3>
                <p class="subtitle" v-if="!loading">Viewing information and history for <strong>@{{ userProfile?.username }}</strong></p>
            </div>
        </div>

        <div v-if="loading" class="loading-state">
            <i class="fas fa-spinner fa-spin icon-large"></i>
            <p>Loading user data...</p>
        </div>

        <div v-else-if="userProfile" class="user-detail-layout">
            <!-- Left Column: User Info -->
            <div class="user-info-sidebar">
                <div class="card profile-summary-card">
                    <div class="avatar-large">
                        <img v-if="userProfile.profile_image" :src="getImageUrl(userProfile.profile_image)" alt="avatar" />
                        <div v-else class="avatar-placeholder">{{ userProfile.username.charAt(0).toUpperCase() }}</div>
                    </div>
                    
                    <h2 class="username-display">{{ userProfile.username }}</h2>
                    <p class="email-display">{{ userProfile.email }}</p>
                    
                    <div class="badge-container">
                        <span class="role-badge" :class="userProfile.role">
                            <i :class="userProfile.role === 'admin' ? 'fas fa-shield-alt' : 'fas fa-user'"></i>
                            {{ userProfile.role.toUpperCase() }}
                        </span>
                        
                        <span class="status-badge" :class="{'active': !userProfile.deleted_at, 'suspended': userProfile.deleted_at}">
                            {{ userProfile.deleted_at ? 'SUSPENDED' : 'ACTIVE' }}
                        </span>
                    </div>

                    <div class="info-list">
                        <div class="info-item">
                            <span class="info-label">User ID:</span>
                            <span class="info-value">#{{ userProfile.id }}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Post Permission:</span>
                            <span class="perm-status" :class="userProfile.post_permission_status || 'none'">
                                {{ (userProfile.post_permission_status || 'none').toUpperCase() }}
                            </span>
                        </div>
                    </div>
                </div>
                
                <div class="card stats-card">
                    <div class="stat-box">
                        <span class="stat-number">{{ userPlaces.length }}</span>
                        <span class="stat-label">Places Added</span>
                    </div>
                    <div class="stat-box">
                        <span class="stat-number">{{ userReviews.length }}</span>
                        <span class="stat-label">Reviews</span>
                    </div>
                </div>
            </div>

            <!-- Right Column: History -->
            <div class="user-history-main">
                <div class="history-tabs">
                    <button :class="{ active: activeTab === 'places' }" @click="activeTab = 'places'">
                        <i class="fas fa-map-marked-alt"></i> Submitted Places
                    </button>
                    <button :class="{ active: activeTab === 'reviews' }" @click="activeTab = 'reviews'">
                        <i class="fas fa-star"></i> Review History
                    </button>
                </div>
                
                <!-- Places Tab -->
                <div v-if="activeTab === 'places'" class="history-content fade-in">
                    <div v-if="userPlaces.length === 0" class="empty-state">
                        <i class="fas fa-map-signs"></i>
                        <p>This user hasn't submitted any places.</p>
                    </div>
                    <div v-else class="list-container">
                        <div v-for="place in userPlaces" :key="place.id" class="list-card">
                            <img :src="getPlaceImage(place.image_url)" alt="place" class="list-img" />
                            <div class="list-details">
                                <div class="list-header">
                                    <h4 @click="openExternal(place.id)">{{ place.name }} <i class="fas fa-external-link-alt small-icon"></i></h4>
                                    <div class="status-actions">
                                        <span class="place-status-badge" :class="place.status">{{ place.status }}</span>
                                        <button v-if="place.status !== 'rejected'" class="btn-action-delete" @click="handleUpdatePlaceStatus(place.id, 'rejected')" title="Delete Place">
                                            <i class="fas fa-trash-alt"></i>
                                        </button>
                                        <button v-else class="btn-action-restore" @click="handleUpdatePlaceStatus(place.id, 'approved')" title="Restore Place">
                                            <i class="fas fa-undo"></i> Restore
                                        </button>
                                    </div>
                                </div>
                                <p class="list-desc">{{ truncate(place.description, 100) }}</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Reviews Tab -->
                <div v-if="activeTab === 'reviews'" class="history-content fade-in">
                    <div v-if="userReviews.length === 0" class="empty-state">
                        <i class="fas fa-comment-slash"></i>
                        <p>This user hasn't written any reviews.</p>
                    </div>
                    <div v-else class="list-container">
                        <div v-for="review in userReviews" :key="review.id" class="list-card">
                            <img :src="getPlaceImage(review.place_image)" alt="place" class="list-img" />
                            <div class="list-details">
                                <div class="list-header">
                                    <h4 @click="openExternal(review.place_id)">{{ review.place_name }} <i class="fas fa-external-link-alt small-icon"></i></h4>
                                    <div class="stars">
                                        <i v-for="n in 5" :key="n" class="fas fa-star" :class="{ 'active': n <= review.rating }"></i>
                                    </div>
                                </div>
                                <p class="review-text"><i class="fas fa-quote-left quote-icon"></i> {{ review.comment_text }}</p>
                                <div class="list-footer">
                                    <span class="date"><i class="far fa-calendar-alt"></i> {{ formatDate(review.visited_at) }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div v-else class="error-state">
            <i class="fas fa-exclamation-circle"></i>
            <p>Could not load user data. They may not exist or have been deleted.</p>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { userRepository } from '@/repositories/userRepository'
import { placeRepository } from '@/repositories/placeRepository'

const route = useRoute()
const router = useRouter()
const userId = route.params.id

const loading = ref(true)
const userProfile = ref(null)
const userPlaces = ref([])
const userReviews = ref([])
const activeTab = ref('places')
const updatingStatus = ref(false)

const handleUpdatePlaceStatus = async (placeId, newStatus) => {
    if (newStatus === 'rejected' && !confirm('Are you sure you want to delete this place?')) return
    
    updatingStatus.value = true
    try {
        await placeRepository.updateStatus(placeId, newStatus)
        // Update local state
        const place = userPlaces.value.find(p => p.id === placeId)
        if (place) place.status = newStatus
    } catch (err) {
        console.error("Failed to update place status:", err)
        alert("Failed to update status")
    } finally {
        updatingStatus.value = false
    }
}

const fetchData = async () => {
    loading.value = true
    try {
        const profileRes = await userRepository.getProfile(userId)
        userProfile.value = profileRes.data

        const [placesRes, reviewsRes] = await Promise.all([
            userRepository.getUserPlaces(userId),
            userRepository.getUserReviews(userId)
        ])
        
        userPlaces.value = placesRes.data
        userReviews.value = reviewsRes.data
    } catch (error) {
        console.error("Error loading user data:", error)
    } finally {
        loading.value = false
    }
}

const getImageUrl = (path) => {
    if (!path) return '';
    if (path.startsWith('http')) return path;
    return `http://127.0.0.1:8000${path.startsWith('/') ? path : '/' + path}`;
}

const getPlaceImage = (imageString) => {
    try {
        if (!imageString || imageString === '[]') return '/placeholder-image.jpg'
        const images = JSON.parse(imageString)
        if (images.length > 0) {
            return `http://127.0.0.1:8000${images[0]}`
        }
    } catch (e) {
        if (imageString && !imageString.includes('[')) return `http://127.0.0.1:8000${imageString}`
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

const openExternal = (placeId) => {
    const routeData = router.resolve({ path: `/places/${placeId}` });
    window.open(routeData.href, '_blank')
}

onMounted(() => {
    fetchData()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap');

.admin-page {
    font-family: 'Kanit', sans-serif;
    padding: 30px 40px;
    background-color: #f8fafc;
    min-height: 100vh;
}

.header-content {
    margin-bottom: 30px;
}

.back-link {
    display: inline-block;
    color: #64748b;
    cursor: pointer;
    font-weight: 500;
    margin-bottom: 15px;
    transition: 0.2s;
}

.back-link:hover {
    color: #3b82f6;
    transform: translateX(-3px);
}

.title-section h3 {
    font-size: 1.6rem;
    font-weight: 600;
    color: #0f172a;
    margin: 0;
}

.subtitle {
    color: #64748b;
    font-size: 0.95rem;
    margin-top: 5px;
}

.loading-state, .error-state {
    text-align: center;
    padding: 80px 20px;
    color: #64748b;
}

.icon-large { font-size: 3rem; margin-bottom: 15px; color: #3b82f6; }

.user-detail-layout {
    display: grid;
    grid-template-columns: 320px 1fr;
    gap: 30px;
}

.card {
    background: white;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
    padding: 25px;
    margin-bottom: 20px;
}

.profile-summary-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

.avatar-large {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 4px solid #f1f5f9;
    overflow: hidden;
    margin-bottom: 15px;
}

.avatar-large img { width: 100%; height: 100%; object-fit: cover; }
.avatar-placeholder { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: #eff6ff; color: #3b82f6; font-size: 3rem; font-weight: 600; }

.username-display { margin: 0 0 5px 0; color: #0f172a; font-size: 1.4rem; }
.email-display { margin: 0 0 20px 0; color: #64748b; font-size: 0.95rem; }

.badge-container { display: flex; gap: 10px; margin-bottom: 25px; }

.role-badge, .status-badge {
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
}
.role-badge.admin { background: #fee2e2; color: #ef4444; }
.role-badge.user { background: #f1f5f9; color: #475569; }

.status-badge.active { background: #d1fae5; color: #059669; }
.status-badge.suspended { background: #fee2e2; color: #ef4444; }

.info-list { width: 100%; border-top: 1px dashed #e2e8f0; padding-top: 20px; }
.info-item { display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 0.9rem; }
.info-label { color: #64748b; }
.info-value { color: #0f172a; font-weight: 600; }

.perm-status { font-weight: 700; font-size: 0.8rem; padding: 2px 8px; border-radius: 10px; }
.perm-status.approved { background: #d1fae5; color: #059669; }
.perm-status.pending { background: #fef3c7; color: #d97706; }
.perm-status.none { background: #f1f5f9; color: #64748b; }

.stats-card { display: flex; justify-content: space-around; padding: 20px; }
.stat-box { text-align: center; }
.stat-number { display: block; font-size: 1.8rem; font-weight: 700; color: #3b82f6; line-height: 1; }
.stat-label { font-size: 0.85rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }

.history-tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    border-bottom: 2px solid #e2e8f0;
}

.history-tabs button {
    background: none; border: none; padding: 12px 20px; font-size: 1.05rem; font-weight: 600;
    color: #64748b; cursor: pointer; border-bottom: 3px solid transparent; transition: 0.2s;
    font-family: inherit;
}
.history-tabs button:hover { color: #3b82f6; }
.history-tabs button.active { color: #3b82f6; border-bottom-color: #3b82f6; }

.empty-state { text-align: center; padding: 60px 20px; background: white; border-radius: 16px; border: 1px solid #e2e8f0; color: #94a3b8; }
.empty-state i { font-size: 3rem; margin-bottom: 15px; color: #cbd5e1; }

.list-container { display: flex; flex-direction: column; gap: 15px; }

.list-card {
    display: flex; gap: 20px; background: white; border-radius: 12px; padding: 20px;
    border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.02); transition: 0.2s;
}
.list-card:hover { border-color: #cbd5e1; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }

.list-img { width: 120px; height: 120px; border-radius: 8px; object-fit: cover; }

.list-details { flex: 1; display: flex; flex-direction: column; }
.list-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }
.list-header h4 { margin: 0; font-size: 1.2rem; color: #0f172a; cursor: pointer; transition: 0.2s; }
.list-header h4:hover { color: #3b82f6; }
.small-icon { font-size: 0.8rem; color: #94a3b8; margin-left: 5px; }

.place-status-badge { padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; }
.place-status-badge.approved { background: #d1fae5; color: #059669; }
.place-status-badge.pending { background: #fef3c7; color: #d97706; }
.place-status-badge.rejected { background: #fee2e2; color: #ef4444; }

.status-actions {
    display: flex;
    align-items: center;
    gap: 10px;
}

.btn-action-delete {
    background: none;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    padding: 5px;
    border-radius: 4px;
    transition: 0.2s;
}

.btn-action-delete:hover {
    color: #ef4444;
    background: #fee2e2;
}

.btn-action-restore {
    background: #d1fae5;
    color: #059669;
    border: 1px solid #059669;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
    display: flex;
    align-items: center;
    gap: 5px;
}

.btn-action-restore:hover {
    background: #059669;
    color: white;
}

.list-desc { margin: 0 0 15px 0; color: #64748b; font-size: 0.95rem; line-height: 1.5; }

.stars { color: #e2e8f0; font-size: 0.9rem; }
.stars .active { color: #f59e0b; }

.review-text { margin: 0 0 15px 0; font-size: 0.95rem; color: #334155; font-style: italic; flex: 1; }
.quote-icon { color: #cbd5e1; font-size: 0.8rem; margin-right: 5px; }

.list-footer { border-top: 1px solid #f1f5f9; padding-top: 10px; }
.date { font-size: 0.85rem; color: #94a3b8; }

.fade-in { animation: fadeIn 0.3s ease-in-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

@media (max-width: 1024px) { .user-detail-layout { grid-template-columns: 1fr; } .user-info-sidebar { display: flex; gap: 20px; } .card { margin-bottom: 0; flex: 1; } }
@media (max-width: 768px) { .user-info-sidebar { flex-direction: column; } .list-card { flex-direction: column; } .list-img { width: 100%; height: 160px; } }
</style>
