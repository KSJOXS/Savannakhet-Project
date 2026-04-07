<template>
    <div class="ta-hotel-detail">
        <Navbar />

        <div class="container-main" v-if="hotel">
            <div class="hotel-header-section">
                <div class="breadcrumb">
                    Savannakhet Hotels > <span class="active">{{ hotel.name }}</span>
                </div>
                
                <div class="header-content">
                    <div class="title-area">
                        <h1>{{ hotel.name }}</h1>
                        <div class="meta-row">
                            <div class="bubbles">
                                <i v-for="s in 5" :key="s" :class="[(hotel.rating_avg || 0) >= s ? 'fas' : 'far', 'fa-circle']"></i>
                            </div>
                            <span class="review-count">{{ comments.length }} reviews</span>
                            <span class="divider">#1 of 15 hotels in Savannakhet</span>
                        </div>
                    </div>
                    <div class="header-actions">
                        <button class="btn-action" @click="toggleHeart" :class="{ active: isFavorite }">
                            <i class="fas fa-heart"></i> {{ isFavorite ? 'Saved' : 'Save' }}
                        </button>
                        <button class="btn-action"><i class="fas fa-share-square"></i> Share</button>
                    </div>
                </div>
            </div>

            <div class="gallery-grid" @click="openLightbox">
                <div class="main-img">
                    <img :src="galleryImages[0]" alt="Hotel Main Image" />
                </div>
                <div class="sub-imgs">
                    <img v-for="(img, i) in galleryImages.slice(1, 3)" :key="i" :src="img" alt="Sub Image" />
                    <div class="more-photos-overlay" v-if="galleryImages.length > 3">
                        <img :src="galleryImages[3]" alt="More" />
                        <div class="text">+{{ galleryImages.length - 3 }} Photos</div>
                    </div>
                </div>
            </div>

            <div class="content-layout">
                <div class="left-col">
                    <section class="about-hotel">
                        <h2>About</h2>
                        <p class="hotel-desc">{{ hotel.description }}</p>
                    </section>

                    <div class="amenities-box">
                        <h3>Property amenities</h3>
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

                    <section class="reviews-section">
                        <h2>Reviews ({{ comments.length }})</h2>
                        
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
                                    <div>
                                        <strong>{{ comment.username }}</strong>
                                        <div class="r-rating">
                                            <i v-for="s in 5" :key="s" :class="[comment.rating >= s ? 'fas' : 'far', 'fa-circle']"></i>
                                        </div>
                                    </div>
                                </div>
                                <p class="r-text">{{ comment.comment_text }}</p>
                            </div>
                        </div>
                    </section>
                </div>

                <div class="right-col">
                    <div class="booking-widget">
                        <div class="price-header">
                            <span class="label">Best Price at</span>
                            <div class="price-row">
                                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Agoda_logo.svg/1200px-Agoda_logo.svg.png" height="20" />
                                <span class="price">${{ hotel.price || '45' }}</span>
                            </div>
                        </div>
                        
                        <div class="date-picker-box">
                            <div class="date-input">
                                <small>Check In</small>
                                <div>Mon 06/04/26</div>
                            </div>
                            <div class="date-input">
                                <small>Check Out</small>
                                <div>Wed 08/04/26</div>
                            </div>
                        </div>

                        <button class="btn-view-deal" @click="openMap">
                            View Deal <i class="fas fa-external-link-alt"></i>
                        </button>
                        <p class="free-cancel"><i class="fas fa-check"></i> Free cancellation until 05/04/26</p>
                    </div>

                    <div class="mini-map-card">
                        <iframe width="100%" height="150" frameborder="0" style="border:0; border-radius: 8px;"
                            :src="`https://maps.google.com/maps?q=${hotel.location_lat},${hotel.location_lng}&z=15&output=embed`"
                            allowfullscreen>
                        </iframe>
                        <button class="btn-map-link" @click="openMap">Show on Map</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { placeRepository } from '@/repositories/placeRepository'
import { favoriteRepository } from '@/repositories/favoriteRepository'
import Navbar from '@/components/Navbar.vue'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const hotel = ref(null)
const comments = ref([])
const user = ref(JSON.parse(localStorage.getItem('user')))
const isFavorite = ref(false)

const newComment = ref('')
const newRating = ref(5)
const submitting = ref(false)

// 🖼️ จัดการรูปภาพ
const galleryImages = computed(() => {
    if (!hotel.value) return []
    let urls = []
    if (hotel.value.image_url?.startsWith('[')) {
        try { urls = JSON.parse(hotel.value.image_url) } catch(e) { urls = [hotel.value.image_url] }
    } else {
        urls = [hotel.value.image_url]
    }
    return urls.map(url => url.startsWith('http') ? url : `http://localhost:8000/${url}`)
})

const fetchData = async () => {
    const id = route.params.id
    try {
        const res = await placeRepository.getById(id)
        hotel.value = res.data
        
        // ดึงรีวิว
        const revRes = await placeRepository.getComments(id)
        comments.value = revRes.data

        // เช็ค Favorite
        if (user.value) {
            const favRes = await favoriteRepository.getUserFavorites(user.value.id)
            isFavorite.value = favRes.data.some(f => f.place_id === parseInt(id))
        }
    } catch (err) { console.error(err) }
}

const toggleHeart = async () => {
    if (!user.value) return router.push('/login')
    try {
        const res = await favoriteRepository.toggleFavorite(user.value.id, hotel.value.id)
        isFavorite.value = res.data.status === 'added'
        if (isFavorite.value) {
            await axios.post('http://localhost:8000/api/interactions/', {
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
        await axios.post('http://localhost:8000/api/interactions/', {
            place_id: hotel.value.id, rating: newRating.value, comment: newComment.value, interaction_type: 'review'
        })
        newComment.value = ''; fetchData();
    } catch (err) { console.error(err) } finally { submitting.value = false }
}

const openMap = () => window.open(`https://www.google.com/maps/search/?api=1&query=${hotel.value.location_lat},${hotel.value.location_lng}`, '_blank')

onMounted(fetchData)
</script>

<style scoped>
.ta-hotel-detail { background: #f2f2f2; min-height: 100vh; font-family: 'Inter', sans-serif; color: #000; }
.container-main { max-width: 1140px; margin: 0 auto; padding: 20px; }

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
</style>