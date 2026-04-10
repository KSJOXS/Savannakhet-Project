<template>
    <div class="admin-page">
        <div class="page-header">
            <h2>Place Management</h2>
            <button class="btn-primary" @click="$router.push('/admin/location/create')">
                <i class="fas fa-plus"></i> Add New Place
            </button>
        </div>

        <div class="filter-bar">
            <div class="search-box">
                <i class="fas fa-search"></i>
                <input v-model="searchQuery" type="text" placeholder="Search by place name..." />
            </div>

            <div class="filter-controls">
                <select v-model="selectedCategory" class="filter-select">
                    <option value="">All Categories</option>
                    <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                        {{ cat.name }}
                    </option>
                </select>

                <select v-model="selectedStatus" class="filter-select">
                    <option value="">All Statuses</option>
                    <option value="1">Published</option>
                    <option value="0">Draft</option>
                </select>

                <button v-if="searchQuery || selectedCategory !== '' || selectedStatus !== ''" @click="resetFilters"
                    class="btn-clear">
                    Clear
                </button>
            </div>
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
                    <tr v-for="place in filteredPlaces" :key="place.id">
                        <td>
                            <img :src="getThumbnail(place.image_url)" class="thumb-img"
                                @error="e => e.target.src = PLACEHOLDER">
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
                    <tr v-if="filteredPlaces.length === 0">
                        <td colspan="5" style="text-align: center; padding: 40px; color: #64748b;">
                            <i class="fas fa-search"
                                style="font-size: 2rem; margin-bottom: 10px; color: #cbd5e1; display: block;"></i>
                            No places found matching your filters.
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { placeRepository } from '@/repositories/placeRepository'
import { categoryRepository } from '@/repositories/categoryRepository'

const places = ref([])
const categories = ref([])

// 🔍 State สำหรับตัวกรอง
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedStatus = ref('')

const PLACEHOLDER = `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='70' height='45' viewBox='0 0 70 45'%3E%3Crect width='70' height='45' fill='%23f1f5f9'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' fill='%2394a3b8' font-size='9' font-family='sans-serif'%3ENo Image%3C/text%3E%3C/svg%3E`

// 🧠 Computed Property สำหรับกรองข้อมูลตาราง
const filteredPlaces = computed(() => {
    return places.value.filter(place => {
        // 1. กรองชื่อ (Search)
        const matchSearch = place.name.toLowerCase().includes(searchQuery.value.toLowerCase())

        // 2. กรองหมวดหมู่ (Category)
        const matchCategory = selectedCategory.value === '' || place.category_id === selectedCategory.value

        // 3. กรองสถานะ (Status)
        const matchStatus = selectedStatus.value === '' || Number(place.is_published) === Number(selectedStatus.value)

        return matchSearch && matchCategory && matchStatus
    })
})

// ฟังก์ชันล้างตัวกรอง
const resetFilters = () => {
    searchQuery.value = ''
    selectedCategory.value = ''
    selectedStatus.value = ''
}

const getThumbnail = (imageUrl) => {
    if (!imageUrl) return PLACEHOLDER;
    let url = imageUrl;
    if (typeof url === 'string' && url.trim().startsWith('[')) {
        try {
            const arr = JSON.parse(url);
            if (Array.isArray(arr) && arr.length > 0) {
                url = arr[0];
            } else {
                return PLACEHOLDER;
            }
        } catch {
            url = url.replace(/^\["?|"?\]$/g, '').replace(/\\"/g, '');
        }
    }
    if (url === PLACEHOLDER || url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) {
        return url;
    }
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
    } catch (error) {
        console.error("Error:", error)
    }
}

const handleDelete = async (id) => {
    if (confirm('Are you sure you want to delete this place?')) {
        try {
            await placeRepository.delete(id)
            await fetchData()
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

/* 🌟 สไตล์สำหรับ Filter Bar 🌟 */
.filter-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: white;
    padding: 15px 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
    flex-wrap: wrap;
    gap: 15px;
}

.search-box {
    position: relative;
    flex: 1;
    min-width: 250px;
    max-width: 400px;
}

.search-box i {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: #94a3b8;
}

.search-box input {
    width: 100%;
    padding: 10px 10px 10px 40px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    outline: none;
    font-size: 0.95rem;
    transition: 0.2s;
    background: #f8fafc;
}

.search-box input:focus {
    border-color: #3498db;
    background: white;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.filter-controls {
    display: flex;
    gap: 12px;
    align-items: center;
    flex-wrap: wrap;
}

.filter-select {
    padding: 10px 15px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    outline: none;
    font-size: 0.95rem;
    cursor: pointer;
    background-color: white;
    color: #475569;
    transition: 0.2s;
}

.filter-select:hover {
    border-color: #cbd5e1;
}

.filter-select:focus {
    border-color: #3498db;
}

.btn-clear {
    background: transparent;
    color: #ef4444;
    border: 1px solid #fca5a5;
    padding: 8px 15px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 600;
    transition: 0.2s;
}

.btn-clear:hover {
    background: #fef2f2;
}

/* Table Style */
.table-container {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    overflow-x: auto;
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
    font-weight: 600;
}

.status-draft {
    color: #64748b;
    background: #f1f5f9;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}

.badge {
    background: #e8f4fd;
    color: #2980b9;
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 500;
}

/* ปุ่มต่างๆ */
.btn-primary {
    background: #3498db;
    color: white;
    border: none;
    padding: 10px 18px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: 0.2s;
}

.btn-primary:hover {
    background: #2980b9;
}

.btn-edit {
    background: #f39c12;
    color: white;
    border: none;
    padding: 8px 14px;
    border-radius: 6px;
    margin-right: 8px;
    cursor: pointer;
    font-weight: 500;
    transition: 0.2s;
}

.btn-edit:hover {
    background: #e67e22;
}

.btn-delete {
    background: #ef4444;
    color: white;
    border: none;
    padding: 8px 14px;
    border-radius: 6px;
    cursor: pointer;
    transition: 0.2s;
}

.btn-delete:hover {
    background: #dc2626;
}
</style>
