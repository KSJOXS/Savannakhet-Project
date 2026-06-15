<template>
    <div class="explore-page">
        <Navbar />

        <header class="hero" :style="heroStyle">
            <transition name="slide-fade">
                <div class="hero-bg" :key="currentHeroIndex" :style="slideStyle"></div>
            </transition>
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <h1>{{ t('recommend.hero_title') }}</h1>
                <p>{{ t('recommend.hero_subtitle') }}</p>
            </div>

            <div v-if="heroImages.length > 1" class="hero-dots">
                <span v-for="(_, idx) in heroImages" :key="'hero-dot-' + idx"
                    :class="['dot', { active: currentHeroIndex === idx }]" @click="currentHeroIndex = idx">
                </span>
            </div>
        </header>


        <section v-if="!user" class="featured-section">
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
                            <div class="rating-pill">⭐ {{ place.rating_avg || '0.0' }}</div>
                        </div>
                        <div class="card-body">
                            <span class="card-tag">{{ getCategoryName(place.category_id) }}</span>
                            <h3>{{ place.name }}</h3>
                            <p class="desc">{{ place.description }}</p>
                            <div class="card-footer">
                                <span class="location-tag"><i class="fas fa-map-marker-alt"></i> Savannakhet</span>
                                <span class="btn-detail">{{ t('landmarks.openGuide') }} →</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>


        <div class="main-container">
            <section class="explore-all-section" ref="exploreAllSection">
                <div class="section-header">
                    <!-- <h2>{{ t('recommend.explore_all') }}</h2> -->
                </div>



                <div class="explore-layout">
                    <aside class="sidebar">
                        <!-- Smart Trip Planner Banner -->
                        <div class="trip-planner-banner" @click="router.push('/trip-planner')">
                            <div class="banner-icon">
                                <i class="fas fa-magic"></i>
                            </div>
                            <div class="banner-text">
                                <h3>{{ t('explore.ai_planner_title') }}</h3>
                                <p>{{ t('explore.ai_planner_subtitle') }}</p>
                            </div>
                            <i class="fas fa-arrow-right arrow-icon"></i>
                        </div>

                        <div class="filter-card mt-20">
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
                                    <button :class="['cat-pill', { active: !selectedCategory }]"
                                        @click="filterByCategory(null)">{{ t('recommend.all') }}</button>
                                    <button v-for="cat in displayedCategories" :key="cat.id"
                                        :class="['cat-pill', { active: selectedCategory === cat.id }]"
                                        @click="filterByCategory(cat.id)">
                                        {{ cat.name }}
                                    </button>
                                    <button v-if="categories.length > 8" @click="showAllCategories = !showAllCategories" class="cat-pill show-more-btn">
                                        {{ showAllCategories ? '▲ ' + (t('recommend.show_less') || 'Thu gọn / Show less') : '▼ ' + (t('recommend.show_more') || 'Xem thêm / Show more') }}
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
                            <div class="spinner"></div>
                            <p>{{ t('recommend.searching') }}</p>
                        </div>

                        <div v-else class="places-grid">
                            <div v-for="place in filteredPlaces" :key="place.id" class="ta-card list-card"
                                @click="goToDetail(place.id)">
                                <div class="card-img-wrapper">
                                    <img :src="getCoverImage(place)" :alt="place.name" />
                                    <button v-if="!user || user.role !== 'admin'" class="btn-heart"
                                        :class="{ active: isFavorite(place.id) }" @click.stop="toggleHeart(place.id)">
                                        <i class="fas fa-heart"></i>
                                    </button>
                                </div>
                                <div class="card-info">
                                    <span class="card-tag">{{ getCategoryName(place.category_id) }}</span>
                                    <h3>{{ place.name }}</h3>
                                    <div class="rating-row mb-10">
                                        <i class="fas fa-star" style="color: #f59e0b;"></i>
                                        <span class="rating-num">{{ place.rating_avg || '0.0' }}</span>
                                    </div>
                                    <p class="description">{{ place.description }}</p>
                                    <div class="card-footer">
                                        <span class="location-tag">✨ {{ t('landmarks.verified') }}</span>
                                        <span class="btn-detail">{{ t('landmarks.openGuide') }} →</span>
                                    </div>
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

            <section v-if="topRatedPlaces.length > 0" class="horizontal-section">
                <div class="section-header">
                    <h2>{{ t('recommend.top_rated') }}</h2>
                    <p>{{ t('recommend.top_desc') }}</p>
                </div>
                <div class="carousel-container">
                    <div v-for="place in topRatedPlaces" :key="'top-' + place.id" class="ta-card"
                        @click="goToDetail(place.id)">
                        <div class="card-img-wrapper">
                            <img :src="getCoverImage(place)" :alt="place.name" />
                            <div class="rank-badge">{{ t('recommend.top_rated_badge') }}</div>
                            <button v-if="!user || user.role !== 'admin'" class="btn-heart"
                                :class="{ active: isFavorite(place.id) }" @click.stop="toggleHeart(place.id)">
                                <i class="fas fa-heart"></i>
                            </button>
                        </div>
                        <div class="card-info">
                            <span class="card-tag">{{ getCategoryName(place.category_id) }}</span>
                            <h3 class="truncate">{{ place.name }}</h3>
                            <div class="rating-row">
                                <i class="fas fa-star" style="color: #f59e0b;"></i>
                                <span class="rating-num">{{ place.rating_avg || '0.0' }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

        </div>

        <!-- ❤️ Based on your favorites (Warm Start - Shows at bottom) -->
        <section v-if="favoriteRecommendations.length > 0" class="horizontal-section"
            style="background: #f8fafc; padding: 60px 0;">
            <div class="container">
                <div class="section-header" style="margin-bottom: 35px; text-align: left;">
                    <p class="section-eyebrow"
                        style="color: #f59e0b; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 0.85rem; margin-bottom: 8px;">
                        ❤️ {{ t('recommend.interest_title') || 'อ้างอิงจากความสนใจของคุณ' }}</p>
                    <h2 style="font-size: 2.2rem; color: #0f172a; font-weight: 800; line-height: 1.2;">{{
                        t('recommend.interest_title') || 'อ้างอิงจากความสนใจของคุณ' }}</h2>
                    <p style="margin: 6px 0 0; font-size: 1.05rem; color: #64748b;">{{ t('recommend.interest_subtitle')
                        || 'สถานที่ที่คุณน่าจะชอบจากรายการโปรดของคุณ' }}</p>
                </div>
                <div class="places-grid">
                    <div v-for="place in favoriteRecommendations" :key="'fav-' + place.id" class="ta-card list-card"
                        @click="goToDetail(place.id)">
                        <div class="card-img-wrapper">
                            <img :src="getCoverImage(place)" :alt="place.name" />
                            <div class="interest-badge">❤️ {{ t('recommend.for_you') || 'Recommended' }}</div>
                            <button v-if="!user || user.role !== 'admin'" class="btn-heart"
                                :class="{ active: isFavorite(place.id) }" @click.stop="toggleHeart(place.id)">
                                <i class="fas fa-heart"></i>
                            </button>
                        </div>
                        <div class="card-info">
                            <span class="card-tag">{{ getCategoryName(place.category_id) }}</span>
                            <h3 class="truncate">{{ place.name }}</h3>
                            <div class="rating-row mb-10">
                                <i class="fas fa-star" style="color: #f59e0b;"></i>
                                <span class="rating-num">{{ place.rating_avg || '0.0' }}</span>
                            </div>
                            <p class="description">{{ place.description }}</p>
                            <div class="card-footer">
                                <span class="location-tag">✨ {{ t('landmarks.verified') }}</span>
                                <span class="btn-detail">{{ t('landmarks.openGuide') }} →</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="heritage-section">
            <div class="container heritage-container">
                <div class="heritage-images">
                    <img src="/images/heritage/main.png"
                        alt="Savannakhet Heritage" class="heritage-main-img" />
                    <div class="heritage-float-img">
                        <img src="/images/heritage/culture.png"
                            alt="Lao Culture" />
                    </div>
                </div>
                <div class="heritage-content">
                    <p class="section-eyebrow">{{ t('heritage.eyebrow') }}</p>
                    <h2 class="heritage-title" v-html="t('heritage.title')"></h2>
                    <p class="heritage-desc">
                        {{ t('heritage.desc1') }}
                    </p>
                    <p class="heritage-desc">
                        {{ t('heritage.desc2') }}
                    </p>
                    <ul class="heritage-highlights">
                        <li>
                            <div class="highlight-icon"><i class="fas fa-landmark"></i></div>
                            <div class="highlight-text">
                                <strong>{{ t('heritage.highlight1_title') }}</strong>
                                <span>{{ t('heritage.highlight1_desc') }}</span>
                            </div>
                        </li>
                        <li>
                            <div class="highlight-icon"><i class="fas fa-vihara"></i></div>
                            <div class="highlight-text">
                                <strong>{{ t('heritage.highlight2_title') }}</strong>
                                <span>{{ t('heritage.highlight2_desc') }}</span>
                            </div>
                        </li>
                        <li>
                            <div class="highlight-icon"><i class="fas fa-bone"></i></div>
                            <div class="highlight-text">
                                <strong>{{ t('heritage.highlight3_title') }}</strong>
                                <span>{{ t('heritage.highlight3_desc') }}</span>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </section>

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
const recentInteractionCategoryIds = ref([])
const showAllCategories = ref(false)

const displayedCategories = computed(() => {
    return showAllCategories.value ? categories.value : categories.value.slice(0, 8)
})

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
    return `http://127.0.0.1:8000${targetUrl.startsWith('/') ? '' : '/'}${targetUrl}`;
}

