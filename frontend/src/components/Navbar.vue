<template>
    <header class="ta-header">
        <div class="ta-top-row">
            <div class="nav-container">

                <div class="nav-left">
                    <div class="brand" @click="router.push('/')">
                        <div class="brand-logo">
                            <img src="@/assets/dino-logo.png" alt="Dino Logo" class="nav-logo-img" />
                        </div>
                        <span class="brand-text">Savannakhet</span>
                    </div>

                    <div class="nav-search" v-if="route.path !== '/explore'">
                        <div class="ta-search-pill" @click="router.push('/explore')">
                            <i class="fas fa-search"></i>
                            <input type="text" placeholder="Search destinations, hotels..." readonly />
                        </div>
                    </div>
                </div>

                <div class="nav-right">

                    <div class="nav-item-dropdown" @mouseenter="isDiscoverOpen = true"
                        @mouseleave="isDiscoverOpen = false">
                        <div class="nav-item"
                            :class="{ active: route.path === '/explore' || route.path === '/history' || isDiscoverOpen }">
                            <span>{{ getTranslation('nav.discover', 'Discover') }}</span>
                            <i class="fas fa-chevron-down dropdown-icon" :class="{ rotated: isDiscoverOpen }"></i>
                        </div>
                        <transition name="fade-slide">
                            <div v-if="isDiscoverOpen" class="ta-dropdown-menu">
                                <router-link to="/explore" class="ta-dropdown-item" @click="isDiscoverOpen = false">
                                    <i class="fas fa-compass"></i> Explore All Places
                                </router-link>
                                <router-link to="/history" class="ta-dropdown-item" @click="isDiscoverOpen = false">
                                    <i class="fas fa-book-open"></i> Story of Savannakhet
                                </router-link>
                            </div>
                        </transition>
                    </div>

                    <div class="nav-item-dropdown" @mouseenter="isContributeOpen = true"
                        @mouseleave="isContributeOpen = false">
                        <div class="nav-item" :class="{ active: isContributeOpen }">
                            <span>{{ getTranslation('nav.contribute', 'Contribute') }}</span>
                            <i class="fas fa-chevron-down dropdown-icon" :class="{ rotated: isContributeOpen }"></i>
                        </div>
                        <transition name="fade-slide">
                            <div v-if="isContributeOpen" class="ta-dropdown-menu">
                                <router-link to="/write-review" class="ta-dropdown-item"
                                    @click="isContributeOpen = false">
                                    <i class="fas fa-pen-nib"></i> {{ getTranslation('nav.writeReview', 'Write Review')
                                    }}
                                </router-link>
                                <router-link to="/submit-place" class="ta-dropdown-item"
                                    @click="isContributeOpen = false">
                                    <i class="fas fa-camera"></i> {{ getTranslation('nav.postPhoto', 'Post Photo') }}
                                </router-link>
                                <div class="dropdown-divider"></div>
                                <router-link to="/submit-place" class="ta-dropdown-item"
                                    @click="isContributeOpen = false">
                                    <i class="fas fa-plus-circle"></i> {{ getTranslation('nav.addPlace', 'Add Place') }}
                                </router-link>
                            </div>
                        </transition>
                    </div>

                    <div class="nav-item-dropdown" @mouseenter="isUtilitiesOpen = true"
                        @mouseleave="isUtilitiesOpen = false">
                        <div class="nav-item" :class="{ active: route.path.includes('/utilities') || isUtilitiesOpen }">
                            <i class="fas fa-toolbox"></i>
                            <span>{{ getTranslation('nav.tools', 'Tools') }}</span>
                            <i class="fas fa-chevron-down dropdown-icon" :class="{ rotated: isUtilitiesOpen }"></i>
                        </div>
                        <transition name="fade-slide">
                            <div v-if="isUtilitiesOpen" class="ta-dropdown-menu">
                                <router-link to="/utilities?tab=currency" class="ta-dropdown-item"
                                    @click="isUtilitiesOpen = false">
                                    <i class="fas fa-exchange-alt"></i> {{ getTranslation('nav.currency', `Currency
                                    Converter`) }}
                                </router-link>
                                <router-link to="/utilities?tab=phrasebook" class="ta-dropdown-item"
                                    @click="isUtilitiesOpen = false">
                                    <i class="fas fa-language"></i> {{ getTranslation('nav.phrasebook', `Lao
                                    Phrasebook`) }}
                                </router-link>
                                <router-link to="/utilities?tab=transport" class="ta-dropdown-item"
                                    @click="isUtilitiesOpen = false">
                                    <i class="fas fa-bus"></i> {{ getTranslation('nav.transport', `Transport Guide`) }}
                                </router-link>
                            </div>
                        </transition>
                    </div>

                    <div class="nav-item-dropdown" @mouseenter="isSupportOpen = true"
                        @mouseleave="isSupportOpen = false">
                        <div class="nav-item" :class="{ active: isSupportOpen }">
                            <i class="fas fa-headset"></i>
                            <span>{{ getTranslation('nav.support', 'Support') }}</span>
                            <i class="fas fa-chevron-down dropdown-icon" :class="{ rotated: isSupportOpen }"></i>
                        </div>
                        <transition name="fade-slide">
                            <div v-if="isSupportOpen" class="ta-dropdown-menu">
                                <router-link to="/about" class="ta-dropdown-item" @click="isSupportOpen = false">
                                    <i class="fas fa-building"></i> {{ getTranslation('nav.about', 'About Us') }}
                                </router-link>
                                <router-link to="/faq" class="ta-dropdown-item" @click="isSupportOpen = false">
                                    <i class="fas fa-question-circle"></i> {{ getTranslation('nav.faq', 'Help & FAQ') }}
                                </router-link>
                                <router-link to="/guide" class="ta-dropdown-item" @click="isSupportOpen = false">
                                    <i class="fas fa-map"></i> {{ getTranslation('nav.userGuide', 'User Guide') }}
                                </router-link>
                                <div class="dropdown-divider"></div>
                                <router-link to="/contact" class="ta-dropdown-item" @click="isSupportOpen = false">
                                    <i class="fas fa-envelope"></i> {{ getTranslation('nav.contact', 'Contact Us') }}
                                </router-link>
                            </div>
                        </transition>
                    </div>

                    <router-link v-if="isLoggedIn && (!user || user.role !== 'admin')" to="/favorites"
                        class="nav-item icon-only">
                        <i class="far fa-heart"></i>
                    </router-link>

                    <div class="lang-switcher">
                        <button class="lang-btn" @click="isLangOpen = !isLangOpen">
                            <i class="fas fa-globe"></i>
                            <div class="lang-divider"></div>
                            <span>{{ currentFlagLabel }}</span>
                        </button>
                        <div v-if="isLangOpen" class="lang-overlay" @click="isLangOpen = false"></div>
                        <transition name="fade-slide">
                            <div v-if="isLangOpen" class="ta-dropdown-menu lang-menu">
                                <div v-for="loc in safeSupportedLocales" :key="loc.code" class="lang-item"
                                    :class="{ active: locale === loc.code }" @click.stop="switchLang(loc.code)">
                                    <span class="lang-flag">{{ loc.flag }}</span>
                                    <span>{{ loc.label }}</span>
                                    <i v-if="locale === loc.code" class="fas fa-check lang-check"></i>
                                </div>
                            </div>
                        </transition>
                    </div>

                    <div v-if="!isLoggedIn" class="auth-group">
                        <router-link to="/login" class="btn-ta-ghost">{{ getTranslation('nav.signIn', 'Sign In') }}</router-link>
                        <router-link to="/login" class="btn-ta-solid">{{ getTranslation('nav.join', 'Join') }}</router-link>
                    </div>

                    <div v-else class="user-group">
                        <div class="user-avatar" :title="username" @click="isProfileOpen = !isProfileOpen">
                            <img v-if="user && user.profile_image" :src="getImageUrl(user.profile_image)"
                                alt="avatar" />
                            <div v-else class="avatar-placeholder">
                                {{ username ? username.charAt(0).toUpperCase() : 'U' }}
                            </div>
                        </div>

                        <div v-if="isProfileOpen" class="dropdown-overlay" @click="isProfileOpen = false"></div>

                        <transition name="fade-slide">
                            <div v-if="isProfileOpen" class="ta-dropdown-menu profile-menu">
                                <router-link to="/profile" class="ta-dropdown-item" @click="isProfileOpen = false">
                                    <i class="far fa-user-circle"></i> {{ getTranslation('nav.profile', 'My Profile') }}
                                </router-link>
                                <router-link to="/profile?tab=reviews" class="ta-dropdown-item"
                                    @click="isProfileOpen = false">
                                    <i class="fas fa-history"></i> {{ getTranslation('nav.myReviews', 'Review History')
                                    }}
                                </router-link>
                                <router-link to="/favorites" class="ta-dropdown-item" @click="isProfileOpen = false">
                                    <i class="fas fa-suitcase-rolling"></i> {{ getTranslation('nav.myTrips', 'My Trips')
                                    }}
                                </router-link>
                                <router-link to="/profile?tab=bookings" class="ta-dropdown-item"
                                    @click="isProfileOpen = false">
                                    <i class="far fa-calendar-alt"></i> {{ getTranslation('nav.bookings', 'Bookings') }}
                                </router-link>
                                <router-link to="/profile?tab=settings" class="ta-dropdown-item"
                                    @click="isProfileOpen = false">
                                    <i class="fas fa-cog"></i> {{ getTranslation('nav.settings', 'Settings') }}
                                </router-link>
                                <div class="dropdown-divider"></div>
                                <div class="ta-dropdown-item logout" @click="handleLogoutAndClose">
                                    <i class="fas fa-sign-out-alt"></i> {{ getTranslation('nav.signOut', 'Sign Out') }}
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
                    <router-link v-if="!isLoggedIn" to="/" class="sub-nav-item" :class="{ active: route.path === '/' }">
                        {{ getTranslation('nav.home', 'Home') }}
                    </router-link>
                    <router-link to="/hotels" class="sub-nav-item" :class="{ active: route.path.includes('/hotels') }">
                        {{ getTranslation('nav.hotels', 'Hotels') }}
                    </router-link>
                    <router-link to="/explore?tab=things-to-do" class="sub-nav-item"
                        :class="{ active: route.path === '/explore' && (!route.query.tab || route.query.tab === 'things-to-do') }">
                        {{ getTranslation('nav.thingsToDo', 'Things To Do') }}
                    </router-link>
                    <router-link to="/restaurants" class="sub-nav-item"
                        :class="{ active: route.path.includes('/restaurants') }">
                        {{ getTranslation('nav.restaurants', 'Restaurants') }}
                    </router-link>
                    <router-link to="/nature" class="sub-nav-item" :class="{ active: route.path.includes('/nature') }">
                        {{ getTranslation('nav.nature', 'Nature') }}
                    </router-link>
                    <router-link to="/landmarks" class="sub-nav-item"
                        :class="{ active: route.path.includes('/landmarks') }">
                        {{ getTranslation('nav.landmarks', 'Landmarks') }}
                    </router-link>
                    <router-link to="/community" class="sub-nav-item"
                        :class="{ active: route.path.includes('/community') }">
                        <i class="fas fa-users" style="margin-right: 5px;"></i> {{ getTranslation('nav.community',
                        'Community') }}
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

