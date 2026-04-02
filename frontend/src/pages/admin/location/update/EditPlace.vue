<template>
    <div class="edit-page-container">
        <div class="header-section">
            <div class="header-content">
                <button class="btn-back" @click="$router.push('/admin/places')">
                    <i class="fas fa-arrow-left"></i> ย้อนกลับ
                </button>
                <div class="title-group">
                    <h1>แก้ไขข้อมูลสถานที่</h1>
                    <p class="subtitle">จัดการรายละเอียด พิกัด และรูปภาพของสถานที่</p>
                </div>
            </div>
        </div>

        <div class="main-layout">
            <form @submit.prevent="updatePlace" class="form-grid">
                <div class="left-column">
                    <div class="card info-card" :class="{ 'is-locked': form.is_published }">
                        <div class="card-header">
                            <i class="fas fa-edit"></i> <span>ข้อมูลทั่วไป</span>
                            <div v-if="form.is_published" class="lock-badge">
                                <i class="fas fa-lock"></i> ข้อมูลถูกล็อค (ปิด Public เพื่อแก้ไข)
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="input-row">
                                <div class="input-group">
                                    <label>ชื่อสถานที่</label>
                                    <input v-model="form.name" :disabled="form.is_published"
                                        placeholder="ระบุชื่อสถานที่..." required>
                                </div>
                                <div class="input-group">
                                    <label>หมวดหมู่</label>
                                    <select v-model="form.category_id" :disabled="form.is_published">
                                        <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}
                                        </option>
                                    </select>
                                </div>
                            </div>

                            <div class="input-group" v-if="!form.is_published" style="margin-top: 10px;">
                                <label style="color: #6366f1;"><i class="fas fa-paste"></i> วางที่อยู่/Plus Code จาก
                                    Google Maps (Auto Lock)</label>
                                <div style="display: flex; gap: 10px;">
                                    <input v-model="addressPaste" @paste="handlePasteAddress"
                                        placeholder="วาง Plus Code เช่น HP4W+G5V หรือชื่อสถานที่..."
                                        style="border: 2px solid #6366f1; background: #f5f3ff;">
                                    <button type="button" @click="searchFromAddress"
                                        style="background: #6366f1; color: white; border: none; padding: 0 20px; border-radius: 10px; cursor: pointer;">
                                        ตรวจจับ
                                    </button>
                                </div>
                            </div>

                            <div class="input-group">
                                <label>รายละเอียด</label>
                                <textarea v-model="form.description" :disabled="form.is_published" rows="4"
                                    placeholder="บรรยายรายละเอียดสถานที่..."></textarea>
                            </div>
                        </div>
                    </div>

                    <div class="card map-card">
                        <div class="card-header">
                            <i class="fas fa-map-marked-alt"></i> <span>ตำแหน่งบนแผนที่</span>
                            <div class="coords-display">
                                <span>LAT: {{ form.location_lat }}</span>
                                <span>LNG: {{ form.location_lng }}</span>
                            </div>
                        </div>
                        <div class="card-body p-0">
                            <div class="map-wrapper-large">
                                <div v-if="form.is_published" class="map-overlay-locked">
                                    <div class="overlay-msg">
                                        <i class="fas fa-info-circle"></i> ปิดสถานะ Draft เพื่อแก้ไขพิกัด
                                    </div>
                                </div>
                                <div id="map-container"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="right-column">
                    <div class="card upload-card" :class="{ 'is-locked': form.is_published }">
                        <div class="card-header">
                            <i class="fas fa-image"></i> รูปภาพหน้าปก
                        </div>
                        <div class="card-body">
                            <div class="upload-zone" :class="{ 'has-image': form.image_url }">
                                <img v-if="form.image_url" :src="form.image_url" class="img-preview" alt="Preview">

                                <div v-if="!form.is_published" class="upload-overlay">
                                    <label class="upload-btn-label">
                                        <i class="fas fa-cloud-upload-alt"></i>
                                        <span>{{ form.image_url ? 'เปลี่ยนรูปภาพ' : 'อัปโหลดรูปภาพ' }}</span>
                                        <input type="file" @change="onFileChange" accept="image/*" hidden>
                                    </label>
                                </div>

                                <div v-if="!form.image_url" class="empty-state">
                                    <i class="fas fa-images"></i>
                                    <p>ยังไม่มีรูปภาพประกอบ</p>
                                </div>
                            </div>
                            <p class="upload-hint">* รองรับไฟล์ JPG, PNG (แนะนำ 1200x800px)</p>
                        </div>
                    </div>

                    <div class="card status-card">
                        <div class="card-header">
                            <i class="fas fa-cog"></i> การตั้งค่าสถานะ
                        </div>
                        <div class="card-body">
                            <div class="status-toggle-box" :class="form.is_published ? 'active' : 'draft'">
                                <div class="toggle-info">
                                    <strong>สถานะการแสดงผล</strong>
                                    <span>{{ form.is_published ? 'Public (เปิดใช้งาน)' : 'Draft (กำลังร่าง)' }}</span>
                                </div>
                                <label class="switch">
                                    <input type="checkbox" v-model="form.is_published">
                                    <span class="slider round"></span>
                                </label>
                            </div>

                            <div class="btn-group-vertical">
                                <button type="submit" class="btn-submit-full">
                                    <i class="fas fa-check-circle"></i> บันทึกข้อมูลทั้งหมด
                                </button>
                                <button type="button" class="btn-cancel-full" @click="$router.push('/admin/places')">
                                    ยกเลิก
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
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const categories = ref([])
const map = ref(null)
const marker = ref(null)
const addressPaste = ref('') // ตัวแปรสำหรับรับค่าที่ Paste

