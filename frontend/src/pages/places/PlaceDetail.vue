<template>
    <div class="ta-detail-page">
        <Navbar />

        <div class="ta-container" v-if="place">
            <div class="top-actions">
                <button @click="router.back()" class="btn-back">
                    <i class="fas fa-arrow-left"></i> กลับไปค้นหา
                </button>
            </div>

            <div class="place-header">
                <div class="header-main">
                    <h1>{{ place.name }}</h1>
                    <div class="meta-row">
                        <div class="rating-bubbles">
                            <i v-for="s in 5" :key="'h-' + s"
                                :class="[(place.rating_avg || 0) >= s ? 'fas' : 'far', 'fa-circle']"></i>
                        </div>
                        <span class="review-count">{{ comments.length }} รีวิว</span>
                        <span class="divider">•</span>
                        <span class="category-link">{{ getCategoryName(place.category_id) }}</span>
                        <span class="divider">•</span>
                        <span class="location-text top-location-link" @click="openMapOverlay" title="คลิกเพื่อดูแผนที่">
                            <i class="fas fa-map-marker-alt"></i> {{ addressText }}
                        </span>
                    </div>
                </div>
                <div class="header-actions">
                    <button v-if="!user || user.role !== 'admin'"
                        :class="['btn-action btn-save', { active: isFavorite }]" @click="toggleHeart">
                        <i class="fas fa-heart"></i> {{ isFavorite ? 'Saved' : 'Save' }}
                    </button>
                </div>
            </div>

            <div class="gallery-grid" @click="openLightbox">
                <div class="main-photo">
                    <img :src="galleryImages[0]" alt="Main Place Image" />
                </div>
                <div class="side-photos" v-if="galleryImages.length > 1">
                    <img :src="galleryImages[1]" alt="Place Image 2" />
                    <img v-if="galleryImages.length > 2" :src="galleryImages[2]" alt="Place Image 3"
                        class="third-img" />
                    <div v-else class="empty-photo-slot"></div>
                </div>
                <button class="btn-view-photos"><i class="fas fa-th"></i> ดูรูปภาพทั้งหมด ({{ galleryImages.length }})</button>
            </div>

            <!-- Sticky Navigation -->
            <div class="sticky-nav-wrapper" ref="stickyNavRef">
                <div class="sticky-nav" :class="{ 'is-sticky': isSticky }">
                    <div class="nav-links">
                        <a v-if="isHotel" href="#deals" :class="{ active: activeSection === 'deals' }" @click.prevent="scrollTo('deals')">ราคาพิเศษ</a>
                        <a href="#about" :class="{ active: activeSection === 'about' }" @click.prevent="scrollTo('about')">เกี่ยวกับ</a>
                        <a href="#location" :class="{ active: activeSection === 'location' }" @click.prevent="scrollTo('location')">ที่ตั้ง</a>
                        <a href="#reviews" :class="{ active: activeSection === 'reviews' }" @click.prevent="scrollTo('reviews')">รีวิว</a>
                    </div>
                </div>
            </div>

            <div class="content-split">
                <div class="main-column">
                    <section class="about-section" id="about">
                        <h2>เกี่ยวกับสถานที่นี้</h2>
                        <p class="description-text">{{ place.description }}</p>
                    </section>

                    <hr class="section-divider" />

                    <section class="reviews-section" id="reviews">
                        <h2>รีวิวจากนักเดินทาง ({{ comments.length }})</h2>

                        <div class="write-review-box" v-if="user && user.role !== 'admin'">
                            <div class="u-avatar-large">{{ user.username ? user.username.charAt(0).toUpperCase() : 'U'
                                }}</div>
                            <div class="review-input-area">
                                <p class="prompt-text">คุณคิดอย่างไรกับสถานที่นี้?</p>
                                <div class="star-picker">
                                    <i v-for="star in 5" :key="'picker-' + star"
                                        :class="[newRating >= star ? 'fas' : 'far', 'fa-circle']"
                                        @click="newRating = star"></i>
                                    <span class="rating-label">{{ ratingLabels[newRating - 1] }}</span>
                                </div>
                                <textarea v-model="newComment"
                                    placeholder="เขียนรีวิวของคุณเพื่อแบ่งปันประสบการณ์..."></textarea>
                                <div class="action-row">
                                    <button class="btn-submit" @click="submitComment"
                                        :disabled="submitting || !newComment.trim()">
                                        {{ submitting ? 'กำลังส่ง...' : 'ส่งรีวิว' }}
                                    </button>
                                </div>
                                <p v-if="reviewSuccess" class="success-msg"><i class="fas fa-check-circle"></i>
                                    ส่งรีวิวสำเร็จ!</p>
                            </div>
                        </div>
                        <div v-else-if="!user" class="login-prompt">
                            <p>กรุณาเข้าสู่ระบบเพื่อเขียนรีวิว</p>
                            <button @click="router.push('/login')" class="btn-login-outline">ลงชื่อเข้าใช้</button>
                        </div>

                        <div class="review-list">
                            <div v-if="comments.length === 0" class="no-reviews">
                                <i class="far fa-comment-alt"></i>
                                <p>ยังไม่มีรีวิวสำหรับสถานที่นี้ เป็นคนแรกที่รีวิวสิ!</p>
                            </div>

                            <div v-for="comment in comments" :key="comment.id" class="review-item">
                                <div class="reviewer-info">
                                    <div class="r-avatar">{{ comment.username?.charAt(0).toUpperCase() }}</div>
                                    <div class="r-details">
                                        <strong>{{ comment.username }}</strong>
                                        <span class="r-date">เขียนรีวิวเมื่อเร็วๆ นี้</span>
                                    </div>
                                </div>
                                <div class="review-content">
                                    <div class="rating-bubbles small">
                                        <i v-for="s in 5" :key="'rev-' + comment.id + '-' + s"
                                            :class="[comment.rating >= s ? 'fas' : 'far', 'fa-circle']"></i>
                                    </div>
                                    <p class="r-text">{{ comment.comment_text }}</p>
                                </div>
                            </div>
                        </div>
                    </section>
                </div>

                <div class="sidebar-column">
                    <!-- Hotel Booking Deals -->
                    <div class="sidebar-card booking-card" v-if="isHotel" id="deals">
                        <h3>ตรวจสอบราคาที่พัก</h3>
                        <div class="partner-deal">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/4/41/Booking.com_Logo_2022.png" height="24" alt="Booking.com" />
                            <a :href="`https://www.booking.com/searchresults.html?ss=${place.name}`" target="_blank" class="btn-partner">ดูราคา</a>
                        </div>
                        <div class="partner-deal">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Agoda_logo.svg/1200px-Agoda_logo.svg.png" height="24" alt="Agoda" />
                            <a :href="`https://www.agoda.com/search?text=${place.name}`" target="_blank" class="btn-partner">ดูราคา</a>
                        </div>
                    </div>


                </div>
            </div>

            <!-- Large Map Section -->
            <div class="large-map-section" id="location">
                <h2>Location</h2>
                <p class="map-address"><i class="fas fa-map-marker-alt"></i> {{ addressText }}</p>
                <div class="large-map-container" v-if="place.location_lat && place.location_lng">
                    <iframe width="100%" height="450" frameborder="0" style="border:0;"
                        :src="`https://maps.google.com/maps?q=${place.location_lat},${place.location_lng}&z=15&output=embed`"
                        allowfullscreen>
                    </iframe>
                </div>
            </div>

            <!-- Nearby Area Section (Explore) -->
            <div class="nearby-section" v-if="nearbyRestaurants.length > 0 || nearbyAttractions.length > 0">
                <div class="nearby-grid">
                    <!-- Column 1: Getting There -->
                    <div class="nearby-col getting-there-col">
                        <h3>Getting there</h3>
                        <div class="walk-score-box">
                            <div class="score-text">
                                <span class="score-title">Somewhat walkable <i class="fas fa-info-circle"></i></span>
                                <span class="score-desc">Grade: 64 out of 100</span>
                            </div>
                            <div class="score-number">64</div>
                        </div>
                        <div class="airport-info">
                            <p><i class="fas fa-plane"></i> <strong>Savannakhet Airport</strong></p>
                            <span class="distance-line"><i class="fas fa-car side-icon"></i> 1.2 miles</span>
                        </div>
                    </div>

                    <!-- Column 2: Restaurants -->
                    <div class="nearby-col">
                        <div class="col-header">
                            <div>
                                <h3>{{ nearbyRestaurantsTotal }} Restaurants</h3>
                                <span>within 0.75 miles</span>
                            </div>
                            <button class="btn-text-link" @click="openMapOverlay">View on map</button>
                        </div>
                        
                        <div class="nearby-list">
                            <div v-for="n in nearbyRestaurants" :key="n.id" class="nearby-item" @click="goToRecDetail(n.id)">
                                <h4>{{ n.name }}</h4>
                                <div class="n-rating">
                                    <span class="n-score">{{ n.rating_avg || '0.0' }}</span>
                                    <div class="bubbles">
                                        <i v-for="s in 5" :key="s" :class="[(n.rating_avg || 0) >= s ? 'fas' : 'far', 'fa-circle']"></i>
                                    </div>
                                    <span class="n-reviews">({{ getCommentCountText(n) }} reviews)</span>
                                </div>
                                <div class="n-meta">
                                    <i class="fas fa-walking"></i> {{ getDistanceText(n._distance) }} <span class="dot-divider">•</span> $$ - $$$ <span class="dot-divider">•</span> {{ getCategoryName(n.category_id) }}
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Column 3: Attractions -->
                    <div class="nearby-col right-col">
                        <div class="col-header">
                            <div>
                                <h3>{{ nearbyAttractionsTotal }} Attractions</h3>
                                <span>within 0.75 miles</span>
                            </div>
                            <button class="btn-text-link" @click="openMapOverlay">View on map</button>
                        </div>

                        <div class="nearby-list">
                            <div v-for="n in nearbyAttractions" :key="n.id" class="nearby-item" @click="goToRecDetail(n.id)">
                                <h4>{{ n.name }}</h4>
                                <div class="n-rating">
                                    <span class="n-score">{{ n.rating_avg || '0.0' }}</span>
                                    <div class="bubbles">
                                        <i v-for="s in 5" :key="s" :class="[(n.rating_avg || 0) >= s ? 'fas' : 'far', 'fa-circle']"></i>
                                    </div>
                                    <span class="n-reviews">({{ getCommentCountText(n) }} reviews)</span>
                                </div>
                                <div class="n-meta">
                                    <i class="fas fa-walking"></i> {{ getDistanceText(n._distance) }} <span class="dot-divider">•</span> {{ getCategoryName(n.category_id) }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Recommended Places Section -->
            <div class="recommended-section" v-if="recommendedPlaces.length > 0">
                <h2>สถานที่แนะนำเพิ่มเติม</h2>
                <div class="recommended-grid">
                    <div v-for="rec in recommendedPlaces" :key="rec.id" class="rec-card" @click="goToRecDetail(rec.id)">
                        <div class="rec-img-wrapper">
                            <img :src="getRecCoverImage(rec)" :alt="rec.name" />
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

        <div v-else class="loading-screen">
            <div class="spinner"></div>
            <p>กำลังโหลดข้อมูล...</p>
        </div>

        <div v-if="isLightboxOpen" class="lightbox-overlay" @click="closeLightbox" @wheel.prevent="handleScrollZoom">
            <button class="btn-close-lightbox" @click="closeLightbox"><i class="fas fa-times"></i></button>
            <button v-if="galleryImages.length > 1" class="btn-nav prev" @click.stop="prevImage"><i
                    class="fas fa-chevron-left"></i></button>
            <img :src="galleryImages[currentImageIndex]" class="lightbox-img"
                :style="{ transform: `scale(${zoomLevel})` }" @click.stop />
            <button v-if="galleryImages.length > 1" class="btn-nav next" @click.stop="nextImage"><i
                    class="fas fa-chevron-right"></i></button>
        </div>

        <MapOverlay 
            v-if="place"
            :is-open="showMapModal" 
            :places="allPlaces" 
            :categories="categories"
            :initial-selected-id="place.id"
            title="Explore Places" 
            @close="showMapModal = false" 
        />
    </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { placeRepository } from '@/repositories/placeRepository'
import { categoryRepository } from '@/repositories/categoryRepository'
import { favoriteRepository } from '@/repositories/favoriteRepository'
import Navbar from '@/components/Navbar.vue'
import MapOverlay from '@/components/MapOverlay.vue'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const place = ref(null)
const categories = ref([])
const comments = ref([])
const user = ref(JSON.parse(localStorage.getItem('user')))
const isFavorite = ref(false)
const reviewSuccess = ref(false)
const addressText = ref('กำลังค้นหาตำแหน่ง...')
const showMapModal = ref(false)
const allPlaces = ref([])

const newComment = ref('')
const newRating = ref(5)
const submitting = ref(false)

const ratingLabels = ['แย่มาก', 'พอใช้', 'ปานกลาง', 'ดี', 'ยอดเยี่ยม']

const currentImageIndex = ref(0)
const isLightboxOpen = ref(false)
const zoomLevel = ref(1)

const galleryImages = computed(() => {
    const getValidImageUrl = (rawUrl) => {
        if (!rawUrl) return null;
        let url = rawUrl;
        if (typeof url === 'string' && url.trim().startsWith('[')) {
            try {
                const parsed = JSON.parse(url);
                if (Array.isArray(parsed) && parsed.length > 0) url = parsed[0];
            } catch (e) {
                url = url.replace(/^\["?|"?\]$/g, '').replace(/\\"/g, '');
            }
        }
        if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) return url;
        return `http://localhost:8000${url.startsWith('/') ? '' : '/'}${url}`;
    }

    if (place.value?.images && Array.isArray(place.value.images) && place.value.images.length > 0) {
        return place.value.images.map(img => getValidImageUrl(img.image_url || img.url || img));
    }
    else if (place.value?.image_url) {
        let parsedArray = [];
        if (typeof place.value.image_url === 'string' && place.value.image_url.trim().startsWith('[')) {
            try { parsedArray = JSON.parse(place.value.image_url); } catch (e) { }
        }
        if (parsedArray.length > 0) return parsedArray.map(img => getValidImageUrl(img));
        else return [getValidImageUrl(place.value.image_url)];
    }

    return ['data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22800%22%20height%3D%22450%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20fill%3D%22%23e2e8f0%22%2F%3E%3Ctext%20x%3D%2250%25%22%20y%3D%2250%25%22%20fill%3D%22%2364748b%22%20font-family%3D%22sans-serif%22%20font-size%3D%2224%22%20text-anchor%3D%22middle%22%20dy%3D%22.3em%22%3ENo%20Image%20Available%3C%2Ftext%3E%3C%2Fsvg%3E']
})

const isHotel = computed(() => {
    if (!place.value || !categories.value.length) return false;
    const cat = categories.value.find(c => c.id === place.value.category_id);
    return cat && (cat.name.toLowerCase().includes('hotel') || cat.parent_type === 'hotel');
});

const recommendedPlaces = computed(() => {
    if (!place.value || !allPlaces.value.length) return [];
    return allPlaces.value
        .filter(p => p.category_id === place.value.category_id && p.id !== place.value.id)
        .slice(0, 4);
});

// Haversine Distance Calculator
const getDistance = (lat1, lon1, lat2, lon2) => {
    if (!lat1 || !lon1 || !lat2 || !lon2) return null;
    const R = 6371; // km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = 0.5 - Math.cos(dLat)/2 + Math.cos(lat1*Math.PI/180) * Math.cos(lat2*Math.PI/180) * (1 - Math.cos(dLon))/2;
    return R * 2 * Math.asin(Math.sqrt(a));
}

const nearbyRestaurantsTotal = ref(0);
const nearbyAttractionsTotal = ref(0);

const nearbyRestaurants = computed(() => {
    if (!place.value || !allPlaces.value.length) return [];
    const lat1 = parseFloat(place.value.location_lat);
    const lng1 = parseFloat(place.value.location_lng);
    
    let filtered = allPlaces.value.filter(p => {
        if(p.id === place.value.id) return false;
        const cat = categories.value.find(c => c.id === p.category_id);
        if(!cat || cat.parent_type !== 'restaurant') return false;
        
        p._distance = getDistance(lat1, lng1, parseFloat(p.location_lat), parseFloat(p.location_lng));
        return p._distance === null || p._distance < 1.2; // roughly 0.75 miles
    }).sort((a,b) => (a._distance || 0) - (b._distance || 0));
    
    nearbyRestaurantsTotal.value = filtered.length;
    return filtered.slice(0, 4);
});

const nearbyAttractions = computed(() => {
    if (!place.value || !allPlaces.value.length) return [];
    const lat1 = parseFloat(place.value.location_lat);
    const lng1 = parseFloat(place.value.location_lng);
    
    let filtered = allPlaces.value.filter(p => {
        if(p.id === place.value.id) return false;
        const cat = categories.value.find(c => c.id === p.category_id);
        if(!cat || cat.parent_type === 'restaurant' || cat.parent_type === 'hotel') return false;
        
        p._distance = getDistance(lat1, lng1, parseFloat(p.location_lat), parseFloat(p.location_lng));
        return p._distance === null || p._distance < 1.2;
    }).sort((a,b) => (a._distance || 0) - (b._distance || 0));
    
    nearbyAttractionsTotal.value = filtered.length;
    return filtered.slice(0, 4);
});

const getDistanceText = (km) => {
    if(km === null || km === undefined) return "5 min";
    const min = Math.round(km * 12);
    return min < 1 ? "1 min" : min + " min";
}

const getCommentCountText = (pl) => {
    if (pl && pl.review_count !== undefined) {
        return pl.review_count;
    }
    return 0; // Fallback to 0 if we don't have it
}

const stickyNavRef = ref(null);
const isSticky = ref(false);
const activeSection = ref('about');

const handleScroll = () => {
    if (stickyNavRef.value) {
        const rect = stickyNavRef.value.getBoundingClientRect();
        isSticky.value = rect.top <= 0;
    }

    const sections = ['deals', 'about', 'location', 'reviews'];
    for (const sec of sections) {
        const el = document.getElementById(sec);
        if (el) {
            const rect = el.getBoundingClientRect();
            if (rect.top >= -50 && rect.top < 300) {
                activeSection.value = sec;
                break;
            }
        }
    }
};

const scrollTo = (id) => {
    activeSection.value = id;
    const el = document.getElementById(id);
    if (el) {
        const y = el.getBoundingClientRect().top + window.scrollY - 70;
        window.scrollTo({ top: y, behavior: 'smooth' });
    }
};

const getRecCoverImage = (p) => {
    let url = '';
    if (p.images && p.images.length > 0) {
        url = p.images[0].image_url || p.images[0].url || p.images[0];
    } else if (p.image_url) {
        try {
            if (p.image_url.startsWith('[')) url = JSON.parse(p.image_url)[0];
            else url = p.image_url;
        } catch (e) { url = p.image_url; }
    }
    if (!url) return 'https://via.placeholder.com/300x200?text=No+Image';
    return url.startsWith('http') ? url : `http://localhost:8000/${url.replace(/^\//,'')}`;
};

const goToRecDetail = (id) => {
    router.push(`/places/${id}`).then(() => {
        window.location.reload();
    });
};

const handleScrollZoom = (e) => {
    const zoomStep = 0.15;
    if (e.deltaY < 0) zoomLevel.value = Math.min(zoomLevel.value + zoomStep, 5);
    else zoomLevel.value = Math.max(zoomLevel.value - zoomStep, 0.5);
}

const openLightbox = () => {
    isLightboxOpen.value = true
    zoomLevel.value = 1
    document.body.style.overflow = 'hidden'
}

const closeLightbox = () => {
    isLightboxOpen.value = false
    zoomLevel.value = 1
    document.body.style.overflow = 'auto'
}

const nextImage = () => {
    zoomLevel.value = 1
    if (currentImageIndex.value < galleryImages.value.length - 1) currentImageIndex.value++
    else currentImageIndex.value = 0
}

const prevImage = () => {
    zoomLevel.value = 1
    if (currentImageIndex.value > 0) currentImageIndex.value--
    else currentImageIndex.value = galleryImages.value.length - 1
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
    window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeydown)
    window.removeEventListener('scroll', handleScroll)
    document.body.style.overflow = 'auto'
})

