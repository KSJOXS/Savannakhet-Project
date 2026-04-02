<template>
    <div class="admin-page">
        <div class="header-content">
            <div class="title-section">
                <h3><i class="fas fa-users-cog"></i> จัดการผู้ใช้งาน</h3>
                <p class="subtitle">ตรวจสอบรายชื่อ กำหนดสิทธิ์ และจัดการบัญชีผู้ใช้งานในระบบ Savannakhet Smart Travel
                </p>
            </div>
            <div class="user-stats">
                <div class="stat-item">
                    <span class="stat-label">จำนวนผู้ใช้ทั้งหมด</span>
                    <span class="stat-value">{{ activeUsersCount }}</span>
                </div>
            </div>
        </div>

        <div class="card filter-card">
            <div class="search-form">
                <div class="input-wrapper">
                    <i class="fas fa-search"></i>
                    <input v-model="searchQuery" placeholder="ค้นหาด้วยชื่อผู้ใช้ (Username) หรืออีเมล...">
                </div>
            </div>
        </div>

        <div class="table-container">
            <table class="user-table">
                <thead>
                    <tr>
                        <th class="col-id">ID</th>
                        <th class="col-user">ชื่อผู้ใช้งาน</th>
                        <th class="col-email">อีเมล</th>
                        <th class="col-role">ระดับสิทธิ์</th>
                        <th class="col-deleted">ลบเมื่อ</th>
                        <th class="col-action">จัดการ</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in filteredUsers" :key="user.id" :class="{ 'row-deleting': user.deleted_at }">
                        <td class="col-id">#{{ user.id }}</td>
                        <td class="col-user">
                            <div class="user-info-display">
                                <div class="avatar-circle">
                                    {{ user.username.charAt(0).toUpperCase() }}
                                </div>
                                <span class="username-text">{{ user.username }}</span>
                            </div>
                        </td>
                        <td class="col-email">{{ user.email }}</td>
                        <td class="col-role">
                            <span :class="['role-badge', user.role === 'admin' ? 'admin' : 'user']">
                                <i :class="user.role === 'admin' ? 'fas fa-user-shield' : 'fas fa-user'"></i>
                                {{ user.role === 'admin' ? 'ผู้ดูแลระบบ' : 'สมาชิก' }}
                            </span>
                        </td>
                        <td class="col-deleted">
                            <span v-if="user.deleted_at" class="delete-time">
                                {{ formatDate(user.deleted_at) }}
                            </span>
                            <span v-else>-</span>
                        </td>
                        <td class="col-action">
                            <div class="action-buttons">
                                <template v-if="!user.deleted_at">
                                    <button @click="openEditModal(user)" class="btn-manage btn-edit">
                                        <i class="fas fa-edit"></i>
                                        <span>แก้ไข</span>
                                    </button>
                                    <button v-if="user.role !== 'admin'" @click="confirmDelete(user)"
                                        class="btn-manage btn-delete">
                                        <i class="fas fa-trash-alt"></i>
                                        <span>ลบ</span>
                                    </button>
                                </template>

                                <template v-else>
                                    <button @click="restoreUser(user)" class="btn-manage btn-undo-inline">
                                        <i class="fas fa-undo"></i>
                                        <span>กู้คืนข้อมูล</span>
                                    </button>
                                </template>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>

            <div v-if="filteredUsers.length === 0" class="empty-state">
                <i class="fas fa-user-slash"></i>
                <p>ไม่พบข้อมูลผู้ใช้งาน</p>
            </div>
        </div>

        <div v-if="showDeleteModal" class="modal-overlay">
            <div class="modal-content delete-modal">
                <div class="modal-header">
                    <h4 class="text-danger"><i class="fas fa-exclamation-triangle"></i> ยืนยันการลบข้อมูล</h4>
                </div>
                <div class="modal-body text-center">
                    <p>คุณต้องการลบผู้ใช้งาน <strong>{{ userToDelete?.username }}</strong> ใช่หรือไม่?</p>
                    <p class="sub-text">ข้อมูลจะถูกระงับการใช้งาน แต่ ID จะยังคงเดิมและสามารถกู้คืนได้ภายหลัง</p>
                </div>
                <div class="modal-footer">
                    <button @click="showDeleteModal = false" class="btn-secondary">
                        <i class="fas fa-arrow-left"></i> ย้อนกลับ
                    </button>
                    <button @click="executeSoftDelete" class="btn-danger-confirm">
                        ยืนยันลบข้อมูล
                    </button>
                </div>
            </div>
        </div>

        <div v-if="showEditModal" class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h4><i class="fas fa-user-edit"></i> แก้ไขระดับสิทธิ์</h4>
                    <button @click="showEditModal = false" class="close-btn">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="form-group">
                        <label>ชื่อผู้ใช้งาน:</label>
                        <input type="text" v-model="editingUser.username" disabled class="disabled-input">
                    </div>
                    <div class="form-group">
                        <label>ระดับสิทธิ์ (Role):</label>
                        <select v-model="editingUser.role" class="form-select">
                            <option value="user">สมาชิก (User)</option>
                            <option value="admin">ผู้ดูแลระบบ (Admin)</option>
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button @click="showEditModal = false" class="btn-secondary">ยกเลิก</button>
                    <button @click="updateUserRole" class="btn-primary">บันทึกข้อมูล</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const users = ref([])
