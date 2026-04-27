<template>
    <div class="edit-page-container">
        <div class="header-section">
            <div class="header-content">
                <button class="btn-back" @click="$router.push('/admin/places')">
                    <i class="fas fa-arrow-left"></i> Back
                </button>
                <div class="title-group">
                    <h1>Edit Place</h1>
                    <p class="subtitle">Manage details, coordinates, and images for this location.</p>
                </div>
            </div>
        </div>

        <div class="main-layout">
            <form @submit.prevent="updatePlace" class="form-grid">
                <div class="left-column">
                    <div class="card info-card" :class="{ 'is-locked': form.is_published }">
                        <div class="card-header">
                            <i class="fas fa-edit"></i> <span>General Info</span>
                            <div v-if="form.is_published" class="lock-badge">
                                <i class="fas fa-lock"></i> Locked (Change to Draft to edit)
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="input-row">
                                <div class="input-group">
                                    <label>Place Name</label>
                                    <input v-model="form.name" :disabled="form.is_published"
                                        placeholder="Enter place name..." required>
                                </div>
                                <div class="input-group">
                                    <label>Category</label>
                                    <select v-model="form.category_id" :disabled="form.is_published">
                                        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                                            [{{ cat.parent_type.toUpperCase() }}] {{ cat.name }}
                                        </option>
                                    </select>
                                </div>
                            </div>

                            <div class="input-group" v-if="!form.is_published" style="margin-top: 10px;">
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
                                <label>Description</label>
                                <textarea v-model="form.description" :disabled="form.is_published" rows="4"
                                    placeholder="Place details..."></textarea>
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
                                <div v-if="form.is_published" class="map-overlay-locked">
                                    <div class="overlay-msg">
                                        <i class="fas fa-info-circle"></i> Change to Draft to edit coordinates
                                    </div>
                                </div>
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
                            <span class="img-count-badge">{{ images.length }} / 10</span>
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

                                    <div v-if="!form.is_published" class="gallery-overlay">
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

                                <label v-if="!form.is_published && images.length < 10" class="gallery-add-btn">
                                    <i class="fas fa-plus"></i>
                                    <span>Add</span>
                                    <input type="file" @change="onFileChange" accept="image/*" multiple hidden>
                                </label>
                            </div>

                            <div v-else class="upload-empty-state">
                                <i class="fas fa-cloud-upload-alt"></i>
                                <p>No images uploaded</p>
                                <label v-if="!form.is_published" class="upload-first-btn">
                                    <i class="fas fa-plus"></i> Upload Images
                                    <input type="file" @change="onFileChange" accept="image/*" multiple hidden>
                                </label>
                                <span v-else class="locked-hint">Change to Draft to upload images</span>
                            </div>

                            <p class="upload-hint">
                                <i class="fas fa-info-circle"></i>
                                First image = Cover photo. Click ⭐ to set any image as cover. Max 10 images.
                            </p>
                        </div>
                    </div>

                    <div class="card opening-hours-card">
                        <div class="card-header">
                            <i class="fas fa-clock"></i> Opening Hours
                        </div>
                        <div class="card-body">
                            <div v-for="day in weekDays" :key="day.key" class="oh-row">
                                <div class="oh-day">
                                    <label class="oh-switch">
                                        <input type="checkbox" v-model="openingHours[day.key].closed" :true-value="false" :false-value="true" />
                                        <span class="oh-slider"></span>
                                    </label>
                                    <span class="oh-label">{{ day.label }}</span>
                                </div>
                                <div class="oh-times" v-if="!openingHours[day.key].closed">
                                    <input type="time" v-model="openingHours[day.key].open" class="time-input" />
                                    <span class="oh-dash">—</span>
                                    <input type="time" v-model="openingHours[day.key].close" class="time-input" />
                                </div>
                                <div class="oh-closed-label" v-else>Closed</div>
                            </div>
                        </div>
                    </div>

                    <div class="card status-card">
                        <div class="card-header">
                            <i class="fas fa-cog"></i> Publishing Status
                        </div>
                        <div class="card-body">
                            <div class="status-toggle-box" :class="form.is_published ? 'active' : 'draft'">
                                <div class="toggle-info">
                                    <strong>Status</strong>
                                    <span>{{ form.is_published ? 'Public (Published)' : 'Draft (Hidden)' }}</span>
                                </div>
                                <label class="switch">
                                    <input type="checkbox" v-model="form.is_published">
                                    <span class="slider round"></span>
                                </label>
                            </div>

                            <div class="btn-group-vertical">
                                <button type="submit" class="btn-submit-full" :disabled="isSaving">
                                    <i class="fas" :class="isSaving ? 'fa-spinner fa-spin' : 'fa-check-circle'"></i> 
                                    {{ isSaving ? 'Saving...' : 'Save All Changes' }}
                                </button>
                                <button type="button" class="btn-cancel-full" @click="$router.push('/admin/places')">
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
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { placeRepository } from '@/repositories/placeRepository'
import { categoryRepository } from '@/repositories/categoryRepository'

