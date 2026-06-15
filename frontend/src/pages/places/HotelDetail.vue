<template>
    <div class="ta-hotel-detail">
        <!-- Removed standard Navbar for immersive experience -->

        <div v-if="hotel">
            <div class="premium-hero-wrapper">
                <header class="premium-hero" :style="{ backgroundImage: `url(${galleryImages[0]})` }">
                    <div class="hero-overlay"></div>

                    <!-- Immersive Hero Navbar -->
                    <nav class="hero-nav">
                        <div class="nav-left">
                            <div class="logo" @click="router.push('/')">
                                <span class="logo-main">Savannakhet</span><span class="logo-sub">.travel</span>
                            </div>
                        </div>
                        <div class="nav-right">
                            <div class="nav-items">
                                <a @click="router.push('/landmarks')">{{ t('nav.destinations') }}</a>
                                <a @click="router.push('/trip-planner')">{{ t('nav.tools') }}</a>
                                <a @click="router.push('/hotels')">{{ t('nav.hotels') }}</a>
                                <a @click="router.push('/nature')">{{ t('nav.nature') }}</a>
                            </div>
                            <button class="btn-plan" @click="router.push('/trip-planner')">{{ t('nav.planYourTrip') }}</button>
                        </div>
                    </nav>

                    <div class="hero-content">
                        <div class="top-row">
                            <button @click="router.back()" class="btn-back-minimal">
                                <i class="fas fa-chevron-left"></i>
                            </button>
                            <div class="breadcrumb">SAVANNAKHET HOTELS › {{ hotel.name }}</div>
                        </div>

                        <div class="hero-main-info">
                            <h1 class="serif-title">{{ hotel.name }}</h1>
                            <p class="local-name">Luxury Stay in Savannakhet</p>
                            <p class="hero-description">{{ hotel.description }}</p>
                        </div>
                    </div>
                </header>

                <div class="stats-bar" v-if="hotel.best_months || hotel.ideal_stay || hotel.daily_budget || hotel.location_name">
                    <div class="stat-item" v-if="hotel.best_months">
                        <label>CHECK-IN / BEST MONTHS</label>
                        <div class="stat-value">{{ hotel.best_months }}</div>
                    </div>
                    <div class="stat-item" v-if="hotel.ideal_stay">
                        <label>IDEAL STAY</label>
                        <div class="stat-value">{{ hotel.ideal_stay }}</div>
                    </div>
                    <div class="stat-item" v-if="hotel.daily_budget">
                        <label>{{ t('place.daily_budget') }}</label>
                        <div class="stat-value">
                            {{ hotel.daily_budget }}
                        </div>
                    </div>
                    <div class="stat-item" v-if="hotel.location_name">
                        <label>LOCATION</label>
                        <div class="stat-value">{{ hotel.location_name }}</div>
                    </div>
                </div>

                <div class="tags-container" v-if="(hotel.best_for && hotel.best_for.length > 0) || (hotel.avoid_if && hotel.avoid_if.length > 0)">
                    <div class="tag-column best-for" v-if="hotel.best_for && hotel.best_for.length > 0">
                        <label>AMENITIES / BEST FOR</label>
                        <div class="tag-list">
                            <span v-for="(tag, idx) in hotel.best_for" :key="'bf-'+idx" class="tag">{{ tag }}</span>
                        </div>
                    </div>
                    <div class="tag-column avoid-if" v-if="hotel.avoid_if && hotel.avoid_if.length > 0">
                        <label>GOOD TO KNOW / AVOID IF</label>
                        <div class="tag-list">
                            <span v-for="(tag, idx) in hotel.avoid_if" :key="'ai-'+idx" class="tag">{{ tag }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="container-main">
                <div class="gallery-preview-strip" @click="openLightbox">
                <div v-for="(img, idx) in galleryImages.slice(0, 4)" :key="'strip-'+idx" class="strip-item">
                    <img :src="img" alt="Gallery preview" />
                </div>
                <div v-if="galleryImages.length > 4" class="more-indicator">+{{ galleryImages.length - 4 }}</div>
            </div>


                <!-- Sticky Navigation -->
            <div class="sticky-nav-wrapper" ref="stickyNavRef">
                <div class="sticky-nav" :class="{ 'is-sticky': isSticky }">
                    <div class="nav-links">
                        <a href="#deals" :class="{ active: activeSection === 'deals' }" @click.prevent="scrollTo('deals')">{{ t('place.deals') }}</a>
                        <a href="#about" :class="{ active: activeSection === 'about' }" @click.prevent="scrollTo('about')">{{ t('place.about') }}</a>
                        <a href="#location" :class="{ active: activeSection === 'location' }" @click.prevent="scrollTo('location')">{{ t('place.location') }}</a>
                        <a href="#reviews" :class="{ active: activeSection === 'reviews' }" @click.prevent="scrollTo('reviews')">{{ t('place.reviews') }}</a>
                    </div>
                    <div class="nav-action" v-if="isSticky">
                        <button class="btn-check-availability" @click="scrollTo('deals')">{{ t('hotels.check_availability') }}</button>
                    </div>
                </div>
            </div>

            <div class="content-layout">
                <div class="left-col">
                    <section class="about-hotel" id="about">
                        <h2>{{ t('place.about') }}</h2>
                        <p class="hotel-desc">{{ hotel.description }}</p>
                    </section>

                    <div class="amenities-box">
                        <h3>{{ t('hotels.amenities') }}</h3>
                        <div class="amenities-grid">
                            <div class="amenity-item"><i class="fas fa-parking"></i> Free parking</div>
                            <div class="amenity-item"><i class="fas fa-wifi"></i> Free High Speed Internet (WiFi)</div>
                            <div class="amenity-item"><i class="fas fa-swimming-pool"></i> Pool</div>
                            <div class="amenity-item"><i class="fas fa-dumbbell"></i> Fitness Center</div>
                            <div class="amenity-item"><i class="fas fa-utensils"></i> Restaurant</div>
                            <div class="amenity-item"><i class="fas fa-snowflake"></i> Air conditioning</div>
                        </div>
                    </div>

                    <hr class="divider-line" />

                    <section class="reviews-section" id="reviews">
                        <h2>Reviews ({{ comments?.length || 0 }})</h2>
                        
                        <div class="write-review-card" v-if="user">
                            <div class="u-avatar">{{ user.username.charAt(0) }}</div>
                            <div class="form-body">
                                <strong>Rate your stay:</strong>
                                <div class="star-picker">
                                    <i v-for="s in 5" :key="s" @click="newRating = s" :class="[newRating >= s ? 'fas' : 'far', 'fa-circle']"></i>
                                </div>
                                <textarea v-model="newComment" placeholder="Write about your experience..."></textarea>
                                <button class="btn-submit" @click="submitComment" :disabled="submitting">Submit Review</button>
                            </div>
                        </div>

                        <div class="review-list">
                            <div v-for="comment in comments" :key="comment.id" class="review-item">
                                <div class="reviewer">
                                    <div class="r-avatar">{{ comment.username.charAt(0) }}</div>
                                    <div style="flex-grow: 1; display: flex; justify-content: space-between; align-items: center;">
                                        <div>
                                            <strong>{{ comment.username }}</strong>
                                            <div class="r-rating" v-if="editingCommentId !== comment.id">
                                                <i v-for="s in 5" :key="s" :class="[comment.rating >= s ? 'fas' : 'far', 'fa-circle']"></i>
                                            </div>
                                        </div>
                                        <div class="review-actions" v-if="user && user.username === comment.username" style="position: relative;">
                                            <button @click="toggleDropdown(comment.id)" style="background: none; border: none; cursor: pointer; color: #64748b; padding: 5px; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; transition: background 0.2s;">
                                                <i class="fas fa-ellipsis-h"></i>
                                            </button>
                                            <div v-if="showDropdownFor === comment.id" style="position: absolute; right: 0; top: 100%; background: white; border: 1px solid #e2e8f0; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); z-index: 10; min-width: 120px; overflow: hidden;">
                                                <button @click="startEdit(comment)" style="display: block; width: 100%; text-align: left; padding: 10px 15px; background: none; border: none; cursor: pointer; font-size: 0.9rem; color: #1e293b; transition: background 0.2s;">
                                                    <i class="fas fa-pen" style="margin-right: 8px; color: #64748b;"></i> Edit
                                                </button>
                                                <button @click="deleteReview(comment.id)" style="display: block; width: 100%; text-align: left; padding: 10px 15px; background: none; border: none; cursor: pointer; font-size: 0.9rem; color: #ef4444; transition: background 0.2s;">
                                                    <i class="fas fa-trash" style="margin-right: 8px;"></i> Delete
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div v-if="editingCommentId === comment.id" class="edit-comment-area" style="margin-top: 10px; background: #f8fafc; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0;">
                                    <div class="star-picker" style="margin-bottom: 10px;">
                                        <i v-for="star in 5" :key="'edit-picker-' + star"
                                            :class="[editRating >= star ? 'fas' : 'far', 'fa-circle']"
                                            @click="editRating = star" style="cursor: pointer; color: #f59e0b; margin-right: 5px;"></i>
                                    </div>
                                    <textarea v-model="editCommentText" style="width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; resize: vertical; min-height: 80px; font-family: inherit; font-size: 0.95rem; margin-bottom: 10px;"></textarea>
                                    <div style="display: flex; gap: 10px; justify-content: flex-end;">
                                        <button @click="cancelEdit" style="padding: 8px 16px; background: white; border: 1px solid #cbd5e1; border-radius: 6px; cursor: pointer; color: #475569; font-weight: 600;">Cancel</button>
                                        <button @click="saveEdit(comment.id)" style="padding: 8px 16px; background: #3b82f6; border: none; border-radius: 6px; cursor: pointer; color: white; font-weight: 600;">Save</button>
                                    </div>
                                </div>
                                <p v-else class="r-text">{{ comment.comment_text }}</p>
                            </div>
                        </div>
                    </section>
                </div>

                <div class="right-col">
                    <div class="booking-widget" id="deals">
                        <div class="price-header">
                            <span class="label" style="font-size: 1.1rem; font-weight: 700;">{{ t('hotels.checkPrices') }}</span>
                        </div>
                        
                        <div class="date-picker-box">
                            <div class="date-input">
                                <small>{{ t('hotels.checkin') }}</small>
                                <div style="font-weight: 600;">Mon 12/04</div>
                            </div>
                            <div class="date-input">
                                <small>{{ t('hotels.checkout') }}</small>
                                <div style="font-weight: 600;">Wed 14/04</div>
                            </div>
                        </div>

                        <div class="partner-deal">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/4/41/Booking.com_Logo_2022.png" height="24" alt="Booking.com" />
                            <div class="partner-info">
                                <span class="partner-name">Booking.com</span>
                                <small class="partner-hint">{{ t('hotels.seePrices') }}</small>
                            </div>
                            <a :href="hotel.booking_url || `https://www.booking.com/searchresults.html?ss=${hotel?.name || 'Savannakhet'}`" target="_blank" class="btn-partner">{{ t('hotels.viewPartnerDeal') }} <i class="fas fa-external-link-alt"></i></a>
                        </div>
                        
                        <div class="partner-deal">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Agoda_logo.svg/1200px-Agoda_logo.svg.png" height="24" alt="Agoda" />
                            <div class="partner-info">
                                <span class="partner-name">Agoda</span>
                                <small class="partner-hint">{{ t('hotels.seePrices') }}</small>
                            </div>
                            <a :href="hotel.agoda_url || `https://www.agoda.com/search?text=${hotel?.name || 'Savannakhet'}`" target="_blank" class="btn-partner">{{ t('hotels.viewPartnerDeal') }} <i class="fas fa-external-link-alt"></i></a>
                        </div>

                        <p class="free-cancel"><i class="fas fa-check"></i> {{ t('hotels.free_cancel') }}</p>
                    </div>

                    <div class="mini-map-card" id="location">
                        <iframe width="100%" height="150" frameborder="0" style="border:0; border-radius: 8px;"
                            :src="`https://maps.google.com/maps?q=${hotel.location_lat},${hotel.location_lng}&z=15&output=embed`"
                            allowfullscreen>
                        </iframe>
                        <button class="btn-map-link" @click="openMap">{{ t('place.viewOnMap') }}</button>
                    </div>
                </div>
            </div>

            <!-- Recommended Places -->
            <div class="recommended-section" v-if="recommendedPlaces && recommendedPlaces.length > 0">
                <h2>{{ t('place.recommended') }}</h2>
                <div class="recommended-grid">
                    <div v-for="rec in recommendedPlaces" :key="rec.id" class="rec-card" @click="goToRecDetail(rec.id)">
                        <div class="rec-img-wrapper">
                            <img :src="getRecCoverImage(rec)" :alt="rec.name" />
                            <button class="btn-heart-rec" @click.stop><i class="far fa-heart"></i></button>
                        </div>
                        <div class="rec-info">
                            <h4>{{ rec.name }}</h4>
                            <div class="rec-rating">
                                <span class="bubbles">
                                    <i v-for="s in 5" :key="s" :class="[(rec.rating_avg || 0) >= s ? 'fas' : 'far', 'fa-circle']"></i>
                                </span>
                                <span>{{ rec.rating_avg || '0.0' }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <MapOverlay :is-open="showMapModal" :places="allPlaces" :categories="categories"
                :initial-selected-id="hotel.id" title="Explore Hotels" @close="showMapModal = false" />
        </div>
        </div>

        <div v-else class="loading-screen">
            <div class="spinner"></div>
            <p>{{ t('common.loading') }}</p>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { placeRepository } from '@/repositories/placeRepository'
import { favoriteRepository } from '@/repositories/favoriteRepository'
import Navbar from '@/components/Navbar.vue'
import MapOverlay from '@/components/MapOverlay.vue'
import { categoryRepository } from '@/repositories/categoryRepository'
import { useI18n } from '@/composables/useI18n'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const hotel = ref(null)
const comments = ref([])
const user = ref(JSON.parse(localStorage.getItem('user')))
const isFavorite = ref(false)
const showMapModal = ref(false)
const allPlaces = ref([])
const categories = ref([])

const newComment = ref('')
const newRating = ref(5)
const submitting = ref(false)

const editingCommentId = ref(null)
const editCommentText = ref('')
const editRating = ref(5)
const showDropdownFor = ref(null)

const toggleDropdown = (id) => {
    showDropdownFor.value = showDropdownFor.value === id ? null : id
}

const startEdit = (comment) => {
    editingCommentId.value = comment.id
    editCommentText.value = comment.comment_text || ''
    editRating.value = comment.rating || 5
    showDropdownFor.value = null
}

const cancelEdit = () => {
    editingCommentId.value = null
    editCommentText.value = ''
    editRating.value = 5
}

const saveEdit = async (commentId) => {
    if (!editCommentText.value.trim()) return
    try {
        const formData = new FormData()
        formData.append('user_id', user.value.id)
        formData.append('rating', editRating.value)
        formData.append('comment_text', editCommentText.value)

        await placeRepository.updateUserReview(commentId, formData)
        
        const comment = comments.value.find(c => c.id === commentId)
        if (comment) {
            comment.comment_text = editCommentText.value
            comment.rating = editRating.value
        }
        cancelEdit()
        fetchData()
    } catch (err) {
        console.error("Failed to update comment", err)
    }
}

const deleteReview = async (commentId) => {
    if (!confirm('Are you sure you want to delete this review?')) return
    showDropdownFor.value = null
    try {
        await placeRepository.deleteUserReview(commentId, user.value.id)
        comments.value = comments.value.filter(c => c.id !== commentId)
        fetchData()
    } catch (err) {
        console.error("Failed to delete review", err)
    }
}

const recommendedPlaces = ref([])
const stickyNavRef = ref(null)
const isSticky = ref(false)
const activeSection = ref('about')

// Scroll Handler
const handleScroll = () => {
    if (stickyNavRef.value) {
        const rect = stickyNavRef.value.getBoundingClientRect()
        // It becomes sticky when its top reaches 0
        isSticky.value = rect.top <= 0
    }

    const sections = ['deals', 'about', 'location', 'reviews']
    for (const sec of sections) {
        const el = document.getElementById(sec)
        if (el) {
            const rect = el.getBoundingClientRect()
            if (rect.top >= 0 && rect.top < 300) {
                activeSection.value = sec
                break
            }
        }
    }
}

const scrollTo = (id) => {
    activeSection.value = id
    const el = document.getElementById(id)
    if (el) {
        const y = el.getBoundingClientRect().top + window.scrollY - 70 // Offset for sticky header
        window.scrollTo({ top: y, behavior: 'smooth' })
    }
}

// 🖼️ จัดการรูปภาพ
const galleryImages = computed(() => {
    if (!hotel.value) return ['https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1920&q=80']
    
    const getValidUrl = (rawUrl) => {
        if (!rawUrl || rawUrl === 'null' || rawUrl === 'undefined') return 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1920&q=80';
        let url = rawUrl;
        if (typeof url === 'string' && url.trim().startsWith('[')) {
            try {
                const parsed = JSON.parse(url);
                if (Array.isArray(parsed) && parsed.length > 0) url = parsed[0];
            } catch (e) {
                url = url.replace(/^\["?|"?\]$/g, '').replace(/\\"/g, '');
            }
        }
        if (typeof url !== 'string') return 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1920&q=80';
        if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) return url;
        return `http://127.0.0.1:8000${url.startsWith('/') ? '' : '/'}${url}`;
    }

    let urls = []
    if (hotel.value.image_url?.startsWith('[')) {
        try { urls = JSON.parse(hotel.value.image_url) } catch(e) { urls = [hotel.value.image_url] }
    } else {
        urls = [hotel.value.image_url]
    }
    
    const results = urls.map(url => getValidUrl(url))
    return results.length > 0 ? results : ['https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1920&q=80'];
})

const fetchData = async () => {
    const id = route.params.id
    try {
        const res = await placeRepository.getById(id)
        hotel.value = res.data
        
        // Fetch secondary data asynchronously
        placeRepository.getComments(id)
            .then(revRes => { comments.value = revRes.data })
            .catch(() => { comments.value = [] })

        placeRepository.getAll()
            .then(allRes => {
                allPlaces.value = allRes.data
                recommendedPlaces.value = allRes.data
                    .filter(p => p.category_id === hotel.value.category_id && p.id !== parseInt(id))
                    .slice(0, 4)
            })
            .catch(err => console.error(err))

        categoryRepository.getAll()
            .then(catRes => { categories.value = catRes.data })
            .catch(err => console.error(err))

        if (user.value) {
            favoriteRepository.getUserFavorites(user.value.id)
                .then(favRes => {
                    isFavorite.value = favRes.data.some(f => f.place_id === parseInt(id))
                })
                .catch(err => console.error(err))
        }
    } catch (err) { console.error(err) }
}

const toggleHeart = async () => {
    if (!user.value) return router.push('/login')
    try {
        const res = await favoriteRepository.toggleFavorite(user.value.id, hotel.value.id)
        isFavorite.value = res.data.status === 'added'
        if (isFavorite.value) {
            await axios.post('http://127.0.0.1:8000/api/interactions/', {
                place_id: hotel.value.id, rating: 5, interaction_type: 'like'
            })
        }
    } catch (err) { console.error(err) }
}

const submitComment = async () => {
    submitting.value = true
    try {
        await placeRepository.addComment(hotel.value.id, {
            user_id: user.value.id, rating: newRating.value, comment_text: newComment.value
        })
        await axios.post('http://127.0.0.1:8000/api/interactions/', {
            place_id: hotel.value.id, rating: newRating.value, comment: newComment.value, interaction_type: 'review'
        })
        newComment.value = ''; fetchData();
    } catch (err) { console.error(err) } finally { submitting.value = false }
}

const openMap = () => {
    showMapModal.value = true
}

const getRecCoverImage = (place) => {
    let url = ''
    if (place.images && place.images.length > 0) {
        url = place.images[0].image_url || place.images[0].url || place.images[0]
    } else if (place.image_url) {
        try {
            if (place.image_url.startsWith('[')) {
                url = JSON.parse(place.image_url)[0]
            } else {
                url = place.image_url
            }
        } catch (e) { url = place.image_url }
    }
    if (!url) return 'https://via.placeholder.com/300x200?text=No+Image'
    return url.startsWith('http') ? url : `http://127.0.0.1:8000/${url.replace(/^\//,'')}`
}

const goToRecDetail = (id) => {
    router.push(`/places/${id}`).then(() => {
        window.location.reload()
    })
}

onMounted(() => {
    fetchData()
    window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@700;800;900&display=swap');

.ta-hotel-detail {
    background-color: #ffffff;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    color: #1e293b;
}

/* Premium Hero Section */
.premium-hero-wrapper {
    margin-bottom: 40px;
}

.premium-hero {
    position: relative;
    height: 85vh;
    background-size: cover;
    background-position: center;
    color: white;
    display: flex;
    flex-direction: column;
}

.hero-nav {
    position: relative;
    z-index: 10;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 40px;
    background: linear-gradient(to bottom, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0) 100%);
}

.logo {
    cursor: pointer;
    font-size: 1.5rem;
    font-weight: 900;
}

.logo-main {
    color: white;
}

.logo-sub {
    color: #4ade80;
}

.nav-right {
    display: flex;
    align-items: center;
    gap: 30px;
}

.nav-items {
    display: flex;
    gap: 25px;
}

.nav-items a {
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1px;
    cursor: pointer;
    transition: 0.3s;
}

.nav-items a:hover {
    color: white;
}

.btn-plan {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.4);
    color: white;
    padding: 8px 20px;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 1px;
    cursor: pointer;
    transition: 0.3s;
}

.btn-plan:hover {
    background: white;
    color: black;
}

.hero-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.1) 40%, rgba(0,0,0,0.8) 100%);
}

