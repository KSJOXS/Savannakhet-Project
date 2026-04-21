<template>
    <div class="explore-page">
        <Navbar />

        <header class="hero" :style="heroStyle">
            <transition name="slide-fade">
                <div class="hero-bg" :key="currentHeroIndex" :style="slideStyle"></div>
            </transition>
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <div class="badge-new">{{ t('recommend.hero_badge') }}</div>
                <h1>{{ t('recommend.hero_title') }}</h1>
                <p>{{ t('recommend.hero_subtitle') }}</p>
                <div class="hero-actions">
                    <button @click="executeSearch" class="btn-start">
                        <i class="fas fa-rocket"></i> {{ t('recommend.btn_start') }}
                    </button>
                    <button v-if="!user" @click="router.push('/register')" class="btn-start btn-outline">
                        <i class="fas fa-user-plus"></i> {{ t('recommend.btn_join') }}
                    </button>
                </div>
            </div>

            <div v-if="heroImages.length > 1" class="hero-dots">
                <span v-for="(_, idx) in heroImages" :key="'hero-dot-'+idx" 
                      :class="['dot', { active: currentHeroIndex === idx }]" 
                      @click="currentHeroIndex = idx">
                </span>
            </div>
        </header>

        <div class="stats-bar">
            <div class="stat-item">
                <span class="stat-num">50+</span>
                <span class="stat-label">{{ t('recommend.stat_places') }}</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
                <span class="stat-num">AI</span>
                <span class="stat-label">{{ t('recommend.stat_powered') }}</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
                <span class="stat-num">Free</span>
                <span class="stat-label">{{ t('recommend.stat_free') }}</span>
            </div>
        </div>

        <section class="featured-section">
            <div class="container">
                <div class="section-header">
                    <div>
                        <p class="section-eyebrow">{{ t('recommend.handpicked') }}</p>
                        <h2>{{ t('recommend.featured') }}</h2>
                    </div>
                    <button @click="executeSearch" class="btn-view-all">
                        {{ t('recommend.view_all') }} <i class="fas fa-arrow-right"></i>
                    </button>
                </div>

                <div v-if="loading" class="featured-grid">
                    <div v-for="i in 3" :key="i" class="placeholder-card">
                        <div class="skeleton-img"></div>
                        <div class="skeleton-body">
                            <div class="skeleton-title"></div>
                            <div class="skeleton-text"></div>
                        </div>
                    </div>
                </div>

                <div v-else class="featured-grid">
                    <div v-for="place in featuredPlaces" :key="place.id" class="place-card"
                        @click="router.push(`/places/${place.id}`)">
                        <div class="card-img-wrapper">
                            <img :src="getCoverImage(place)" :alt="place.name">
                            <span class="card-tag">{{ getCategoryName(place.category_id) }}</span>
                            <div class="rating-pill">⭐ {{ place.rating_avg || '0.0' }}</div>
                        </div>
                        <div class="card-body">
                            <h3>{{ place.name }}</h3>
                            <p class="desc">{{ place.description }}</p>
                            <div class="card-footer">
                                <span class="location-tag"><i class="fas fa-map-marker-alt"></i> Savannakhet, Laos</span>
                                <span class="btn-detail">{{ t('place.viewOnMap') }} <i class="fas fa-arrow-right"></i></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <div class="main-container">
            <section v-if="recommendedPlaces.length > 0" class="horizontal-section">
                <div class="section-header">
                    <h2>{{ t('recommend.ai_recom') }}</h2>
                    <p>{{ t('recommend.ai_desc') }}</p>
                </div>
                <div class="carousel-container">
                    <div v-for="place in recommendedPlaces" :key="'rec-'+place.id" class="ta-card ai-card" @click="goToDetail(place.id)">
                        <div class="card-img-wrapper">
                            <img :src="getCoverImage(place)" :alt="place.name" />
                            <button v-if="!user || user.role !== 'admin'" class="btn-heart" :class="{ active: isFavorite(place.id) }" @click.stop="toggleHeart(place.id)">
                                <i class="fas fa-heart"></i>
                            </button>
                        </div>
                        <div class="card-info">
                            <h3 class="truncate">{{ place.name }}</h3>
                            <div class="rating-row">
                                <span class="bubbles"><i class="fas fa-star" style="color: #f59e0b;"></i></span>
                                <span class="rating-num">{{ place.rating_avg || '0.0' }}</span>
                            </div>
                            <p class="cat-text"><i class="fas fa-map-marker-alt"></i> {{ getCategoryName(place.category_id) }}</p>
                        </div>
                    </div>
                </div>
            </section>

            <section v-if="topRatedPlaces.length > 0" class="horizontal-section">
                <div class="section-header">
                    <h2>{{ t('recommend.top_rated') }}</h2>
                    <p>{{ t('recommend.top_desc') }}</p>
                </div>
                <div class="carousel-container">
                    <div v-for="place in topRatedPlaces" :key="'top-'+place.id" class="ta-card" @click="goToDetail(place.id)">
                        <div class="card-img-wrapper">
                            <img :src="getCoverImage(place)" :alt="place.name" />
                            <div class="rank-badge">Top Rated</div>
                            <button v-if="!user || user.role !== 'admin'" class="btn-heart" :class="{ active: isFavorite(place.id) }" @click.stop="toggleHeart(place.id)">
                                <i class="fas fa-heart"></i>
                            </button>
                        </div>
                        <div class="card-info">
                            <h3 class="truncate">{{ place.name }}</h3>
                            <div class="rating-row">
                                <i class="fas fa-star" style="color: #f59e0b;"></i>
                                <span class="rating-num">{{ place.rating_avg || '0.0' }}</span>
                            </div>
                            <p class="cat-text"><i class="fas fa-map-marker-alt"></i> {{ getCategoryName(place.category_id) }}</p>
                        </div>
                    </div>
                </div>
            </section>

            <section class="explore-all-section" ref="exploreAllSection">
                <div class="section-header mt-50">
                    <h2>{{ t('recommend.explore_all') }}</h2>
                </div>
                <div class="explore-layout">
                    <aside class="sidebar">
                        <div class="filter-card">
                            <h3>{{ t('recommend.filters') }}</h3>
                            <div class="filter-group mt-15">
                                <div class="input-with-icon">
                                    <i class="fas fa-search"></i>
                                    <input v-model="searchQuery" type="text" :placeholder="t('explore.search')" />
                                </div>
                            </div>
                            <div class="filter-group">
                                <h4>{{ t('recommend.categories') }}</h4>
                                <div class="category-list">
                                    <button :class="['cat-pill', { active: !selectedCategory }]" @click="filterByCategory(null)">{{ t('recommend.all') }}</button>
                                    <button v-for="cat in categories" :key="cat.id"
                                        :class="['cat-pill', { active: selectedCategory === cat.id }]"
                                        @click="filterByCategory(cat.id)">
                                        {{ cat.name }}
                                    </button>
                                </div>
                            </div>
                            <button @click="resetFilters" class="btn-clear">{{ t('recommend.clear_filters') }}</button>
                        </div>
                    </aside>

                    <main class="content-area">
                        <div class="results-bar">
                            <span>{{ t('recommend.found_places').replace('{count}', filteredPlaces.length) }}</span>
                        </div>

                        <div v-if="loading" class="loading-state">
                            <div class="spinner"></div><p>{{ t('recommend.searching') }}</p>
                        </div>

                        <div v-else class="places-grid">
                            <div v-for="place in filteredPlaces" :key="place.id" class="ta-card list-card" @click="goToDetail(place.id)">
                                <div class="card-img-wrapper">
                                    <img :src="getCoverImage(place)" :alt="place.name" />
                                    <button v-if="!user || user.role !== 'admin'" class="btn-heart" :class="{ active: isFavorite(place.id) }" @click.stop="toggleHeart(place.id)">
                                        <i class="fas fa-heart"></i>
                                    </button>
                                </div>
                                <div class="card-info">
                                    <h3>{{ place.name }}</h3>
                                    <div class="rating-row mb-10">
                                        <i class="fas fa-star" style="color: #f59e0b;"></i>
                                        <span class="rating-num">{{ place.rating_avg || '0.0' }}</span>
                                        <span class="cat-text" style="margin-left: 10px;">• <i class="fas fa-map-marker-alt"></i> {{ getCategoryName(place.category_id) }}</span>
                                    </div>
                                    <p class="description">{{ place.description }}</p>
                                </div>
                            </div>
                        </div>

                        <div v-if="!loading && filteredPlaces.length === 0" class="empty-state">
                            <i class="fas fa-map-marked-alt"></i>
                            <p>{{ t('recommend.no_places') }}</p>
                        </div>
                    </main>
                </div>
            </section>
        </div>

        <section class="history-section">
            <div class="container history-container">
                <div class="history-images">
                    <img src="https://images.unsplash.com/photo-1540611025311-01df3cef54b5?q=80&w=800" alt="Savannakhet City" class="history-main-img" />
                    <div class="history-float-img">
                        <img src="https://images.unsplash.com/photo-1590352528795-9b2f6f5df5fb?q=80&w=400" alt="Lao Culture" />
                    </div>
                </div>
                <div class="history-content">
                    <p class="section-eyebrow">Discover The Heritage</p>
                    <h2>เรื่องราวของนครไกสอน พมวิหาน <br>(แขวงสะหวันนะเขต)</h2>
                    <p>
                        <strong>"สะหวันนะเขต"</strong> หรือที่ปัจจุบันรู้จักกันในชื่อ <strong>นครไกสอน พมวิหาน</strong> เป็นแขวงที่ใหญ่ที่สุดและมีประชากรมากที่สุดในประเทศลาว ตั้งอยู่ริมฝั่งแม่น้ำโขง ตรงข้ามกับจังหวัดมุกดาหารของประเทศไทย
                    </p>
                    <p>
                        เมืองแห่งนี้เต็มไปด้วยเสน่ห์ที่ผสมผสานระหว่างอารยธรรมดั้งเดิมและสถาปัตยกรรมยุคอาณานิคมฝรั่งเศส (French Colonial) ที่ยังคงหลงเหลืออยู่ตามตึกรามบ้านช่องใจกลางเมือง นอกจากนี้ยังมีแหล่งค้นพบฟอสซิลไดโนเสาร์แห่งแรกของลาวอีกด้วย
                    </p>
                    <ul class="history-highlights">
                        <li>
                            <div class="highlight-icon"><i class="fas fa-landmark"></i></div>
                            <div>
                                <strong>สถาปัตยกรรมโคโลเนียล</strong>
                                <span>เดินชมตึกเก่าสุดคลาสสิกที่ใจกลางเมืองเก่า</span>
                            </div>
                        </li>
                        <li>
                            <div class="highlight-icon"><i class="fas fa-vihara"></i></div>
                            <div>
                                <strong>พระธาตุอิงฮัง</strong>
                                <span>ปูชนียสถานศักดิ์สิทธิ์ ศูนย์รวมจิตใจของชาวสะหวันนะเขต</span>
                            </div>
                        </li>
                        <li>
                            <div class="highlight-icon"><i class="fas fa-bone"></i></div>
                            <div>
                                <strong>พิพิธภัณฑ์ไดโนเสาร์</strong>
                                <span>ชมฟอสซิลไดโนเสาร์อายุนับล้านปีที่ถูกค้นพบในแขวงนี้</span>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </section>

        <section class="cta-section">
            <div class="cta-content">
                <template v-if="!user">
                    <h2>{{ t('recommend.ready') }}</h2>
                    <p>{{ t('recommend.create_account') }}</p>
                    <button @click="router.push('/register')" class="btn-cta">
                        <i class="fas fa-user-plus"></i> {{ t('recommend.get_started') }}
                    </button>
                </template>
                
                <template v-else>
                    <h2>พร้อมที่จะออกเดินทางหรือยัง?</h2>
                    <p>ค้นพบและบันทึกสถานที่ใหม่ๆ ในสไตล์ของคุณ</p>
                    <button @click="executeSearch" class="btn-cta">
                        <i class="fas fa-map-marked-alt"></i> ค้นหาสถานที่เพิ่มเติม
                    </button>
                </template>
            </div>
        </section>

        <footer class="simple-footer">
            <p>🌴 Savannakhet Smart Travel &copy; 2026 — Powered by GNN Recommendation</p>
        </footer>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { placeRepository } from '@/repositories/placeRepository'