const topRatedPlaces = computed(() => {
    return [...places.value].sort((a, b) => (parseFloat(b.rating_avg) || 0) - (parseFloat(a.rating_avg) || 0)).slice(0, 8);
})

const fetchData = async () => {
    loading.value = true
    try {
        const [resPlaces, resCats] = await Promise.all([placeRepository.getAll(), categoryRepository.getAll()])
        places.value = resPlaces.data
        
        // Remove duplicate categories by name
        categories.value = resCats.data.filter((cat, index, self) =>
            index === self.findIndex((c) => c.name === cat.name)
        );
        
        featuredPlaces.value = resPlaces.data.slice(0, 3)

        if (user.value && user.value.role !== 'admin') {
            try {
                const favRes = await favoriteRepository.getUserFavorites(user.value.id)
                favoriteIds.value = favRes.data.map(f => f.place_id)
            } catch (err) {
                console.warn("Cannot fetch favorites", err)
            }

            // 🎯 Smart Interest-based Recommendations (works immediately, no GNN training needed)
            fetchInterestBasedRecommendations()

            try {
                // 🤖 Call GNN Recommendation Engine
                const backendUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
                
                // Fetch Recent Interactions to get "Current Interest Categories"
                const interactionRes = await axios.get(`${backendUrl}/api/interactions/user/${user.value.id}/frequent?limit=10`);
                if (interactionRes.data && interactionRes.data.length > 0) {
                    recentInteractionCategoryIds.value = [
                        ...new Set(interactionRes.data.map(item => item.place.category_id))
                    ];
                }

                const aiRes = await axios.get(`${backendUrl}/api/recommendations/${user.value.id}?top_k=12`);
                if (aiRes.data.status === 'success' && aiRes.data.recommended_places?.length > 0) {
                    recommendedPlaces.value = aiRes.data.recommended_places.filter(item => item.place != null);
                } else {
                    // 🔄 Fallback: ดึง "สถานที่ดูบ่อย" แบบธรรมดาถ้า AI ยังไม่พร้อม
                    if (interactionRes.data && interactionRes.data.length > 0) {
                        recommendedPlaces.value = interactionRes.data.map(item => ({
                            place: item.place,
                            reason: t('recommend.viewed_often') || 'สถานที่ที่คุณดูบ่อยช่วงนี้',
                            score: 0.95
                        }));
                    }
                }
            } catch (aiErr) {
                console.warn("AI Recommendations not ready — using recently viewed instead", aiErr);
            }
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
                    return `http://127.0.0.1:8000/${url.startsWith('/') ? url.slice(1) : url}`;
                });
                startSlideshow();
            }
        }
    } catch (settingsError) {
        console.warn('Hero settings for recommend list not found:', settingsError?.response?.status || settingsError.message)
    }
}