const searchQuery = ref('')
const showEditModal = ref(false)
const editingUser = ref({ id: null, username: '', role: '' })
const showDeleteModal = ref(false)
const userToDelete = ref(null)

const fetchUsers = async () => {
    try {
        // ดึงข้อมูลทั้งหมด (รวมถึงคนที่ถูก Soft Delete)
        const res = await axios.get('http://127.0.0.1:8000/users')
        users.value = res.data
    } catch (error) {
        console.error("Fetch Error:", error)
    }
}

// นับจำนวนผู้ใช้ที่ยังไม่ถูกลบ
const activeUsersCount = computed(() => {
    return users.value.filter(u => !u.deleted_at).length
})

const filteredUsers = computed(() => {
    return users.value.filter(u =>
        u.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        u.email.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
})

const openEditModal = (user) => {
    editingUser.value = { ...user }
    showEditModal.value = true
}

const updateUserRole = async () => {
    try {
        await axios.put(`http://127.0.0.1:8000/users/${editingUser.value.id}`, {
            role: editingUser.value.role
        })
        showEditModal.value = false
        await fetchUsers()
    } catch (error) {
        alert("อัปเดตล้มเหลว")
    }
}

const confirmDelete = (user) => {
    userToDelete.value = user
    showDeleteModal.value = true
}

// ฟังก์ชันลบแบบ Soft Delete (อัปเดต deleted_at)
const executeSoftDelete = async () => {
    if (!userToDelete.value) return
    try {
        // ส่ง Patch หรือ Put ไปอัปเดต deleted_at ที่ Backend
        await axios.patch(`http://127.0.0.1:8000/users/${userToDelete.value.id}/soft-delete`)
        showDeleteModal.value = false
        userToDelete.value = null
        await fetchUsers()
    } catch (error) {
        alert("ลบไม่สำเร็จ")
    }
}

// ฟังก์ชันกู้คืน (ล้างค่า deleted_at ให้เป็น null)
const restoreUser = async (user) => {
    try {
        await axios.patch(`http://127.0.0.1:8000/users/${user.id}/restore`)
        await fetchUsers()
        alert(`กู้คืนผู้ใช้ ${user.username} สำเร็จ`)
    } catch (error) {
        alert("กู้คืนล้มเหลว")
    }
}

// ฟังก์ชันจัดรูปแบบวันที่
const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }
    return new Date(dateString).toLocaleDateString('th-TH', options)
}

onMounted(fetchUsers)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap');

.admin-page {
    font-family: 'Kanit', sans-serif;
    padding: 30px 40px;
    background-color: #fcfcfc;
    min-height: 100vh;
}

