<template>
    <div class="about-page">
        <Navbar />

        <div class="about-header">
            <div class="header-container">
                <h1>About Savannakhet Smart Travel</h1>
                <p>Discover how we use AI to create the perfect travel experience for you.</p>
            </div>
        </div>

        <div class="main-layout">
            <div class="intro-section">
                <h2>{{ t('features.title') }}</h2>
                <p class="intro-text">
                    {{ t('features.desc') }}
                </p>
            </div>

            <div class="features-grid">
                <div class="feature-card">
                    <div class="icon-box"><i class="fas fa-brain"></i></div>
                    <h3>{{ t('features.f1Title') }}</h3>
                    <p>{{ t('features.f1Desc') }}</p>
                </div>

                <div class="feature-card">
                    <div class="icon-box"><i class="fas fa-mobile-alt"></i></div>
                    <h3>{{ t('features.f2Title') }}</h3>
                    <p>{{ t('features.f2Desc') }}</p>
                </div>

                <div class="feature-card">
                    <div class="icon-box"><i class="fas fa-project-diagram"></i></div>
                    <h3>{{ t('features.f3Title') }}</h3>
                    <p>{{ t('features.f3Desc') }}</p>
                </div>

                <div class="feature-card">
                    <div class="icon-box"><i class="fas fa-cogs"></i></div>
                    <h3>{{ t('features.f4Title') }}</h3>
                    <p>{{ t('features.f4Desc') }}</p>
                </div>

                <div class="feature-card">
                    <div class="icon-box"><i class="fas fa-shield-alt"></i></div>
                    <h3>{{ t('features.f5Title') }}</h3>
                    <p>{{ t('features.f5Desc') }}</p>
                </div>
            </div>

            <div class="history-section-title">
                <h2>{{ t('timeline.title') }}</h2>
                <p>{{ t('timeline.subtitle') }}</p>
            </div>

            <div class="history-card">
                <div class="history-sidebar">
                    <div v-for="key in periodKeys" :key="key" 
                         class="sidebar-year" 
                         :class="{ active: activePeriodId === key }"
                         @click="activePeriodId = key">
                        {{ t('timeline.periods.' + key) }}
                    </div>
                </div>
                
                <div class="history-content-area">
                    <div class="timeline-line"></div>
                    
                    <transition-group name="fade-list" tag="div">
                        <div v-for="(item, idx) in filteredTimeline" :key="item.week + idx" class="t-item">
                            <div class="t-dot-wrapper">
                                <div class="t-dot" :class="{ 'halo': idx === 0 }"></div>
                            </div>
                            <div class="t-date">
                                <span class="t-year">{{ item.week }}</span>
                                <span class="t-month">{{ item.label }}</span>
                            </div>
                            <div class="t-content">
                                <p class="t-desc">
                                    <strong v-if="item.title" style="display:block; margin-bottom:6px; color:#1e293b; font-size:1.1rem;">{{ item.title }}</strong>
                                    {{ item.desc }}
                                </p>
                            </div>
                        </div>
                    </transition-group>
                    
                    <div class="history-watermark">{{ t('timeline.watermark') }}</div>
                </div>
            </div>
            </div>

        <section class="developer-section">
            <div class="developer-container">
                
                <div class="dev-left">
                    <p class="dev-role">{{ t('about.devRole') }}</p>
                    <h2 class="dev-name">{{ t('about.devName') }}</h2>
                    
                    <div class="dev-img-wrapper">
                        <img src="/my_portfolio.jpg" alt="Developer Profile" />
                    </div>
                </div>

                <div class="dev-right">
                    <div>
                        <p><strong>{{ t('about.quote') }}</strong></p>
                        <p>{{ t('about.p1') }}</p>
                        <p>{{ t('about.p2') }}</p>
                        <p>{{ t('about.p3') }}</p>
                        <p>{{ t('about.p4') }}</p>
                    </div>
                </div>

                <div class="dev-watermark">{{ t('about.watermark') }}</div>
            </div>
        </section>
        </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Navbar from '@/components/Navbar.vue'
