<template>
    <div class="admin-page">
        <div class="page-header">
            <h2>Place Management</h2>
            <button class="btn-primary" @click="$router.push('/admin/location/create')">
                <i class="fas fa-plus"></i> Add New Place
            </button>
        </div>

        <div class="table-container">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Image</th>
                        <th>Place Name</th>
                        <th>Category</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="place in places" :key="place.id">
                        <td>
                            <img :src="getThumbnail(place.image_url)" class="thumb-img" @error="e => e.target.src = PLACEHOLDER">
                        </td>
                        <td><strong>{{ place.name }}</strong></td>
                        <td><span class="badge">{{ getCategoryName(place.category_id) }}</span></td>
                        <td>
                            <span :class="Number(place.is_published) === 1 ? 'status-active' : 'status-draft'">
                                <i class="fas"
                                    :class="Number(place.is_published) === 1 ? 'fa-check-circle' : 'fa-eye-slash'"></i>
                                {{ Number(place.is_published) === 1 ? ' Published' : ' Draft' }}
                            </span>
                        </td>
                        <td>
                            <button @click="$router.push(`/admin/location/update/${place.id}`)" class="btn-edit">
                                <i class="fas fa-edit"></i> Edit
                            </button>
                            <button @click="handleDelete(place.id)" class="btn-delete">
                                <i class="fas fa-trash"></i>
                            </button>
                        </td>
                    </tr>
                    <tr v-if="places.length === 0">
                        <td colspan="5" style="text-align: center; padding: 30px; color: #999;">
                            No places found.
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { placeRepository } from '@/repositories/placeRepository'
import { categoryRepository } from '@/repositories/categoryRepository'

const places = ref([])
const categories = ref([])

const PLACEHOLDER = `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='70' height='45' viewBox='0 0 70 45'%3E%3Crect width='70' height='45' fill='%23f1f5f9'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' fill='%2394a3b8' font-size='9' font-family='sans-serif'%3ENo Image%3C/text%3E%3C/svg%3E`

// 🛠️ ฟังก์ชัน getThumbnail ฉบับอัปเดต จัดการ JSON Array + เติม localhost ให้อัตโนมัติ
const getThumbnail = (imageUrl) => {
    if (!imageUrl) return PLACEHOLDER;
    
    let url = imageUrl;

    // 1. แกะกล่อง JSON Array ออกมาก่อน (ถ้ามี)
    if (typeof url === 'string' && url.trim().startsWith('[')) {
        try {
            const arr = JSON.parse(url);
            if (Array.isArray(arr) && arr.length > 0) {
                url = arr[0]; // เอารูปแรกมาเป็น Thumbnail
            } else {
                return PLACEHOLDER;
            }
        } catch {
            // ถ้าแกะ JSON ไม่ได้ ให้พยายามลบสัญลักษณ์วงเล็บก้ามปูทิ้งเผื่อฟลุค
            url = url.replace(/^\["?|"?\]$/g, '').replace(/\\"/g, '');
        }
    }

    // 2. ถ้ารูปเป็น Placeholder, ลิงก์เว็บนอก หรือ Base64 อยู่แล้ว ก็ใช้ได้เลย
    if (url === PLACEHOLDER || url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) {
        return url;
    }

    // 3. ถ้าเป็นแค่ Path จาก Database ให้เติม URL ของ FastAPI (localhost:8000) เข้าไป
    return `http://localhost:8000${url.startsWith('/') ? '' : '/'}${url}`;
}

const fetchData = async () => {
    try {
        const [p, c] = await Promise.all([
            placeRepository.getAll(true),
            categoryRepository.getAll()
        ])
        places.value = p.data
        categories.value = c.data
        console.log("Response Data:", p.data)
    } catch (error) {
        console.error("Error:", error)
    }
}

const handleDelete = async (id) => {
    if (confirm('Are you sure you want to delete this place?')) {
        try {
            await placeRepository.delete(id)
            await fetchData() // โหลดข้อมูลใหม่หลังจากลบ
        } catch (error) {
            console.error('Delete Error:', error)
            alert('Failed to delete. Please try again.')
        }
    }
}

const getCategoryName = (id) => {
    const cat = categories.value.find(c => c.id === id)
    return cat ? cat.name : 'General'
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