<template>
    <div class="admin-page">
        <div class="page-header">
            <h2>จัดการสถานที่ท่องเที่ยว</h2>
            <button class="btn-primary" @click="$router.push('/admin/location/create')">
                <i class="fas fa-plus"></i> เพิ่มสถานที่
            </button>
        </div>

        <div class="table-container">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>รูป</th>
                        <th>ชื่อสถานที่</th>
                        <th>หมวดหมู่</th>
                        <th>สถานะ</th>
                        <th>จัดการ</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="place in places" :key="place.id">
                        <td>
                            <img :src="place.image_url || 'https://via.placeholder.com/60x40'" class="thumb-img">
                        </td>
                        <td><strong>{{ place.name }}</strong></td>
                        <td><span class="badge">{{ getCategoryName(place.category_id) }}</span></td>
                        <td>
                            <span :class="Number(place.is_published) === 1 ? 'status-active' : 'status-draft'">
                                <i class="fas"
                                    :class="Number(place.is_published) === 1 ? 'fa-check-circle' : 'fa-eye-slash'"></i>
                                {{ Number(place.is_published) === 1 ? ' เผยแพร่แล้ว' : ' ฉบับร่าง' }}
                            </span>
                        </td>
                        <td>
                            <button @click="$router.push(`/admin/location/update/${place.id}`)" class="btn-edit">
                                <i class="fas fa-edit"></i> แก้ไข
                            </button>
                            <button @click="handleDelete(place.id)" class="btn-delete">
                                <i class="fas fa-trash"></i>
                            </button>
                        </td>
                    </tr>
                    <tr v-if="places.length === 0">
                        <td colspan="5" style="text-align: center; padding: 30px; color: #999;">
                            ไม่พบข้อมูลสถานที่
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const places = ref([])
const categories = ref([])

// ฟังก์ชันดึงข้อมูล
// ใน AdminPlaces.vue ส่วน <script setup>

const fetchData = async () => {
    try {
        // ตรวจสอบว่า URL นี้สามารถเข้าถึงได้จริงผ่าน Browser
        const [p, c] = await Promise.all([
            axios.get('http://127.0.0.1:8000/places?include_drafts=true'),
            axios.get('http://127.0.0.1:8000/categories')
        ])
        places.value = p.data
        categories.value = c.data
        console.log("Response Data:", p.data) // ดูใน Console ว่ามี status is_published: false มาไหม
    } catch (error) {
        console.error("Error:", error)
    }
}

// ฟังก์ชันลบข้อมูล
const handleDelete = async (id) => {
    if (confirm('คุณแน่ใจหรือไม่ว่าต้องการลบสถานที่นี้?')) {
        try {
            await axios.delete(`http://127.0.0.1:8000/admin/places/${id}`)
            alert('ลบข้อมูลสำเร็จ')
            await fetchData() // โหลดข้อมูลใหม่หลังจากลบ
        } catch (error) {
            console.error("Delete Error:", error)
            alert('เกิดข้อผิดพลาดในการลบข้อมูล')
        }
    }
}

// แปลง ID หมวดหมู่เป็นชื่อ
const getCategoryName = (id) => {
    const cat = categories.value.find(c => c.id === id)
    return cat ? cat.name : 'ทั่วไป'
}

onMounted(fetchData)
</script>

<style scoped>
.admin-page {
    padding: 20px;
    background: #f8f9fa;
    min-height: 100vh;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.table-container {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    overflow: hidden;
}

.admin-table {
    width: 100%;
    border-collapse: collapse;
}

.admin-table th {
    background: #f1f3f5;
    padding: 15px;
    font-weight: 600;
    color: #495057;
    text-align: left;
}

.admin-table td {
    padding: 15px;
    border-bottom: 1px solid #f1f3f5;
    vertical-align: middle;
}

.thumb-img {
    width: 70px;
    height: 45px;
    object-fit: cover;
    border-radius: 6px;
    border: 1px solid #ddd;
}

/* สถานะ */
.status-active {
    color: #27ae60;
    background: #eafaf1;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
}

.status-draft {
    color: #7f8c8d;
    background: #f4f6f6;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
}

.badge {
    background: #e8f4fd;
    color: #2980b9;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.9rem;
}

/* ปุ่มต่างๆ */
.btn-primary {
    background: #3498db;
    color: white;
    border: none;
    padding: 10px 18px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
    transition: 0.2s;
}

.btn-primary:hover {
    background: #2980b9;
}

.btn-edit {
    background: #f39c12;
    color: white;
    border: none;
    padding: 7px 14px;
    border-radius: 6px;
    margin-right: 8px;
    cursor: pointer;
    transition: 0.2s;
}

.btn-edit:hover {
    background: #e67e22;
}

.btn-delete {
    background: #e74c3c;
    color: white;
    border: none;
    padding: 7px 14px;
    border-radius: 6px;
    cursor: pointer;
    transition: 0.2s;
}

.btn-delete:hover {
    background: #c0392b;
}
</style>