// 🎯 Fetch places from same categories as user's favorites AND user preferences
const favoriteRecommendations = ref([])


// 🎯 Check which categories the user prefers (Cold start)
const userPreferredCategoryIds = computed(() => {
    if (!user.value || !user.value.preferences) return []
    let prefs = user.value.preferences
    if (typeof prefs === 'string') {
        try { prefs = JSON.parse(prefs) } catch (e) { prefs = [] }
    }
    if (Array.isArray(prefs) && prefs.length > 0) {
        return categories.value
            .filter(c => prefs.includes(c.parent_type))
            .map(c => c.id)
    }
    return []
})

const fetchInterestBasedRecommendations = () => {
    if (!places.value.length) return

    // 1. Favorites based (Only shows if they have favorites)
    if (favoriteIds.value.length) {
        const likedCategoryIds = favoriteIds.value
            .map(fid => places.value.find(p => p.id === fid)?.category_id)
            .filter(Boolean)

        if (likedCategoryIds.length) {
            const catCount = {}
            likedCategoryIds.forEach(cid => catCount[cid] = (catCount[cid] || 0) + 1)
            const targetFavoriteCatIds = Object.entries(catCount)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 2)
                .map(e => parseInt(e[0]))

            favoriteRecommendations.value = places.value
                .filter(p => targetFavoriteCatIds.includes(p.category_id) && !favoriteIds.value.includes(p.id))
                .sort((a, b) => (parseFloat(b.rating_avg) || 0) - (parseFloat(a.rating_avg) || 0))
                .slice(0, 12)
        }
    }
}

