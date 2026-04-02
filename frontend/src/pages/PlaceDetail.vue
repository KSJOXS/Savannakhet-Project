<template>
    <div class="detail-page">
        <nav class="navbar-custom">
            <div class="nav-container">
                <div class="nav-logo">
                    <span class="logo-emoji">🌴</span> Savannakhet Smart Travel
                </div>
                <div class="nav-menu">
                    <router-link to="/">หน้าแรก</router-link>
                    <router-link to="/explore" class="btn-explore-nav">ค้นหาสถานที่</router-link>
                    <div v-if="user" class="user-profile">
                        <span class="user-name">สวัสดี, <strong>{{ user.username }}</strong></span>
                        <button @click="logout" class="btn-logout">ออกจากระบบ</button>
                    </div>
                    <div v-else class="auth-buttons">
                        <router-link to="/login">เข้าสู่ระบบ</router-link>
                        <router-link to="/register" class="btn-register-nav">สมัครสมาชิก</router-link>
                    </div>
                </div>
            </div>
        </nav>

        <div class="detail-content-container" v-if="place">
            <button @click="router.back()" class="btn-back-link">
                <i class="fas fa-chevron-left"></i> ย้อนกลับ
            </button>

            <div class="top-split-layout">
                <div class="place-visual-card">
                    <div class="image-wrapper">
                        <img :src="place.image_url || 'https://via.placeholder.com/800x450'" class="place-img" />
                        <div class="cat-tag">{{ getCategoryName(place.category_id) }}</div>
                    </div>
                    <div class="place-header-info">
                        <h1>{{ place.name }}</h1>
                        <div class="rating-badge">
                            <i class="fas fa-star"></i> {{ place.rating_avg || '0.0' }}
                        </div>
                    </div>
                </div>

                <div class="comment-sidebar">
                    <div class="glass-card">
                        <h3>รีวิวสถานที่นี้</h3>
                        <div class="rating-selector">
                            <i v-for="star in 5" :key="star" :class="[newRating >= star ? 'fas' : 'far', 'fa-star']"
                                @click="newRating = star"></i>
                        </div>
                        <textarea v-model="newComment" placeholder="เขียนความประทับใจของคุณ..."></textarea>
                        <button class="btn-send-review" @click="submitComment" :disabled="submitting">
                            {{ submitting ? 'กำลังส่ง...' : 'ส่งรีวิว' }}
                        </button>

                        <div class="review-history mt-4">
                            <p class="history-title">รีวิวจากนักท่องเที่ยว ({{ comments.length }})</p>
                            <div class="scroll-comments">
                                <div v-if="comments.length === 0" class="no-comments-msg">ยังไม่มีรีวิวในขณะนี้</div>
                                <div v-for="comment in comments" :key="comment.id" class="mini-comment-item">
                                    <div class="u-info">
                                        <strong>{{ comment.username }}</strong>
                                        <span class="u-stars">
                                            <i v-for="s in 5" :key="s"
                                                :class="[comment.rating >= s ? 'fas' : 'far', 'fa-star']"></i>
                                        </span>
                                    </div>
                                    <p>{{ comment.comment_text }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="bottom-details-card mt-4">
                <section class="desc-section">
                    <h2 class="section-h"><i class="fas fa-align-left"></i> รายละเอียดสถานที่</h2>
                    <p class="text-desc">{{ place.description }}</p>
                </section>

                <section class="map-section mt-5">
                    <h2 class="section-h"><i class="fas fa-map-marked-alt"></i> แผนที่และตำแหน่งที่ตั้ง</h2>
                    <div class="map-frame-container">
                        <iframe width="100%" height="450" frameborder="0" style="border:0; border-radius: 20px;"
                            :src="`https://www.google.com/maps?q=${place.lat},${place.lng}&output=embed`"
                            allowfullscreen>
                        </iframe>
                    </div>
                    <button class="btn-open-google" @click="openMap">
                        <i class="fab fa-google"></i> เปิดใน Google Maps
                    </button>
                </section>
            </div>
        </div>

        <div v-else class="loading-screen">
            <div class="loader"></div>
            <p>กำลังเตรียมข้อมูลสถานที่...</p>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const place = ref(null)
const categories = ref([])
const comments = ref([])
const user = ref(JSON.parse(localStorage.getItem('user')))

const newComment = ref('')
const newRating = ref(5)
const submitting = ref(false)

const fetchData = async () => {
    const id = route.params.id
    try {
        const [resPlace, resCats] = await Promise.all([
            axios.get(`http://127.0.0.1:8000/places/${id}`),
            axios.get('http://127.0.0.1:8000/categories')
        ])
        place.value = resPlace.data
        categories.value = resCats.data

        // ดึงคอมเมนต์แยกเพื่อป้องกัน 404
        try {
            const resComm = await axios.get(`http://127.0.0.1:8000/places/${id}/comments`)
            comments.value = resComm.data
        } catch (e) { comments.value = [] }
    } catch (err) { console.error(err) }
}

const submitComment = async () => {
    if (!user.value) return router.push('/login')
    if (!newComment.value.trim()) return alert('กรุณาพิมพ์ข้อความรีวิว')

    submitting.value = true
    try {
        await axios.post(`http://127.0.0.1:8000/places/${route.params.id}/comments`, {
            user_id: user.value.id,
            rating: newRating.value,
            comment_text: newComment.value
        })
        newComment.value = ''; newRating.value = 5;
        fetchData()
    } catch (err) { alert('ส่งไม่สำเร็จ') } finally { submitting.value = false }
}

const logout = () => {
    localStorage.removeItem('user');
    user.value = null;
    router.push('/login');
}

const getCategoryName = (id) => categories.value.find(c => c.id === id)?.name || 'ทั่วไป'
const openMap = () => window.open(`https://www.google.com/maps?q=${place.value.lat},${place.value.lng}`, '_blank')

onMounted(fetchData)
</script>

<style scoped>
.detail-page {
    background-color: #207cca;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
}

/* 🧭 Navbar เหมือนเดิม */
.navbar-custom {
    background: white;
    padding: 15px 50px;
    display: flex;
    justify-content: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.nav-container {
    width: 100%;
    max-width: 1200px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-logo {
    font-weight: 800;
    font-size: 1.2rem;
    color: #2c3e50;
    display: flex;
    align-items: center;
    gap: 8px;
}

.nav-menu {
    display: flex;
    align-items: center;
    gap: 20px;
}

.nav-menu a {
    text-decoration: none;
    color: #64748b;
    font-weight: 500;
}

.btn-explore-nav {
    background: #e0f2fe;
    color: #0369a1 !important;
    padding: 8px 16px;
    border-radius: 50px;
}

.btn-register-nav {
    background: #3498db;
    color: white !important;
    padding: 8px 16px;
    border-radius: 50px;
}

.btn-logout {
    background: #fee2e2;
    color: #dc2626;
    border: none;
    padding: 6px 12px;
    border-radius: 8px;
    cursor: pointer;
}

/* 🏠 Main Container */
.detail-content-container {
    max-width: 1200px;
    margin: 30px auto;
    padding: 0 20px;
}

.btn-back-link {
    background: rgba(255, 255, 255, 0.2);
    border: none;
    color: white;
    padding: 8px 18px;
    border-radius: 50px;
    cursor: pointer;
    margin-bottom: 20px;
    transition: 0.3s;
}

.btn-back-link:hover {
    background: rgba(255, 255, 255, 0.3);
}

/* 🔀 Split Layout (ซ้าย-ขวา ไม่ซ้อน) */
.top-split-layout {
    display: flex;
    gap: 30px;
    align-items: stretch;
}

@media (max-width: 992px) {
    .top-split-layout {
        flex-direction: column;
    }
}

.place-visual-card {
    flex: 1.6;
    background: white;
    border-radius: 30px;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.image-wrapper {
    position: relative;
    height: 400px;
}

.place-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.cat-tag {
    position: absolute;
    top: 20px;
    left: 20px;
    background: #3498db;
    color: white;
    padding: 5px 15px;
    border-radius: 50px;
    font-weight: bold;
}

.place-header-info {
    padding: 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.place-header-info h1 {
    font-size: 2.2rem;
    margin: 0;
    color: #1e293b;
}

.rating-badge {
    font-size: 1.3rem;
    color: #f59e0b;
    font-weight: bold;
}

.comment-sidebar {
    flex: 1;
}

.glass-card {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    padding: 30px;
    border-radius: 30px;
    height: 100%;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.glass-card h3 {
    color: #1e293b;
    margin-top: 0;
}

.rating-selector {
    color: #f1c40f;
    font-size: 1.8rem;
    cursor: pointer;
    margin: 15px 0;
}

textarea {
    width: 100%;
    height: 100px;
    padding: 15px;
    border-radius: 15px;
    border: 1px solid #e2e8f0;
    background: #f8fafc;
    margin-bottom: 15px;
    resize: none;
}

.btn-send-review {
    width: 100%;
    background: #3498db;
    color: white;
    border: none;
    padding: 12px;
    border-radius: 12px;
    font-weight: bold;
    cursor: pointer;
}

/* 📜 Review History */
.scroll-comments {
    max-height: 200px;
    overflow-y: auto;
    margin-top: 15px;
}

.mini-comment-item {
    background: white;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    border: 1px solid #f1f5f9;
}

.u-info {
    display: flex;
    justify-content: space-between;
    font-size: 0.9rem;
    margin-bottom: 4px;
}

.u-stars {
    color: #f1c40f;
    font-size: 0.7rem;
}

.history-title {
    font-weight: bold;
    color: #64748b;
    margin-bottom: 5px;
}

/* 📄 Bottom Details */
.bottom-details-card {
    background: white;
    border-radius: 30px;
    padding: 50px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.section-h {
    font-size: 1.4rem;
    color: #334155;
    margin-bottom: 20px;
    border-left: 5px solid #3498db;
    padding-left: 15px;
}

.text-desc {
    line-height: 1.8;
    color: #475569;
    font-size: 1.1rem;
}

.map-frame-container {
    overflow: hidden;
    border-radius: 25px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

.btn-open-google {
    margin-top: 20px;
    background: #2c3e50;
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: 12px;
    font-weight: bold;
    cursor: pointer;
}

/* 🌀 Loading */
.loading-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 80vh;
    color: white;
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
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}
</style>