<template>
    <div class="detail-page">
        <Navbar />

        <div class="detail-content-container" v-if="place">
            <button @click="router.back()" class="btn-back-link">
                <i class="fas fa-chevron-left"></i> Back
            </button>

            <div class="top-split-layout">
                <div class="place-visual-card">
                    <div class="image-gallery-container">
                        <div class="image-wrapper">
                            <img :src="galleryImages[currentImageIndex]" class="place-img clickable-img" alt="Place Image" @click="openLightbox" />
                            <div class="cat-tag">{{ getCategoryName(place.category_id) }}</div>
                            <button v-if="user && user.role !== 'admin'"
                                :class="['btn-heart-lg', { active: isFavorite }]" @click="toggleHeart">
                                <i class="fas fa-heart"></i>
                            </button>
                            <div class="zoom-hint" @click="openLightbox">
                                <i class="fas fa-search-plus"></i>
                            </div>
                        </div>
                        
                        <div class="thumbnails-container" v-if="galleryImages.length > 1">
                            <img v-for="(img, index) in galleryImages" :key="index"
                                :src="img" 
                                :class="['thumb-img', { active: currentImageIndex === index }]"
                                @click="currentImageIndex = index" alt="Thumbnail" />
                        </div>
                    </div>

                    <div class="place-header-info">
                        <div>
                            <h1>{{ place.name }}</h1>
                            <p class="place-location"><i class="fas fa-map-marker-alt"></i> Savannakhet, Laos</p>
                        </div>
                        <div class="rating-badge">
                            <i class="fas fa-star"></i>
                            <span>{{ place.rating_avg || '0.0' }}</span>
                            <small>({{ comments.length }} reviews)</small>
                        </div>
                    </div>
                </div>

                <div class="comment-sidebar">
                    <div class="glass-card">
                        <div class="review-form-section" v-if="user && user.role !== 'admin'">
                            <h3><i class="fas fa-pen"></i> Write a Review</h3>
                            <p class="review-sub">Share your experience at this place</p>

                            <div class="star-picker">
                                <span class="star-label">Your Rating:</span>
                                <div class="stars">
                                    <i v-for="star in 5" :key="star"
                                        :class="[newRating >= star ? 'fas' : 'far', 'fa-star']"
                                        @click="newRating = star"></i>
                                </div>
                                <span class="rating-text">{{ ratingLabels[newRating - 1] }}</span>
                            </div>

                            <textarea v-model="newComment"
                                placeholder="Tell others what you think about this place..."></textarea>

                            <button class="btn-send-review" @click="submitComment" :disabled="submitting">
                                <i class="fas fa-paper-plane"></i>
                                {{ submitting ? 'Submitting...' : 'Submit Review' }}
                            </button>

                            <p v-if="reviewSuccess" class="review-success-msg">
                                <i class="fas fa-check-circle"></i> Review submitted successfully!
                            </p>
                        </div>

                        <div v-else-if="!user" class="login-prompt">
                            <i class="fas fa-user-circle"></i>
                            <p>Sign in to write a review</p>
                            <router-link to="/login" class="btn-login-prompt">Sign In</router-link>
                        </div>

                        <div class="divider-line"></div>

                        <div class="review-history">
                            <p class="history-title">
                                <i class="fas fa-comments"></i>
                                Traveler Reviews
                                <span class="review-count">{{ comments.length }}</span>
                            </p>
                            <div class="scroll-comments">
                                <div v-if="comments.length === 0" class="no-comments-msg">
                                    <i class="fas fa-comment-slash"></i>
                                    <p>No reviews yet. Be the first!</p>
                                </div>
                                <div v-for="comment in comments" :key="comment.id" class="mini-comment-item">
                                    <div class="u-info">
                                        <div class="u-avatar">{{ comment.username?.charAt(0).toUpperCase() }}</div>
                                        <div class="u-meta">
                                            <strong>{{ comment.username }}</strong>
                                            <span class="u-stars">
                                                <i v-for="s in 5" :key="s"
                                                    :class="[comment.rating >= s ? 'fas' : 'far', 'fa-star']"></i>
                                            </span>
                                        </div>
                                    </div>
                                    <p class="comment-text">{{ comment.comment_text }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="bottom-details-card">
                <section class="desc-section">
                    <h2 class="section-h"><i class="fas fa-info-circle"></i> About this place</h2>
                    <p class="text-desc">{{ place.description }}</p>
                </section>

                <section class="map-section">
                    <h2 class="section-h"><i class="fas fa-map-marked-alt"></i> Location & Map</h2>
                    <div class="map-frame-container">
                        <iframe width="100%" height="420" frameborder="0"
                            style="border:0; border-radius: 16px;"
                            :src="`https://www.google.com/maps?q=$${place.location_lat},${place.location_lng}&output=embed`"
                            allowfullscreen>
                        </iframe>
                    </div>
                    <button class="btn-open-google" @click="openMap">
                        <i class="fab fa-google"></i> Open in Google Maps
                    </button>
                </section>
            </div>
        </div>

        <div v-else class="loading-screen">
            <div class="loader"></div>
            <p>Loading place details...</p>
        </div>

        <div v-if="isLightboxOpen" class="lightbox-overlay" @click="closeLightbox" @wheel.prevent="handleScrollZoom">
            <button class="btn-close-lightbox" @click="closeLightbox"><i class="fas fa-times"></i></button>
            
            <button v-if="galleryImages.length > 1" class="btn-nav prev" @click.stop="prevImage">
                <i class="fas fa-chevron-left"></i>
            </button>
            
            <img :src="galleryImages[currentImageIndex]" 
                 class="lightbox-img" 
                 :style="{ transform: `scale(${zoomLevel})` }"
                 @click.stop />
            
            <button v-if="galleryImages.length > 1" class="btn-nav next" @click.stop="nextImage">
                <i class="fas fa-chevron-right"></i>
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { placeRepository } from '@/repositories/placeRepository'
import { categoryRepository } from '@/repositories/categoryRepository'
import { favoriteRepository } from '@/repositories/favoriteRepository'
import Navbar from '@/components/Navbar.vue'

const route = useRoute()
const router = useRouter()
const place = ref(null)
const categories = ref([])
const comments = ref([])
const user = ref(JSON.parse(localStorage.getItem('user')))
const isFavorite = ref(false)
const reviewSuccess = ref(false)

const newComment = ref('')
const newRating = ref(5)
const submitting = ref(false)

const ratingLabels = ['Terrible', 'Poor', 'Average', 'Good', 'Excellent']

const currentImageIndex = ref(0)
const isLightboxOpen = ref(false)

// 🔍 State สำหรับเก็บค่าซูมเริ่มต้นที่ 1 เท่า (100%)
const zoomLevel = ref(1)

const galleryImages = computed(() => {
    const getValidImageUrl = (rawUrl) => {
        if (!rawUrl) return null;
        let url = rawUrl;
        if (typeof url === 'string' && url.trim().startsWith('[')) {
            try {
                const parsed = JSON.parse(url);
                if (Array.isArray(parsed) && parsed.length > 0) {
                    url = parsed[0]; 
                }
            } catch (e) {
                url = url.replace(/^\["?|"?\]$/g, '').replace(/\\"/g, '');
            }
        }
        if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) {
            return url;
        }
        return `http://localhost:8000${url.startsWith('/') ? '' : '/'}${url}`;
    }

    if (place.value?.images && Array.isArray(place.value.images) && place.value.images.length > 0) {
        return place.value.images.map(img => getValidImageUrl(img.image_url || img.url || img));
    } 
    else if (place.value?.image_url) {
        let parsedArray = [];
        if (typeof place.value.image_url === 'string' && place.value.image_url.trim().startsWith('[')) {
            try { parsedArray = JSON.parse(place.value.image_url); } catch(e){}
        }
        
        if (parsedArray.length > 0) {
            return parsedArray.map(img => getValidImageUrl(img));
        } else {
            return [getValidImageUrl(place.value.image_url)];
        }
    }

    return [
        'data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22800%22%20height%3D%22450%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20fill%3D%22%23e2e8f0%22%2F%3E%3Ctext%20x%3D%2250%25%22%20y%3D%2250%25%22%20fill%3D%22%2364748b%22%20font-family%3D%22sans-serif%22%20font-size%3D%2224%22%20text-anchor%3D%22middle%22%20dy%3D%22.3em%22%3ENo%20Image%20Available%3C%2Ftext%3E%3C%2Fsvg%3E'
    ]
})

// 🖱️ ฟังก์ชันรับ Event เลื่อนลูกกลิ้ง (Scroll Wheel) เพื่อซูม
const handleScrollZoom = (e) => {
    // กำหนดความเร็วในการซูมแต่ละครั้ง
    const zoomStep = 0.15; 
    
    if (e.deltaY < 0) {
        // เลื่อนขึ้น = ซูมเข้า (จำกัดให้ซูมสูงสุด 5 เท่า)
        zoomLevel.value = Math.min(zoomLevel.value + zoomStep, 5);
    } else {
        // เลื่อนลง = ซูมออก (จำกัดให้เล็กสุด 0.5 เท่า)
        zoomLevel.value = Math.max(zoomLevel.value - zoomStep, 0.5);
    }
}

const openLightbox = () => {
    isLightboxOpen.value = true
    zoomLevel.value = 1 // รีเซ็ตการซูมเมื่อเปิดใหม่
    document.body.style.overflow = 'hidden' 
}

const closeLightbox = () => {
    isLightboxOpen.value = false
    zoomLevel.value = 1 // รีเซ็ตการซูมเมื่อปิด
    document.body.style.overflow = 'auto' 
}

const nextImage = () => {
    zoomLevel.value = 1 // รีเซ็ตการซูมเมื่อเปลี่ยนรูป
    if (currentImageIndex.value < galleryImages.value.length - 1) {
        currentImageIndex.value++
    } else {
        currentImageIndex.value = 0 
    }
}

const prevImage = () => {
    zoomLevel.value = 1 // รีเซ็ตการซูมเมื่อเปลี่ยนรูป
    if (currentImageIndex.value > 0) {
        currentImageIndex.value--
    } else {
        currentImageIndex.value = galleryImages.value.length - 1 
    }
}

const handleKeydown = (e) => {
    if (!isLightboxOpen.value) return;
    if (e.key === 'Escape') closeLightbox()
    if (e.key === 'ArrowRight') nextImage()
    if (e.key === 'ArrowLeft') prevImage()
}

onMounted(() => {
    fetchData()
    window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeydown)
    document.body.style.overflow = 'auto' 
})

