<template>
    <div class="admin-wrapper">
        <aside class="admin-sidebar">
            <div class="sidebar-logo">
                <i class="fas fa-tools"></i>
                <span>SMART TRAVEL ADMIN</span>
            </div>

            <nav class="sidebar-nav">
                <router-link to="/admin/places" class="nav-link" active-class="active">
                    <i class="fas fa-map-marker-alt"></i> Places
                </router-link>

                <router-link to="/admin/pending-places" class="nav-link" active-class="active">
                    <i class="fas fa-clipboard-check"></i> Pending Approvals
                </router-link>

                <router-link to="/admin/categories" class="nav-link" active-class="active">
                    <i class="fas fa-tags"></i> Categories
                </router-link>

                <router-link to="/admin/comments" class="nav-link" active-class="active">
                    <i class="fas fa-comments"></i> Reviews
                </router-link>

                <router-link to="/admin/messages" class="nav-link" active-class="active">
                    <i class="fas fa-inbox"></i> Inbox
                    <span v-if="unreadMessages > 0" class="badge-count">{{ unreadMessages }}</span>
                </router-link>

                <router-link to="/admin/manage-users" class="nav-link" active-class="active">
                    <i class="fas fa-users"></i> Users
                </router-link>

                <router-link to="/admin/pending-permissions" class="nav-link" active-class="active">
                    <i class="fas fa-user-shield"></i> User Permissions
                </router-link>

                <router-link to="/admin/settings" class="nav-link" active-class="active">
                    <i class="fas fa-cog"></i> Web Settings
                </router-link>

                <router-link to="/admin/dashboard" class="nav-link" active-class="active">
                    <i class="fas fa-chart-line"></i> Dashboard
                </router-link>

                <div class="nav-divider"></div>

                <a href="/" target="_blank" class="nav-link back-home">
                    <i class="fas fa-external-link-alt"></i> Back to Site
                </a>

                <button @click="logout" class="nav-link btn-logout-action">
                    <i class="fas fa-sign-out-alt"></i> Sign Out
                </button>
            </nav>
        </aside>

        <main class="admin-content">
            <header class="admin-top-bar">
                <div class="user-info-admin">
                    <span>Administrator: <strong>Admin</strong></span>
                </div>
            </header>

            <div class="content-view">
                <router-view></router-view>
            </div>
        </main>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const router = useRouter()
const unreadMessages = ref(0)

const fetchUnreadCount = async () => {
    try {
        const res = await api.get('/api/admin/messages/unread-count')
        unreadMessages.value = res.data.unread_count
    } catch (error) {
        console.error('Failed to fetch unread count:', error)
    }
}

const logout = () => {
    if (confirm('Confirm sign out?')) {
        // ล้างข้อมูลการล็อกอิน
        localStorage.removeItem('access_token')
        localStorage.removeItem('user')

        // ส่งกลับไปหน้า Login
        router.push('/login')
    }
}

onMounted(fetchUnreadCount)
</script>

<style scoped>
/* เพิ่มสไตล์เฉพาะให้ปุ่มให้ทำงานเหมือน router-link */
.btn-logout-action {
    background: transparent;
    border: none;
    width: 100%;
    cursor: pointer;
    font-family: inherit;
    font-size: inherit;
    text-align: left;
}

.admin-wrapper {
    display: flex;
    min-height: 100vh;
    background: #f8fafc;
}

/* Sidebar Style */
.admin-sidebar {
    width: 280px;
    background: #1e293b;
    color: white;
    display: flex;
    flex-direction: column;
}

.sidebar-logo {
    padding: 30px;
    font-size: 1.2rem;
    font-weight: 800;
    border-bottom: 1px solid #334155;
    display: flex;
    gap: 10px;
    align-items: center;
}

.sidebar-nav {
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.nav-link {
    color: #94a3b8;
    text-decoration: none;
    padding: 12px 20px;
    border-radius: 12px;
    transition: 0.3s;
    display: flex;
    align-items: center;
    gap: 12px;
}

.nav-link:hover {
    background: rgba(255, 255, 255, 0.05);
    color: white;
}

.nav-link.active {
    background: #3498db;
    color: white;
    box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
}

.badge-count {
    background: #e74c3c;
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 10px;
    margin-left: auto;
}

.nav-divider {
    height: 1px;
    background: #334155;
    margin: 20px 0;
}

.back-home {
    color: #60a5fa;
}

/* Main Area Style */
.admin-content {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.admin-top-bar {
    height: 70px;
    background: white;
    border-bottom: 1px solid #e2e8f0;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 0 40px;
}

.content-view {
    padding: 40px;
}
</style>