const fetchData = async () => {
    const id = route.params.id
    try {
        const [resPlace, resCats, resAll] = await Promise.all([
            placeRepository.getById(id),
            categoryRepository.getAll(),
            placeRepository.getAll()
        ])
        place.value = resPlace.data
        categories.value = resCats.data
        allPlaces.value = resAll.data

        // แปลงพิกัดเป็นชื่อสถานที่ (Reverse Geocoding)
        if (place.value.location_lat && place.value.location_lng) {
            const lat = parseFloat(place.value.location_lat)
            const lng = parseFloat(place.value.location_lng)
            
            try {
                const mapRes = await axios.get(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&accept-language=th,en`)
                if (mapRes.data && mapRes.data.display_name) {
                    const parts = mapRes.data.display_name.split(', ')
                    addressText.value = parts.length > 3 ? parts.slice(0, 3).join(', ') : mapRes.data.display_name
                } else {
                    addressText.value = `📍 พิกัด (Lat: ${lat.toFixed(4)}, Lng: ${lng.toFixed(4)})`
                }
            } catch (e) {
                addressText.value = `📍 พิกัด (Lat: ${lat.toFixed(4)}, Lng: ${lng.toFixed(4)})`
            }
        } else {
            addressText.value = 'ไม่พบข้อมูลตำแหน่ง'
        }

        // --- Save to recently_viewed in localStorage ---
        let rv = JSON.parse(localStorage.getItem('recently_viewed') || '[]')
        rv = rv.filter(item => item !== parseInt(id))
        rv.unshift(parseInt(id))
        if (rv.length > 8) rv.pop()
        localStorage.setItem('recently_viewed', JSON.stringify(rv))

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

        try {
            const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            await axios.post(`${backendUrl}/api/interactions/`, {
                place_id: parseInt(route.params.id),
                rating: newRating.value,
                comment: newComment.value,
                interaction_type: 'review'
            });
        } catch (aiErr) { console.warn("AI Log failed", aiErr); }

        newComment.value = ''
        newRating.value = 5
        reviewSuccess.value = true
        setTimeout(() => reviewSuccess.value = false, 3000)
        fetchData()
    } catch (err) { console.error(err) } finally { submitting.value = false }
}

const toggleHeart = async () => {
    if (!user.value) return router.push('/login')
    try {
        const res = await favoriteRepository.toggleFavorite(user.value.id, route.params.id)
        isFavorite.value = res.data.status === 'added'

        if (isFavorite.value) {
            const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            await axios.post(`${backendUrl}/api/interactions/`, {
                place_id: parseInt(route.params.id),
                rating: 5,
                comment: "Liked",
                interaction_type: 'like'
            });
        }
    } catch (err) { console.error(err) }
}

const getCategoryName = (id) => categories.value.find(c => c.id === id)?.name || 'General'
const openMapOverlay = () => { showMapModal.value = true }
const openGoogleMaps = () => window.open(`https://www.google.com/maps/search/?api=1&query=${place.value.location_lat},${place.value.location_lng}`, '_blank')
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* --- พื้นหลังคลีนแบบ TripAdvisor --- */
.ta-detail-page {
    background-color: #f7f9fa;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    color: #1e293b;
}

.ta-container {
    max-width: 1140px;
    margin: 0 auto;
    padding: 20px 20px 60px;
}

/* --- Top Actions (Back Button) --- */
.top-actions {
    margin-bottom: 15px;
}

.btn-back {
    background: none;
    border: none;
    color: #475569;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0;
    font-family: 'Inter', sans-serif;
}

.btn-back:hover {
    color: #000;
    text-decoration: underline;
}

/* --- Header Section --- */
.place-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;
}

.header-main h1 {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 0 0 10px;
    color: #000;
}

.meta-row {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    font-size: 0.95rem;
    color: #475569;
}

/* วงกลมแบบ TripAdvisor */
.rating-bubbles i {
    color: #00aa6c;
    font-size: 0.9rem;
    margin-right: 2px;
}

.review-count {
    font-weight: 600;
    color: #475569;
    text-decoration: underline;
    cursor: pointer;
}

.divider {
    color: #cbd5e1;
}

.category-link {
    font-weight: 600;
    color: #475569;
}

.top-location-link {
    cursor: pointer;
    transition: color 0.2s;
}

.top-location-link:hover {
    color: #000;
    text-decoration: underline;
}

.header-actions {
    display: flex;
    gap: 10px;
}

.btn-action {
    background: white;
    border: 1px solid #cbd5e1;
    padding: 8px 16px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: 0.2s;
    color: #0f172a;
    font-family: 'Inter', sans-serif;
}

.btn-action:hover {
    border-color: #000;
    background: #f8fafc;
}

.btn-save.active {
    color: #ef4444;
    border-color: #ef4444;
    background: #fef2f2;
}

/* --- Gallery Grid --- */
.gallery-grid {
    display: flex;
    gap: 4px;
    height: 400px;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 30px;
    position: relative;
    cursor: pointer;
}

.gallery-grid:hover::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.05);
    pointer-events: none;
}

.main-photo {
    flex: 2;
    height: 100%;
}

.main-photo img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.side-photos {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
    height: 100%;
}

.side-photos img {
    width: 100%;
    height: calc(50% - 2px);
    object-fit: cover;
}

.empty-photo-slot {
    width: 100%;
    height: calc(50% - 2px);
    background: #e2e8f0;
}

.btn-view-photos {
    position: absolute;
    bottom: 20px;
    right: 20px;
    background: white;
    border: 1px solid #000;
    padding: 8px 16px;
    border-radius: 8px;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* --- Content Split Layout --- */
.content-split {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 40px;
}

@media (max-width: 992px) {
    .content-split {
        grid-template-columns: 1fr;
    }
}

/* Main Column */
.main-column h2 {
    font-size: 1.5rem;
    font-weight: 800;
    margin: 0 0 15px;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 10px;
}

.description-text {
    line-height: 1.7;
    color: #334155;
    font-size: 1.05rem;
}

.section-divider {
    border: none;
    height: 1px;
    background: #e2e8f0;
    margin: 30px 0;
}

/* Reviews Section */
.write-review-box {
    display: flex;
    gap: 15px;
    background: white;
    padding: 24px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    margin-bottom: 30px;
}

.u-avatar-large {
    width: 48px;
    height: 48px;
    background: #000;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    font-weight: 700;
    flex-shrink: 0;
}

.review-input-area {
    flex: 1;
}

.prompt-text {
    font-weight: 700;
    margin: 0 0 10px;
    color: #0f172a;
}

.star-picker {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 15px;
}

.star-picker i {
    color: #00aa6c;
    font-size: 1.5rem;
    cursor: pointer;
    transition: 0.1s;
}

.star-picker i:hover {
    transform: scale(1.1);
}

.rating-label {
    margin-left: 10px;
    font-weight: 600;
    color: #475569;
}

textarea {
    width: 100%;
    height: 100px;
    padding: 15px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    resize: none;
    font-family: inherit;
    margin-bottom: 15px;
    box-sizing: border-box;
}

textarea:focus {
    outline: none;
    border-color: #000;
}

.action-row {
    display: flex;
    justify-content: flex-end;
}

.btn-submit {
    background: #000;
    color: white;
    border: none;
    padding: 10px 24px;
    border-radius: 8px;
    font-weight: 700;
    cursor: pointer;
}

.btn-submit:disabled {
    background: #cbd5e1;
    cursor: not-allowed;
}

.success-msg {
    color: #00aa6c;
    font-weight: 600;
    text-align: right;
    margin-top: 10px;
}

.login-prompt {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    text-align: center;
    margin-bottom: 30px;
}

.btn-login-outline {
    margin-top: 10px;
    background: white;
    border: 1px solid #000;
    padding: 8px 24px;
    border-radius: 8px;
    font-weight: 700;
    cursor: pointer;
}

/* Review List */
.review-item {
    border-bottom: 1px solid #e2e8f0;
    padding: 20px 0;
}

.review-item:last-child {
    border-bottom: none;
}

.reviewer-info {
    display: flex;
    gap: 15px;
    margin-bottom: 10px;
}

.r-avatar {
    width: 40px;
    height: 40px;
    background: #e2e8f0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    color: #475569;
}

.r-details {
    display: flex;
    flex-direction: column;
}

.r-date {
    font-size: 0.8rem;
    color: #64748b;
}

.rating-bubbles.small i {
    font-size: 0.8rem;
}

.r-text {
    margin: 10px 0 0;
    line-height: 1.6;
    color: #334155;
}

.no-reviews {
    text-align: center;
    color: #64748b;
    padding: 40px 0;
}

.no-reviews i {
    font-size: 2rem;
    margin-bottom: 10px;
}

/* Sidebar Column */
.sidebar-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    position: sticky;
    top: 90px;
}

.sidebar-card h3 {
    margin: 0 0 15px;
    font-size: 1.1rem;
    font-weight: 800;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 10px;
}

.map-container {
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 15px;
    border: 1px solid #e2e8f0;
}

.real-address-info {
    line-height: 1.6;
}

.contact-info p {
    margin: 0 0 15px;
    color: #334155;
    display: flex;
    gap: 10px;
    align-items: center;
}

.btn-directions {
    width: 100%;
    background: white;
    border: 1px solid #000;
    padding: 10px;
    border-radius: 8px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
}

.btn-directions:hover {
    background: #f8fafc;
}

/* --- Loading & Lightbox (คงเดิม) --- */
.loading-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 60vh;
}

.spinner {
    border: 4px solid #e2e8f0;
    border-top: 4px solid #000;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin-bottom: 15px;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

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
}

.lightbox-img {
    max-width: 90%;
    max-height: 90vh;
    object-fit: contain;
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
    opacity: 0.7;
}

.btn-close-lightbox:hover {
    opacity: 1;
}

.btn-nav {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(255, 255, 255, 0.1);
    border: none;
    color: white;
    font-size: 2.5rem;
    cursor: pointer;
    padding: 15px 25px;
    border-radius: 12px;
}

.btn-nav.prev {
    left: 30px;
}

.btn-nav.next {
    right: 30px;
}

/* Sticky Navigation */
.sticky-nav-wrapper {
    position: sticky;
    top: 0;
    z-index: 100;
    background: white;
    border-bottom: 1px solid #e0e0e0;
    height: 60px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.sticky-nav {
    display: flex;
    align-items: center;
    max-width: 1140px;
    margin: 0 auto;
    height: 100%;
}

.nav-links {
    display: flex;
    gap: 30px;
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
    position: relative;
    top: 1px;
}

.nav-links a:hover {
    color: #000;
}

.nav-links a.active {
    color: #00aa6c;
    border-bottom-color: #00aa6c;
}

/* Booking Deals in Sidebar */
.booking-card {
    margin-bottom: 20px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
}

.partner-deal {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #e2e8f0;
}

.partner-deal:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.btn-partner {
    background: #fcd34d;
    color: #000;
    font-weight: 700;
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 0.85rem;
    transition: 0.2s;
}

.btn-partner:hover {
    background: #f59e0b;
}

/* Recommended Places Section */
.recommended-section {
    margin-top: 40px;
    padding-top: 30px;
    border-top: 1px solid #e2e8f0;
}

.recommended-section h2 {
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: 20px;
    color: #0f172a;
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
    height: 140px;
    width: 100%;
}

.rec-img-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.rec-info {
    padding: 12px;
}

.rec-info h4 {
    margin: 0 0 8px;
    font-size: 0.95rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.3;
}

.rec-rating {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 0.8rem;
    color: #475569;
    font-weight: 600;
}

.rec-rating i {
    color: #00aa6c;
}

/* Large Map Section */
.large-map-section {
    margin-top: 40px;
    padding-top: 30px;
    border-top: 1px solid #e2e8f0;
}

.large-map-section h2 {
    font-size: 1.5rem;
    font-weight: 800;
    margin: 0 0 10px;
    color: #0f172a;
}

.map-address {
    font-size: 1rem;
    color: #475569;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.large-map-container {
    width: 100%;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}

/* Nearby Section */
.nearby-section {
    margin-top: 40px;
    padding-top: 30px;
    border-top: 1px solid #e2e8f0;
}

.nearby-grid {
    display: grid;
    grid-template-columns: 1.2fr 1.5fr 1.5fr;
    gap: 30px;
}

.nearby-col h3 {
    font-size: 1.15rem;
    font-weight: 800;
    margin: 0 0 5px;
    color: #0f172a;
}

.col-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 2px solid #000;
    padding-bottom: 15px;
    margin-bottom: 15px;
}

.col-header span {
    font-size: 0.85rem;
    color: #475569;
}

.btn-text-link {
    background: none;
    border: none;
    color: #000;
    font-weight: 700;
    text-decoration: underline;
    cursor: pointer;
    font-size: 0.85rem;
    padding: 0;
}

.btn-text-link:hover {
    color: #00aa6c;
}

/* Getting there column */
.getting-there-col {
    padding-right: 20px;
}

.getting-there-col h3 {
    border-bottom: none;
    margin-bottom: 20px;
}

.walk-score-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.score-title {
    display: block;
    font-weight: 700;
    color: #00aa6c;
    font-size: 0.95rem;
    margin-bottom: 4px;
}

.score-title i {
    color: #64748b;
    font-size: 0.8rem;
}

.score-desc {
    font-size: 0.8rem;
    color: #475569;
}

.score-number {
    font-size: 1.8rem;
    font-weight: 800;
    color: #00aa6c;
}

.airport-info p {
    margin: 0 0 5px;
    font-size: 0.95rem;
}

.airport-info i {
    color: #64748b;
    margin-right: 8px;
}

.distance-line {
    font-size: 0.85rem;
    color: #475569;
    padding-left: 24px;
}
.side-icon {
    font-size: 0.8rem!important;
    margin-right: 4px!important;
}

/* List Items */
.nearby-list {
    display: flex;
    flex-direction: column;
}

.nearby-item {
    padding: 15px 0;
    border-bottom: 1px solid #e2e8f0;
    cursor: pointer;
}

.nearby-item:last-child {
    border-bottom: none;
}

.nearby-item:hover h4 {
    text-decoration: underline;
}

.nearby-item h4 {
    margin: 0 0 6px;
    font-size: 0.95rem;
    font-weight: 700;
}

.n-rating {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 6px;
    font-size: 0.85rem;
}

.n-score {
    font-weight: 700;
}

.n-rating .bubbles i {
    color: #00aa6c;
    font-size: 0.75rem;
}

.n-reviews {
    color: #475569;
    font-size: 0.8rem;
    text-decoration: underline;
}

.n-meta {
    font-size: 0.85rem;
    color: #475569;
}

.n-meta i {
    color: #94a3b8;
    margin-right: 4px;
}

@media (max-width: 992px) {
    .nearby-grid {
        grid-template-columns: 1fr;
        gap: 40px;
    }
    .getting-there-col {
        padding-right: 0;
        border-right: none;
    }
}

@media (max-width: 992px) {
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
