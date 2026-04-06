<template>
    <nav class="navbar">
        <div class="nav-container">
            <div class="brand" @click="router.push('/')" style="cursor: pointer;">
                🌴 <span class="brand-text">Savannakhet Smart Travel</span>
            </div>

            <div class="nav-menu">
                <router-link v-if="!isLoggedIn" to="/" class="nav-item">Home</router-link>

                <router-link to="/explore" class="nav-btn-explore">
                    <i class="fas fa-search"></i> Explore
                </router-link>

                <router-link v-if="isLoggedIn && (!user || user.role !== 'admin')" to="/favorites" class="nav-item nav-fav">
                    <i class="fas fa-heart"></i> Favorites
                </router-link>

                <div v-if="!isLoggedIn" class="auth-group">
                    <router-link to="/login" class="link-login">Sign In</router-link>
                    <router-link to="/register" class="btn-register-pill">Sign Up</router-link>
                </div>

                <div v-else class="user-control">
                    <div class="user-info">
                        <span class="user-label">Hello,</span>
                        <span class="user-name">{{ username }}</span>
                    </div>
                    <router-link to="/profile" class="btn-setting">
                        <i class="fas fa-cog"></i> Settings
                    </router-link>
                    <button @click="handleLogout" class="btn-logout-minimal">
                        Sign Out
                    </button>
                </div>
            </div>
        </div>
    </nav>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { user, isAuthenticated, logout } = useAuth()
const isLoggedIn = ref(isAuthenticated())
const username = ref(user.value ? user.value.username : '')

const checkAuth = () => {
    isLoggedIn.value = isAuthenticated()
    username.value = user.value ? user.value.username : 'User'
}

onMounted(checkAuth)
watch(() => router.currentRoute.value.path, checkAuth)

const handleLogout = () => {
    logout()
    checkAuth()
    router.push('/login')
}
</script>

<style scoped>
/* 📌 ปรับปรุงพื้นฐาน Navbar ให้ดูพรีเมียม */
.navbar {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    /* เอฟเฟกต์กระจกฝ้า */
    padding: 12px 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 25px;
}

.brand {
    font-size: 1.25rem;
    font-weight: 800;
    color: #2c3e50;
    display: flex;
    align-items: center;
    gap: 8px;
}

.nav-menu {
    display: flex;
    gap: 25px;
    align-items: center;
}

/* 📌 สไตล์เมนูทั่วไป */
.nav-item {
    text-decoration: none;
    color: #64748b;
    font-weight: 600;
    font-size: 0.95rem;
    transition: 0.2s;
}

.nav-item:hover {
    color: #3498db;
}

.nav-fav {
    color: #ef4444 !important;
}

/* 🌟 ปุ่มไฮไลท์ "ค้นหา" ตามแบบมืออาชีพ */
.nav-btn-explore {
    background: #ebf5ff;
    color: #3498db;
    padding: 10px 22px;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 700;
    font-size: 0.9rem;
    transition: 0.3s;
    display: flex;
    align-items: center;
    gap: 8px;
}

.nav-btn-explore:hover {
    background: #3498db;
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(52, 152, 219, 0.2);
}

/* 📌 Auth Buttons */
.auth-group {
    display: flex;
    align-items: center;
    gap: 15px;
    border-left: 1px solid #e2e8f0;
    padding-left: 20px;
}

.link-login {
    text-decoration: none;
    color: #3498db;
    font-weight: 700;
    font-size: 0.95rem;
}

.btn-register-pill {
    background: #3498db;
    color: white;
    padding: 10px 24px;
    border-radius: 50px;
    /* ทรงมนตามรูป */
    text-decoration: none;
    font-weight: 700;
    box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
    transition: 0.3s;
}

.btn-register-pill:hover {
    background: #2980b9;
    transform: scale(1.05);
}

/* 📌 User Profile After Login */
.user-control {
    display: flex;
    align-items: center;
    gap: 15px;
    background: #f8fafc;
    padding: 6px 6px 6px 18px;
    border-radius: 50px;
}

.user-info {
    display: flex;
    flex-direction: column;
}

.user-label {
    font-size: 0.7rem;
    color: #94a3b8;
    text-transform: uppercase;
}

.user-name {
    font-weight: 700;
    color: #1e293b;
    font-size: 0.9rem;
}

.btn-setting {
    background: #f1f5f9;
    color: #475569;
    border: none;
    padding: 8px 15px;
    border-radius: 50px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.8rem;
    transition: 0.2s;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 5px;
}

.btn-setting:hover {
    background: #e2e8f0;
    color: #1e293b;
}

.btn-logout-minimal {
    background: white;
    color: #ef4444;
    border: 1px solid #fee2e2;
    padding: 8px 15px;
    border-radius: 50px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.8rem;
    transition: 0.2s;
}

.btn-logout-minimal:hover {
    background: #ef4444;
    color: white;
}
</style>