const route = useRoute()
const router = useRouter()
const categories = ref([])
const map = ref(null)
const marker = ref(null)
const addressPaste = ref('')
const isSaving = ref(false)

const weekDays = [
    { key: 'mon', label: 'Monday' },
    { key: 'tue', label: 'Tuesday' },
    { key: 'wed', label: 'Wednesday' },
    { key: 'thu', label: 'Thursday' },
    { key: 'fri', label: 'Friday' },
    { key: 'sat', label: 'Saturday' },
    { key: 'sun', label: 'Sunday' },
]

const defaultDayHours = () => ({ open: '08:00', close: '17:00', closed: false })

const openingHours = ref({
    mon: defaultDayHours(),
    tue: defaultDayHours(),
    wed: defaultDayHours(),
    thu: defaultDayHours(),
    fri: defaultDayHours(),
    sat: defaultDayHours(),
    sun: defaultDayHours(),
})

const images = ref([]) // เก็บ Base64 หรือ URL สำหรับโชว์ในหน้าเว็บ
const rawFiles = ref([]) // เก็บก้อนไฟล์จริง (File object) เตรียมส่งให้ Backend

const form = ref({
    name: '',
    category_id: 1,
    description: '',
    location_lat: 16.5662,
    location_lng: 104.7525,
    is_published: true
})

