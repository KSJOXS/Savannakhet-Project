<template>
    <div class="write-review-page">
        <Navbar />

        <div class="wr-container">
            <div class="ta-review-box">

                <div class="ta-rm-left">
                    <h1 class="ta-rm-title">{{ t('review.tellUsTitle') || 'Tell us, how was your visit?' }}</h1>

                    <div class="ta-place-selector">
                        <div v-if="!selectedPlace" class="search-place-wrapper">
                            <label>📍 {{ t('review.searchLabel') || 'Search for the place you visited:' }}</label>
                            <div class="ta-search-input">
                                <i class="fas fa-search"></i>
                                <input type="text" v-model="placeSearchQuery" @input="searchPlaces"
                                    :placeholder="t('review.searchPlaceholder') || 'Search hotels, restaurants, landmarks...'" />
                            </div>
                            <div v-if="searchResults.length > 0" class="search-results ta-results">
                                <div v-for="p in searchResults" :key="p.id" class="search-item ta-item"
                                    @click="selectPlace(p)">
                                    <img :src="getPlaceImage(p)" class="ta-tiny-img" />
                                    <div>
                                        <strong>{{ p.name }}</strong>
                                        <p class="ta-tiny-cat">{{ p.category_name || 'Place' }}</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div v-else class="ta-selected-card">
                            <div class="ta-selected-img">
                                <img :src="getPlaceImage(selectedPlace)" />
                            </div>
                            <div class="ta-selected-info">
                                <h3>{{ selectedPlace.name }}</h3>
                                <p><i class="fas fa-map-marker-alt"></i> Savannakhet, Laos</p>
                                <button class="ta-change-btn" @click="resetSelection">
                                    {{ t('review.changePlace') || 'Change Place' }}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="ta-rm-right">
                    <div class="ta-form-section">

                        <div class="ta-field" v-if="selectedPlace">
                            <label>{{ t('review.rateExperience') || 'How would you rate your experience?' }}</label>
                            <div class="ta-circle-rating">
                                <i v-for="s in 5" :key="s" @click="newPost.rating = s" @mouseenter="hoverRating = s"
                                    @mouseleave="hoverRating = 0"
                                    :class="[(hoverRating || newPost.rating) >= s ? 'fas' : 'far', 'fa-circle']">
                                </i>
                                <span class="ta-rating-text" v-if="newPost.rating || hoverRating">
                                    {{ ratingLabels[(hoverRating || newPost.rating) - 1] }}
                                </span>
                            </div>
                        </div>

                        <div class="ta-field">
                            <label>{{ t('review.titleLabel') || 'Title your review' }}</label>
                            <input type="text" v-model="newPost.title" class="ta-input"
                                :placeholder="t('review.titlePlaceholder') || 'Summarize your visit or highlight an interesting detail...'" />
                        </div>

                        <div class="ta-field">
                            <label>{{ t('review.writeLabel') || 'Write your review' }}</label>
                            <textarea v-model="newPost.comment" class="ta-textarea"
                                :placeholder="t('review.writePlaceholder') || 'Share the details of your experience...'"></textarea>
                            <div class="ta-char-count" :class="{ 'text-danger': newPost.comment.length > 1000 }">
                                {{ newPost.comment.length }}/1000 {{ t('common.characters') || 'chars' }}
                            </div>
                        </div>

                        <div class="ta-field">
                            <label>{{ t('review.addPhotos') || 'Add some photos (Optional)' }}</label>
                            <label class="ta-photo-dropzone">
                                <input type="file" multiple accept="image/*" @change="handleImageUpload" hidden />
                                <i class="fas fa-image"></i>
                                <strong>{{ t('review.clickToAdd') || 'Click to add photos' }}</strong>
                                <span>{{ t('review.orDrag') || 'or drag and drop' }}</span>
                            </label>

                            <div class="ta-image-previews" v-if="imagePreviews.length > 0">
                                <div v-for="(src, idx) in imagePreviews" :key="idx" class="ta-preview-thumb">
                                    <img :src="src" />
                                    <button type="button" @click="removeImage(idx)">&times;</button>
                                </div>
                            </div>
                        </div>

                        <div class="ta-submit-area">
                            <label class="ta-checkbox">
                                <input type="checkbox" v-model="newPost.agreed" />
                                <span>{{ t('review.certify') || `I certify that this review is based on my own
                                    experience and is my genuine opinion.` }}</span>
                            </label>

                            <!-- Validation hints -->
                            <div v-if="validationMsg" class="ta-validation-msg">
                                ⚠️ {{ validationMsg }}
                            </div>

                            <button class="ta-btn-submit"
                                :disabled="submitting || !newPost.comment || !newPost.agreed"
                                @click="submitPost">
                                <span v-if="submitting">⏳ {{ t('common.sending') || 'Sending...' }}</span>
                                <span v-else>{{ t('review.submitBtn') || 'Submit Review' }}</span>
                            </button>
                        </div>

                    </div>
                </div>

            </div>
        </div>
    </div>
    <!-- Toast Notification -->
    <transition name="toast-slide">
        <div v-if="toast.show" class="wr-toast" :class="toast.type">
            <span class="toast-icon">{{ toast.type === 'success' ? '✅' : '❌' }}</span>
            <span>{{ toast.message }}</span>
        </div>
    </transition>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import { placeRepository } from '@/repositories/placeRepository'