.hero-content {
    position: relative;
    z-index: 2;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 0 40px 60px;
}

.top-row {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: auto;
}

.btn-back-minimal {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: 0.3s;
}

.btn-back-minimal:hover {
    background: white;
    color: black;
}

.breadcrumb {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1px;
    color: rgba(255, 255, 255, 0.8);
}

.hero-main-info {
    margin-top: auto;
    max-width: 800px;
}

.verified-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(34, 197, 94, 0.2);
    border: 1px solid rgba(34, 197, 94, 0.4);
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 1px;
    color: #4ade80;
    margin-bottom: 20px;
}

.status-dot {
    width: 6px;
    height: 6px;
    background: #4ade80;
    border-radius: 50%;
    box-shadow: 0 0 8px #4ade80;
}

.date-sep {
    opacity: 0.3;
}

.serif-title {
    font-family: 'Playfair Display', serif;
    font-size: 8rem;
    font-weight: 900;
    line-height: 0.85;
    margin: 0;
    letter-spacing: -4px;
    text-transform: capitalize;
}

.local-name {
    font-size: 2rem;
    color: rgba(255, 255, 255, 0.5);
    margin: 10px 0 30px;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
}

.hero-description {
    font-size: 1.3rem;
    line-height: 1.7;
    color: rgba(255, 255, 255, 0.9);
    font-weight: 400;
    max-width: 800px;
}

