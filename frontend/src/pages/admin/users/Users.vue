<template>
    <div class="admin-page">

        <!-- Header -->
        <div class="page-header">
            <div>
                <h2>User Management</h2>
                <p class="subtitle">Manage accounts, roles, and access permissions.</p>
            </div>
            <div class="header-stats">
                <div class="stat-chip"><i class="fas fa-users"></i> {{ users.length }} Total</div>
                <div class="stat-chip active-chip"><i class="fas fa-circle dot-green"></i> {{ activeUsersCount }} Active</div>
            </div>
        </div>

        <!-- Filter Bar -->
        <div class="filter-bar">
            <div class="search-box">
                <i class="fas fa-search"></i>
                <input v-model="searchQuery" placeholder="Search by username or email..." />
            </div>
            <div class="role-tabs">
                <button v-for="f in roleFilters" :key="f.value"
                    :class="['tab-btn', { active: roleFilter === f.value }]"
                    @click="roleFilter = f.value">
                    {{ f.label }}
                    <span class="tab-count">{{ getRoleCount(f.value) }}</span>
                </button>
            </div>
        </div>

        <!-- Table -->
        <div class="table-card">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Avatar</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Post Permission</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in filteredUsers" :key="user.id"
                        :class="{ 'row-suspended': user.deleted_at }">
                        <td>
                            <div class="user-avatar">
                                <img v-if="user.profile_image" :src="getImageUrl(user.profile_image)" alt="avatar" />
                                <span v-else>{{ user.username.charAt(0).toUpperCase() }}</span>
                            </div>
                        </td>
                        <td class="username-cell">
                            <span class="username-text">{{ user.username }}</span>
                            <small class="user-id">#{{ user.id }}</small>
                        </td>
                        <td class="email-cell">{{ user.email }}</td>
                        <td>
                            <span :class="['chip', user.role === 'admin' ? 'chip-red' : 'chip-gray']">
                                <i :class="user.role === 'admin' ? 'fas fa-shield-alt' : 'fas fa-user'"></i>
                                {{ user.role === 'admin' ? 'Admin' : 'User' }}
                            </span>
                        </td>
                        <td>
                            <span v-if="user.post_permission_status === 'approved'" class="chip chip-green">
                                <i class="fas fa-check-circle"></i> Granted
                            </span>
                            <span v-else-if="user.post_permission_status === 'pending'" class="chip chip-yellow">
                                <i class="fas fa-hourglass-half"></i> Pending
                            </span>
                            <span v-else class="chip chip-gray">
                                <i class="fas fa-minus-circle"></i> None
                            </span>
                        </td>
                        <td>
                            <span v-if="!user.deleted_at" class="chip chip-green">
                                <i class="fas fa-circle dot-green"></i> Active
                            </span>
                            <span v-else class="chip chip-red">
                                <i class="fas fa-ban"></i> Suspended
                            </span>
                        </td>
                        <td>
                            <div class="action-group">
                                <router-link :to="`/admin/users/${user.id}`" class="action-btn btn-blue" title="View Profile">
                                    <i class="fas fa-eye"></i>
                                </router-link>

                                <template v-if="!user.deleted_at">
                                    <button @click="openEditModal(user)" class="action-btn btn-orange" title="Edit">
                                        <i class="fas fa-edit"></i> Edit
                                    </button>
                                    <button v-if="user.role !== 'admin'" @click="confirmDelete(user)" class="action-btn btn-red" title="Suspend">
                                        <i class="fas fa-ban"></i>
                                    </button>
                                </template>

                                <template v-else>
                                    <button v-if="isRestorable(user)" @click="restoreUser(user)" class="action-btn btn-teal" title="Restore">
                                        <i class="fas fa-undo"></i> Restore
                                    </button>
                                    <span v-else class="chip chip-red" style="font-size:0.78rem; white-space:nowrap;">
                                        <i class="fas fa-lock"></i> Permanent
                                    </span>
                                </template>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>

            <div v-if="filteredUsers.length === 0" class="empty-state">
                <i class="fas fa-user-slash"></i>
                <p>No users found.</p>
            </div>
        </div>

        <!-- Suspend Modal -->
        <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
            <div class="modal-box danger-modal">
                <div class="danger-icon"><i class="fas fa-exclamation-triangle"></i></div>
                <h4>Suspend Account?</h4>
                <p>Are you sure you want to suspend <strong>{{ userToDelete?.username }}</strong>?</p>
                <p class="sub-text">The account can be restored within 3 days.</p>
                <div class="modal-actions">
                    <button @click="showDeleteModal = false" class="btn-ghost">Cancel</button>
                    <button @click="executeSoftDelete" class="btn-danger-confirm">Confirm Suspend</button>
                </div>
            </div>
        </div>

        <!-- Edit Modal -->
        <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal = false">
            <div class="modal-box">
                <div class="modal-head">
                    <h4><i class="fas fa-user-edit"></i> Edit User Info</h4>
                    <button @click="showEditModal = false" class="close-x">&times;</button>
                </div>
                <div class="modal-form">
                    <label>Username</label>
                    <input type="text" v-model="editingUser.username" class="form-input" />
                    <label>Email</label>
                    <input type="email" v-model="editingUser.email" class="form-input" />
                </div>
                <div class="modal-actions">
                    <button @click="showEditModal = false" class="btn-ghost">Cancel</button>
                    <button @click="updateUserData" class="btn-save">Save Changes</button>
                </div>
            </div>
        </div>

    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { userRepository } from '@/repositories/userRepository'

