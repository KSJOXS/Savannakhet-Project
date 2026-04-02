<template>
    <div class="admin-layout">
        <aside class="admin-sidebar">
            <div class="sidebar-brand">
                <span class="emoji">🌴</span> Admin Panel
            </div>
            <nav class="sidebar-nav">
                <router-link to="/admin" class="nav-item active">
                    <i class="fas fa-map-marker-alt"></i> จัดการสถานที่
                </router-link>
                <router-link to="/admin/categories" class="nav-item">
                    <i class="fas fa-tags"></i> จัดการหมวดหมู่
                </router-link>
                <router-link to="/admin/comments" class="nav-item">
                    <i class="fas fa-comments"></i> ตรวจสอบรีวิว
                </router-link>
                <div class="nav-divider"></div>
                <router-link to="/" class="nav-item">
                    <i class="fas fa-external-link-alt"></i> กลับสู่หน้าเว็บ
                </router-link>
            </nav>
        </aside>

        <main class="admin-main">
            <header class="admin-header">
                <h2>จัดการสถานที่ท่องเที่ยว</h2>
                <button class="btn-add" @click="openAddModal">
                    <i class="fas fa-plus"></i> เพิ่มสถานที่ใหม่
                </button>
            </header>

            <div class="admin-card">
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>รูปภาพ</th>
                            <th>ชื่อสถานที่</th>
                            <th>หมวดหมู่</th>
                            <th>คะแนน</th>
                            <th>จัดการ</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="place in places" :key="place.id">
                            <td>{{ place.id }}</td>
                            <td>
                                <img :src="place.image_url || 'https://via.placeholder.com/50'" class="table-img" />
                            </td>
                            <td><strong>{{ place.name }}</strong></td>
                            <td><span class="badge">{{ getCategoryName(place.category_id) }}</span></td>
                            <td><i class="fas fa-star text-warning"></i> {{ place.rating_avg || '0.0' }}</td>
                            <td class="actions">
                                <button class="btn-edit" @click="editPlace(place)"><i class="fas fa-edit"></i></button>
                                <button class="btn-delete" @click="deletePlace(place.id)"><i
                                        class="fas fa-trash"></i></button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </main>

        <div v-if="showModal" class="admin-modal-overlay">
            <div class="admin-modal">
                <h3>{{ isEdit ? 'แก้ไขสถานที่' : 'เพิ่มสถานที่ใหม่' }}</h3>
                <form @submit.prevent="savePlace">
                    <div class="form-group">
                        <label>ชื่อสถานที่</label>
                        <input v-model="form.name" required placeholder="เช่น Wat Xayaphoum" />
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>หมวดหมู่</label>
                            <select v-model="form.category_id">
                                <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>URL รูปภาพ</label>
                            <input v-model="form.image_url" placeholder="https://..." />
                        </div>
                    </div>
                    <div class="form-group">
                        <label>รายละเอียด</label>
                        <textarea v-model="form.description" rows="3"></textarea>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Latitude</label>
                            <input v-model="form.lat" type="number" step="any" />
                        </div>
                        <div class="form-group">
                            <label>Longitude</label>
                            <input v-model="form.lng" type="number" step="any" />
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" @click="showModal = false" class="btn-cancel">ยกเลิก</button>
                        <button type="submit" class="btn-save">บันทึกข้อมูล</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const places = ref([])
const categories = ref([])
const showModal = ref(false)
const isEdit = ref(false)

const form = ref({
    id: null,
    name: '',
    category_id: 1,
    image_url: '',
    description: '',
    lat: '',
    lng: ''
})

const fetchData = async () => {
    try {
        const [resPlaces, resCats] = await Promise.all([
            axios.get('http://127.0.0.1:8000/places'),
            axios.get('http://127.0.0.1:8000/categories')
        ])
        places.value = resPlaces.data
        categories.value = resCats.data
    } catch (err) {
        console.error("Fetch error:", err)
    }
}

const openAddModal = () => {
    isEdit.value = false
    form.value = { name: '', category_id: 1, image_url: '', description: '', lat: '', lng: '' }
    showModal.value = true
}

const editPlace = (place) => {
    isEdit.value = true
    form.value = { ...place }
    showModal.value = true
}

const savePlace = async () => {
    try {
        if (isEdit.value) {
            await axios.put(`http://127.0.0.1:8000/places/${form.value.id}`, form.value)
        } else {
            await axios.post('http://127.0.0.1:8000/places', form.value)
        }
        showModal.value = false
        fetchData()
    } catch (err) {
        alert('ไม่สามารถบันทึกข้อมูลได้')
    }
}

const deletePlace = async (id) => {
    if (!confirm('คุณแน่ใจหรือไม่ที่จะลบสถานที่นี้?')) return
    try {
        await axios.delete(`http://127.0.0.1:8000/places/${id}`)
        fetchData()
    } catch (err) {
        alert('ลบไม่สำเร็จ')
    }
}

const getCategoryName = (id) => categories.value.find(c => c.id === id)?.name || 'ทั่วไป'

onMounted(fetchData)
</script>

<style scoped>
.admin-layout {
    display: flex;
    min-height: 100vh;
    background-color: #f1f5f9;
}

/* Sidebar */
.admin-sidebar {
    width: 260px;
    background: #1e293b;
    color: white;
    padding: 20px;
}

.sidebar-brand {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 40px;
}

.sidebar-nav {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.nav-item {
    color: #94a3b8;
    text-decoration: none;
    padding: 12px 15px;
    border-radius: 10px;
    transition: 0.3s;
}

.nav-item:hover,
.nav-item.active {
    background: #334155;
    color: white;
}

.nav-divider {
    height: 1px;
    background: #334155;
    margin: 15px 0;
}

/* Main Content */
.admin-main {
    flex: 1;
    padding: 40px;
}

.admin-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}

.btn-add {
    background: #3498db;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 10px;
    font-weight: bold;
    cursor: pointer;
}

/* Table */
.admin-card {
    background: white;
    border-radius: 15px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.admin-table {
    width: 100%;
    border-collapse: collapse;
}

.admin-table th {
    background: #f8fafc;
    padding: 15px;
    text-align: left;
    border-bottom: 1px solid #e2e8f0;
    color: #64748b;
}

.admin-table td {
    padding: 15px;
    border-bottom: 1px solid #f1f5f9;
}

.table-img {
    width: 50px;
    height: 50px;
    border-radius: 8px;
    object-fit: cover;
}

.badge {
    background: #e0f2fe;
    color: #0369a1;
    padding: 4px 10px;
    border-radius: 50px;
    font-size: 0.85rem;
}

/* Actions */
.actions {
    display: flex;
    gap: 10px;
}

.btn-edit {
    color: #3498db;
    background: none;
    border: none;
    font-size: 1.1rem;
    cursor: pointer;
}

.btn-delete {
    color: #ef4444;
    background: none;
    border: none;
    font-size: 1.1rem;
    cursor: pointer;
}

/* Modal */
.admin-modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 100;
}

.admin-modal {
    background: white;
    width: 500px;
    padding: 30px;
    border-radius: 20px;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
}

.btn-save {
    background: #3498db;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: bold;
}

.btn-cancel {
    background: #f1f5f9;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
}
</style>