/* Stats Bar */
.stats-bar {
    max-width: 1280px;
    margin: 0 auto 0;
    background: white;
    position: relative;
    z-index: 5;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    border: 1px solid #f1f5f9;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

.stat-item {
    padding: 30px 40px;
    border-right: 1px solid #f1f5f9;
}

.stat-item:last-child {
    border-right: none;
}

.stat-item label {
    display: block;
    font-size: 0.6rem;
    font-weight: 900;
    color: #8c8c8c;
    letter-spacing: 3px;
    margin-bottom: 12px;
    text-transform: uppercase;
}

.stat-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #111111;
    font-family: 'Playfair Display', serif;
}

/* Tags Section */
.tags-container {
    max-width: 1280px;
    margin: 40px auto;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
}

.tag-column {
    padding: 30px 35px;
    background: white;
    border: 1px solid #f1f5f9;
}

.tag-column label {
    display: block;
    font-size: 0.65rem;
    font-weight: 900;
    letter-spacing: 2.5px;
    margin-bottom: 20px;
    color: #8c8c8c;
}

.best-for {
    border-left: 3px solid #1a735c;
}

.avoid-if {
    border-left: 3px solid #b04c36;
}

.tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.tag {
    padding: 6px 12px;
    border-radius: 2px;
    font-size: 0.8rem;
    font-weight: 600;
}