const fetchData = async () => {
    const id = route.params.id
    try {
        const [resPlace, resCats] = await Promise.all([
            placeRepository.getById(id),
            categoryRepository.getAll()
        ])
        place.value = resPlace.data
        categories.value = resCats.data

        if (user.value && user.value.role !== 'admin') {
            const favRes = await favoriteRepository.getUserFavorites(user.value.id)
            isFavorite.value = favRes.data.some(f => f.place_id === parseInt(id))
        }

        try {
            const resComm = await placeRepository.getComments(id)
            comments.value = resComm.data
        } catch (e) { comments.value = [] }
    } catch (err) { console.error(err) }
}

const submitComment = async () => {
    if (!user.value) return router.push('/login')
    if (!newComment.value.trim()) return

    submitting.value = true
    reviewSuccess.value = false
    try {
        await placeRepository.addComment(route.params.id, {
            user_id: user.value.id,
            rating: newRating.value,
            comment_text: newComment.value
        })
        newComment.value = ''
        newRating.value = 5
        reviewSuccess.value = true
        setTimeout(() => reviewSuccess.value = false, 3000)
        fetchData()
    } catch (err) {
        console.error('Submit failed:', err)
    } finally {
        submitting.value = false
    }
}

const toggleHeart = async () => {
    if (!user.value) return router.push('/login')
    try {
        const res = await favoriteRepository.toggleFavorite(user.value.id, route.params.id)
        isFavorite.value = res.data.status === 'added'
    } catch (err) {
        console.error('Failed to toggle favorite:', err)
    }
}