import { useAuth } from '@/composables/useAuth'
import { useI18n } from '@/composables/useI18n'

const router = useRouter()
const { user } = useAuth()
const { t } = useI18n()
const submitting = ref(false)
const validationMsg = ref('')

// Toast notification
const toast = ref({ show: false, message: '', type: 'success' })
const showToast = (message, type = 'success') => {
    toast.value = { show: true, message, type }
    setTimeout(() => { toast.value.show = false }, 3500)
}

const placeSearchQuery = ref('')
const searchResults = ref([])
const selectedPlace = ref(null)

const hoverRating = ref(0)

// Translated Labels for logic
const ratingLabels = computed(() => [
    t('rating.terrible') || 'Terrible',
    t('rating.poor') || 'Poor',
    t('rating.average') || 'Average',
    t('rating.good') || 'Good',
    t('rating.excellent') || 'Excellent'
])

const companions = computed(() => [
    t('companion.business') || 'Business',
    t('companion.couples') || 'Couples',
    t('companion.family') || 'Family',
    t('companion.friends') || 'Friends',
    t('companion.solo') || 'Solo'
])

const newPost = ref({
    rating: 0,
    visitDate: '',
    companion: '',
    title: '',
    comment: '',
    agreed: false
})
const postImages = ref([])
const imagePreviews = ref([])

const getPlaceImage = (p) => {
    if (!p) return '';
    let url = '';
    if (p.images && p.images.length > 0) url = p.images[0].image_url || p.images[0].url || p.images[0];
    else if (p.image_url) {
        try {
            if (p.image_url.startsWith('[')) url = JSON.parse(p.image_url)[0];
            else url = p.image_url;
        } catch (e) { url = p.image_url; }
    }
    if (!url) return 'https://via.placeholder.com/150?text=No+Image';
    return url.startsWith('http') ? url : `http://localhost:8000/${url.replace(/^\//, '')}`;
}

const searchPlaces = async () => {
    if (placeSearchQuery.value.length < 2) {
        searchResults.value = []
        return
    }
    try {
        const res = await placeRepository.getAll()
        searchResults.value = res.data.filter(p =>
            p.name.toLowerCase().includes(placeSearchQuery.value.toLowerCase())
        ).slice(0, 6)
    } catch (err) { console.error(err) }
}

const selectPlace = (p) => {
    selectedPlace.value = p
    placeSearchQuery.value = ''
    searchResults.value = []
    newPost.value.rating = 5 // Default rating 5 stars when selected
}

const resetSelection = () => {
    selectedPlace.value = null
    placeSearchQuery.value = ''
    searchResults.value = []
}

const handleImageUpload = (e) => {
    const files = Array.from(e.target.files)
    files.forEach(file => {
        postImages.value.push(file)
        imagePreviews.value.push(URL.createObjectURL(file))
    })
    e.target.value = null
}

const removeImage = (idx) => {
    postImages.value.splice(idx, 1)
    imagePreviews.value.splice(idx, 1)
}