const filteredPlaces = computed(() => {
    const results = places.value.filter(p => {
        const matchesSearch = p.name.toLowerCase().includes(searchQuery.value.toLowerCase())
        const matchesCat = !selectedCategory.value || p.category_id === selectedCategory.value
        return matchesSearch && matchesCat
    })

    const recommendedIds = recommendedPlaces.value.map(item => item.place.id)

    // Sort: AI/Frequently Viewed first, then Interaction-based, then Preferred categories, then by rating
    return [...results].sort((a, b) => {
        // 1. AI Recommendation Priority (Strongest)
        const aIsRecommended = recommendedIds.includes(a.id)
        const bIsRecommended = recommendedIds.includes(b.id)
        if (aIsRecommended && !bIsRecommended) return -1
        if (!aIsRecommended && bIsRecommended) return 1

        // 2. Recent Interaction Category Match (Warm Start - based on actual views/likes)
        const aIsRecent = recentInteractionCategoryIds.value.includes(a.category_id)
        const bIsRecent = recentInteractionCategoryIds.value.includes(b.category_id)
        if (aIsRecent && !bIsRecent) return -1
        if (!aIsRecent && bIsRecent) return 1

        // 3. Signup Preference Category Match (Cold Start)
        const aIsPreferred = userPreferredCategoryIds.value.includes(a.category_id)
        const bIsPreferred = userPreferredCategoryIds.value.includes(b.category_id)
        if (aIsPreferred && !bIsPreferred) return -1
        if (!aIsPreferred && bIsPreferred) return 1

        // 4. Rating Priority (Fallback)
        return (parseFloat(b.rating_avg) || 0) - (parseFloat(a.rating_avg) || 0)
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
        if (res.data.status === 'added') {
            favoriteIds.value.push(placeId)
            // 🤖 Log this "like" interaction for GNN learning (weight = 5.0)
            placeRepository.logInteraction(user.value.id, placeId, 'like').catch(() => { })
        } else {
            favoriteIds.value = favoriteIds.value.filter(id => id !== placeId)
        }
        // Re-calculate interest-based recommendations immediately
        fetchInterestBasedRecommendations()
    } catch (err) { console.error(err) }
}
const isFavorite = (id) => favoriteIds.value.includes(id)

onMounted(async () => { 
    window.scrollTo(0, 0)
    await fetchData() 
    window.scrollTo(0, 0)
})
onUnmounted(() => { if (heroInterval) clearInterval(heroInterval) })
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:wght@700;800;900&display=swap');

.explore-page {
    background-color: #faf9f6;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    color: #1e293b;
}

/* ─── Hero ─── */
.hero {
    position: relative;
    min-height: 220px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: white;
    overflow: hidden;
    z-index: 50;
}

.hero-bg {
    position: absolute;
    inset: 0;
    background-position: center;
    background-size: cover;
    z-index: 0;
}

.slide-fade-enter-active {
    transition: opacity 1s ease;
}

.slide-fade-leave-active {
    transition: opacity 1s ease;
    position: absolute;
    inset: 0;
}

.hero-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4));
    z-index: 1;
}