const users = ref([])
const searchQuery = ref('')
const roleFilter = ref('all')
const showEditModal = ref(false)
const editingUser = ref({ id: null, username: '', email: '' })
const showDeleteModal = ref(false)
const userToDelete = ref(null)

const fetchUsers = async () => {
    try {
        const res = await userRepository.getAll()
        users.value = res.data
    } catch (error) {
        console.error("Fetch Error:", error)
    }
}

const activeUsersCount = computed(() => users.value.filter(u => !u.deleted_at).length)

const filteredUsers = computed(() => {
    return users.value.filter(u => {
        const matchSearch =
            u.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            u.email.toLowerCase().includes(searchQuery.value.toLowerCase())
        const matchRole = roleFilter.value === 'all' || u.role === roleFilter.value
        return matchSearch && matchRole
    })
})

const roleFilters = [
    { value: 'all', label: 'All Users' },
    { value: 'user', label: 'User' },
    { value: 'admin', label: 'Admin' },
]

const getRoleCount = (role) => {
    if (role === 'all') return users.value.length
    return users.value.filter(u => u.role === role).length
}

const openEditModal = (user) => {
    editingUser.value = { id: user.id, username: user.username, email: user.email }
    showEditModal.value = true
}

const updateUserData = async () => {
    try {
        const formData = new FormData()
        formData.append('username', editingUser.value.username)
        formData.append('email', editingUser.value.email)
        await userRepository.updateProfile(editingUser.value.id, formData)
        showEditModal.value = false
        await fetchUsers()
    } catch (error) {
        alert(error.response?.data?.detail || 'Failed to update user.')
    }
}

const confirmDelete = (user) => {
    userToDelete.value = user
    showDeleteModal.value = true
}

const executeSoftDelete = async () => {
    if (!userToDelete.value) return
    try {
        await userRepository.softDelete(userToDelete.value.id)
        showDeleteModal.value = false
        userToDelete.value = null
        await fetchUsers()
    } catch (error) {
        alert('Failed to suspend user.')
    }
}

const restoreUser = async (user) => {
    try {
        await userRepository.restore(user.id)
        await fetchUsers()
    } catch (error) {
        alert(error.response?.data?.detail || 'Restore failed.')
    }
}

const isRestorable = (user) => {
    if (!user.deleted_at) return false
    const diff = (new Date() - new Date(user.deleted_at)) / (1000 * 60 * 60 * 24)
    return diff <= 3
}

const getImageUrl = (path) => {
    if (!path) return ''
    if (path.startsWith('http')) return path
    return `http://localhost:8000${path.startsWith('/') ? path : '/' + path}`
}

onMounted(fetchUsers)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.admin-page {
    font-family: 'Inter', sans-serif;
    padding: 32px 40px;
    background: #f8fafc;
    min-height: 100vh;
}

/* ─── Header ─────────────────────────────── */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
}

.page-header h2 {
    font-size: 1.55rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
}

.subtitle {
    color: #64748b;
    font-size: 0.92rem;
    margin: 4px 0 0;
}

.header-stats {
    display: flex;
    gap: 10px;
}

.stat-chip {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    font-size: 0.88rem;
    font-weight: 600;
    color: #475569;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.active-chip {
    background: #f0fdf4;
    border-color: #bbf7d0;
    color: #16a34a;
}

