<template>
    <div class="submit-page-container">
        <div class="header-section">
            <div class="header-content">
                <div class="title-group">
                    <h1>Add a New Place</h1>
                    <p class="subtitle">Know a great spot? Share it with the community!</p>
                </div>
            </div>
        </div>

        <div class="main-layout">
            
            <!-- STATE 1: Need Permission -->
            <div v-if="permissionStatus === 'none'" class="permission-state-card">
                <i class="fas fa-lock icon-large"></i>
                <h2>Permission Required</h2>
                <p>You need administrator approval before you can submit places to the directory.</p>
                <button @click="requestPermission" class="btn-primary-action" :disabled="isRequesting">
                    <i class="fas" :class="isRequesting ? 'fa-spinner fa-spin' : 'fa-paper-plane'"></i>
                    {{ isRequesting ? 'Requesting...' : 'Request Permission' }}
                </button>
            </div>

            <!-- STATE 2: Pending Approval -->
            <div v-else-if="permissionStatus === 'pending'" class="permission-state-card">
                <i class="fas fa-hourglass-half icon-large text-warning"></i>
                <h2>Waiting for Approval</h2>
                <p>Your request to submit places is currently being reviewed by an administrator. Please check back later.</p>
                <button @click="$router.push('/')" class="btn-secondary-action">
                    Return to Home
                </button>
            </div>

            <!-- STATE 3: Approved Form -->
            <form v-else-if="permissionStatus === 'approved'" @submit.prevent="submitPlace" class="form-grid">
                <div class="left-column">
                    <div class="card info-card">
                        <div class="card-header">
                            <i class="fas fa-info-circle"></i> <span>General Info</span>
                        </div>
                        <div class="card-body">
                            <div class="input-row">
                                <div class="input-group">
                                    <label>Place Name <span class="text-danger">*</span></label>
                                    <input v-model="form.name" placeholder="Enter place name..." required>
                                </div>
                                <div class="input-group">
                                    <label>Category <span class="text-danger">*</span></label>
                                    <select v-model="form.category_id" required>
                                        <option value="" disabled>Select category</option>
                                        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                                            [{{ cat.parent_type.toUpperCase() }}] {{ cat.name }}
                                        </option>
                                    </select>
                                </div>
                            </div>

                            <div class="input-group" style="margin-top: 10px;">
                                <label style="color: #6366f1;"><i class="fas fa-paste"></i> Paste Google Maps Plus Code/Address</label>
                                <div style="display: flex; gap: 10px;">
                                    <input v-model="addressPaste" @paste="handlePasteAddress"
                                        placeholder="E.g., HP4W+G5V or Place Name..."
                                        style="border: 2px solid #6366f1; background: #f5f3ff;">
                                    <button type="button" @click="searchFromAddress"
                                        style="background: #6366f1; color: white; border: none; padding: 0 20px; border-radius: 10px; cursor: pointer;">
                                        Detect
                                    </button>
                                </div>
                            </div>

                            <div class="input-group">
                                <label>Description <span class="text-danger">*</span></label>
                                <textarea v-model="form.description" rows="4" placeholder="Share your experience or details..." required></textarea>
                            </div>
                        </div>
                    </div>

                    <div class="card map-card">
                        <div class="card-header">
                            <i class="fas fa-map-marked-alt"></i> <span>Map Location</span>
                            <div class="coords-display">
                                <span>LAT: {{ form.location_lat }}</span>
                                <span>LNG: {{ form.location_lng }}</span>
                            </div>
                        </div>
                        <div class="card-body p-0">
                            <div class="map-wrapper-large">
                                <div id="map-container"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="right-column">
                    <div class="card upload-card">
                        <div class="card-header">
                            <i class="fas fa-images"></i>
                            <span>Place Images</span>
                            <span class="img-count-badge">{{ images.length }} / 5</span>
                        </div>
                        <div class="card-body">
                            <div class="gallery-grid" v-if="images.length > 0">
                                <div v-for="(img, index) in images" :key="index"
                                    class="gallery-item"
                                    :class="{ 'is-cover': index === 0 }">
                                    <img :src="img" class="gallery-img" alt="Place image">

                                    <div v-if="index === 0" class="cover-badge">
                                        <i class="fas fa-star"></i> Cover
                                    </div>

                                    <div class="gallery-overlay">
                                        <button v-if="index !== 0" type="button"
                                            class="img-action-btn set-cover-btn"
                                            @click="setCover(index)"
                                            title="Set as Cover">
                                            <i class="fas fa-star"></i>
                                        </button>
                                        <button type="button"
                                            class="img-action-btn delete-img-btn"
                                            @click="removeImage(index)"
                                            title="Remove">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </div>
                                </div>

                                <label v-if="images.length < 5" class="gallery-add-btn">
                                    <i class="fas fa-plus"></i>
                                    <span>Add</span>
                                    <input type="file" @change="onFileChange" accept="image/*" multiple hidden>
                                </label>
                            </div>

                            <div v-else class="upload-empty-state">
                                <i class="fas fa-cloud-upload-alt"></i>
                                <p>No images uploaded</p>
                                <label class="upload-first-btn">
                                    <i class="fas fa-plus"></i> Upload Images
                                    <input type="file" @change="onFileChange" accept="image/*" multiple hidden>
                                </label>
                            </div>

                            <p class="upload-hint">
                                <i class="fas fa-info-circle"></i>
                                Add up to 5 photos to showcase this place!
                            </p>
                        </div>
                    </div>

                    <div class="card submit-action-card">
                        <div class="card-body">
                            <p class="info-note">
                                <i class="fas fa-shield-alt"></i> All submitted places require admin approval before appearing on the public list.
                            </p>
                            <div class="btn-group-vertical">
                                <button type="submit" class="btn-submit-full" :disabled="isSaving">
                                    <i class="fas" :class="isSaving ? 'fa-spinner fa-spin' : 'fa-paper-plane'"></i> 
                                    {{ isSaving ? 'Submitting...' : 'Submit Place' }}
                                </button>
                                <button type="button" class="btn-cancel-full" @click="$router.push('/')">
                                    Cancel
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
/* global L */
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { placeRepository } from '@/repositories/placeRepository'
import { categoryRepository } from '@/repositories/categoryRepository'
import { userRepository } from '@/repositories/userRepository'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { user, login } = useAuth()
const categories = ref([])
const map = ref(null)
const marker = ref(null)
const addressPaste = ref('')
const isSaving = ref(false)

