<template>
    <header class="ta-header">
        <div class="ta-top-row">
            <div class="nav-container">

                <div class="nav-left">
                    <div class="brand" @click="router.push('/')">
                        <div class="brand-logo">
                            <i class="fas fa-map-marked-alt"></i>
                        </div>
                        <span class="brand-text">Savannakhet</span>
                    </div>

                    <div class="nav-search" v-if="route.path !== '/explore'">
                        <div class="ta-search-pill" @click="router.push('/explore')">
                            <i class="fas fa-search"></i>
                            <input type="text" placeholder="Search..." readonly />
                        </div>
                    </div>
                </div>

                <div class="nav-right">
                    <router-link to="/explore" class="nav-item">
                        <span>{{ t('nav.discover') }}</span>
                    </router-link>

                    <div 
                        class="nav-item-dropdown"
                        @mouseenter="isReviewOpen = true"
                        @mouseleave="isReviewOpen = false"
                    >
                        <div class="nav-item" :class="{ active: route.path.includes('/review') || route.path.includes('/submit') }">
                            <span>{{ t('nav.review') }}</span>
                            <i class="fas fa-chevron-down dropdown-icon" :class="{ rotated: isReviewOpen }"></i>
                        </div>

                        <transition name="fade-slide">
                            <div v-if="isReviewOpen" class="about-dropdown-menu">
                                <router-link to="/profile?tab=reviews" class="about-dropdown-item" @click="isReviewOpen = false">
                                    <i class="fas fa-pen-nib"></i> {{ t('nav.writeReview') }}
                                </router-link>
                                <router-link to="/submit-place" class="about-dropdown-item" @click="isReviewOpen = false">
                                    <i class="fas fa-camera"></i> {{ t('nav.postPhoto') }}
                                </router-link>
                                <router-link to="/submit-place" class="about-dropdown-item" @click="isReviewOpen = false">
                                    <i class="fas fa-plus-circle"></i> {{ t('nav.addPlace') }}
                                </router-link>
                            </div>
                        </transition>
                    </div>

                    <div 
                        class="nav-item-dropdown"
                        @mouseenter="isAboutOpen = true"
                        @mouseleave="isAboutOpen = false"
                    >
                        <div class="nav-item" :class="{ active: route.path === '/about' || route.path === '/contact' }">
                            <i class="fas fa-info-circle"></i> <span>{{ t('nav.about') }}</span>
                            <i class="fas fa-chevron-down dropdown-icon" :class="{ rotated: isAboutOpen }"></i>
                        </div>

                        <transition name="fade-slide">
                            <div v-if="isAboutOpen" class="about-dropdown-menu">
                                <router-link to="/about" class="about-dropdown-item" @click="isAboutOpen = false">
                                    <i class="fas fa-building"></i> {{ t('nav.about') }}
                                </router-link>
                                <router-link to="/contact" class="about-dropdown-item" @click="isAboutOpen = false">
                                    <i class="fas fa-headset"></i> {{ t('nav.contact') || 'Contact' }}
                                </router-link>
                            </div>
                        </transition>
                    </div>

                    <router-link v-if="isLoggedIn && (!user || user.role !== 'admin')" to="/favorites" class="nav-item">
                        <i class="far fa-heart"></i> <span>{{ t('nav.saves') }}</span>
                    </router-link>

                    <div class="lang-switcher">
                        <button class="lang-btn" @click="isLangOpen = !isLangOpen">
                            <i class="fas fa-globe"></i>
                            <div class="lang-divider"></div>
                            <span>{{ currentFlagLabel }}</span>
                            <i class="fas fa-chevron-down" :class="{ rotated: isLangOpen }"></i>
                        </button>
                        <div v-if="isLangOpen" class="lang-overlay" @click="isLangOpen = false"></div>
                        <transition name="fade-slide">
                            <div v-if="isLangOpen" class="lang-dropdown">
                                <div
                                    v-for="loc in supportedLocales"
                                    :key="loc.code"
                                    class="lang-item"
                                    :class="{ active: locale === loc.code }"
                                    @click="switchLang(loc.code)"
                                >
                                    <span class="lang-flag">{{ loc.flag }}</span>
                                    <span>{{ loc.label }}</span>
                                    <i v-if="locale === loc.code" class="fas fa-check lang-check"></i>
                                </div>
                            </div>
                        </transition>
                    </div>

                    <div v-if="!isLoggedIn" class="auth-group">
                        <router-link to="/login" class="btn-ta-solid">{{ t('nav.signIn') }}</router-link>
                    </div>

                    <div v-else class="user-group">
                        <div class="user-avatar" :title="username" @click="isDropdownOpen = !isDropdownOpen" style="padding: 0; overflow: hidden; border: none; background: none;">
                            <img v-if="user && user.profile_image" :src="getImageUrl(user.profile_image)" alt="avatar" style="width:100%; height:100%; object-fit:cover; border-radius:50%; border:2px solid #3498db;" />
                            <div v-else style="width:100%; height:100%; display:flex; align-items:center; justify-content:center; background:#000; color:white; border-radius:50%;">
                                {{ username ? username.charAt(0).toUpperCase() : 'U' }}
                            </div>
                        </div>

                        <div v-if="isDropdownOpen" class="dropdown-overlay" @click="isDropdownOpen = false"></div>

                        <transition name="fade-slide">
                            <div v-if="isDropdownOpen" class="profile-dropdown">
                                <div class="dropdown-arrow"></div>

                                <router-link to="/favorites" class="dropdown-item" @click="isDropdownOpen = false">
                                    <i class="fas fa-suitcase-rolling"></i> {{ t('nav.myTrips') }}
                                </router-link>
                                <router-link to="/profile" class="dropdown-item" @click="isDropdownOpen = false">
                                    <i class="far fa-user-circle"></i> {{ t('nav.profile') }}
                                </router-link>
                                <router-link to="/profile?tab=reviews" class="dropdown-item" @click="isDropdownOpen = false">
                                    <i class="fas fa-history"></i> {{ t('nav.socialHistory') || 'Social History' }}
                                </router-link>
                                <router-link to="/profile?tab=bookings" class="dropdown-item" @click="isDropdownOpen = false">
                                    <i class="far fa-calendar-alt"></i> {{ t('nav.bookings') }}
                                </router-link>
                                <router-link to="/profile?tab=messages" class="dropdown-item" @click="isDropdownOpen = false">
                                    <i class="far fa-envelope"></i> {{ t('nav.messages') }}
                                </router-link>
                                <router-link to="/profile?tab=settings" class="dropdown-item" @click="isDropdownOpen = false">
                                    <i class="fas fa-user-cog"></i> {{ t('nav.accountInfo') }}
                                </router-link>

                                <div class="dropdown-divider"></div>

                                <div class="dropdown-item logout" @click="handleLogoutAndClose">
                                    <i class="fas fa-sign-out-alt"></i> {{ t('nav.signOut') }}
                                </div>
                            </div>
                        </transition>
                    </div>
                </div>

            </div>
        </div>

        <div class="ta-bottom-row">
            <div class="nav-container">
                <div class="sub-nav-list">

                    <router-link 
                        v-if="!isLoggedIn" 
                        to="/" 
                        class="sub-nav-item"
                        :class="{ active: route.path === '/' }">
                        {{ t('nav.home') }}
                    </router-link>

                    <router-link to="/hotels" class="sub-nav-item" :class="{ active: route.path.includes('/hotels') }">
                        {{ t('nav.hotels') }}
                    </router-link>

                    <router-link to="/explore?tab=things-to-do" class="sub-nav-item"
                        :class="{ active: route.path === '/explore' && (!route.query.tab || route.query.tab === 'things-to-do') }">
                        {{ t('nav.thingsToDo') }}
                    </router-link>

                    <router-link to="/restaurants" class="sub-nav-item"
                        :class="{ active: route.path.includes('/restaurants') }">
                        {{ t('nav.restaurants') }}
                    </router-link>

                    <router-link to="/nature" class="sub-nav-item" :class="{ active: route.path.includes('/nature') }">
                        {{ t('nav.nature') }}
                    </router-link>

                    <router-link to="/landmarks" class="sub-nav-item" :class="{ active: route.path.includes('/landmarks') }">
                        {{ t('nav.landmarks') }}
                    </router-link>
                    
                    <router-link to="/community" class="sub-nav-item" :class="{ active: route.path.includes('/community') }">
                        <i class="fas fa-users"></i> {{ t('nav.community') || 'Community' }}
                    </router-link>
                </div>
            </div>
        </div>
    </header>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { useI18n } from '@/composables/useI18n'