const getCategoryName = (id) => categories.value.find(c => c.id === id)?.name || 'General'
const openMap = () => window.open(`https://www.google.com/maps?q=$${place.value.location_lat},${place.value.location_lng}`, '_blank')
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.detail-page {
    background: linear-gradient(135deg, #1e5799 0%, #2989d8 50%, #207cca 100%);
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
}

.detail-content-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 30px 20px 60px;
}

.btn-back-link {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.2);
    border: none;
    color: white;
    padding: 10px 20px;
    border-radius: 50px;
    cursor: pointer;
    margin-bottom: 25px;
    font-weight: 600;
    font-size: 0.9rem;
    transition: 0.3s;
    font-family: 'Inter', sans-serif;
}

.btn-back-link:hover {
    background: rgba(255, 255, 255, 0.35);
    transform: translateX(-4px);
}

.top-split-layout {
    display: flex;
    gap: 28px;
    align-items: stretch;
    margin-bottom: 28px;
}

@media (max-width: 992px) {
    .top-split-layout { flex-direction: column; }
}

.place-visual-card {
    flex: 1.5;
    background: white;
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
}

.image-gallery-container {
    display: flex;
    flex-direction: column;
}

.image-wrapper {
    position: relative;
    height: 380px;
    background: #f1f5f9;
    overflow: hidden;
}

.clickable-img {
    cursor: zoom-in;
}
.clickable-img:hover {
    opacity: 0.95;
}