// --- Parse image_url: ดึงข้อมูลจาก DB แล้วเติม localhost:8000 ให้อัตโนมัติ ---
const parseImages = (imageUrl) => {
    if (!imageUrl) return []
    
    let arr = []
    if (typeof imageUrl === 'string' && imageUrl.trim().startsWith('[')) {
        try { 
            arr = JSON.parse(imageUrl) 
        } catch { 
            arr = [imageUrl.replace(/^\["?|"?\]$/g, '').replace(/\\"/g, '')] 
        }
    } else {
        arr = [imageUrl]
    }

    return arr.map(url => {
        if (!url) return null;
        if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) {
            return url;
        }
        return `http://localhost:8000${url.startsWith('/') ? '' : '/'}${url}`;
    }).filter(Boolean);
}

watch(() => form.value.is_published, (newVal) => {
    if (marker.value) {
        if (newVal) marker.value.dragging.disable()
        else marker.value.dragging.enable()
    }
})

const initMap = () => {
    if (map.value) return;
    const lat = parseFloat(form.value.location_lat) || 16.5662
    const lng = parseFloat(form.value.location_lng) || 104.7525

    map.value = L.map('map-container', { zoomControl: false }).setView([lat, lng], 15)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map.value)
    L.control.zoom({ position: 'bottomright' }).addTo(map.value);

    marker.value = L.marker([lat, lng], { draggable: !form.value.is_published }).addTo(map.value)

    map.value.on('click', (e) => {
        if (!form.value.is_published) updateMarkerPosition(e.latlng.lat, e.latlng.lng)
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

    // 1. ตรวจสอบว่าเป็นการวางลิงก์ Google Maps ที่มีพิกัด (เช่น /@16.5401,104.7570,15z)
    const urlMatch = input.match(/@(-?\d+\.\d+),(-?\d+\.\d+)/)
    
    // 2. ตรวจสอบว่าเป็นการวางพิกัดตรงๆ (เช่น 16.5401, 104.7570)
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

    // 3. Fallback ไปใช้ระบบค้นหาชื่อฟรีด้วย Nominatim (อาจจะไม่เจอชื่อที่เป๊ะแบบ Google Maps)
    const geocoder = L.Control.Geocoder.nominatim()
    geocoder.geocode(input, (results) => {
        if (results && results.length > 0) {
            const { center } = results[0]
            map.value.setView(center, 17)
            updateMarkerPosition(center.lat, center.lng)
        } else {
            alert('Location not found in free database.\n\nTip: Copy the whole Google Maps Link (URL) or exact coordinates (e.g., 16.540, 104.757) instead!')
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

// --- Multi-image handlers ---
const onFileChange = (e) => {
    const files = Array.from(e.target.files)
    files.forEach(file => {
        if (images.value.length >= 10) return
        
        // เช็คขนาดไฟล์ (5MB)
        if (file.size > 5 * 1024 * 1024) {
            alert(`File ${file.name} is too large (Max 5MB).`)
            return
        }

        // 1. เก็บไฟล์จริงไว้เตรียมส่ง
        rawFiles.value.push(file)

        // 2. แปลงเป็น Base64 ไว้โชว์หน้าเว็บ
        const reader = new FileReader()
        reader.onload = (ev) => {
            images.value.push(ev.target.result)
        }
        reader.readAsDataURL(file)
    })
    e.target.value = '' // reset
}

const removeImage = (index) => {
    images.value.splice(index, 1)
    
    // ลบไฟล์จริงออกด้วย ถ้าหากเป็นรูปใหม่ที่เพิ่งเพิ่มเข้ามา
    if (rawFiles.value[index]) {
        rawFiles.value.splice(index, 1)
    }
}

const setCover = (index) => {
    // เลื่อนรูปพรีวิวมาเป็นปก
    const [img] = images.value.splice(index, 1)
    images.value.unshift(img) 

    // เลื่อนไฟล์จริงมาเป็นปกด้วย (เพื่อส่งให้ API ตามลำดับ)
    if (rawFiles.value[index]) {
        const [file] = rawFiles.value.splice(index, 1)
        rawFiles.value.unshift(file)
    }
}

const fetchDetails = async () => {
    const id = route.params.id
    try {
        const [resPlace, resCats] = await Promise.all([
            placeRepository.getById(id),
            categoryRepository.getAll()
        ])
        const data = resPlace.data
        form.value = {
            ...data,
            location_lat: parseFloat(data.location_lat) || 16.5662,
            location_lng: parseFloat(data.location_lng) || 104.7525,
            is_published: !!data.is_published
        }
        
        // Load opening hours if present
        if (data.opening_hours && typeof data.opening_hours === 'object') {
            weekDays.forEach(d => {
                if (data.opening_hours[d.key]) {
                    openingHours.value[d.key] = { ...defaultDayHours(), ...data.opening_hours[d.key] }
                }
            })
        }

        // โหลดรูปเก่ามาแสดง
        images.value = parseImages(data.image_url)
        // สำหรับรูปเก่า เราไม่รู้ว่าเป็นไฟล์อะไร (เพราะมันอยู่บนเซิร์ฟเวอร์แล้ว) 
        // เราเลยเอาค่า URL ไปใส่ใน rawFiles ไว้ชั่วคราว เพื่อรักษาจำนวน index ให้เท่ากันกับ images
        rawFiles.value = [...images.value] 

        categories.value = resCats.data
        await nextTick()
        initMap()
    } catch (error) {
        console.error("Error:", error)
    }
}

// --- บันทึกข้อมูลด้วย FormData (เหมือนหน้า Add) ---
const updatePlace = async () => {
    const id = route.params.id
    isSaving.value = true

    try {
        const formData = new FormData()
        formData.append('name', form.value.name)
        formData.append('description', form.value.description)
        formData.append('category_id', form.value.category_id)
        formData.append('is_published', form.value.is_published ? 1 : 0)
        formData.append('location_lat', form.value.location_lat)
        formData.append('location_lng', form.value.location_lng)

        formData.append('opening_hours', JSON.stringify(openingHours.value))

        // ตรวจสอบรูปภาพ
        let hasNewImage = false;
        rawFiles.value.forEach((fileOrUrl) => {
            if (fileOrUrl instanceof File) {
                // ถ้าเป็น File แสดงว่าเพิ่งอัปโหลดใหม่
                formData.append('images', fileOrUrl)
                hasNewImage = true;
            }
        })

        // ถ้าไม่มีรูปใหม่เลย จะส่งแค่ข้อมูลทั่วไป (FastAPI จะรู้ว่าไม่ต้องอัปเดตไฟล์)
        if (!hasNewImage) {
            // เราอาจจะต้องทำระบบส่งรูปเก่าไปบอก FastAPI ด้วย แต่ในเบื้องต้นส่งแค่นี้ก่อน
        }

        await placeRepository.update(id, formData)
        
        alert('✅ Saved successfully')
        router.push('/admin/places')
    } catch (error) {
        console.error("Update Error:", error)
        alert('❌ Failed to save. ' + (error.response?.data?.detail || ''))
    } finally {
        isSaving.value = false
    }
}

onMounted(fetchDetails)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap');

.edit-page-container {
    background: #f1f5f9;
    min-height: 100vh;
    font-family: 'Kanit', sans-serif;
    color: #1e293b;
}

.header-section {
    background: white;
    padding: 20px 30px;
    border-bottom: 1px solid #e2e8f0;
    position: sticky;
    top: 0;
    z-index: 1000;
}

.header-content {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 20px;
}

.btn-back {
    padding: 10px 15px;
    border-radius: 10px;
    border: 1px solid #cbd5e1;
    background: white;
    cursor: pointer;
}

.title-group h1 {
    font-size: 1.4rem;
    margin: 0;
}

.subtitle {
    font-size: 0.85rem;
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

.map-wrapper-large {
    height: 600px;
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

.map-overlay-locked {
    position: absolute;
    inset: 0;
    background: rgba(255, 255, 255, 0.4);
    z-index: 999;
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(1px);
}

.overlay-msg {
    background: #1e293b;
    color: white;
    padding: 10px 20px;
    border-radius: 30px;
    font-size: 0.9rem;
}

/* ===================== GALLERY STYLES ===================== */
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

/* Empty upload state */
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

.locked-hint { font-size: 0.85rem; color: #94a3b8; }

.upload-hint {
    font-size: 0.8rem;
    color: #94a3b8;
    margin: 0;
    display: flex;
    align-items: flex-start;
    gap: 6px;
    line-height: 1.5;
}

/* ===================== STATUS CARD ===================== */
.status-toggle-box {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 20px;
}
.status-toggle-box.active { background: #ecfdf5; border: 1px solid #a7f3d0; }
.status-toggle-box.draft  { background: #fff1f2; border: 1px solid #fecdd3; }

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

.btn-group-vertical { display: flex; flex-direction: column; }

/* Switch Toggle */
.switch { position: relative; width: 50px; height: 26px; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider {
    position: absolute; cursor: pointer; inset: 0;
    background: #cbd5e1; transition: .4s; border-radius: 34px;
}
.slider:before {
    position: absolute; content: "";
    height: 18px; width: 18px;
    left: 4px; bottom: 4px;
    background: white; transition: .4s; border-radius: 50%;
}
input:checked + .slider { background: #10b981; }
input:checked + .slider:before { transform: translateX(24px); }

/* Lock badge */
.lock-badge {
    margin-left: auto;
    font-size: 0.78rem;
    background: #fff7ed;
    color: #c2410c;
    padding: 3px 10px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 5px;
}
</style>