const router = useRouter()
const route = useRoute()
const { user, isAuthenticated, logout } = useAuth()
const { t, setLocale, locale, supportedLocales } = useI18n()

const isLoggedIn = ref(isAuthenticated())
const username = ref(user.value ? user.value.username : '')
const isDropdownOpen = ref(false)
const isLangOpen = ref(false)
const isAboutOpen = ref(false)
const isReviewOpen = ref(false)

const currentFlagLabel = computed(() => {
    const found = supportedLocales.find(l => l.code === locale.value)
    return found ? found.label : 'English'
})

const switchLang = (code) => {
    isLangOpen.value = false
    setLocale(code)
}

const getImageUrl = (url) => {
    if (!url) return '';
    if (url.startsWith('http') || url.startsWith('data:')) return url;
    return `http://localhost:8000/${url.startsWith('/') ? url.slice(1) : url}`;
}

const checkAuth = () => {
    isLoggedIn.value = isAuthenticated()
    username.value = user.value ? user.value.username : 'User'
}

onMounted(checkAuth)

watch(() => router.currentRoute.value.path, () => {
    checkAuth()
    isDropdownOpen.value = false
    isLangOpen.value = false
    isAboutOpen.value = false
    isReviewOpen.value = false
})

const handleLogoutAndClose = () => {
    isDropdownOpen.value = false
    logout()
    checkAuth()
    router.push('/login')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap');

/* โครงสร้างหลักของ Header */
.ta-header {
    background: #ffffff;
    position: sticky;
    top: 0;
    z-index: 1000;
    font-family: 'Inter', sans-serif;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* แถวบนสุด (Top Row) */
.ta-top-row {
    height: 76px;
    display: flex;
    align-items: center;
}

.nav-container {
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-left {
    display: flex;
    align-items: center;
    gap: 30px;
}

/* Brand Logo */
.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
}

.brand-logo {
    width: 38px;
    height: 38px;
    background: #00aa6c;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
}

.brand-text {
    font-size: 1.6rem;
    font-weight: 900;
    color: #000000;
    letter-spacing: -0.5px;
}

/* Search Box ด้านบน */
.nav-search {
    width: 350px;
}

.ta-search-pill {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 40px;
    padding: 10px 20px;
    width: 100%;
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
    transition: 0.2s ease-in-out;
}

.ta-search-pill:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.ta-search-pill i {
    color: #0f172a;
    font-size: 1.1rem;
}

.ta-search-pill input {
    border: none;
    background: transparent;
    font-family: inherit;
    font-size: 0.95rem;
    color: #475569;
    font-weight: 500;
    outline: none;
    cursor: pointer;
    width: 100%;
}

/* Right Menu */
.nav-right {
    display: flex;
    align-items: center;
    gap: 8px;
}

.nav-item {
    text-decoration: none;
    color: #000000;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 10px 16px;
    border-radius: 24px;
    transition: background 0.2s;
    display: flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;
}

.nav-item:hover {
    background: #f1f5f9;
}

.nav-item.active {
    background: #e2e8f0;
}

/* 🚨 About Dropdown Menu CSS 🚨 */
.nav-item-dropdown {
    position: relative;
    padding: 10px 0;
}

.dropdown-icon {
    font-size: 0.7rem;
    transition: transform 0.2s;
    margin-left: 2px;
}

.dropdown-icon.rotated {
    transform: rotate(180deg);
}

.about-dropdown-menu {
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    border: 1px solid #f1f5f9;
    min-width: 180px;
    overflow: hidden;
    z-index: 1002;
    padding: 8px 0;
}

.about-dropdown-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 20px;
    color: #0f172a;
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    transition: background 0.2s;
}

.about-dropdown-item i {
    color: #64748b;
    width: 16px;
    text-align: center;
}

.about-dropdown-item:hover {
    background: #f8fafc;
    color: #00aa6c;
}

.about-dropdown-item:hover i {
    color: #00aa6c;
}


/* Auth & User Buttons */
.auth-group {
    margin-left: 10px;
}

.btn-ta-solid {
    background: #000000;
    color: #ffffff;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 10px 24px;
    border-radius: 24px;
    transition: 0.2s;
    display: inline-block;
}

.btn-ta-solid:hover {
    background: #334155;
}

.user-group {
    position: relative;
    display: flex;
    align-items: center;
    margin-left: 10px;
}

.user-avatar {
    width: 42px;
    height: 42px;
    background: #000000;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1.2rem;
    cursor: pointer;
    transition: box-shadow 0.2s;
    position: relative;
    z-index: 1002;
}

.user-avatar:hover {
    box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.1);
}