import { categoryRepository } from '@/repositories/categoryRepository'
import settingRepository from '@/repositories/settingRepository'
import { favoriteRepository } from '@/repositories/favoriteRepository'
import { useAuth } from '@/composables/useAuth'
import { useI18n } from '@/composables/useI18n'
import Navbar from '@/components/Navbar.vue'
import axios from 'axios'

const router = useRouter()
const { user } = useAuth()
const { t } = useI18n()
const places = ref([])
const categories = ref([])
const featuredPlaces = ref([])
const loading = ref(true)
const searchQuery = ref('')
const selectedCategory = ref(null)
const favoriteIds = ref([])
const recommendedPlaces = ref([])

// 🏞️ ข้อมูลสำหรับ Hero Slider (ดึงจาก Settings)
const heroImages = ref([])
const currentHeroIndex = ref(0)
let heroInterval = null

// รูปภาพสำรองกรณี Admin ยังไม่ได้อัปโหลด
const DEFAULT_HERO = 'https://images.unsplash.com/photo-1540611025311-01df3cef54b5?q=80&w=2070'

const heroStyle = computed(() => ({
    backgroundColor: '#1e293b',
    backgroundImage: heroImages.value.length === 0 ? `url(${DEFAULT_HERO})` : 'none',
}))

const slideStyle = computed(() => {
    if (!heroImages.value.length) return {};
    return {
        backgroundImage: `url(${heroImages.value[currentHeroIndex.value]})`,
    };
})