const i18n = useI18n()
const t = i18n.t || ((key) => key)
const locale = i18n.locale || ref('en')
const setLocale = i18n.setLocale
const supportedLocales = i18n.supportedLocales || []

// State ควบคุม Dropdown 
const isDiscoverOpen = ref(false) // 🚨 ตัวแปรใหม่สำหรับ Discover
const isContributeOpen = ref(false)
const isUtilitiesOpen = ref(false)
const isSupportOpen = ref(false)
const isLangOpen = ref(false)
const isProfileOpen = ref(false)

const isLoggedIn = ref(isAuthenticated())
const username = ref(user.value ? user.value.username : '')

const safeSupportedLocales = computed(() => {
    if (supportedLocales && supportedLocales.length > 0) {
        return supportedLocales;
    }
    return [
        { code: 'en', flag: 'GB', label: 'English' },
        { code: 'lo', flag: 'LA', label: 'ລາວ' },
        { code: 'th', flag: 'TH', label: 'ไทย' },
        { code: 'vi', flag: 'VN', label: 'Việt' }
    ];
})

const getTranslation = (key, fallback) => {
    const translated = t(key);
    return translated === key ? fallback : translated;
}

const currentFlagLabel = computed(() => {
    const currentCode = typeof locale === 'object' && locale !== null ? locale.value : locale;
    const found = safeSupportedLocales.value.find(l => l.code === currentCode)
    return found ? found.label : 'English'
})