/* Dropdown Profile */
.dropdown-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1001;
    cursor: default;
}

.profile-dropdown {
    position: absolute;
    top: calc(100% + 15px);
    right: 0;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    width: 220px;
    padding: 10px 0;
    z-index: 1002;
    border: 1px solid #f1f5f9;
}

.dropdown-arrow {
    position: absolute;
    top: -6px;
    right: 18px;
    width: 14px;
    height: 14px;
    background: #ffffff;
    transform: rotate(45deg);
    border-left: 1px solid #f1f5f9;
    border-top: 1px solid #f1f5f9;
}

.dropdown-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 20px;
    color: #0f172a;
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s;
}

.dropdown-item i {
    width: 20px;
    text-align: center;
    color: #64748b;
    font-size: 1.1rem;
}

.dropdown-item:hover {
    background: #f8fafc;
}

.dropdown-item:hover i {
    color: #00aa6c;
}

.dropdown-divider {
    height: 1px;
    background: #e2e8f0;
    margin: 8px 0;
}

.dropdown-item.logout {
    color: #ef4444;
}

.dropdown-item.logout i {
    color: #ef4444;
}

/* Language Switcher */
.lang-switcher {
    position: relative;
}

.lang-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    background: transparent;
    border: none;
    padding: 8px 12px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    color: #0f172a;
    transition: 0.2s;
    font-family: inherit;
}