.hero-content {
    position: relative;
    z-index: 10;
    padding: 0 20px;
}

.hero-content h1 {
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 800;
    margin-bottom: 10px;
    letter-spacing: -1px;
}

.hero-content p {
    font-size: clamp(1rem, 2vw, 1.3rem);
    opacity: 0.9;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
    opacity: 0;
}

.hero-dots {
    position: absolute;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 8px;
    z-index: 55;
}

.dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    border: 2px solid rgba(255, 255, 255, 0.7);
    background: transparent;
    cursor: pointer;
    transition: 0.3s;
}

.dot.active {
    background: white;
    transform: scale(1.3);
}

.hero-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, rgba(0, 0, 0, 0.2) 0%, rgba(0, 0, 0, 0.5) 100%);
    z-index: 1;
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 820px;
    padding: 0 24px;
}

.badge-new {
    background: rgba(255, 255, 255, 0.18);
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 5px 15px;
    border-radius: 50px;
    display: inline-block;
    margin-bottom: 8px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    backdrop-filter: blur(4px);
}

.hero-content h1 {
    font-size: 1.8rem;
    font-weight: 800;
    margin-bottom: 6px;
    line-height: 1.1;
    text-shadow: 0 2px 15px rgba(0, 0, 0, 0.2);
}

.hero-content p {
    font-size: 0.85rem;
    margin-bottom: 14px;
    line-height: 1.5;
    font-weight: 500;
    opacity: 0.95;
}

.hero-actions {
    display: flex;
    gap: 14px;
    justify-content: center;
}

.btn-start {
    background: #3498db;
    color: white;
    border: none;
    padding: 8px 24px;
    border-radius: 50px;
    font-size: 0.82rem;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
    transition: 0.3s;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'Inter', sans-serif;
}

.btn-start:hover {
    background: #2980b9;
    transform: translateY(-4px);
    box-shadow: 0 14px 30px rgba(0, 0, 0, 0.3);
}

.btn-outline {
    background: rgba(255, 255, 255, 0.15);
    border: 1.5px solid rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(4px);
}

.btn-outline:hover {
    background: rgba(255, 255, 255, 0.28);
}

/* ─── Featured Section ─── */
.featured-section {
    padding: 80px 20px;
    background: #f8fafc;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 40px;
}

.section-eyebrow {
    font-size: 0.82rem;
    font-weight: 700;
    color: #3498db;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 6px;
}

.section-header h2 {
    font-size: 2.1rem;
    font-weight: 800;
    color: #1e293b;
    margin: 0;
}

.btn-view-all {
    background: none;
    border: none;
    color: #3498db;
    font-weight: 700;
    cursor: pointer;
    font-size: 0.92rem;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: 0.2s;
    font-family: 'Inter', sans-serif;
}

.btn-view-all:hover {
    gap: 10px;
    color: #2980b9;
}

/* Trip Planner Banner */
.trip-planner-banner {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    border-radius: 16px;
    padding: 18px 20px;
    display: flex;
    align-items: center;
    gap: 15px;
    color: white;
    cursor: pointer;
    transition: 0.3s;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
    margin-bottom: 20px;
}

.trip-planner-banner:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
}

.banner-icon {
    background: rgba(255, 255, 255, 0.2);
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
}

.banner-text h3 {
    margin: 0 0 4px;
    font-size: 1rem;
    font-weight: 800;
}

.banner-text p {
    margin: 0;
    font-size: 0.8rem;
    opacity: 0.9;
}

.arrow-icon {
    margin-left: auto;
    font-size: 1.1rem;
}

.mt-20 {
    margin-top: 20px;
}

/* ─── Cards ─── */
.featured-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 28px;
}

.place-card,
.ta-card {
    position: relative;
    background: #0f172a;
    border-radius: 4px;
    overflow: hidden;
    height: 480px;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    border: none;
    display: flex;
    flex-direction: column;
}

.ta-card {
    flex: 0 0 320px;
}