const submitPost = async () => {
    validationMsg.value = ''

    // Check login
    if (!user.value) {
        showToast('กรุณาเข้าสู่ระบบก่อนเขียนรีวิว', 'error')
        setTimeout(() => router.push('/login'), 1500)
        return
    }
    if (!newPost.value.comment.trim()) {
        validationMsg.value = 'กรุณาเขียนรีวิวของคุณก่อน'
        return
    }
    if (!newPost.value.agreed) {
        validationMsg.value = 'กรุณายืนยันว่ารีวิวนี้เป็นความคิดเห็นของคุณจริงๆ'
        return
    }

    submitting.value = true
    try {
        const fd = new FormData()
        fd.append('user_id', user.value.id)

        // Place and rating are optional
        if (selectedPlace.value) {
            fd.append('place_id', selectedPlace.value.id)
            if (newPost.value.rating) {
                fd.append('rating', newPost.value.rating)
            }
        }

        let finalCommentText = newPost.value.comment.trim()
        if (newPost.value.title) finalCommentText = `**${newPost.value.title}**\n${finalCommentText}`

        fd.append('comment_text', finalCommentText)

        // Upload images
        postImages.value.forEach(img => fd.append('images', img))

        await placeRepository.addComment(fd)

        showToast('ส่งรีวิวสำเร็จ! 🎉 กำลังพาคุณกลับไปยัง Community...', 'success')

        // Reset form
        newPost.value = { rating: 0, title: '', comment: '', agreed: false }
        postImages.value = []
        imagePreviews.value = []
        selectedPlace.value = null

        setTimeout(() => router.push('/community'), 2000)
    } catch (err) {
        console.error('Post failed:', err)
        const errMsg = err?.response?.data?.detail || 'ไม่สามารถส่งรีวิวได้ กรุณาลองใหม่อีกครั้ง'
        showToast(errMsg, 'error')
    } finally {
        submitting.value = false
    }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

.write-review-page {
    background: #f1f5f9;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    padding-bottom: 50px;
}

.wr-container {
    max-width: 1000px;
    margin: 40px auto;
    padding: 0 20px;
}

.ta-review-box {
    background: #ffffff;
    border-radius: 16px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.05);
    display: flex;
    overflow: hidden;
    border: 1px solid #e2e8f0;
}

/* Left Column */
.ta-rm-left {
    width: 350px;
    background: #ffffff;
    border-right: 1px solid #e2e8f0;
    padding: 40px 30px;
    display: flex;
    flex-direction: column;
}

.ta-rm-title {
    font-size: 2rem;
    font-weight: 900;
    color: #00aa6c;
    line-height: 1.1;
    margin-bottom: 30px;
    letter-spacing: -1px;
}

.ta-place-selector label {
    font-weight: 700;
    color: #0f172a;
    display: block;
    margin-bottom: 10px;
}

.ta-search-input {
    position: relative;
    display: flex;
    align-items: center;
}

.ta-search-input i {
    position: absolute;
    left: 15px;
    color: #94a3b8;
}

.ta-search-input input {
    width: 100%;
    padding: 12px 15px 12px 40px;
    border: 1px solid #cbd5e1;
    border-radius: 30px;
    outline: none;
    font-family: inherit;
    font-size: 0.95rem;
    transition: 0.2s;
}

.ta-search-input input:focus {
    border-color: #00aa6c;
    box-shadow: 0 0 0 3px rgba(0, 170, 108, 0.1);
}

.ta-results {
    margin-top: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
}

.ta-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px;
    border-bottom: 1px solid #f1f5f9;
    cursor: pointer;
}

.ta-item:hover {
    background: #f8fafc;
}

.ta-item:last-child {
    border-bottom: none;
}

.ta-tiny-img {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    object-fit: cover;
}

.ta-item strong {
    display: block;
    font-size: 0.9rem;
    color: #0f172a;
}

.ta-tiny-cat {
    margin: 0;
    font-size: 0.75rem;
    color: #64748b;
}

/* Selected Place Card */
.ta-selected-card {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
}

.ta-selected-img img {
    width: 100%;
    height: 180px;
    object-fit: cover;
}

.ta-selected-info {
    padding: 15px;
}

.ta-selected-info h3 {
    margin: 0 0 5px;
    font-size: 1.1rem;
    font-weight: 800;
    color: #0f172a;
}

.ta-selected-info p {
    margin: 0 0 15px;
    font-size: 0.85rem;
    color: #64748b;
}

.ta-change-btn {
    background: white;
    border: 1px solid #cbd5e1;
    color: #475569;
    padding: 8px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    transition: 0.2s;
}

.ta-change-btn:hover {
    background: #f1f5f9;
    color: #0f172a;
}

/* Right Column (Form) */
.ta-rm-right {
    flex: 1;
    background: #ffffff;
    padding: 40px;
    position: relative;
}

.ta-form-section {
    max-width: 600px;
    margin: 0 auto;
}

/* Disabled Overlay */
.disabled-section {
    opacity: 0.4;
    pointer-events: none;
    filter: grayscale(100%);
}

.ta-overlay-lock {
    position: absolute;
    inset: 0;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
}