const permissionStatus = ref('loading')
const isRequesting = ref(false)

const images = ref([]) 
const rawFiles = ref([]) 

const form = ref({
    name: '',
    category_id: '',
    description: '',
    location_lat: 16.5662, // Savannakhet starting coordinates
    location_lng: 104.7525
})

const initMap = () => {
    if (map.value) return;
    const lat = parseFloat(form.value.location_lat)
    const lng = parseFloat(form.value.location_lng)

    map.value = L.map('map-container', { zoomControl: false }).setView([lat, lng], 15)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map.value)
    L.control.zoom({ position: 'bottomright' }).addTo(map.value);

    marker.value = L.marker([lat, lng], { draggable: true }).addTo(map.value)

    map.value.on('click', (e) => {
        updateMarkerPosition(e.latlng.lat, e.latlng.lng)
    })

    marker.value.on('dragend', () => {
        const pos = marker.value.getLatLng()
        updateMarkerPosition(pos.lat, pos.lng)
    })
}

const handlePasteAddress = (e) => {
    const pasteData = e.clipboardData.getData('text')
    addressPaste.value = pasteData
    setTimeout(() => searchFromAddress(), 100)
}

const searchFromAddress = () => {
    if (!addressPaste.value) return
    const input = addressPaste.value.trim()
    const urlMatch = input.match(/@(-?\d+\.\d+),(-?\d+\.\d+)/)
    const coordMatch = input.match(/^(-?\d+\.\d+)[\s,]+(-?\d+\.\d+)$/)

    let lat = null
    let lng = null

    if (urlMatch) {
        lat = parseFloat(urlMatch[1])
        lng = parseFloat(urlMatch[2])
    } else if (coordMatch) {
        lat = parseFloat(coordMatch[1])
        lng = parseFloat(coordMatch[2])
    }

    if (lat !== null && lng !== null) {
        map.value.setView([lat, lng], 17)
        updateMarkerPosition(lat, lng)
        return
    }

    const geocoder = L.Control.Geocoder.nominatim()
    geocoder.geocode(input, (results) => {
        if (results && results.length > 0) {
            const { center } = results[0]
            map.value.setView(center, 17)
            updateMarkerPosition(center.lat, center.lng)
        } else {
            alert('Location not found. Try copying exact coordinates.')
        }
    })
}

const updateMarkerPosition = (lat, lng) => {
    const fixedLat = isNaN(lat) ? 16.5662 : parseFloat(parseFloat(lat).toFixed(6))
    const fixedLng = isNaN(lng) ? 104.7525 : parseFloat(parseFloat(lng).toFixed(6))
    if (marker.value) marker.value.setLatLng([fixedLat, fixedLng])
    form.value.location_lat = fixedLat
    form.value.location_lng = fixedLng
}