.place-card:hover,
.ta-card:hover {
    transform: translateY(-5px) scale(1.01);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.ai-card {
    border: 2px solid #8b5cf6;
}

.ai-badge {
    position: absolute;
    top: 10px;
    left: 10px;
    background: linear-gradient(135deg, #8b5cf6, #6d28d9);
    color: white;
    padding: 4px 10px;
    border-radius: 50px;
    font-size: 0.72rem;
    font-weight: 700;
    box-shadow: 0 2px 8px rgba(109, 40, 217, 0.4);
}

.ai-reason {
    font-size: 0.78rem;
    color: #8b5cf6;
    margin: 6px 0 0;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 5px;
}

.interest-card {
    border: 2px solid #f59e0b;
}

.interest-badge {
    position: absolute;
    top: 10px;
    left: 10px;
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: white;
    padding: 4px 10px;
    border-radius: 50px;
    font-size: 0.72rem;
    font-weight: 700;
    box-shadow: 0 2px 8px rgba(217, 119, 6, 0.4);
}

.card-img-wrapper {
    position: absolute;
    inset: 0;
    height: 100%;
    overflow: hidden;
    z-index: 0;
}

.card-img-wrapper::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, 
        rgba(0,0,0,0) 0%, 
        rgba(0,0,0,0.2) 40%, 
        rgba(0,0,0,0.8) 80%, 
        rgba(0,0,0,0.95) 100%);
    z-index: 1;
}

.ta-card .card-img-wrapper {
    height: 100%;
}

.card-img-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
}

.place-card:hover .card-img-wrapper img,
.ta-card:hover .card-img-wrapper img {
    transform: scale(1.05);
}