.ta-overlay-lock p {
    background: #0f172a;
    color: white;
    padding: 10px 20px;
    border-radius: 30px;
    font-weight: 700;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.ta-field {
    margin-bottom: 30px;
}

.ta-field label {
    display: block;
    font-size: 1.1rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 12px;
}

/* Rating Circles */
.ta-circle-rating {
    display: flex;
    align-items: center;
    gap: 10px;
}

.ta-circle-rating i {
    font-size: 2.2rem;
    color: #00aa6c;
    cursor: pointer;
    transition: 0.1s;
}

.ta-circle-rating i:hover {
    transform: scale(1.1);
}

.ta-rating-text {
    margin-left: 15px;
    font-weight: 700;
    color: #00aa6c;
    font-size: 1.1rem;
}

/* Inputs */
.ta-input {
    width: 100%;
    padding: 12px 15px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-family: inherit;
    font-size: 1rem;
    outline: none;
}

.ta-input:focus {
    border-color: #00aa6c;
    box-shadow: 0 0 0 3px rgba(0, 170, 108, 0.1);
}

/* Pills */
.ta-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.ta-pill {
    padding: 8px 18px;
    border: 1px solid #cbd5e1;
    border-radius: 30px;
    font-size: 0.9rem;
    font-weight: 600;
    color: #475569;
    cursor: pointer;
    transition: 0.2s;
    background: white;
}

.ta-pill:hover {
    border-color: #00aa6c;
    color: #00aa6c;
}

.ta-pill.active {
    background: #00aa6c;
    color: white;
    border-color: #00aa6c;
}

/* Textarea */
.ta-textarea {
    width: 100%;
    height: 140px;
    padding: 15px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    resize: vertical;
    font-family: inherit;
    font-size: 1rem;
    outline: none;
}

.ta-textarea:focus {
    border-color: #00aa6c;
}

.ta-char-count {
    text-align: right;
    font-size: 0.8rem;
    color: #64748b;
    margin-top: 5px;
}

/* Photo Upload */
.ta-photo-dropzone {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 30px;
    border: 2px dashed #cbd5e1;
    border-radius: 12px;
    background: white;
    cursor: pointer;
    transition: 0.2s;
}

.ta-photo-dropzone:hover {
    background: #f8fafc;
    border-color: #00aa6c;
}

.ta-photo-dropzone i {
    font-size: 2rem;
    color: #94a3b8;
    margin-bottom: 10px;
}

.ta-photo-dropzone strong {
    color: #0f172a;
}

.ta-photo-dropzone span {
    color: #64748b;
    font-size: 0.85rem;
}

.ta-image-previews {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 15px;
}

.ta-preview-thumb {
    position: relative;
    width: 80px;
    height: 80px;
}

.ta-preview-thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 8px;
}

.ta-preview-thumb button {
    position: absolute;
    top: -5px;
    right: -5px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
}

/* Submit Area */
.ta-submit-area {
    margin-top: 40px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.ta-checkbox {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 0.85rem;
    color: #475569;
    cursor: pointer;
}

.ta-checkbox input {
    margin-top: 3px;
}

.ta-btn-submit {
    background: #0f172a;
    color: white;
    font-size: 1.1rem;
    font-weight: 800;
    padding: 16px;
    border-radius: 30px;
    border: none;
    cursor: pointer;
    transition: 0.2s;
    text-align: center;
}

.ta-btn-submit:not(:disabled):hover {
    background: #00aa6c;
    box-shadow: 0 10px 20px rgba(0, 170, 108, 0.2);
}

.ta-btn-submit:disabled {
    background: #cbd5e1;
    cursor: not-allowed;
}

/* Validation Message */
.ta-validation-msg {
    background: #fff7ed;
    border: 1px solid #fed7aa;
    color: #c2410c;
    padding: 10px 15px;
    border-radius: 10px;
    font-size: 0.9rem;
    font-weight: 600;
}

/* Toast Notification */
.wr-toast {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 24px;
    border-radius: 50px;
    font-weight: 700;
    font-size: 0.95rem;
    z-index: 9999;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    min-width: 260px;
    justify-content: center;
}

.wr-toast.success {
    background: #0f172a;
    color: white;
}

.wr-toast.error {
    background: #ef4444;
    color: white;
}

.toast-icon {
    font-size: 1.2rem;
}

/* Toast animation */
.toast-slide-enter-active,
.toast-slide-leave-active {
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.toast-slide-enter-from,
.toast-slide-leave-to {
    opacity: 0;
    transform: translateX(-50%) translateY(30px);
}

/* Responsive */
@media (max-width: 800px) {
    .ta-review-box {
        flex-direction: column;
    }

    .ta-rm-left {
        width: 100%;
        border-right: none;
        border-bottom: 1px solid #e2e8f0;
        padding: 20px;
    }

    .ta-rm-right {
        padding: 20px;
    }

    .ta-rm-title {
        font-size: 1.6rem;
    }
}
</style>