const startSlideshow = () => {
    if (heroInterval) clearInterval(heroInterval);
    if (heroImages.value.length > 1) {
        heroInterval = setInterval(() => {
            currentHeroIndex.value = (currentHeroIndex.value + 1) % heroImages.value.length;
        }, 5000);
    }
}

const exploreAllSection = ref(null)
const executeSearch = () => {
    if (exploreAllSection.value) {
        exploreAllSection.value.scrollIntoView({ behavior: 'smooth' })
    }
}

const getCoverImage = (place) => {
    const noImageUrl = 'data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22400%22%20height%3D%22300%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20fill%3D%22%23e2e8f0%22%2F%3E%3Ctext%20x%3D%2250%25%22%20y%3D%2250%25%22%20fill%3D%22%2364748b%22%20font-family%3D%22sans-serif%22%20font-size%3D%2220%22%20text-anchor%3D%22middle%22%20dy%3D%22.3em%22%3ENo%20Image%3C%2Ftext%3E%3C%2Fsvg%3E';
    let targetUrl = place.image_url;

    if (!targetUrl || targetUrl === '[]') return noImageUrl;

    if (typeof targetUrl === 'string' && targetUrl.trim().startsWith('[')) {
        try {
            const parsed = JSON.parse(targetUrl);
            if (Array.isArray(parsed) && parsed.length > 0) targetUrl = parsed[0];
        } catch (e) {
            targetUrl = targetUrl.replace(/^\["?|"?\]$/g, '').replace(/\\"/g, '');
        }
    }

    if (targetUrl.startsWith('http://') || targetUrl.startsWith('https://') || targetUrl.startsWith('data:')) return targetUrl;
    return `http://localhost:8000${targetUrl.startsWith('/') ? '' : '/'}${targetUrl}`;
}

const topRatedPlaces = computed(() => {
    return [...places.value].sort((a, b) => (parseFloat(b.rating_avg) || 0) - (parseFloat(a.rating_avg) || 0)).slice(0, 8);
})

const fetchData = async () => {
    loading.value = true
    try {
        const [resPlaces, resCats] = await Promise.all([placeRepository.getAll(), categoryRepository.getAll()])
        places.value = resPlaces.data
        categories.value = resCats.data
        featuredPlaces.value = resPlaces.data.slice(0, 3)

        if (user.value && user.value.role !== 'admin') {
            try {
                const favRes = await favoriteRepository.getUserFavorites(user.value.id)
                favoriteIds.value = favRes.data.map(f => f.place_id)
            } catch (err) { console.warn("Cannot fetch favorites", err) }

            try {
                const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
                const aiRes = await axios.get(`${backendUrl}/api/recommendations/${user.value.id}?top_k=8`);
                if (aiRes.data.status === 'success') {
                    recommendedPlaces.value = aiRes.data.recommended_place_ids
                        .map(id => places.value.find(p => p.id === id))
                        .filter(p => p !== undefined);
                }
            } catch (aiErr) { console.warn("AI Not ready", aiErr); }
        }
    } catch (err) { console.error("API Error:", err) } finally { loading.value = false }

    // 3. 🌟 ดึงข้อมูล hero_images_recommend 🌟
    try {
        const resSetting = await settingRepository.getByKey('hero_images_recommend')
        if (resSetting.data && resSetting.data.value) {
            const parsed = JSON.parse(resSetting.data.value);
            if (Array.isArray(parsed) && parsed.length > 0) {
                heroImages.value = parsed.map(url => {
                    if (url.startsWith('http') || url.startsWith('data:')) return url;
                    return `http://localhost:8000/${url.startsWith('/') ? url.slice(1) : url}`;
                });
                startSlideshow();
            }
        }
    } catch (settingsError) {
        console.warn('Hero settings for recommend list not found:', settingsError?.response?.status || settingsError.message)
    }
}

const filteredPlaces = computed(() => {
    return places.value.filter(p => {
        const matchesSearch = p.name.toLowerCase().includes(searchQuery.value.toLowerCase())
        const matchesCat = !selectedCategory.value || p.category_id === selectedCategory.value
        return matchesSearch && matchesCat
    })
})

const filterByCategory = (id) => selectedCategory.value = id
const resetFilters = () => { searchQuery.value = ''; selectedCategory.value = null }
const getCategoryName = (id) => categories.value.find(c => c.id === id)?.name || 'General'

const goToDetail = (id) => router.push(`/places/${id}`)

const toggleHeart = async (placeId) => {
    if (!user.value) return router.push('/login')
    try {
        const res = await favoriteRepository.toggleFavorite(user.value.id, placeId)
        if (res.data.status === 'added') favoriteIds.value.push(placeId)
        else favoriteIds.value = favoriteIds.value.filter(id => id !== placeId)
    } catch (err) { console.error(err) }
}
const isFavorite = (id) => favoriteIds.value.includes(id)

onMounted(() => { fetchData() })
onUnmounted(() => { if (heroInterval) clearInterval(heroInterval) })
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

.explore-page { background-color: #f7f9fa; min-height: 100vh; font-family: 'Inter', sans-serif; color: #1e293b; }

/* ─── Hero ─── */
.hero { position: relative; min-height: 580px; display: flex; align-items: center; justify-content: center; text-align: center; color: white; overflow: hidden; z-index: 50; }
.hero-bg { position: absolute; inset: 0; background-position: center; background-size: cover; z-index: 0; }
.slide-fade-enter-active { transition: opacity 1s ease; }
.slide-fade-leave-active { transition: opacity 1s ease; position: absolute; inset: 0; }
.slide-fade-enter-from, .slide-fade-leave-to { opacity: 0; }

.hero-dots { position: absolute; bottom: 24px; left: 50%; transform: translateX(-50%); display: flex; gap: 8px; z-index: 55; }
.dot { width: 10px; height: 10px; border-radius: 50%; border: 2px solid rgba(255,255,255,0.7); background: transparent; cursor: pointer; transition: 0.3s; }
.dot.active { background: white; transform: scale(1.3); }

.hero-overlay { position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(0, 0, 0, 0.2) 0%, rgba(0, 0, 0, 0.5) 100%); z-index: 1; }
.hero-content { position: relative; z-index: 2; max-width: 820px; padding: 0 24px; }
.badge-new { background: rgba(255, 255, 255, 0.18); border: 1px solid rgba(255, 255, 255, 0.3); padding: 7px 18px; border-radius: 50px; display: inline-block; margin-bottom: 22px; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.5px; backdrop-filter: blur(4px); }
.hero-content h1 { font-size: 3.8rem; font-weight: 800; margin-bottom: 16px; line-height: 1.15; text-shadow: 0 2px 20px rgba(0,0,0,0.2); }
.hero-content p { font-size: 1.15rem; margin-bottom: 36px; line-height: 1.6; font-weight: 500; }
.hero-actions { display: flex; gap: 14px; justify-content: center; }

.btn-start { background: #3498db; color: white; border: none; padding: 15px 38px; border-radius: 50px; font-size: 1rem; font-weight: 700; cursor: pointer; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25); transition: 0.3s; display: inline-flex; align-items: center; gap: 9px; font-family: 'Inter', sans-serif; }
.btn-start:hover { background: #2980b9; transform: translateY(-4px); box-shadow: 0 14px 30px rgba(0, 0, 0, 0.3); }
.btn-outline { background: rgba(255, 255, 255, 0.15); border: 1.5px solid rgba(255, 255, 255, 0.6); backdrop-filter: blur(4px); }
.btn-outline:hover { background: rgba(255, 255, 255, 0.28); }

/* ─── Stats Bar ─── */
.stats-bar { background: white; display: flex; justify-content: center; align-items: center; gap: 48px; padding: 22px 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); }
.stat-item { display: flex; flex-direction: column; align-items: center; }
.stat-num { font-size: 1.6rem; font-weight: 800; color: #3498db; line-height: 1; }
.stat-label { font-size: 0.78rem; color: #94a3b8; font-weight: 500; margin-top: 3px; }
.stat-divider { width: 1px; height: 36px; background: #e2e8f0; }

/* ─── Featured Section ─── */
.featured-section { padding: 80px 20px; background: #f8fafc; }
.container { max-width: 1200px; margin: 0 auto; }
.section-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 40px; }
.section-eyebrow { font-size: 0.82rem; font-weight: 700; color: #3498db; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 6px; }
.section-header h2 { font-size: 2.1rem; font-weight: 800; color: #1e293b; margin: 0; }
.btn-view-all { background: none; border: none; color: #3498db; font-weight: 700; cursor: pointer; font-size: 0.92rem; display: flex; align-items: center; gap: 6px; transition: 0.2s; font-family: 'Inter', sans-serif; }
.btn-view-all:hover { gap: 10px; color: #2980b9; }

/* ─── Cards ─── */
.featured-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 28px; }
.place-card, .ta-card { background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06); transition: all 0.3s ease; cursor: pointer; border: 1px solid #f1f5f9; }
.ta-card { flex: 0 0 280px; scroll-snap-align: start; }
.place-card:hover, .ta-card:hover { transform: translateY(-8px); box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12); }
.ai-card { border: 2px solid #3498db; }

.card-img-wrapper { position: relative; height: 220px; overflow: hidden; }
.ta-card .card-img-wrapper { height: 190px; }
.card-img-wrapper img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; }
.place-card:hover .card-img-wrapper img, .ta-card:hover .card-img-wrapper img { transform: scale(1.05); }

.card-tag { position: absolute; top: 14px; left: 14px; background: #3498db; color: white; padding: 5px 13px; border-radius: 50px; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.3px; }
.rating-pill { position: absolute; top: 14px; right: 14px; background: rgba(0,0,0,0.55); color: white; padding: 5px 11px; border-radius: 50px; font-size: 0.78rem; font-weight: 700; backdrop-filter: blur(4px); }
.rank-badge { position: absolute; top: 10px; left: 10px; background: #000; color: white; padding: 4px 10px; font-size: 0.75rem; font-weight: 800; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.3); }

.btn-heart { position: absolute; top: 10px; right: 10px; background: rgba(255,255,255,0.9); border: none; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.2); color: #94a3b8; transition: 0.2s; z-index: 10; }
.btn-heart.active { color: #ef4444; }
.btn-heart:hover { transform: scale(1.1); }

.card-body, .card-info { padding: 22px 24px; color: #1e293b; }
.card-info { padding: 16px; }
.card-body h3, .card-info h3 { margin: 0 0 8px; font-size: 1.15rem; font-weight: 800; }
.truncate { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.desc, .description { color: #64748b; font-size: 0.85rem; line-height: 1.6; margin-bottom: 16px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

.card-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 14px; border-top: 1px solid #f1f5f9; }
.location-tag { color: #94a3b8; font-size: 0.78rem; display: flex; align-items: center; gap: 5px; }
.location-tag i { color: #3498db; }
.btn-detail { color: #3498db; font-weight: 700; font-size: 0.83rem; display: flex; align-items: center; gap: 5px; transition: 0.2s; }
.place-card:hover .btn-detail { gap: 8px; }

.rating-row { display: flex; align-items: center; margin-bottom: 6px; }
.rating-num { font-size: 0.9rem; font-weight: 700; margin-left: 6px; }
.cat-text { font-size: 0.85rem; color: #64748b; margin: 0; }

/* --- Main Layout --- */
.main-container { max-width: 1400px; margin: 0 auto; padding: 40px 20px; position: relative; z-index: 10; }
.horizontal-section { margin-bottom: 50px; }
.carousel-container { display: flex; overflow-x: auto; gap: 20px; padding-bottom: 20px; scroll-snap-type: x mandatory; scrollbar-width: thin; scrollbar-color: #cbd5e1 transparent; }
.carousel-container::-webkit-scrollbar { height: 8px; }
.carousel-container::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }

/* --- Explore All Section --- */
.mt-50 { margin-top: 50px; scroll-margin-top: 100px; } 
.mb-10 { margin-bottom: 10px; }
.explore-layout { display: grid; grid-template-columns: 300px 1fr; gap: 30px; margin-top: 20px; }
.sidebar { position: sticky; top: 90px; height: fit-content; }
.filter-card { background: white; padding: 25px; border-radius: 16px; border: 1px solid #e2e8f0; color: #1e293b; }
.filter-card h3 { margin: 0; font-size: 1.25rem; font-weight: 800; }
.filter-card h4 { margin: 15px 0 10px; font-size: 0.95rem; font-weight: 700; color: #475569; }
.mt-15 { margin-top: 15px; }

.input-with-icon { position: relative; display: flex; align-items: center; }
.input-with-icon i { position: absolute; left: 12px; color: #94a3b8; }
.input-with-icon input { width: 100%; padding: 10px 10px 10px 35px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.9rem; background: #f8fafc; outline: none; }
.input-with-icon input:focus { border-color: #3498db; }

.category-list { display: flex; flex-wrap: wrap; gap: 8px; }
.cat-pill { padding: 6px 14px; border-radius: 20px; border: 1px solid #cbd5e1; background: white; color: #475569; font-size: 0.85rem; font-weight: 600; cursor: pointer; transition: 0.2s; }
.cat-pill:hover { border-color: #000; color: #000; }
.cat-pill.active { background: #000; color: white; border-color: #000; }
.btn-clear { width: 100%; padding: 12px; margin-top: 20px; background: none; border: 1px solid #cbd5e1; border-radius: 8px; font-weight: 700; color: #1e293b; cursor: pointer; transition: 0.2s; }
.btn-clear:hover { background: #f1f5f9; }

.results-bar { margin-bottom: 20px; font-size: 1.1rem; color: #1e293b;}
.places-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 25px; }
.list-card { flex: none; }

/* ─── 🚨 History Section CSS 🚨 ─── */
.history-section {
    background-color: #ffffff;
    padding: 80px 20px;
    border-top: 1px solid #e2e8f0;
}
.history-container {
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 1.1fr;
    gap: 60px;
    align-items: center;
}
.history-images {
    position: relative;
    width: 100%;
}
.history-main-img {
    width: 90%;
    height: 500px;
    object-fit: cover;
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}
.history-float-img {
    position: absolute;
    bottom: -30px;
    right: 0;
    width: 50%;
    height: 250px;
    border-radius: 16px;
    overflow: hidden;
    border: 8px solid white;
    box-shadow: 0 15px 30px rgba(0,0,0,0.15);
}
.history-float-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.history-content {
    padding-right: 20px;
}
.history-content h2 {
    font-size: 2.2rem;
    font-weight: 800;
    color: #1e293b;
    line-height: 1.3;
    margin-bottom: 20px;
}
.history-content p {
    font-size: 1.05rem;
    color: #475569;
    line-height: 1.7;
    margin-bottom: 16px;
}
.history-highlights {
    list-style: none;
    padding: 0;
    margin-top: 30px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.history-highlights li {
    display: flex;
    align-items: flex-start;
    gap: 16px;
}
.highlight-icon {
    width: 45px;
    height: 45px;
    background: #f0f9ff;
    color: #3498db;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
}
.history-highlights li strong {
    display: block;
    color: #1e293b;
    font-size: 1.05rem;
    margin-bottom: 4px;
}
.history-highlights li span {
    color: #64748b;
    font-size: 0.9rem;
    line-height: 1.4;
}

@media (max-width: 992px) {
    .history-container {
        grid-template-columns: 1fr;
        gap: 50px;
    }
    .history-main-img {
        width: 100%;
        height: 400px;
    }
    .history-float-img {
        width: 60%;
        right: 20px;
    }
    .history-content {
        padding-right: 0;
    }
}

/* ─── CTA Section ─── */
.cta-section { background: linear-gradient(135deg, #1e5799 0%, #2989d8 50%, #207cca 100%); padding: 80px 20px; text-align: center; color: white; }
.cta-content h2 { font-size: 2.4rem; font-weight: 800; margin: 0 0 14px; }
.cta-content p { font-size: 1.1rem; opacity: 0.88; margin-bottom: 32px; max-width: 500px; margin-left: auto; margin-right: auto; }
.btn-cta { background: white; color: #1e5799; border: none; padding: 16px 42px; border-radius: 50px; font-size: 1rem; font-weight: 800; cursor: pointer; transition: 0.3s; font-family: 'Inter', sans-serif; display: inline-flex; align-items: center; gap: 10px; box-shadow: 0 8px 24px rgba(0,0,0,0.2); }
.btn-cta:hover { transform: translateY(-4px); box-shadow: 0 16px 32px rgba(0,0,0,0.25); }

/* ─── Skeletons & Loaders ─── */
.placeholder-card { background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06); }
.skeleton-img { width: 100%; height: 220px; background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%); background-size: 200% 100%; animation: shimmer 1.4s infinite; }
.skeleton-body { padding: 22px; }
.skeleton-title { width: 60%; height: 18px; background: #eee; border-radius: 6px; margin-bottom: 12px; animation: shimmer 1.4s infinite; }
.skeleton-text { width: 100%; height: 13px; background: #f5f5f5; border-radius: 6px; animation: shimmer 1.4s infinite; }
@keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }

.loading-state, .empty-state { text-align: center; padding: 100px 0; color: #64748b;}
.spinner { border: 4px solid #e2e8f0; border-top: 4px solid #000; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 20px; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

.simple-footer { text-align: center; padding: 32px 40px; color: #94a3b8; border-top: 1px solid #e2e8f0; font-size: 0.88rem; background: white; }

@media (max-width: 992px) { .explore-layout { grid-template-columns: 1fr; } .sidebar { position: relative; top: 0; margin-bottom: 20px; } }
@media (max-width: 768px) { .hero-content h1 { font-size: 2.2rem; } .hero-content p { font-size: 1rem; margin-bottom: 25px;} }
</style>