.zoom-hint {
    position: absolute;
    bottom: 15px;
    right: 15px;
    background: rgba(0,0,0,0.6);
    color: white;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
    backdrop-filter: blur(4px);
    transition: 0.3s;
}

.image-wrapper:hover .zoom-hint {
    transform: scale(1.1);
    background: rgba(0,0,0,0.8);
}

.place-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: opacity 0.3s ease-in-out;
}

.thumbnails-container {
    display: flex;
    gap: 12px;
    padding: 16px 28px 0;
    overflow-x: auto;
    scrollbar-width: none; 
    -ms-overflow-style: none;
}
.thumbnails-container::-webkit-scrollbar {
    display: none;
}

.thumb-img {
    width: 80px;
    height: 60px;
    object-fit: cover;
    border-radius: 10px;
    cursor: pointer;
    opacity: 0.5;
    transition: all 0.2s ease;
    border: 2px solid transparent;
}

.thumb-img:hover {
    opacity: 0.8;
}

.thumb-img.active {
    opacity: 1;
    border-color: #3498db;
    transform: scale(1.05);
}

.cat-tag {
    position: absolute;
    top: 18px;
    left: 18px;
    background: #3498db;
    color: white;
    padding: 6px 16px;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.btn-heart-lg {
    position: absolute;
    top: 18px;
    right: 18px;
    background: rgba(255,255,255,0.95);
    border: none;
    border-radius: 50%;
    width: 48px;
    height: 48px;
    font-size: 1.3rem;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    transition: 0.3s;
    color: #cbd5e1;
    z-index: 10;
}

.btn-heart-lg.active { color: #ef4444; }
.btn-heart-lg:hover { transform: scale(1.1); }

.place-header-info {
    padding: 24px 28px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
}

.place-header-info h1 {
    font-size: 1.9rem;
    margin: 0 0 6px;
    color: #1e293b;
    font-weight: 800;
}

.place-location {
    margin: 0;
    color: #64748b;
    font-size: 0.9rem;
}

.place-location i { color: #3498db; margin-right: 4px; }

.rating-badge {
    display: flex;
    align-items: center;
    gap: 6px;
    background: #fef9ee;
    border: 1px solid #fde68a;
    padding: 10px 18px;
    border-radius: 14px;
    white-space: nowrap;
}

.rating-badge i { color: #f59e0b; font-size: 1.1rem; }
.rating-badge span { font-size: 1.4rem; font-weight: 800; color: #1e293b; }
.rating-badge small { color: #94a3b8; font-size: 0.78rem; }

.comment-sidebar { flex: 1; }

.glass-card {
    background: rgba(255, 255, 255, 0.97);
    backdrop-filter: blur(10px);
    padding: 28px;
    border-radius: 24px;
    height: 100%;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
    box-sizing: border-box;
}

.review-form-section h3 {
    color: #1e293b;
    margin: 0 0 4px;
    font-size: 1.1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.review-form-section h3 i { color: #3498db; }

.review-sub {
    color: #94a3b8;
    font-size: 0.83rem;
    margin: 0 0 18px;
}

.star-picker {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
    flex-wrap: wrap;
}

.star-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #475569;
}

.stars i {
    font-size: 1.5rem;
    color: #f59e0b;
    cursor: pointer;
    transition: 0.15s;
}

.stars i:hover { transform: scale(1.15); }

.rating-text {
    font-size: 0.82rem;
    font-weight: 600;
    color: #64748b;
    background: #f1f5f9;
    padding: 3px 10px;
    border-radius: 50px;
}

textarea {
    width: 100%;
    height: 90px;
    padding: 12px 15px;
    border-radius: 12px;
    border: 1.5px solid #e2e8f0;
    background: #f8fafc;
    margin-bottom: 12px;
    resize: none;
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    box-sizing: border-box;
    transition: 0.2s;
}

textarea:focus { border-color: #3498db; outline: none; background: white; }

.btn-send-review {
    width: 100%;
    background: linear-gradient(135deg, #3498db, #2980b9);
    color: white;
    border: none;
    padding: 12px;
    border-radius: 12px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.3s;
    font-family: 'Inter', sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    box-shadow: 0 4px 12px rgba(52,152,219,0.3);
}

.btn-send-review:hover:not(:disabled) { transform: translateY(-2px); }
.btn-send-review:disabled { opacity: 0.6; cursor: not-allowed; }

.review-success-msg {
    color: #10b981;
    font-size: 0.85rem;
    font-weight: 600;
    text-align: center;
    margin-top: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
}

.login-prompt {
    text-align: center;
    padding: 20px 0;
    color: #94a3b8;
}

.login-prompt i { font-size: 2.5rem; margin-bottom: 8px; }
.login-prompt p { margin: 0 0 12px; font-size: 0.9rem; }

.btn-login-prompt {
    background: #3498db;
    color: white;
    padding: 9px 22px;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.88rem;
    transition: 0.2s;
}

.btn-login-prompt:hover { background: #2980b9; }

.divider-line {
    height: 1px;
    background: #f1f5f9;
    margin: 18px 0;
}

.history-title {
    font-weight: 700;
    color: #334155;
    margin: 0 0 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.95rem;
}

.history-title i { color: #3498db; }

.review-count {
    background: #3498db;
    color: white;
    font-size: 0.75rem;
    padding: 2px 8px;
    border-radius: 50px;
    font-weight: 600;
}

.scroll-comments {
    max-height: 240px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.no-comments-msg {
    text-align: center;
    color: #94a3b8;
    padding: 20px 0;
}

.no-comments-msg i { font-size: 1.5rem; margin-bottom: 6px; }
.no-comments-msg p { margin: 0; font-size: 0.88rem; }

.mini-comment-item {
    background: #f8fafc;
    padding: 12px 14px;
    border-radius: 12px;
    border: 1px solid #f1f5f9;
}

.u-info {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 6px;
}

.u-avatar {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #3498db, #2980b9);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 0.85rem;
    font-weight: 700;
    flex-shrink: 0;
}

.u-meta { display: flex; flex-direction: column; }
.u-meta strong { font-size: 0.88rem; color: #1e293b; }
.u-stars { color: #f59e0b; font-size: 0.68rem; }

.comment-text {
    margin: 0;
    font-size: 0.85rem;
    color: #475569;
    line-height: 1.5;
}

.bottom-details-card {
    background: white;
    border-radius: 24px;
    padding: 40px;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    gap: 36px;
}

.section-h {
    font-size: 1.2rem;
    color: #1e293b;
    margin: 0 0 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 700;
    padding-left: 14px;
    border-left: 4px solid #3498db;
}

.section-h i { color: #3498db; }

.text-desc {
    line-height: 1.8;
    color: #475569;
    font-size: 1rem;
    margin: 0;
}

.map-frame-container {
    overflow: hidden;
    border-radius: 16px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
    margin-bottom: 16px;
}

.btn-open-google {
    background: #2c3e50;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 12px;
    font-weight: 700;
    cursor: pointer;
    font-family: 'Inter', sans-serif;
    transition: 0.3s;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.btn-open-google:hover { background: #1e293b; transform: translateY(-2px); }

.loading-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 80vh;
    color: white;
    font-family: 'Inter', sans-serif;
}

.loader {
    border: 4px solid rgba(255, 255, 255, 0.3);
    border-top: 4px solid #fff;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
    margin-bottom: 20px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* 📸 Lightbox CSS */
.lightbox-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.9);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(10px);
}

/* 🔍 แก้ไข CSS รูปใน Lightbox ให้สมูทเวลาซูม */
.lightbox-img {
    max-width: 90%;
    max-height: 90vh;
    object-fit: contain;
    border-radius: 8px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    /* เพิ่ม transition เฉพาะตอนซูม (transform) เพื่อความลื่นไหล */
    transition: transform 0.15s ease-out; 
}

.btn-close-lightbox {
    position: absolute;
    top: 25px;
    right: 35px;
    background: none;
    border: none;
    color: white;
    font-size: 2rem;
    cursor: pointer;
    transition: 0.2s;
    opacity: 0.7;
}

.btn-close-lightbox:hover {
    opacity: 1;
    transform: scale(1.1);
}

.btn-nav {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(255,255,255,0.1);
    border: none;
    color: white;
    font-size: 2.5rem;
    cursor: pointer;
    padding: 15px 25px;
    border-radius: 12px;
    transition: 0.3s;
    backdrop-filter: blur(4px);
    z-index: 10; /* ให้ปุ่มอยู่เหนือรูปที่ขยายเสมอ */
}

.btn-nav:hover {
    background: rgba(255,255,255,0.25);
}

.btn-nav.prev { left: 30px; }
.btn-nav.next { right: 30px; }

@media (max-width: 768px) {
    .btn-nav { font-size: 1.5rem; padding: 10px 15px; }
    .btn-nav.prev { left: 10px; }
    .btn-nav.next { right: 10px; }
    .btn-close-lightbox { top: 15px; right: 20px; font-size: 1.8rem; }
}
</style>