.lang-divider {
    width: 1px;
    height: 16px;
    background: #cbd5e1;
    margin: 0 4px;
}

.lang-btn:hover {
    background: #f1f5f9;
    border-radius: 24px;
}

.lang-btn .fa-chevron-down {
    font-size: 0.7rem;
    transition: transform 0.2s;
}

.lang-btn .fa-chevron-down.rotated {
    transform: rotate(180deg);
}

.lang-overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    z-index: 1001;
}

.lang-dropdown {
    position: absolute;
    top: calc(100% + 10px);
    right: 0;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    border: 1px solid #f1f5f9;
    min-width: 160px;
    overflow: hidden;
    z-index: 1002;
}

.lang-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 11px 16px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    color: #0f172a;
    transition: background 0.15s;
}

.lang-item:hover {
    background: #f8fafc;
}

.lang-item.active {
    background: #f0fdf4;
    color: #00aa6c;
    font-weight: 700;
}

.lang-flag {
    font-size: 1.1rem;
}

.lang-check {
    margin-left: auto;
    color: #00aa6c;
    font-size: 0.8rem;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
    transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}

/* แถวล่าง: Sub-navigation Menu */
.ta-bottom-row {
    background: #ffffff;
    border-top: 1px solid #f1f5f9;
}

.sub-nav-list {
    display: flex;
    gap: 30px;
    overflow-x: auto;
    scrollbar-width: none;
}

.sub-nav-list::-webkit-scrollbar {
    display: none;
}

.sub-nav-item {
    text-decoration: none;
    color: #475569;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 12px 0;
    border-bottom: 2px solid transparent;
    white-space: nowrap;
    transition: 0.2s;
}

.sub-nav-item:hover {
    color: #0f172a;
    border-bottom: 2px solid #cbd5e1;
}

/* ขีดเส้นใต้สีดำสำหรับหน้าที่กำลังเลือกอยู่ */
.sub-nav-item.active {
    color: #000000;
    border-bottom: 2px solid #000000;
}

/* Responsive */
@media (max-width: 992px) {
    .nav-search {
        display: none;
    }
}

@media (max-width: 768px) {
    .brand-text {
        font-size: 1.3rem;
    }

    .nav-item span {
        display: none;
    }

    .nav-item i {
        font-size: 1.2rem;
    }

    .sub-nav-list {
        gap: 20px;
    }
}
</style>