const switchLang = (code) => {
    isLangOpen.value = false
    try {
        if (typeof setLocale === 'function') setLocale(code);
        else if (locale && typeof locale === 'object' && 'value' in locale) locale.value = code;
        localStorage.setItem('lang', code);
    } catch (error) {
        console.error("Language switch error:", error);
    }
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

watch(() => route.path, () => {
    checkAuth()
    isDiscoverOpen.value = false
    isContributeOpen.value = false
    isUtilitiesOpen.value = false
    isSupportOpen.value = false
    isLangOpen.value = false
    isProfileOpen.value = false
})

const handleLogoutAndClose = () => {
    isProfileOpen.value = false
    logout()
    checkAuth()
    router.push('/login')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.ta-header {
    background: #ffffff;
    position: sticky;
    top: 0;
    z-index: 1000;
    font-family: 'Inter', sans-serif;
    box-shadow: 0 2px 15px rgba(0, 0, 0, 0.04);
}

.ta-top-row {
    height: 80px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #f1f5f9;
}

.nav-container {
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-left {
    display: flex;
    align-items: center;
    gap: 40px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
}

.brand-logo {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    transition: transform 0.3s ease;
}

.brand:hover .brand-logo {
    transform: rotate(-10deg) scale(1.1);
}

.nav-logo-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.brand-text {
    font-size: 1.5rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
}

.ta-search-pill {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 40px;
    padding: 10px 24px;
    width: 320px;
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.ta-search-pill:hover {
    background: #ffffff;
    border-color: #cbd5e1;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.ta-search-pill i {
    color: #00aa6c;
}

.ta-search-pill input {
    border: none;
    background: transparent;
    font-family: inherit;
    font-size: 0.95rem;
    color: #475569;
    outline: none;
    cursor: pointer;
    width: 100%;
}

.nav-right {
    display: flex;
    align-items: center;
    gap: 12px;
}

.nav-item {
    text-decoration: none;
    color: #334155;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 10px 18px;
    border-radius: 30px;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
}

.nav-item:hover,
.nav-item.active {
    background: #f1f5f9;
    color: #0f172a;
}

.nav-item.icon-only {
    padding: 10px;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    justify-content: center;
}

.nav-item.icon-only i {
    font-size: 1.2rem;
}

.nav-item-dropdown {
    position: relative;
}

.dropdown-icon {
    font-size: 0.7rem;
    transition: transform 0.3s;
    color: #94a3b8;
}

.dropdown-icon.rotated {
    transform: rotate(180deg);
}

.ta-dropdown-menu {
    position: absolute;
    top: calc(100% + 15px);
    right: 0;
    background: #ffffff;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
    border: 1px solid #f1f5f9;
    min-width: 220px;
    overflow: hidden;
    z-index: 1002;
    padding: 10px 0;
}

.ta-dropdown-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 24px;
    color: #475569;
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    transition: all 0.2s;
    cursor: pointer;
}

.ta-dropdown-item i {
    color: #94a3b8;
    width: 18px;
    text-align: center;
    font-size: 1.1rem;
    transition: color 0.2s;
}

.ta-dropdown-item:hover {
    background: #f8fafc;
    color: #0f172a;
}

.ta-dropdown-item:hover i {
    color: #00aa6c;
}

.dropdown-divider {
    height: 1px;
    background: #f1f5f9;
    margin: 8px 24px;
}

.ta-dropdown-item.logout {
    color: #ef4444;
}

.ta-dropdown-item.logout:hover i {
    color: #ef4444;
}

.auth-group {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-left: 15px;
}

.btn-ta-ghost {
    color: #0f172a;
    text-decoration: none;
    font-weight: 700;
    font-size: 0.95rem;
    padding: 10px 18px;
    border-radius: 30px;
    transition: all 0.2s;
}

.btn-ta-ghost:hover {
    background: #f1f5f9;
    color: #00aa6c;
}

.btn-ta-solid {
    background: #0f172a;
    color: #ffffff;
    text-decoration: none;
    font-weight: 700;
    font-size: 0.95rem;
    padding: 10px 24px;
    border-radius: 30px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
}

.btn-ta-solid:hover {
    background: #00aa6c;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 170, 108, 0.3);
}

.user-group {
    position: relative;
    margin-left: 10px;
}

.user-avatar {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    cursor: pointer;
    transition: transform 0.2s;
    border: 2px solid transparent;
}

.user-avatar:hover {
    transform: scale(1.05);
    border-color: #00aa6c;
}

.user-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
}

.avatar-placeholder {
    width: 100%;
    height: 100%;
    background: #0f172a;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1.2rem;
}

.lang-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    background: transparent;
    border: none;
    padding: 8px 12px;
    font-weight: 600;
    cursor: pointer;
    color: #334155;
    border-radius: 30px;
    transition: 0.2s;
}

.lang-btn:hover {
    background: #f1f5f9;
}

.lang-divider {
    width: 1px;
    height: 14px;
    background: #cbd5e1;
}

.lang-menu {
    min-width: 160px;
}

.lang-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 24px;
    cursor: pointer;
    color: #475569;
    font-weight: 500;
    transition: 0.2s;
}

.lang-item:hover {
    background: #f8fafc;
    color: #0f172a;
}

.lang-switcher {
    position: relative;
}

.lang-item.active {
    background: #e6f7f0;
    color: #00aa6c;
    font-weight: 700;
}

.lang-check {
    margin-left: auto;
    color: #00aa6c;
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

.dropdown-overlay,
.lang-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1001;
}

.ta-bottom-row {
    background: #ffffff;
}

.sub-nav-list {
    display: flex;
    gap: 32px;
    overflow-x: auto;
    scrollbar-width: none;
}

.sub-nav-list::-webkit-scrollbar {
    display: none;
}

.sub-nav-item {
    text-decoration: none;
    color: #64748b;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 16px 0;
    border-bottom: 2px solid transparent;
    white-space: nowrap;
    transition: all 0.2s;
}

.sub-nav-item:hover {
    color: #0f172a;
}

.sub-nav-item.active {
    color: #0f172a;
    border-bottom: 2px solid #0f172a;
}

@media (max-width: 1100px) {
    .nav-search {
        display: none;
    }
}

@media (max-width: 900px) {
    .nav-item span {
        display: none;
    }

    .sub-nav-list {
        gap: 20px;
    }
}
</style>