import { useI18n } from '@/composables/useI18n'

const { t } = useI18n()

const periodKeys = ['feb', 'mar', 'apr', 'may', 'jun']

const activePeriodId = ref('feb')

const filteredTimeline = computed(() => {
    const items = t('timeline.items')
    if (Array.isArray(items)) {
        return items.filter(item => item.periodId === activePeriodId.value)
    }
    return []
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

.about-page {
    background-color: #f7f9fa;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    color: #1e293b;
    padding-bottom: 0;
}

/* Header */
.about-header {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    padding: 60px 20px;
    text-align: center;
    color: white;
}

.header-container h1 {
    font-size: 2.5rem;
    font-weight: 900;
    margin: 0 0 10px;
}

.header-container p {
    font-size: 1.1rem;
    color: #94a3b8;
    max-width: 600px;
    margin: 0 auto;
}

/* Main Content */
.main-layout {
    max-width: 1100px;
    margin: 40px auto 100px;
    padding: 0 20px;
}

.intro-section {
    text-align: center;
    margin-bottom: 40px;
}

.intro-section h2 {
    font-size: 1.8rem;
    font-weight: 800;
    color: #000;
    margin-bottom: 15px;
}

.intro-text {
    font-size: 1.05rem;
    color: #475569;
    line-height: 1.6;
    max-width: 800px;
    margin: 0 auto;
}

/* Grid Cards */
.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    padding-bottom: 40px;
}

.feature-card {
    background: white;
    padding: 30px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    transition: 0.3s;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    border-color: #cbd5e1;
}

.icon-box {
    width: 60px;
    height: 60px;
    background: #f1f5f9;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    color: #3498db;
    margin-bottom: 20px;
}

.feature-card h3 {
    font-size: 1.2rem;
    font-weight: 800;
    margin: 0 0 15px;
    color: #0f172a;
}

.feature-card p {
    font-size: 0.95rem;
    color: #475569;
    line-height: 1.6;
    margin: 0;
}

/* ─── 🚨 History Timeline CSS 🚨 ─── */
.history-section-title {
    text-align: center;
    margin-top: 60px;
    margin-bottom: 30px;
}
.history-section-title h2 {
    font-size: 2.2rem;
    font-weight: 800;
    color: #1e293b;
    margin-bottom: 8px;
}
.history-section-title p {
    color: #64748b;
    font-size: 1.1rem;
}

.history-card {
    display: flex;
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    margin: 0 auto;
    min-height: 500px;
}

.history-sidebar {
    width: 280px;
    background: #206fa3;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
    padding: 40px 0;
}

.sidebar-year {
    color: rgba(255, 255, 255, 0.5);
    font-size: 1.4rem;
    padding: 20px 0;
    text-align: center;
    cursor: pointer;
    transition: 0.3s;
    position: relative;
}

.sidebar-year:hover {
    color: rgba(255, 255, 255, 0.8);
}

.sidebar-year.active {
    color: white;
    font-size: 2.2rem;
    font-weight: 800;
}

.sidebar-year.active::after {
    content: '';
    position: absolute;
    right: -20px;
    top: 50%;
    transform: translateY(-50%);
    border-top: 20px solid transparent;
    border-bottom: 20px solid transparent;
    border-left: 20px solid #206fa3;
    z-index: 10;
}

.history-content-area {
    flex: 1;
    padding: 80px 60px;
    position: relative;
    overflow: hidden;
}

.timeline-line {
    position: absolute;
    left: 65px; 
    top: 80px;
    bottom: 80px;
    width: 1px;
    background: #e2e8f0;
}

.t-item {
    display: flex;
    align-items: flex-start;
    margin-bottom: 50px;
    position: relative;
    z-index: 2;
}

.t-item:last-child {
    margin-bottom: 0;
}

.t-dot-wrapper {
    width: 10px;
    display: flex;
    justify-content: center;
    margin-top: 6px;
    background: white; 
    padding: 4px 0;
}

.t-dot {
    width: 10px;
    height: 10px;
    background: #206fa3;
    border-radius: 50%;
}

.t-dot.halo {
    box-shadow: 0 0 0 6px #e0f2fe; 
}

.t-date {
    display: flex;
    flex-direction: column;
    gap: 5px;
    width: 140px;
    padding-left: 40px;
    color: #64748b;
    font-size: 0.9rem;
}

.t-year {
    font-weight: 800;
    color: #206fa3;
    font-size: 1.05rem;
}

.t-month {
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.5px;
}

.t-content {
    flex: 1;
    padding-right: 80px;
}

.t-desc {
    margin: 0;
    color: #475569;
    line-height: 1.6;
    font-size: 1rem;
}

.history-watermark {
    position: absolute;
    right: -70px;
    top: 50%;
    transform: translateY(-50%) rotate(90deg);
    font-size: 7rem;
    font-weight: 900;
    color: #206fa3;
    opacity: 0.04;
    letter-spacing: 5px;
    pointer-events: none;
    user-select: none;
}

.fade-list-enter-active,
.fade-list-leave-active {
    transition: all 0.4s ease;
}
.fade-list-enter-from {
    opacity: 0;
    transform: translateY(15px);
}
.fade-list-leave-to {
    opacity: 0;
    transform: translateY(-15px);
    position: absolute;
}

/* ─── 🚨 Developer Profile Section 🚨 ─── */
.developer-section {
    background-color: #206fa3;
    color: white;
    padding: 100px 0;
    position: relative;
    overflow: hidden;
}

.developer-container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 20px;
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: 60px;
    position: relative;
    z-index: 2;
}