.best-for .tag {
    background: #eaf4f1;
    color: #1a735c;
    border: 1px solid #d3e8e1;
}

.avoid-if .tag {
    background: #faebe7;
    color: #b04c36;
    border: 1px solid #f5d5cc;
}



.tag-column {
    padding: 30px;
    border: 1px solid #e2e8f0;
}

.tag-column label {
    display: block;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 1.5px;
}



.best-for {
    border-left: 4px solid #4ade80;
}

.avoid-if {
    border-left: 4px solid #f87171;
}

.tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.tag {
    background: #f1f5f9;
    padding: 6px 14px;
    border-radius: 4px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #475569;
}

.best-for .tag {
    background: #f0fdf4;
    color: #166534;
    border: 1px solid #bbf7d0;
}

.avoid-if .tag {
    background: #fef2f2;
    color: #991b1b;
    border: 1px solid #fecaca;
}

/* Gallery Strip */
.gallery-preview-strip {
    max-width: 1280px;
    margin: 40px auto;
    display: flex;
    gap: 15px;
    height: 450px;
    cursor: pointer;
}

.strip-item {
    flex: 1;
    border-radius: 8px;
    overflow: hidden;
}

.strip-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: 0.3s;
}

.strip-item:hover img {
    transform: scale(1.05);
}

