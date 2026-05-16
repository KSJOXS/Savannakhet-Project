<template>
    <div class="lang-switcher-auth">
        <button class="lang-btn" @click="isOpen = !isOpen">
            <i class="fas fa-globe"></i>
            <span class="current-lang">{{ currentLangLabel }}</span>
            <i class="fas fa-chevron-down" :class="{ rotated: isOpen }"></i>
        </button>

        <transition name="fade-slide">
            <div v-if="isOpen" class="lang-menu">
                <div v-for="loc in supportedLocales" :key="loc.code" class="lang-item"
                    :class="{ active: locale === loc.code }" @click="switchLang(loc.code)">
                    <span class="lang-flag">{{ loc.flag }}</span>
                    <span>{{ loc.label }}</span>
                    <i v-if="locale === loc.code" class="fas fa-check"></i>
                </div>
            </div>
        </transition>

        <div v-if="isOpen" class="overlay" @click="isOpen = false"></div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from '@/composables/useI18n'

const { locale, setLocale, supportedLocales } = useI18n()
const isOpen = ref(false)

const currentLangLabel = computed(() => {
    const found = supportedLocales.find(l => l.code === locale.value)
    return found ? found.label : 'English'
})

const switchLang = (code) => {
    setLocale(code)
    isOpen.value = false
    localStorage.setItem('lang', code)
}
</script>

<style scoped>
.lang-switcher-auth {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
}

.lang-btn {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 10px 16px;
    border-radius: 50px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    font-weight: 600;
    color: #1e293b;
    transition: 0.3s;
}

.lang-btn:hover {
    background: white;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.lang-btn i:first-child {
    color: #3498db;
}

.lang-btn i:last-child {
    font-size: 0.7rem;
    transition: 0.3s;
}

.lang-btn i.rotated {
    transform: rotate(180deg);
}

.lang-menu {
    position: absolute;
    top: calc(100% + 10px);
    right: 0;
    background: white;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    min-width: 180px;
    padding: 8px;
    overflow: hidden;
    z-index: 1001;
}

.lang-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 10px;
    cursor: pointer;
    transition: 0.2s;
    color: #475569;
    font-weight: 500;
}

.lang-item:hover {
    background: #f1f5f9;
    color: #1e293b;
}

.lang-item.active {
    background: #eff6ff;
    color: #3498db;
    font-weight: 700;
}

.lang-item i {
    margin-left: auto;
    font-size: 0.8rem;
}

.overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1000;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
    transition: all 0.3s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}

.lang-flag {
    font-size: 1.2rem;
}

@media (max-width: 640px) {
    .current-lang {
        display: none;
    }
    .lang-btn {
        padding: 10px;
    }
}
</style>
