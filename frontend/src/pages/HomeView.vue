<template>
    <div class="home-page">
        <Navbar />

        <header class="hero">
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <div class="badge-new">✨ AI-Powered Recommendation System</div>
                <h1>Discover Savannakhet</h1>
                <p>Experience the beauty of Southern Laos with our intelligent GNN travel guide.</p>
                <div class="hero-actions">
                    <button @click="router.push('/explore')" class="btn-start">
                        <i class="fas fa-rocket"></i> Start Exploring
                    </button>
                    <button @click="router.push('/register')" class="btn-start btn-outline">
                        <i class="fas fa-user-plus"></i> Join Free
                    </button>
                </div>
            </div>
        </header>

        <div class="stats-bar">
            <div class="stat-item">
                <span class="stat-num">50+</span>
                <span class="stat-label">Places</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
                <span class="stat-num">AI</span>
                <span class="stat-label">Powered</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
                <span class="stat-num">Free</span>
                <span class="stat-label">Forever</span>
            </div>
        </div>

        <section class="featured-section">
            <div class="container">
                <div class="section-header">
                    <div>
                        <p class="section-eyebrow">Handpicked for you</p>
                        <h2>Featured Places</h2>
                    </div>
                    <button @click="router.push('/explore')" class="btn-view-all">
                        View All <i class="fas fa-arrow-right"></i>
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
                                <span class="btn-detail">View <i class="fas fa-arrow-right"></i></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="cta-section">
            <div class="cta-content">
                <h2>Ready to Explore?</h2>
                <p>Create a free account to save favorites and get personalized recommendations.</p>
                <button @click="router.push('/register')" class="btn-cta">
                    <i class="fas fa-user-plus"></i> Get Started — It's Free
                </button>
            </div>
        </section>

        <footer class="simple-footer">
            <p>🌴 Savannakhet Smart Travel &copy; 2026 — Powered by GNN Recommendation</p>
        </footer>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { placeRepository } from '@/repositories/placeRepository'
import { categoryRepository } from '@/repositories/categoryRepository'
import Navbar from '../components/Navbar.vue'

const router = useRouter()
const featuredPlaces = ref([])
const categories = ref([])
const loading = ref(true)

// 📷 ฟังก์ชันจัดการปกรูปภาพ (เหมือนหน้า Explore)
const getCoverImage = (place) => {
    const noImageUrl = 'data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22400%22%20height%3D%22300%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20fill%3D%22%23e2e8f0%22%2F%3E%3Ctext%20x%3D%2250%25%22%20y%3D%2250%25%22%20fill%3D%22%2364748b%22%20font-family%3D%22sans-serif%22%20font-size%3D%2220%22%20text-anchor%3D%22middle%22%20dy%3D%22.3em%22%3ENo%20Image%3C%2Ftext%3E%3C%2Fsvg%3E';

    let targetUrl = null;

    if (place.images && Array.isArray(place.images) && place.images.length > 0) {
        targetUrl = place.images[0].image_url || place.images[0].url || place.images[0];
    } else if (place.image_url) {
        targetUrl = place.image_url;
    }

    if (!targetUrl) return noImageUrl;

    // ดักจับ JSON Array ซ้อน String
    if (typeof targetUrl === 'string' && targetUrl.trim().startsWith('[')) {
        try {
            const parsed = JSON.parse(targetUrl);
            if (Array.isArray(parsed) && parsed.length > 0) {
                targetUrl = parsed[0];
            }
        } catch (e) {
            targetUrl = targetUrl.replace(/^\["?|"?\]$/g, '').replace(/\\"/g, '');
        }
    }

    if (targetUrl.startsWith('http://') || targetUrl.startsWith('https://') || targetUrl.startsWith('data:')) {
        return targetUrl;
    }

    return `http://localhost:8000${targetUrl.startsWith('/') ? '' : '/'}${targetUrl}`;
}

const fetchData = async () => {
    try {
        const [resPlaces, resCats] = await Promise.all([
            placeRepository.getAll(),
            categoryRepository.getAll()
        ])
        featuredPlaces.value = resPlaces.data.slice(0, 3)
        categories.value = resCats.data
    } catch (error) {
        console.error('Error fetching home data:', error)
    } finally {
        loading.value = false
    }
}

const getCategoryName = (id) => {
    const cat = categories.value.find(c => c.id === id)
    return cat ? cat.name : 'General'
}

onMounted(fetchData)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.home-page {
    font-family: 'Inter', sans-serif;
}

/* ─── Hero ─── */
.hero {
    position: relative;
    background: url('https://images.unsplash.com/photo-1540611025311-01df3cef54b5?q=80&w=2070') center/cover;
    min-height: 580px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: white;
}

.hero-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(30, 87, 153, 0.88), rgba(32, 124, 202, 0.82));
}