.more-indicator {
    width: 120px;
    background: #f1f5f9;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    color: #64748b;
}

.container-main {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 40px 60px;
}

/* Header */
.hotel-header-section { background: white; padding: 20px; border-radius: 12px 12px 0 0; border-bottom: 1px solid #e0e0e0; }
.breadcrumb { font-size: 0.8rem; color: #475569; margin-bottom: 10px; }
.header-content { display: flex; justify-content: space-between; align-items: flex-start; }
.header-content h1 { font-size: 2.2rem; font-weight: 800; margin: 0 0 10px; }
.meta-row { display: flex; align-items: center; gap: 10px; font-size: 0.95rem; }
.bubbles i { color: #00aa6c; margin-right: 2px; font-size: 0.8rem; }
.header-actions { display: flex; gap: 10px; }
.btn-action { background: white; border: 1px solid #000; padding: 8px 16px; border-radius: 20px; font-weight: 700; cursor: pointer; }
.btn-action.active { color: #ef4444; border-color: #ef4444; }

/* Gallery */
.gallery-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 4px; height: 400px; background: white; padding: 0 10px 10px; cursor: pointer; }
.main-img img { width: 100%; height: 100%; object-fit: cover; }
.sub-imgs { display: flex; flex-direction: column; gap: 4px; }
.sub-imgs img { height: 50%; object-fit: cover; }
.more-photos-overlay { position: relative; height: 50%; }
.more-photos-overlay img { width: 100%; height: 100%; }
.more-photos-overlay .text { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); color: white; display: flex; align-items: center; justify-content: center; font-weight: 800; }

/* Layout */
.content-layout { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-top: 20px; }
.left-col { background: white; padding: 25px; border-radius: 12px; }
.right-col { display: flex; flex-direction: column; gap: 20px; }

/* Amenities */
.amenities-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px; }
.amenity-item { display: flex; align-items: center; gap: 10px; font-size: 0.9rem; }
.amenity-item i { width: 20px; }

/* Booking Widget */
.booking-widget { background: white; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.price-header { margin-bottom: 15px; }
.price-row { display: flex; justify-content: space-between; align-items: center; margin-top: 5px; }
.price { font-size: 1.8rem; font-weight: 900; }
.date-picker-box { display: flex; border: 1px solid #cbd5e1; border-radius: 8px; margin-bottom: 15px; }
.date-input { flex: 1; padding: 10px; border-right: 1px solid #cbd5e1; }
.date-input:last-child { border-right: none; }
.btn-view-deal { width: 100%; background: #fcd34d; border: none; padding: 15px; border-radius: 25px; font-weight: 800; font-size: 1.1rem; cursor: pointer; }
.free-cancel { font-size: 0.8rem; color: #00aa6c; margin-top: 10px; text-align: center; font-weight: 600; }

/* Reviews */
.write-review-card { display: flex; gap: 15px; padding: 20px; border: 1px solid #e0e0e0; border-radius: 12px; margin-bottom: 30px; }
.u-avatar { width: 40px; height: 40px; background: #000; color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; }
.form-body { flex: 1; }
.star-picker { margin: 10px 0; color: #00aa6c; font-size: 1.2rem; cursor: pointer; }
textarea { width: 100%; height: 80px; padding: 10px; margin: 10px 0; border: 1px solid #cbd5e1; border-radius: 8px; }
.btn-submit { background: #000; color: #fff; border: none; padding: 10px 20px; border-radius: 20px; font-weight: 700; cursor: pointer; }

.review-item { padding: 20px 0; border-bottom: 1px solid #eee; }
.reviewer { display: flex; gap: 12px; margin-bottom: 10px; }
.r-rating i { color: #00aa6c; font-size: 0.7rem; }

/* Sticky Navigation */
.sticky-nav-wrapper {
    position: sticky;
    top: 0;
    z-index: 100;
    background: white;
    border-bottom: 1px solid #e0e0e0;
    margin-top: 15px;
    height: 60px; /* Fixed height to prevent jumpiness when sticky */
}

.sticky-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1100px;
    margin: 0 auto;
    height: 100%;
}

.nav-links {
    display: flex;
    gap: 20px;
    height: 100%;
}

.nav-links a {
    text-decoration: none;
    color: #475569;
    font-weight: 700;
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    border-bottom: 3px solid transparent;
    transition: 0.2s;
    height: 100%;
}

.nav-links a:hover {
    color: #000;
}

.nav-links a.active {
    color: #000;
    border-bottom-color: #000;
}

.nav-action {
    display: flex;
    align-items: center;
}

.btn-check-availability {
    background: #00aa6c;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 24px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
}

.btn-check-availability:hover {
    background: #008f5a;
}

/* Partnerships in Booking Widget */
.partner-deal {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    border-bottom: 1px solid #e2e8f0;
}

.btn-partner {
    background: #fcd34d;
    color: #000;
    font-weight: 700;
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.9rem;
    transition: line-height 0.2s;
}
.btn-partner:hover {
    background: #f59e0b;
}

/* Recommended Places */
.recommended-section {
    margin-top: 40px;
}

.recommended-section h2 {
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: 20px;
}

.recommended-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
}

.rec-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
    cursor: pointer;
    transition: 0.2s;
}

.rec-card:hover {
    box-shadow: 0 10px 20px rgba(0,0,0,0.08);
}

.rec-img-wrapper {
    position: relative;
    height: 160px;
}

.rec-img-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.btn-heart-rec {
    position: absolute;
    top: 10px;
    right: 10px;
    background: white;
    border: none;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    font-size: 0.9rem;
}

.rec-info {
    padding: 15px;
}

.rec-info h4 {
    margin: 0 0 8px;
    font-size: 1rem;
    font-weight: 700;
    line-height: 1.3;
}

.rec-rating i {
    color: #00aa6c;
    font-size: 0.7rem;
    margin-right: 2px;
}

.rec-rating span:last-child {
    margin-left: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #475569;
}

@media (max-width: 768px) {
    .recommended-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 480px) {
    .recommended-grid {
        grid-template-columns: 1fr;
    }
}

.loading-screen {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    background: white;
    z-index: 9999;
    color: #1e293b;
}

.spinner {
    width: 40px; height: 40px;
    border: 4px solid #f1f5f9;
    border-top: 4px solid #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 15px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