.table-container {
    background: white;
    border-radius: 12px;
    border: 1px solid #f1f5f9;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    overflow: hidden;
}

.user-table {
    width: 100%;
    border-collapse: collapse;
}

.user-table th {
    background: #f8fafc;
    padding: 16px 20px;
    text-align: left;
    font-size: 0.85rem;
    color: #64748b;
    border-bottom: 1px solid #f1f5f9;
}

.user-table td {
    padding: 16px 20px;
    border-bottom: 1px solid #f1f5f9;
    vertical-align: middle;
    transition: 0.3s;
}

.col-deleted {
    font-size: 0.85rem;
    color: #94a3b8;
}

.delete-time {
    color: #ef4444;
    font-weight: 500;
}

/* Effect เมื่อแถวถูกลบ (Soft Deleted) */
.row-deleting td {
    background-color: #fffbeb;
    opacity: 0.8;
}

.row-deleting .username-text {
    color: #92400e;
    text-decoration: line-through;
}

.action-buttons {
    display: flex;
    gap: 8px;
}

.btn-manage {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: 0.2s;
    font-size: 0.85rem;
    color: white;
}

.btn-edit {
    background-color: #f59e0b;
}

.btn-delete {
    background-color: #ef4444;
}

.btn-undo-inline {
    background-color: #fbbf24;
    color: #1e293b;
    font-weight: 600;
    animation: pulse 1.5s infinite;
}

.btn-undo-inline:hover {
    background-color: #f59e0b;
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(251, 191, 36, 0.7);
    }

    70% {
        box-shadow: 0 0 0 10px rgba(251, 191, 36, 0);
    }

    100% {
        box-shadow: 0 0 0 0 rgba(251, 191, 36, 0);
    }
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 30px;
    border-left: 5px solid #3b82f6;
    padding-left: 20px;
}

.title-section h3 {
    font-size: 1.6rem;
    font-weight: 600;
    color: #1e293b;
    margin: 0;
}

.subtitle {
    color: #94a3b8;
    font-size: 0.95rem;
    margin-top: 5px;
}

.stat-item {
    background: white;
    padding: 10px 20px;
    border-radius: 12px;
    border: 1px solid #f1f5f9;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
}

.stat-value {
    color: #3b82f6;
    font-weight: 600;
    font-size: 1.2rem;
}

.filter-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #f1f5f9;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    margin-bottom: 25px;
}

.input-wrapper {
    position: relative;
    max-width: 400px;
}

.input-wrapper i {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: #94a3b8;
}

.input-wrapper input {
    width: 100%;
    padding: 10px 15px 10px 45px;
    border: 1.5px solid #e2e8f0;
    border-radius: 10px;
    outline: none;
    background: #f8fafc;
}

.user-info-display {
    display: flex;
    align-items: center;
    gap: 12px;
}

.avatar-circle {
    width: 35px;
    height: 35px;
    background: #eff6ff;
    color: #3b82f6;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
}

.role-badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.role-badge.admin {
    background: #fee2e2;
    color: #ef4444;
}

.role-badge.user {
    background: #f1f5f9;
    color: #475569;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.55);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    padding: 25px;
    border-radius: 12px;
    width: 420px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.delete-modal {
    border-top: 5px solid #ef4444;
}

.btn-danger-confirm {
    background-color: #ef4444;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
}

.btn-secondary {
    background: #f1f5f9;
    color: #64748b;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 5px;
}

.empty-state {
    padding: 60px;
    text-align: center;
    color: #94a3b8;
}

/* Form Styles */
.form-group {
    margin-bottom: 15px;
    text-align: left;
}

.form-group label {
    display: block;
    margin-bottom: 6px;
    font-size: 0.9rem;
    font-weight: 500;
    color: #475569;
}

.form-group input,
.form-select {
    width: 100%;
    padding: 10px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    outline: none;
}

.disabled-input {
    background: #f1f5f9;
    cursor: not-allowed;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 25px;
}

.btn-primary {
    background: #3b82f6;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
}

.close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
}
</style>