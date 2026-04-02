<template>
    <div class="admin-page">
        <div class="header-content">
            <div class="title-section">
                <h3><i class="fas fa-tags"></i> จัดการหมวดหมู่</h3>
                <p class="subtitle">เพิ่มหรือลบหมวดหมู่สำหรับสถานที่ท่องเที่ยวในระบบ</p>
            </div>
        </div>

        <div class="card add-card">
            <div class="add-cat-form">
                <div class="input-wrapper">
                    <i class="fas fa-plus-circle"></i>
                    <input v-model="newCatName" @keyup.enter="addCategory" placeholder="ระบุชื่อหมวดหมู่ใหม่ที่นี่...">
                </div>
                <button @click="addCategory" class="btn-primary">
                    <i class="fas fa-save"></i> เพิ่มหมวดหมู่
                </button>
            </div>
        </div>

        <div v-if="categories.length > 0" class="cat-grid">
            <div v-for="cat in categories" :key="cat.id" class="cat-card">
                <div class="cat-info">
                    <div class="icon-box">
                        <i class="fas fa-folder"></i>
                    </div>
                    <span class="cat-name">{{ cat.name }}</span>
                </div>
                <button @click="deleteCategory(cat.id)" class="btn-del" title="ลบหมวดหมู่">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </div>
        </div>

        <div v-else class="empty-state">
            <div class="empty-icon">
                <i class="fas fa-folder-open"></i>
            </div>
            <p>ยังไม่มีข้อมูลหมวดหมู่ในระบบ</p>
            <span>เริ่มสร้างหมวดหมู่แรกจากฟอร์มด้านบน</span>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const categories = ref([])
const newCatName = ref('')

const fetchCats = async () => {
    try {
        const res = await axios.get('http://127.0.0.1:8000/categories')
        categories.value = res.data
    } catch (error) {
        console.error("Fetch Error:", error)
    }
}

const addCategory = async () => {
    const name = newCatName.value.trim()
    if (!name) return
    try {
        await axios.post('http://127.0.0.1:8000/categories', { name: name })
        newCatName.value = ''
        await fetchCats()
    } catch (error) {
        alert("ไม่สามารถเพิ่มหมวดหมู่ได้")
    }
}

const deleteCategory = async (id) => {
    if (confirm('ยืนยันการลบหมวดหมู่นี้?')) {
        try {
            await axios.delete(`http://127.0.0.1:8000/categories/${id}`)
            await fetchCats()
        } catch (error) {
            alert("ไม่สามารถลบได้ เนื่องจากหมวดหมู่นี้ถูกใช้งานอยู่")
        }
    }
}

onMounted(fetchCats)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap');

.admin-page {
    font-family: 'Kanit', sans-serif;
    color: #334155;
    padding: 30px 40px;
    /* เพิ่ม Padding ซ้ายขวาให้สมดุลกับ Sidebar */
    max-width: 1200px;
    margin: 0;
    /* ชิดซ้ายเพื่อให้เข้ากับ Sidebar Layout */
    min-height: 100vh;
    background-color: #fcfcfc;
}

/* Header Section */
.header-content {
    margin-bottom: 30px;
    border-left: 5px solid #3b82f6;
    padding-left: 20px;
}

.title-section h3 {
    font-size: 1.6rem;
    font-weight: 600;
    color: #1e293b;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 12px;
}

.subtitle {
    color: #94a3b8;
    font-size: 0.95rem;
    margin-top: 4px;
}

/* Card Form */
.card.add-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    border: 1px solid #f1f5f9;
    margin-bottom: 35px;
}

.add-cat-form {
    display: flex;
    gap: 12px;
}

.input-wrapper {
    position: relative;
    flex: 1;
}

.input-wrapper i {
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);
    color: #94a3b8;
}

.input-wrapper input {
    width: 100%;
    padding: 12px 12px 12px 48px;
    border: 1.5px solid #e2e8f0;
    border-radius: 10px;
    font-size: 0.95rem;
    transition: 0.2s;
    background: #f8fafc;
}

.input-wrapper input:focus {
    background: white;
    border-color: #3b82f6;
    outline: none;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.05);
}

.btn-primary {
    background: #3b82f6;
    color: white;
    border: none;
    padding: 0 24px;
    border-radius: 10px;
    font-weight: 500;
    cursor: pointer;
    transition: 0.2s;
    display: flex;
    align-items: center;
    gap: 8px;
}

.btn-primary:hover {
    background: #2563eb;
    transform: translateY(-1px);
}

/* Cat Grid */
.cat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 16px;
}

.cat-card {
    background: white;
    padding: 16px 20px;
    border-radius: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid #f1f5f9;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    transition: 0.3s;
}

.cat-card:hover {
    transform: translateY(-3px);
    border-color: #3b82f6;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
}

.cat-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.icon-box {
    width: 40px;
    height: 40px;
    background: #f1f5f9;
    /* สีเทาอ่อนตามที่เห็นในภาพตัวอย่าง */
    color: #64748b;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    font-size: 1.1rem;
}

.cat-name {
    font-weight: 500;
    color: #334155;
}

.btn-del {
    color: #cbd5e1;
    background: transparent;
    border: none;
    width: 32px;
    height: 32px;
    border-radius: 6px;
    cursor: pointer;
    transition: 0.2s;
}

.btn-del:hover {
    color: #f43f5e;
    background: #fff1f2;
}

/* Empty State */
.empty-state {
    text-align: center;
    padding: 80px 20px;
    background: #f8fafc;
    border: 2px dashed #e2e8f0;
    border-radius: 16px;
    color: #94a3b8;
}

@media (max-width: 640px) {
    .admin-page {
        padding: 20px;
    }

    .add-cat-form {
        flex-direction: column;
    }

    .btn-primary {
        height: 45px;
        justify-content: center;
    }
}
</style>