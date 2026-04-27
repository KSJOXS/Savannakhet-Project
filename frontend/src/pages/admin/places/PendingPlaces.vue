<template>
    <div class="pending-places-container">
        <div class="header-section">
            <div class="title-group">
                <h1>Pending Approvals</h1>
                <p class="subtitle">Review and approve places submitted by users.</p>
            </div>
        </div>

        <div class="content-section">
            <div v-if="loading" class="loading-state">
                <i class="fas fa-spinner fa-spin"></i> Loading pending places...
            </div>
            
            <div v-else-if="pendingPlaces.length === 0" class="empty-state">
                <div class="empty-icon"><i class="fas fa-check-circle"></i></div>
                <h3>All caught up!</h3>
                <p>There are no pending places to review.</p>
            </div>

            <div v-else class="table-container">
                <table class="ta-table">
                    <thead>
                        <tr>
                            <th>Place</th>
                            <th>Category</th>
                            <th>Submitted By</th>
                            <th>Location</th>
                            <th class="actions-col">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="place in pendingPlaces" :key="place.id">
                            <td>
                                <div class="place-info">
                                    <div class="place-img-wrapper">
                                        <img :src="getCoverImage(place.image_url)" alt="cover" class="place-thumbnail">
                                    </div>
                                    <div class="place-details">
                                        <strong>{{ place.name }}</strong>
                                        <span class="place-desc">{{ truncate(place.description, 50) }}</span>
                                    </div>
                                </div>
                            </td>
                            <td>
                                <span class="category-badge">
                                    {{ place.category ? place.category.name : 'Unknown' }}
                                </span>
                            </td>
                            <td>
                                <span class="user-badge"><i class="fas fa-user"></i> User #{{ place.owner_id }}</span>
                            </td>
                            <td>
                                <a :href="`https://maps.google.com/?q=${place.location_lat},${place.location_lng}`" target="_blank" class="map-link">
                                    <i class="fas fa-map-marker-alt"></i> View Map
                                </a>
                            </td>
                            <td class="actions-col">
                                <button class="btn-approve" @click="updateStatus(place.id, 'approved')" :disabled="processingId === place.id">
                                    <i class="fas fa-check"></i> Approve
                                </button>
                                <button class="btn-reject" @click="updateStatus(place.id, 'rejected')" :disabled="processingId === place.id">
                                    <i class="fas fa-times"></i> Reject
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { placeRepository } from '@/repositories/placeRepository'

const pendingPlaces = ref([])
const loading = ref(true)
const processingId = ref(null)

const loadPendingPlaces = async () => {
    loading.value = true
    try {
        const res = await placeRepository.getPendingPlaces()
        pendingPlaces.value = res.data
    } catch (error) {
        console.error("Failed to load pending places:", error)
        alert("Could not load pending places.")
    } finally {
        loading.value = false
    }
}

const updateStatus = async (id, status) => {
    if (!confirm(`Are you sure you want to ${status} this place?`)) return
    
    processingId.value = id
    try {
        await placeRepository.updateStatus(id, status)
        // Remove from list
        pendingPlaces.value = pendingPlaces.value.filter(p => p.id !== id)
        alert(`Place successfully ${status}.`)
    } catch (error) {
        console.error(`Failed to ${status} place:`, error)
        alert(`Could not update status.`)
    } finally {
        processingId.value = null
    }
}

const getCoverImage = (imageString) => {
    try {
        if (!imageString || imageString === '[]') return '/placeholder-image.jpg'
        const images = JSON.parse(imageString)
        if (images.length > 0) {
            return `http://localhost:8000${images[0]}`
        }
    } catch (e) {
        console.error(e)
    }
    return '/placeholder-image.jpg'
}

const truncate = (text, length) => {
    if (!text) return ''
    return text.length > length ? text.substring(0, length) + '...' : text
}

onMounted(() => {
    loadPendingPlaces()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap');

.pending-places-container {
    font-family: 'Kanit', sans-serif;
    color: #1e293b;
}

.header-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}

.title-group h1 {
    font-size: 1.8rem;
    margin: 0 0 5px 0;
    color: #0f172a;
}

.subtitle {
    color: #64748b;
    margin: 0;
}

.content-section {
    background: white;
    border-radius: 15px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    padding: 25px;
    min-height: 400px;
}

.loading-state {
    text-align: center;
    padding: 50px;
    color: #64748b;
    font-size: 1.1rem;
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80px 20px;
    color: #64748b;
    text-align: center;
}

.empty-icon {
    font-size: 4rem;
    color: #10b981;
    margin-bottom: 15px;
    opacity: 0.8;
}

.empty-state h3 {
    margin: 0 0 10px 0;
    font-size: 1.5rem;
    color: #0f172a;
}

.table-container {
    overflow-x: auto;
}

.ta-table {
    width: 100%;
    border-collapse: collapse;
}

.ta-table th {
    background: #f8fafc;
    padding: 15px;
    text-align: left;
    font-weight: 600;
    color: #475569;
    border-bottom: 2px solid #e2e8f0;
}

.ta-table td {
    padding: 15px;
    border-bottom: 1px solid #f1f5f9;
    vertical-align: middle;
}

.ta-table tr:hover {
    background: #f8fafc;
}

.place-info {
    display: flex;
    align-items: center;
    gap: 15px;
}

.place-thumbnail {
    width: 60px;
    height: 60px;
    border-radius: 10px;
    object-fit: cover;
}

.place-details {
    display: flex;
    flex-direction: column;
}

.place-desc {
    font-size: 0.85rem;
    color: #64748b;
    margin-top: 4px;
}

.category-badge {
    background: #e0e7ff;
    color: #4f46e5;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
}

.user-badge {
    background: #f1f5f9;
    color: #475569;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.85rem;
}

.map-link {
    color: #3b82f6;
    text-decoration: none;
    font-weight: 500;
}
.map-link:hover {
    text-decoration: underline;
}

.actions-col {
    text-align: right;
    min-width: 180px;
}

.btn-approve, .btn-reject {
    padding: 8px 14px;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: 0.2s;
    font-size: 0.9rem;
    margin-left: 8px;
}

.btn-approve {
    background: #10b981;
    color: white;
}
.btn-approve:hover:not(:disabled) {
    background: #059669;
}

.btn-reject {
    background: #ef4444;
    color: white;
}
.btn-reject:hover:not(:disabled) {
    background: #dc2626;
}

button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
</style>