.dev-left {
    display: flex;
    flex-direction: column;
}

.dev-role {
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 2px;
    margin: 0 0 10px;
    text-transform: uppercase;
    border-bottom: 2px solid white;
    padding-bottom: 5px;
    display: inline-block;
    width: fit-content;
}

.dev-name {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 0 0 30px;
    line-height: 1.2;
}

.dev-img-wrapper {
    width: 200px;
    height: 250px;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 15px 35px rgba(0,0,0,0.2);
}

.dev-img-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.dev-right {
    padding-top: 10px;
    padding-right: 80px; 
}

.dev-right p {
    font-size: 1.05rem;
    line-height: 1.8;
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: 20px;
}

.dev-right p strong {
    font-size: 1.15rem;
    color: white;
}

.dev-watermark {
    position: absolute;
    right: -40px;
    top: 50%;
    transform: translateY(-50%) rotate(90deg);
    font-size: 5rem;
    font-weight: 900;
    color: white;
    opacity: 0.15;
    letter-spacing: 5px;
    pointer-events: none;
    user-select: none;
    white-space: nowrap;
}

.deco-circle {
    position: absolute;
    bottom: -60px;
    left: -40px;
    width: 150px;
    height: 150px;
    background: white;
    border-radius: 50%;
    opacity: 0.9;
    z-index: 1;
}

/* Responsive */
@media (max-width: 992px) {
    .history-card { flex-direction: column; }
    .history-sidebar { width: 100%; flex-direction: row; padding: 20px 0; flex-wrap: wrap; }
    .sidebar-year { width: auto; padding: 10px 20px; font-size: 1rem; }
    .sidebar-year.active { font-size: 1.5rem; }
    .sidebar-year.active::after {
        right: 50%; top: auto; bottom: -20px; transform: translateX(50%);
        border-left: 15px solid transparent; border-right: 15px solid transparent;
        border-top: 15px solid #206fa3; border-bottom: none;
    }
    .history-content-area { padding: 40px 20px; }
    .timeline-line { left: 25px; }
    .t-date { flex-direction: column; width: 90px; padding-left: 25px; gap: 2px; }
    .t-content { padding-right: 0; }
    .history-watermark { display: none; }

    /* Developer Section Responsive */
    .developer-container { grid-template-columns: 1fr; gap: 30px; }
    .dev-right { padding-right: 0; }
    .dev-watermark { display: none; }
    .dev-img-wrapper { width: 150px; height: 150px; border-radius: 50%; }
}

</style>