const onFileChange = (e) => {
    const files = Array.from(e.target.files)
    files.forEach(file => {
        if (images.value.length >= 5) return
        
        if (file.size > 5 * 1024 * 1024) {
            alert(`File ${file.name} is too large (Max 5MB).`)
            return
        }

        rawFiles.value.push(file)

        const reader = new FileReader()
        reader.onload = (ev) => {
            images.value.push(ev.target.result)
        }
        reader.readAsDataURL(file)
    })
    e.target.value = ''
}

const removeImage = (index) => {
    images.value.splice(index, 1)
    rawFiles.value.splice(index, 1)
}

const setCover = (index) => {
    const [img] = images.value.splice(index, 1)
    images.value.unshift(img) 

    const [file] = rawFiles.value.splice(index, 1)
    rawFiles.value.unshift(file)
}

const submitPlace = async () => {
    if (!form.value.name || !form.value.category_id || !form.value.description) {
        alert("Please fill in Name, Category, and Description.")
        return
    }
    
    if(!user.value || !user.value.id) {
        alert("You must be logged in to submit a place.")
        router.push('/login')
        return
    }

    isSaving.value = true
    try {
        const formData = new FormData()
        formData.append('name', form.value.name)
        formData.append('description', form.value.description)
        formData.append('category_id', form.value.category_id)
        formData.append('location_lat', form.value.location_lat)
        formData.append('location_lng', form.value.location_lng)
        formData.append('user_id', user.value.id)

        rawFiles.value.forEach((file) => {
            formData.append('images', file) 
        })

        await placeRepository.submit(formData)
        
        alert('🎉 Place submitted successfully! Waiting for admin approval.')
        router.push('/')
    } catch (error) {
        console.error("Submit Error:", error)
        alert('❌ Failed to submit place.')
    } finally {
        isSaving.value = false
    }
}

const requestPermission = async () => {
    isRequesting.value = true
    try {
        await userRepository.requestPostPermission(user.value.id)
        permissionStatus.value = 'pending'
        
        // Update local user state
        const updatedUser = { ...user.value, post_permission_status: 'pending' }
        login(updatedUser, localStorage.getItem('access_token'))
        
        alert('Permission request sent successfully!')
    } catch (error) {
        console.error(error)
        alert('Failed to request permission.')
    } finally {
        isRequesting.value = false
    }
}

onMounted(async () => {
    if(!user.value) {
        router.push('/login')
        return
    }
    
    // Fetch fresh profile to get latest status
    try {
        const profileRes = await userRepository.getProfile(user.value.id)
        const profileData = profileRes.data
        permissionStatus.value = profileData.post_permission_status || 'none'
        
        // Update local context
        login(profileData, localStorage.getItem('access_token'))
    } catch(e) {
        console.error("Could not fetch user profile", e)
        permissionStatus.value = 'none'
    }

    if (permissionStatus.value === 'approved') {
        try {
            const res = await categoryRepository.getAll()
            categories.value = res.data
            await nextTick()
            initMap()
        } catch (error) {
            console.error("Failed to load categories:", error)
        }
    }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap');

.submit-page-container {
    background: #f1f5f9;
    min-height: 100vh;
    font-family: 'Kanit', sans-serif;
    color: #1e293b;
    padding-bottom: 50px;
}

.text-danger { color: #e74c3c; }

.header-section {
    background: white;
    padding: 20px 30px;
    border-bottom: 1px solid #e2e8f0;
}

.header-content {
    max-width: 1400px;
    margin: 0 auto;
}

.title-group h1 {
    font-size: 1.8rem;
    margin: 0 0 5px 0;
    color: #0f172a;
}

.subtitle {
    font-size: 1rem;
    color: #64748b;
    margin: 0;
}

.main-layout {
    max-width: 1400px;
    margin: 30px auto;
    padding: 0 20px;
}

.form-grid {
    display: grid;
    grid-template-columns: 1fr 400px;
    gap: 25px;
}

@media (max-width: 1024px) {
    .form-grid { grid-template-columns: 1fr; }
}

.card {
    background: white;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    margin-bottom: 25px;
}

.card-header {
    padding: 15px 25px;
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 600;
    border-radius: 20px 20px 0 0;
}

.img-count-badge {
    margin-left: auto;
    background: #e2e8f0;
    color: #64748b;
    font-size: 0.78rem;
    padding: 2px 10px;
    border-radius: 20px;
    font-weight: 500;
}

.card-body {
    padding: 25px;
}

.input-row {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 15px;
}

@media (max-width: 600px) {
    .input-row { grid-template-columns: 1fr; }
}

.input-group {
    margin-bottom: 15px;
}

label {
    display: block;
    font-size: 0.9rem;
    font-weight: 500;
    margin-bottom: 5px;
    color: #475569;
}

input, select, textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    outline: none;
    font-family: 'Kanit', sans-serif;
    box-sizing: border-box;
}

input:focus, select:focus, textarea:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.map-wrapper-large {
    height: 400px;
    position: relative;
    border-radius: 0 0 20px 20px;
    overflow: hidden;
}

#map-container { height: 100%; width: 100%; }

.coords-display {
    margin-left: auto;
    font-size: 0.8rem;
    background: #e2e8f0;
    padding: 4px 12px;
    border-radius: 15px;
    display: flex;
    gap: 12px;
}

.gallery-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 14px;
}

.gallery-item {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    aspect-ratio: 4/3;
    border: 2px solid #e2e8f0;
    cursor: pointer;
    transition: 0.2s;
}

.gallery-item.is-cover {
    border-color: #f59e0b;
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.2);
}

