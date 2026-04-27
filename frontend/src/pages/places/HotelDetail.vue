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

            <!-- Sticky Navigation -->
            <div class="sticky-nav-wrapper" ref="stickyNavRef">
                <div class="sticky-nav" :class="{ 'is-sticky': isSticky }">
                    <div class="nav-links">
                        <a href="#deals" :class="{ active: activeSection === 'deals' }" @click.prevent="scrollTo('deals')">Deals</a>
                        <a href="#about" :class="{ active: activeSection === 'about' }" @click.prevent="scrollTo('about')">About</a>
                        <a href="#location" :class="{ active: activeSection === 'location' }" @click.prevent="scrollTo('location')">Location</a>
                        <a href="#reviews" :class="{ active: activeSection === 'reviews' }" @click.prevent="scrollTo('reviews')">Reviews</a>
                    </div>
                    <div class="nav-action" v-if="isSticky">
                        <button class="btn-check-availability" @click="scrollTo('deals')">Check availability</button>
                    </div>
                </div>
            </div>

            <div class="content-layout">
                <div class="left-col">
                    <section class="about-hotel" id="about">
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

                    <section class="reviews-section" id="reviews">
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
                            <span class="label" style="font-size: 1.1rem; font-weight: 700;">View prices for your travel dates</span>
                        </div>
                        
                        <div class="date-picker-box">
                            <div class="date-input">
                                <small>Check In</small>
                                <div style="font-weight: 600;">Mon 12/04</div>
                            </div>
                            <div class="date-input">
                                <small>Check Out</small>
                                <div style="font-weight: 600;">Wed 14/04</div>
                            </div>
                        </div>

                        <div class="partner-deal">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/4/41/Booking.com_Logo_2022.png" height="24" alt="Booking.com" />
                            <a :href="`https://www.booking.com/searchresults.html?ss=${hotel?.name || 'Savannakhet'}`" target="_blank" class="btn-partner">View deal</a>
                        </div>
                        
                        <div class="partner-deal">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Agoda_logo.svg/1200px-Agoda_logo.svg.png" height="24" alt="Agoda" />
                            <a :href="`https://www.agoda.com/search?text=${hotel?.name || 'Savannakhet'}`" target="_blank" class="btn-partner">View deal</a>
                        </div>

                        <p class="free-cancel"><i class="fas fa-check"></i> Free cancellation on most rooms</p>
                    </div>

                    <div class="mini-map-card" id="location">
                        <iframe width="100%" height="150" frameborder="0" style="border:0; border-radius: 8px;"
                            :src="`https://maps.google.com/maps?q=${hotel.location_lat},${hotel.location_lng}&z=15&output=embed`"
                            allowfullscreen>
                        </iframe>
                        <button class="btn-map-link" @click="openMap">Show on Map</button>
                    </div>
                </div>
            </div>

            <!-- Recommended Places -->
            <div class="recommended-section" v-if="recommendedPlaces.length > 0">
                <h2>You might also like</h2>
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
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
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

        // ดึง Recommendations (สถานที่อื่นๆ ใน category เดียวกัน)
        const allRes = await placeRepository.getAll()
        recommendedPlaces.value = allRes.data
            .filter(p => p.category_id === hotel.value.category_id && p.id !== parseInt(id))
            .slice(0, 4)

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
    return url.startsWith('http') ? url : `http://localhost:8000/${url.replace(/^\//,'')}`
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
</style>