.card-tag {
    position: relative;
    z-index: 2;
    display: inline-block;
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.65rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

.rating-pill {
    position: absolute;
    top: 14px;
    right: 14px;
    background: rgba(0, 0, 0, 0.55);
    color: white;
    padding: 5px 11px;
    border-radius: 50px;
    font-size: 0.78rem;
    font-weight: 700;
    backdrop-filter: blur(4px);
}

.rank-badge {
    position: absolute;
    top: 10px;
    left: 10px;
    background: #000;
    color: white;
    padding: 4px 10px;
    font-size: 0.75rem;
    font-weight: 800;
    border-radius: 6px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.btn-heart {
    position: absolute;
    top: 10px;
    right: 10px;
    background: rgba(255, 255, 255, 0.9);
    border: none;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    color: #94a3b8;
    transition: 0.2s;
    z-index: 50;
}

.btn-heart.active {
    color: #ef4444;
}

.btn-heart:hover {
    transform: scale(1.1);
}

.card-body,
.card-info {
    position: relative;
    z-index: 2;
    padding: 30px 24px;
    margin-top: auto;
    color: white;
    display: flex;
    flex-direction: column;
    height: 100%;
    justify-content: flex-end;
}

.card-info {
    padding: 24px;
}

.card-body h3,
.card-info h3 {
    margin: 0 0 8px;
    font-size: 1.4rem;
    font-weight: 800;
    font-family: 'Playfair Display', serif;
    color: white;
    letter-spacing: -0.5px;
    line-height: 1.1;
}

.truncate {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.desc,
.description {
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.9rem;
    line-height: 1.5;
    margin-bottom: 20px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 15px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    margin-top: 5px;
}

.location-tag {
    color: rgba(255, 255, 255, 0.5);
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.btn-detail {
    color: white;
    font-weight: 800;
    font-size: 0.75rem;
    letter-spacing: 1px;
    transition: 0.2s;
}

.place-card:hover .btn-detail {
    color: #3b82f6;
}

.rating-row {
    display: flex;
    align-items: center;
    margin-bottom: 6px;
}

.rating-num {
    font-size: 0.9rem;
    font-weight: 700;
    margin-left: 6px;
}

.cat-text {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0;
}

/* --- Main Layout --- */
.main-container {
    max-width: 1700px;
    width: 96%;
    margin: 0 auto;
    padding: 40px 15px;
    position: relative;
    z-index: 10;
}

.horizontal-section {
    margin-bottom: 50px;
}

.carousel-container {
    display: flex;
    overflow-x: auto;
    gap: 20px;
    padding-bottom: 20px;
    scroll-snap-type: x mandatory;
    scrollbar-width: thin;
    scrollbar-color: #cbd5e1 transparent;
}

.carousel-container::-webkit-scrollbar {
    height: 8px;
}

.carousel-container::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 10px;
}

/* --- Explore All Section --- */
.mt-50 {
    margin-top: 50px;
    scroll-margin-top: 100px;
}

.mb-10 {
    margin-bottom: 10px;
}

.explore-layout {
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: 30px;
    margin-top: 20px;
    align-items: start;
}

.sidebar {
    position: sticky;
    top: 90px;
    height: fit-content;
    max-height: calc(100vh - 100px);
    overflow-y: auto;
    padding-right: 8px; /* space for scrollbar */
}

.sidebar::-webkit-scrollbar {
    width: 6px;
}
.sidebar::-webkit-scrollbar-thumb {
    background: #e2e8f0;
    border-radius: 10px;
}

.filter-card {
    background: white;
    padding: 28px 24px;
    border-radius: 20px;
    border: 1px solid #f1f5f9;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05);
    color: #1e293b;
}

.filter-card h3 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 800;
}

.filter-card h4 {
    margin: 15px 0 10px;
    font-size: 0.95rem;
    font-weight: 700;
    color: #475569;
}

.mt-15 {
    margin-top: 15px;
}

.input-with-icon {
    position: relative;
    display: flex;
    align-items: center;
}

.input-with-icon i {
    position: absolute;
    left: 16px;
    color: #64748b;
    font-size: 1.1rem;
    transition: color 0.3s ease;
}

.input-with-icon input {
    width: 100%;
    padding: 12px 16px 12px 42px;
    border: 2px solid transparent;
    border-radius: 12px;
    font-size: 0.95rem;
    background: #f1f5f9;
    outline: none;
    transition: all 0.3s ease;
}

.input-with-icon input:focus {
    border-color: #3498db;
    background: white;
    box-shadow: 0 0 0 4px rgba(52, 152, 219, 0.1);
}

.category-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.cat-pill {
    width: 100%;
    text-align: left;
    padding: 12px 18px;
    border-radius: 12px;
    border: 1px solid transparent;
    background: transparent;
    color: #475569;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.cat-pill:hover {
    background: #f1f5f9;
    color: #0f172a;
    transform: translateX(4px);
}

.cat-pill.active {
    background: #eff6ff;
    color: #2563eb;
    border: 1px solid #bfdbfe;
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.05);
    transform: translateX(4px);
}

.cat-pill.active::after {
    content: '✓';
    font-weight: bold;
    color: #2563eb;
    font-size: 1.1rem;
}

.show-more-btn {
    justify-content: center;
    color: #3b82f6;
    font-weight: 700;
    background: transparent;
    border: 1px dashed #bfdbfe;
}
.show-more-btn:hover {
    background: #eff6ff;
    color: #2563eb;
    transform: none;
}

.btn-clear {
    width: 100%;
    padding: 12px;
    margin-top: 25px;
    background: #f8fafc;
    border: 1px dashed #cbd5e1;
    border-radius: 12px;
    font-weight: 700;
    color: #64748b;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-clear:hover {
    background: #f1f5f9;
    border-color: #94a3b8;
    color: #334155;
}

.results-bar {
    margin-bottom: 20px;
    font-size: 1.1rem;
    color: #1e293b;
}

.places-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 25px;
}

.list-card {
    flex: none;
}

/* ─── 🚨 History Section CSS 🚨 ─── */
/* ─── 🚨 Heritage Section (Beautified) 🚨 ─── */
.heritage-section {
    background-color: #ffffff;
    padding: 100px 20px;
    border-top: 1px solid #f1f5f9;
    position: relative;
    overflow: hidden;
}

.heritage-container {
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 80px;
    align-items: center;
}

.heritage-images {
    position: relative;
    width: 100%;
}

.heritage-main-img {
    width: 95%;
    height: 550px;
    object-fit: cover;
    border-radius: 24px;
    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.12);
    transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.heritage-images:hover .heritage-main-img {
    transform: scale(1.02);
}