const form = ref({
    name: '',
    category_id: 1,
    image_url: '',
    description: '',
    location_lat: 16.5662,
    location_lng: 104.7525,
    is_published: true
})

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

// ฟังก์ชันดักจับการวาง (Paste)
const handlePasteAddress = (e) => {
    const pasteData = e.clipboardData.getData('text')
    addressPaste.value = pasteData
    setTimeout(() => searchFromAddress(), 100) // ดีเลย์นิดหน่อยให้ Input อัปเดต
}

// ฟังก์ชันแปลงที่อยู่เป็นพิกัดและล็อกหมุด
const searchFromAddress = () => {
    if (!addressPaste.value) return
    const geocoder = L.Control.Geocoder.nominatim()
    geocoder.geocode(addressPaste.value, (results) => {
        if (results && results.length > 0) {
            const { center } = results[0]
            map.value.setView(center, 17)
            updateMarkerPosition(center.lat, center.lng)
        } else {
            alert("ไม่พบตำแหน่งนี้ กรุณาลองระบุชื่อแขวงหรือเมืองเพิ่ม เช่น 'Savannakhet'")
        }
    })
}

const updateMarkerPosition = (lat, lng) => {
    // ป้องกันค่า NaN และปัดเศษทศนิยม
    const fixedLat = isNaN(lat) ? 16.5662 : parseFloat(parseFloat(lat).toFixed(6))
    const fixedLng = isNaN(lng) ? 104.7525 : parseFloat(parseFloat(lng).toFixed(6))

    if (marker.value) marker.value.setLatLng([fixedLat, fixedLng])
    form.value.location_lat = fixedLat
    form.value.location_lng = fixedLng
}

const onFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
        const reader = new FileReader()
        reader.onload = (ev) => { form.value.image_url = ev.target.result }
        reader.readAsDataURL(file)
    }
}

const fetchDetails = async () => {
    const id = route.params.id
    try {
        const [resPlace, resCats] = await Promise.all([
            axios.get(`http://127.0.0.1:8000/places/${id}`),
            axios.get('http://127.0.0.1:8000/categories')
        ])
        const data = resPlace.data
        form.value = {
            ...data,
            location_lat: parseFloat(data.location_lat) || 16.5662,
            location_lng: parseFloat(data.location_lng) || 104.7525,
            is_published: !!data.is_published
        }
        categories.value = resCats.data
        await nextTick()
        initMap()
    } catch (error) {
        console.error("Error:", error)
    }
}

const updatePlace = async () => {
    const id = route.params.id
    try {
        // ใช้ PUT ตามที่คุณต้องการ แก้ไข URL ให้ตรงกับ Backend ของคุณ
        await axios.put(`http://127.0.0.1:8000/admin/places/${id}`, form.value)
        alert("✅ บันทึกเรียบร้อย")
        router.push('/admin/places')
    } catch (error) {
        // แสดงรายละเอียด error ใน alert
        const msg = error.response?.status === 405 ? "405 Method Not Allowed (ตรวจสอบ Backend PUT route)" : "บันทึกไม่สำเร็จ";
        alert("❌ " + msg)
    }
}

onMounted(fetchDetails)
</script>

<style scoped>
/* CSS เดิมของคุณทั้งหมด */
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

input,
select,
textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    outline: none;
}

.map-wrapper-large {
    height: 600px;
    position: relative;
    border-radius: 0 0 20px 20px;
    overflow: hidden;
}

#map-container {
    height: 100%;
    width: 100%;
}

.coords-display {
    margin-left: auto;
    font-size: 0.8rem;
    background: #e2e8f0;
    padding: 4px 12px;
    border-radius: 15px;
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

.upload-zone {
    width: 100%;
    height: 280px;
    background: #f8fafc;
    border: 2px dashed #cbd5e1;
    border-radius: 15px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

.img-preview {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.upload-overlay {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: 0.3s;
}

.upload-zone:hover .upload-overlay {
    opacity: 1;
}

.upload-btn-label {
    background: white;
    padding: 10px 20px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
}

.status-toggle-box {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 20px;
}

.status-toggle-box.active {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
}

.status-toggle-box.draft {
    background: #fff1f2;
    border: 1px solid #fecdd3;
}

.btn-submit-full {
    background: #10b981;
    color: white;
    border: 1px none;
    padding: 15px;
    border-radius: 12px;
    width: 100%;
    font-weight: 700;
    cursor: pointer;
}

.btn-cancel-full {
    background: white;
    border: 1px solid #cbd5e1;
    padding: 12px;
    border-radius: 12px;
    color: #64748b;
    cursor: pointer;
    margin-top: 10px;
    width: 100%;
}

.switch {
    position: relative;
    width: 50px;
    height: 26px;
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    inset: 0;
    background: #cbd5e1;
    transition: .4s;
    border-radius: 34px;
}

.slider:before {
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 4px;
    bottom: 4px;
    background: white;
    transition: .4s;
    border-radius: 50%;
}

input:checked+.slider {
    background: #10b981;
}

input:checked+.slider:before {
    transform: translateX(24px);
}
</style>