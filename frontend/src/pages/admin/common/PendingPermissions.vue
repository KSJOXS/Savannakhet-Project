<template>
    <div class="pending-permissions-container">
        <div class="header-section">
            <div class="title-group">
                <h1>User Post Permissions</h1>
                <p class="subtitle">Review requests from users who want to add places to the directory.</p>
            </div>
        </div>

        <div class="content-section">
            <div v-if="loading" class="loading-state">
                <i class="fas fa-spinner fa-spin"></i> Loading permission requests...
            </div>
            
            <div v-else-if="pendingUsers.length === 0" class="empty-state">
                <div class="empty-icon"><i class="fas fa-check-circle"></i></div>
                <h3>All caught up!</h3>
                <p>There are no pending user requests right now.</p>
            </div>

            <div v-else class="table-container">
                <table class="ta-table">
                    <thead>
                        <tr>
                            <th>User ID</th>
                            <th>Username</th>
                            <th>Email</th>
                            <th class="actions-col">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="user in pendingUsers" :key="user.id">
                            <td>
                                <strong>#{{ user.id }}</strong>
                            </td>
                            <td>
                                <div class="user-info">
                                    <div class="avatar">
                                        <img v-if="user.profile_image" :src="getImageUrl(user.profile_image)" alt="avatar">
                                        <div v-else class="avatar-placeholder">{{ user.username.charAt(0).toUpperCase() }}</div>
                                    </div>
                                    <span>{{ user.username }}</span>
                                </div>
                            </td>
                            <td>{{ user.email }}</td>
                            <td class="actions-col">
                                <button class="btn-approve" @click="updateStatus(user.id, 'approved')" :disabled="processingId === user.id">
                                    <i class="fas fa-check"></i> Grant Access
                                </button>
                                <button class="btn-reject" @click="updateStatus(user.id, 'rejected')" :disabled="processingId === user.id">
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
import { userRepository } from '@/repositories/userRepository'

const pendingUsers = ref([])
const loading = ref(true)
const processingId = ref(null)

const loadPendingPermissions = async () => {
    loading.value = true
    try {
        const res = await userRepository.getPendingPermissions()
        pendingUsers.value = res.data
    } catch (error) {
        console.error("Failed to load pending permissions:", error)
        alert("Could not load pending requests.")
    } finally {
        loading.value = false
    }
}

const updateStatus = async (id, status) => {
    if (!confirm(`Are you sure you want to ${status === 'approved' ? 'grant access to' : 'reject'} this user?`)) return
    
    processingId.value = id
    try {
        await userRepository.updatePostPermission(id, status)
        // Remove from list
        pendingUsers.value = pendingUsers.value.filter(u => u.id !== id)
        alert(`User permission successfully updated to ${status}.`)
    } catch (error) {
        console.error(`Failed to update permission:`, error)
        alert(`Could not update status.`)
    } finally {
        processingId.value = null
    }
}

const getImageUrl = (path) => {
    if (!path) return '';
    if (path.startsWith('http')) return path;
    return `http://localhost:8000${path}`;
}

onMounted(() => {
    loadPendingPermissions()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap');

.pending-permissions-container {
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

.user-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    overflow: hidden;
    background: #e2e8f0;
}

.avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #475569;
    font-weight: 600;
}

.actions-col {
    text-align: right;
    min-width: 200px;
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