.heritage-float-img {
    position: absolute;
    bottom: -40px;
    right: -20px;
    width: 55%;
    height: 280px;
    border-radius: 20px;
    overflow: hidden;
    border: 10px solid white;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.heritage-images:hover .heritage-float-img {
    transform: translateY(-10px) rotate(2deg);
}

.heritage-float-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.heritage-content {
    padding-left: 20px;
}

.heritage-title {
    font-size: 2.8rem;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.2;
    margin-bottom: 24px;
    font-family: 'Playfair Display', serif; /* Elegant title font */
}

.heritage-desc {
    font-size: 1.1rem;
    color: #475569;
    line-height: 1.8;
    margin-bottom: 20px;
    font-weight: 400;
}

.heritage-highlights {
    list-style: none;
    padding: 0;
    margin-top: 40px;
    display: flex;
    flex-direction: column;
    gap: 25px;
}

.heritage-highlights li {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 15px;
    border-radius: 16px;
    transition: all 0.3s ease;
    border: 1px solid transparent;
}

.heritage-highlights li:hover {
    background: #f8fafc;
    border-color: #e2e8f0;
    transform: translateX(10px);
}

.highlight-icon {
    width: 54px;
    height: 54px;
    background: #f1f5f9;
    color: #00aa6c; /* Consistent brand color */
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    flex-shrink: 0;
    transition: all 0.3s ease;
}

.heritage-highlights li:hover .highlight-icon {
    background: #00aa6c;
    color: white;
    transform: scale(1.1) rotate(-5deg);
}

.highlight-text strong {
    display: block;
    color: #0f172a;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 4px;
}

.highlight-text span {
    color: #64748b;
    font-size: 0.95rem;
    line-height: 1.5;
}

@media (max-width: 992px) {
    .heritage-container {
        grid-template-columns: 1fr;
        gap: 60px;
        text-align: center;
    }

    .heritage-main-img {
        width: 100%;
        height: 450px;
    }

    .heritage-float-img {
        width: 60%;
        right: 10px;
        bottom: -30px;
    }

    .heritage-content {
        padding-left: 0;
    }

    .heritage-title {
        font-size: 2.2rem;
    }
    
    .heritage-highlights li {
        justify-content: center;
        text-align: left;
    }
}

/* ─── CTA Section ─── */
.cta-section {
    background: linear-gradient(135deg, #1e5799 0%, #2989d8 50%, #207cca 100%);
    padding: 80px 20px;
    text-align: center;
    color: white;
}

.cta-content h2 {
    font-size: 2.4rem;
    font-weight: 800;
    margin: 0 0 14px;
}

.cta-content p {
    font-size: 1.1rem;
    opacity: 0.88;
    margin-bottom: 32px;
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
}

.btn-cta {
    background: white;
    color: #1e5799;
    border: none;
    padding: 16px 42px;
    border-radius: 50px;
    font-size: 1rem;
    font-weight: 800;
    cursor: pointer;
    transition: 0.3s;
    font-family: 'Inter', sans-serif;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.btn-cta:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 32px rgba(0, 0, 0, 0.25);
}

/* ─── Skeletons & Loaders ─── */
.placeholder-card {
    background: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.skeleton-img {
    width: 100%;
    height: 220px;
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: shimmer 1.4s infinite;
}

.skeleton-body {
    padding: 22px;
}

.skeleton-title {
    width: 60%;
    height: 18px;
    background: #eee;
    border-radius: 6px;
    margin-bottom: 12px;
    animation: shimmer 1.4s infinite;
}

.skeleton-text {
    width: 100%;
    height: 13px;
    background: #f5f5f5;
    border-radius: 6px;
    animation: shimmer 1.4s infinite;
}

@keyframes shimmer {
    0% {
        background-position: -200% 0;
    }

    100% {
        background-position: 200% 0;
    }
}

.loading-state,
.empty-state {
    text-align: center;
    padding: 100px 0;
    color: #64748b;
}

.spinner {
    border: 4px solid #e2e8f0;
    border-top: 4px solid #000;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}



@media (max-width: 992px) {
    .explore-layout {
        grid-template-columns: 1fr;
    }

    .sidebar {
        position: relative;
        top: 0;
        margin-bottom: 20px;
    }
}

@media (max-width: 768px) {
    .hero-content h1 {
        font-size: 1.8rem;
    }

    .hero-content p {
        font-size: 0.9rem;
        margin-bottom: 20px;
    }
}

</style>