.gallery-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.cover-badge {
    position: absolute;
    top: 6px;
    left: 6px;
    background: #f59e0b;
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 4px;
}

.gallery-overlay {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    opacity: 0;
    transition: 0.25s;
}

.gallery-item:hover .gallery-overlay { opacity: 1; }

.img-action-btn {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    transition: 0.2s;
}

.set-cover-btn { background: #f59e0b; color: white; }
.set-cover-btn:hover { background: #d97706; transform: scale(1.1); }

.delete-img-btn { background: #f43f5e; color: white; }
.delete-img-btn:hover { background: #e11d48; transform: scale(1.1); }

.gallery-add-btn {
    aspect-ratio: 4/3;
    border: 2px dashed #cbd5e1;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    cursor: pointer;
    color: #94a3b8;
    font-size: 0.85rem;
    transition: 0.2s;
    font-weight: 500;
}

.gallery-add-btn:hover {
    border-color: #3b82f6;
    color: #3b82f6;
    background: #eff6ff;
}

.gallery-add-btn i { font-size: 1.4rem; }

.upload-empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    background: #f8fafc;
    border: 2px dashed #cbd5e1;
    border-radius: 15px;
    color: #94a3b8;
    margin-bottom: 14px;
    gap: 12px;
}

.upload-empty-state i { font-size: 2.5rem; }
.upload-empty-state p { margin: 0; font-weight: 500; }

.upload-first-btn {
    background: #3b82f6;
    color: white;
    padding: 10px 22px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'Kanit', sans-serif;
    transition: 0.2s;
}
.upload-first-btn:hover { background: #2563eb; }

.upload-hint {
    font-size: 0.8rem;
    color: #94a3b8;
    margin: 0;
    display: flex;
    align-items: flex-start;
    gap: 6px;
    line-height: 1.5;
}

.info-note {
    background: #eff6ff;
    color: #1e3a8a;
    padding: 15px;
    border-radius: 10px;
    font-size: 0.9rem;
    margin-bottom: 20px;
    border-left: 4px solid #3b82f6;
}

.btn-submit-full {
    background: #10b981;
    color: white;
    border: none;
    padding: 15px;
    border-radius: 12px;
    width: 100%;
    font-weight: 700;
    font-family: 'Kanit', sans-serif;
    cursor: pointer;
    transition: 0.2s;
    font-size: 1.1rem;
}
.btn-submit-full:hover:not(:disabled) { background: #059669; }
.btn-submit-full:disabled { opacity: 0.7; cursor: not-allowed; }

.btn-cancel-full {
    background: white;
    border: 1px solid #cbd5e1;
    padding: 12px;
    border-radius: 12px;
    color: #64748b;
    cursor: pointer;
    margin-top: 10px;
    width: 100%;
    font-family: 'Kanit', sans-serif;
    transition: 0.2s;
}
.btn-cancel-full:hover { background: #f8fafc; }

/* Permission States */
.permission-state-card {
    background: white;
    border-radius: 20px;
    padding: 60px 20px;
    text-align: center;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    max-width: 600px;
    margin: 50px auto;
}

.icon-large {
    font-size: 4rem;
    color: #cbd5e1;
    margin-bottom: 20px;
}
.text-warning { color: #f59e0b; }

.permission-state-card h2 {
    font-size: 1.8rem;
    color: #0f172a;
    margin-bottom: 15px;
}

.permission-state-card p {
    color: #64748b;
    font-size: 1.1rem;
    margin-bottom: 30px;
}

.btn-primary-action {
    background: #3b82f6;
    color: white;
    border: none;
    padding: 12px 30px;
    border-radius: 12px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    transition: 0.2s;
}
.btn-primary-action:hover:not(:disabled) { background: #2563eb; }
.btn-primary-action:disabled { opacity: 0.7; cursor: not-allowed; }

.btn-secondary-action {
    background: white;
    color: #475569;
    border: 1px solid #cbd5e1;
    padding: 12px 30px;
    border-radius: 12px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    transition: 0.2s;
}
.btn-secondary-action:hover { background: #f8fafc; }
</style>