.dot-green { color: #22c55e; font-size: 0.6rem; }

/* ─── Filter Bar ──────────────────────────── */
.filter-bar {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.search-box {
    display: flex;
    align-items: center;
    gap: 10px;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 0 16px;
    height: 42px;
    flex: 1;
    max-width: 400px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.search-box i { color: #94a3b8; }

.search-box input {
    border: none;
    outline: none;
    font-size: 0.9rem;
    color: #334155;
    background: transparent;
    width: 100%;
    font-family: inherit;
}

.role-tabs {
    display: flex;
    gap: 6px;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 5px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.tab-btn {
    padding: 6px 14px;
    border: none;
    border-radius: 7px;
    background: transparent;
    color: #64748b;
    font-size: 0.88rem;
    font-weight: 500;
    cursor: pointer;
    transition: 0.15s;
    font-family: inherit;
    display: flex;
    align-items: center;
    gap: 6px;
}

.tab-btn:hover { background: #f1f5f9; color: #334155; }

.tab-btn.active {
    background: #3b82f6;
    color: white;
}

.tab-count {
    background: rgba(255,255,255,0.25);
    border-radius: 10px;
    padding: 1px 7px;
    font-size: 0.78rem;
    font-weight: 700;
}

.tab-btn:not(.active) .tab-count {
    background: #f1f5f9;
    color: #64748b;
}

/* ─── Table ───────────────────────────────── */
.table-card {
    background: white;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    overflow: hidden;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table thead tr {
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
}

.data-table th {
    padding: 14px 20px;
    text-align: left;
    font-size: 0.8rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.data-table td {
    padding: 14px 20px;
    border-bottom: 1px solid #f1f5f9;
    vertical-align: middle;
    font-size: 0.93rem;
    color: #334155;
}

.data-table tbody tr:last-child td { border-bottom: none; }
.data-table tbody tr:hover td { background: #fafbfc; }

.row-suspended td { background: #fffbeb !important; }
.row-suspended .username-text { text-decoration: line-through; color: #92400e; }

/* ─── Avatar ──────────────────────────────── */
.user-avatar {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    overflow: hidden;
    background: #eff6ff;
    color: #3b82f6;
    font-weight: 700;
    font-size: 1.05rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid #e0eaff;
}

.user-avatar img { width: 100%; height: 100%; object-fit: cover; }

/* ─── Cells ───────────────────────────────── */
.username-cell {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.username-text { font-weight: 600; color: #0f172a; }
.user-id { font-size: 0.78rem; color: #94a3b8; }
.email-cell { color: #475569; font-size: 0.9rem; }

/* ─── Chips ───────────────────────────────── */
.chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 11px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    white-space: nowrap;
}

.chip-green  { background: #dcfce7; color: #15803d; }
.chip-red    { background: #fee2e2; color: #dc2626; }
.chip-yellow { background: #fef9c3; color: #ca8a04; }
.chip-gray   { background: #f1f5f9; color: #475569; }

/* ─── Actions ─────────────────────────────── */
.action-group {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
}

.action-btn {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 6px 13px;
    border: none;
    border-radius: 7px;
    font-size: 0.83rem;
    font-weight: 600;
    cursor: pointer;
    transition: 0.15s;
    color: white;
    font-family: inherit;
    text-decoration: none;
}

.action-btn:hover { opacity: 0.85; transform: translateY(-1px); }

.btn-blue  { background: #3b82f6; }
.btn-orange { background: #f59e0b; }
.btn-red   { background: #ef4444; }
.btn-teal  { background: #14b8a6; }

/* ─── Empty state ─────────────────────────── */
.empty-state {
    text-align: center;
    padding: 60px;
    color: #94a3b8;
}
.empty-state i { font-size: 2.5rem; margin-bottom: 12px; display: block; }

/* ─── Modals ──────────────────────────────── */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(15,23,42,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    backdrop-filter: blur(3px);
}

.modal-box {
    background: white;
    border-radius: 16px;
    width: 420px;
    padding: 28px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}

.danger-modal { text-align: center; }

.danger-icon {
    width: 64px; height: 64px;
    background: #fee2e2; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 16px;
    font-size: 1.8rem; color: #dc2626;
}

.danger-modal h4 { font-size: 1.2rem; color: #0f172a; margin: 0 0 10px; }
.danger-modal p { color: #64748b; margin: 4px 0; }
.sub-text { font-size: 0.85rem !important; color: #94a3b8 !important; }

.modal-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}
.modal-head h4 { font-size: 1.1rem; margin: 0; color: #0f172a; display: flex; align-items: center; gap: 8px; }

.close-x { background: none; border: none; font-size: 1.4rem; cursor: pointer; color: #94a3b8; }

.modal-form {
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin-bottom: 20px;
}

.modal-form label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #475569;
    margin-top: 10px;
}

.form-input {
    padding: 10px 14px;
    border: 1px solid #cbd5e1;
    border-radius: 9px;
    font-size: 0.95rem;
    font-family: inherit;
    outline: none;
    transition: 0.15s;
}

.form-input:focus { border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59,130,246,0.1); }

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
}

.btn-ghost {
    background: #f1f5f9; color: #475569; border: none;
    padding: 10px 20px; border-radius: 9px; cursor: pointer;
    font-size: 0.9rem; font-weight: 500; font-family: inherit;
}

.btn-save {
    background: #3b82f6; color: white; border: none;
    padding: 10px 22px; border-radius: 9px; cursor: pointer;
    font-size: 0.9rem; font-weight: 600; font-family: inherit;
}

.btn-danger-confirm {
    background: #ef4444; color: white; border: none;
    padding: 10px 22px; border-radius: 9px; cursor: pointer;
    font-size: 0.9rem; font-weight: 600; font-family: inherit;
}

@media (max-width: 768px) {
    .admin-page { padding: 20px; }
    .page-header { flex-direction: column; align-items: flex-start; gap: 12px; }
    .filter-bar { flex-direction: column; align-items: stretch; }
    .search-box { max-width: 100%; }
    .data-table { font-size: 0.85rem; }
}
</style>