.hero-content {
    position: relative;
    z-index: 1;
    max-width: 820px;
    padding: 0 24px;
}

.badge-new {
    background: rgba(255, 255, 255, 0.18);
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 7px 18px;
    border-radius: 50px;
    display: inline-block;
    margin-bottom: 22px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    backdrop-filter: blur(4px);
}

.hero-content h1 {
    font-size: 3.8rem;
    font-weight: 800;
    margin-bottom: 16px;
    line-height: 1.15;
    text-shadow: 0 2px 20px rgba(0,0,0,0.2);
}

.hero-content p {
    font-size: 1.15rem;
    opacity: 0.9;
    margin-bottom: 36px;
    line-height: 1.6;
}

.hero-actions {
    display: flex;
    gap: 14px;
    justify-content: center;
    flex-wrap: wrap;
}

.btn-start {
    background: #3498db;
    color: white;
    border: none;
    padding: 15px 38px;
    border-radius: 50px;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
    transition: 0.3s;
    display: inline-flex;
    align-items: center;
    gap: 9px;
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

/* ─── Stats Bar ─── */
.stats-bar {
    background: white;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 48px;
    padding: 22px 40px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}

.stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.stat-num {
    font-size: 1.6rem;
    font-weight: 800;
    color: #3498db;
    line-height: 1;
}

.stat-label {
    font-size: 0.78rem;
    color: #94a3b8;
    font-weight: 500;
    margin-top: 3px;
}

.stat-divider {
    width: 1px;
    height: 36px;
    background: #e2e8f0;
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

/* ─── Grid & Cards ─── */
.featured-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 28px;
}

.place-card {
    background: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    transition: all 0.3s ease;
    cursor: pointer;
    border: 1px solid #f1f5f9;
}

.place-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
}

.card-img-wrapper {
    position: relative;
    height: 220px;
    overflow: hidden;
}

.card-img-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
}

.place-card:hover .card-img-wrapper img {
    transform: scale(1.05);
}

.card-tag {
    position: absolute;
    top: 14px;
    left: 14px;
    background: #3498db;
    color: white;
    padding: 5px 13px;
    border-radius: 50px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.3px;
}

.rating-pill {
    position: absolute;
    top: 14px;
    right: 14px;
    background: rgba(0,0,0,0.55);
    color: white;
    padding: 5px 11px;
    border-radius: 50px;
    font-size: 0.78rem;
    font-weight: 700;
    backdrop-filter: blur(4px);
}

.card-body {
    padding: 22px 24px;
}

.card-body h3 {
    margin: 0 0 8px;
    color: #1e293b;
    font-size: 1.1rem;
    font-weight: 700;
}

.desc {
    color: #64748b;
    font-size: 0.85rem;
    line-height: 1.6;
    margin-bottom: 16px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    min-height: 2.7em;
}

.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 14px;
    border-top: 1px solid #f1f5f9;
}

.location-tag {
    color: #94a3b8;
    font-size: 0.78rem;
    display: flex;
    align-items: center;
    gap: 5px;
}

.location-tag i { color: #3498db; }

.btn-detail {
    color: #3498db;
    font-weight: 700;
    font-size: 0.83rem;
    display: flex;
    align-items: center;
    gap: 5px;
    transition: 0.2s;
}

.place-card:hover .btn-detail {
    gap: 8px;
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
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}

.btn-cta:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 32px rgba(0,0,0,0.25);
}

/* ─── Skeleton ─── */
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
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

/* ─── Footer ─── */
.simple-footer {
    text-align: center;
    padding: 32px 40px;
    color: #94a3b8;
    border-top: 1px solid #e2e8f0;
    font-size: 0.88rem;
    background: white;
}
</style>