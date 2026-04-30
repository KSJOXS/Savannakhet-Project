<template>
  <div class="community-page">
    <Navbar />

    <div class="community-container">
      <div class="feed-header">
        <h1>{{ t('nav.communityFeed') || 'Community Feed' }}</h1>
        <p>{{ t('recommend.hero_subtitle') }}</p>
      </div>

      <div v-if="user" class="write-post-card">
        <div class="write-post-header">
          <img :src="getUserAvatar(user.profile_image)" alt="avatar" class="mini-avatar" />
          <div class="fake-input" @click="goToWriteReview">
            {{ t('place.writeReviewPlaceholder') || "What's on your mind? Share your experience..." }}
          </div>
        </div>
        <div class="write-post-footer">
          <button class="btn-action" @click="goToWriteReview">
            <i class="fas fa-camera text-success"></i> Photo/Video
          </button>
          <button class="btn-action" @click="goToWriteReview">
            <i class="fas fa-map-marker-alt text-danger"></i> Check In Place
          </button>
        </div>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading the latest stories...</p>
      </div>

      <div v-else-if="feed.length === 0" class="empty-feed">
        <i class="fas fa-users"></i>
        <p>No posts yet. Be the first to share your experience!</p>
      </div>

      <div v-else class="feed-list">
        <div v-for="post in feed" :key="post.id" class="post-card">
          <div class="post-header">
            <div class="user-meta">
              <img :src="getUserAvatar(post.profile_image)" alt="avatar" class="user-avatar" />
              <div class="user-info">
                <span class="username">{{ post.username }}</span>
                <span class="post-date">{{ formatDate(post.visited_at) }}</span>
              </div>
            </div>
            <div class="place-badge" v-if="post.place_id">
              <router-link :to="`/places/${post.place_id}`">
                <i class="fas fa-map-marker-alt"></i> {{ post.place_name }}
              </router-link>
            </div>
          </div>

          <div class="post-content">
            <div class="rating-stars" v-if="post.place_id && post.rating">
              <i v-for="s in 5" :key="s" :class="[post.rating >= s ? 'fas' : 'far', 'fa-star']"></i>
            </div>
            <p class="comment-text" v-html="formatComment(post.comment)"></p>
          </div>

          <div v-if="post.images && post.images.length > 0" class="post-images">
            <div class="image-grid" :class="`images-${Math.min(post.images.length, 3)}`">
              <div v-for="(img, idx) in post.images.slice(0, 3)" :key="idx" class="img-wrapper"
                @click="openLightbox(post.images, idx)">
                <img :src="getImageUrl(img)" alt="post image" />
                <div v-if="idx === 2 && post.images.length > 3" class="more-overlay">
                  +{{ post.images.length - 3 }}
                </div>
              </div>
            </div>
          </div>

          <div class="post-footer">
            <button class="btn-like" :class="{ 'liked': isLiked(post) }" @click="handleLike(post)">
              <i :class="[isLiked(post) ? 'fas' : 'far', 'fa-heart']"></i>
              {{ post.liked_by.length }}
            </button>
            <button class="btn-share" @click="toggleComments(post.id)">
              <i class="far fa-comment"></i> Comment {{ post.post_comments?.length || '' }}
            </button>
          </div>

          <div v-if="showCommentsFor === post.id" class="comments-section">
            <div class="comments-list">
              <div v-for="c in post.post_comments" :key="c.id" class="comment-item">
                <img :src="getUserAvatar(c.profile_image)" alt="avatar" class="comment-avatar" />
                <div class="comment-body">
                  <div class="comment-bubble">
                    <span class="comment-username">{{ c.username }}</span>
                    <span class="comment-text-inline">{{ c.comment_text }}</span>
                  </div>
                  <div class="comment-meta">
                    <span class="comment-time">{{ formatTimeAgo(c.created_at) }}</span>
                    <button v-if="user && user.username === c.username" @click="deleteComment(post.id, c.id)"
                      class="btn-delete-comment">Delete</button>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="user" class="comment-input-area">
              <img :src="getUserAvatar(user.profile_image)" alt="avatar" class="comment-avatar" />
              <div class="comment-input-wrapper">
                <input type="text" v-model="newCommentTexts[post.id]" placeholder="Write a comment..."
                  @keyup.enter="submitComment(post)" />
                <button @click="submitComment(post)" :disabled="!newCommentTexts[post.id]?.trim()"><i
                    class="fas fa-paper-plane"></i></button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="lightbox.show" class="lightbox-overlay" @click="lightbox.show = false">
      <div class="lightbox-content" @click.stop>
        <button class="close-btn" @click="lightbox.show = false">&times;</button>
        <img :src="getImageUrl(lightbox.images[lightbox.index])" />
        <div v-if="lightbox.images.length > 1" class="nav-btns">
          <button @click="prevImg">❮</button>
          <button @click="nextImg">❯</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import { placeRepository } from '@/repositories/placeRepository'
import { useI18n } from '@/composables/useI18n'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { t } = useI18n()
const { user } = useAuth()
const loading = ref(true)
const feed = ref([])

const goToWriteReview = () => {
  router.push('/write-review')
}

// Format Comment
const formatComment = (text) => {
  if (!text) return '';
  let formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  return formatted.replace(/\n/g, '<br>');
}

const lightbox = ref({ show: false, images: [], index: 0 })

const fetchFeed = async () => {
  loading.value = true
  try {
    const res = await placeRepository.getCommunityFeed()
    feed.value = res.data
  } catch (err) {
    console.error("Failed to fetch feed:", err)
  } finally {
    loading.value = false
  }
}

const getImageUrl = (url) => {
  if (!url) return '';
  if (url.startsWith('http') || url.startsWith('data:')) return url;
  return `http://localhost:8000/${url.startsWith('/') ? url.slice(1) : url}`;
}

const getUserAvatar = (url) => {
  if (url) return getImageUrl(url);
  return 'https://ui-avatars.com/api/?background=random&color=fff&name=User';
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
  })
}

const isLiked = (post) => user.value && post.liked_by.includes(user.value.id)

const handleLike = async (post) => {
  if (!user.value) return alert('Please login to like posts')
  try {
    const res = await placeRepository.toggleLike(post.id, user.value.id)
    if (res.data.status === 'liked') post.liked_by.push(user.value.id)
    else post.liked_by = post.liked_by.filter(id => id !== user.value.id)
  } catch (err) { console.error("Like failed:", err) }
}

const showCommentsFor = ref(null)
const newCommentTexts = ref({})

const toggleComments = (postId) => showCommentsFor.value = showCommentsFor.value === postId ? null : postId

const submitComment = async (post) => {
  const text = newCommentTexts.value[post.id]?.trim()
  if (!text || !user.value) return
  try {
    const fd = new FormData()
    fd.append('user_id', user.value.id)
    fd.append('comment_text', text)
    await placeRepository.addPostComment(post.id, fd)
    newCommentTexts.value[post.id] = ''
    fetchFeed()
  } catch (err) { console.error("Failed to post comment", err) }
}

const deleteComment = async (postId, commentId) => {
  if (!confirm('Delete this comment?')) return
  try {
    await placeRepository.deletePostComment(commentId, user.value.id)
    fetchFeed()
  } catch (err) { console.error("Failed to delete comment", err) }
}

const formatTimeAgo = (dateStr) => {
  const diff = new Date() - new Date(dateStr)
  const minutes = Math.floor(diff / 60000)
  if (minutes < 1) return 'Just now'
  if (minutes < 60) return `${minutes}m`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}h`
  const days = Math.floor(hours / 24)
  return `${days}d`
}

const openLightbox = (images, index) => lightbox.value = { show: true, images, index }
const nextImg = () => lightbox.value.index = (lightbox.value.index + 1) % lightbox.value.images.length
const prevImg = () => lightbox.value.index = (lightbox.value.index - 1 + lightbox.value.images.length) % lightbox.value.images.length

onMounted(fetchFeed)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

.community-page {
  background: #f0f2f5;
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
}

.community-container {
  max-width: 700px;
  margin: 40px auto;
  padding: 0 15px;
}

.feed-header {
  text-align: center;
  margin-bottom: 30px;
}

.feed-header h1 {
  font-size: 2.5rem;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 10px;
}

.feed-header p {
  color: #65676b;
  font-size: 1.1rem;
}

.write-post-card {
  background: white;
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.write-post-header {
  display: flex;
  gap: 12px;
  align-items: center;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f2f5;
}

.mini-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.fake-input {
  flex: 1;
  background: #f0f2f5;
  padding: 10px 15px;
  border-radius: 20px;
  color: #65676b;
  cursor: pointer;
  transition: 0.2s;
}

.fake-input:hover {
  background: #e4e6eb;
}

.write-post-footer {
  display: flex;
  padding-top: 10px;
}

.btn-action {
  flex: 1;
  background: none;
  border: none;
  padding: 8px;
  border-radius: 8px;
  color: #65676b;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: 0.2s;
}

.btn-action:hover {
  background: #f2f2f2;
}

.text-success {
  color: #00aa6c;
}

.text-danger {
  color: #f3425f;
}

.post-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  padding: 15px;
  transition: 0.3s;
}

.post-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.user-meta {
  display: flex;
  gap: 12px;
}

.user-avatar {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #e0e0e0;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: 700;
  font-size: 1rem;
  color: #050505;
}

.post-date {
  font-size: 0.85rem;
  color: #65676b;
}

.place-badge a {
  background: #e6f7f0;
  color: #00aa6c;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  text-decoration: none;
  transition: 0.2s;
}

.place-badge a:hover {
  background: #00aa6c;
  color: white;
}

.post-content {
  margin-bottom: 15px;
}

.rating-stars {
  color: #00aa6c;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.comment-text {
  color: #0f172a;
  line-height: 1.6;
  font-size: 1rem;
  white-space: pre-wrap;
}

.post-images {
  margin: 0 -15px 15px;
  background: #f0f2f5;
}

.image-grid {
  display: grid;
  gap: 2px;
  height: 400px;
}

.images-1 {
  grid-template-columns: 1fr;
}

.images-2 {
  grid-template-columns: 1fr 1fr;
}

.images-3 {
  grid-template-columns: 2fr 1fr;
  grid-template-rows: 1fr 1fr;
}

.images-3 .img-wrapper:first-child {
  grid-row: span 2;
}

.img-wrapper {
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.img-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: 0.3s;
}

.img-wrapper:hover img {
  transform: scale(1.05);
}

.more-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 700;
}

.post-footer {
  display: flex;
  gap: 10px;
  padding-top: 10px;
  border-top: 1px solid #f1f5f9;
}

.btn-like,
.btn-share {
  flex: 1;
  background: none;
  border: none;
  padding: 8px;
  border-radius: 6px;
  color: #64748b;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: 0.2s;
}

.btn-like:hover,
.btn-share:hover {
  background: #f1f5f9;
}

.btn-like.liked {
  color: #ef4444;
}

.btn-like.liked i {
  animation: heartBeat 0.3s ease-in-out;
}

@keyframes heartBeat {
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.3);
  }

  100% {
    transform: scale(1);
  }
}

.lightbox-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lightbox-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
}

.lightbox-content img {
  max-width: 100%;
  max-height: 90vh;
  object-fit: contain;
}

.close-btn {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: white;
  font-size: 2rem;
  cursor: pointer;
}

.nav-btns {
  position: absolute;
  top: 50%;
  left: -50px;
  right: -50px;
  display: flex;
  justify-content: space-between;
  transform: translateY(-50%);
}

.nav-btns button {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 2rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  transition: 0.2s;
}

.nav-btns button:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Comments Section */
.comments-section {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #f1f5f9;
}

.comment-item {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
}

.comment-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.comment-body {
  display: flex;
  flex-direction: column;
}

.comment-bubble {
  background: #f1f5f9;
  padding: 8px 12px;
  border-radius: 18px;
  display: flex;
  flex-direction: column;
  word-break: break-word;
}

.comment-username {
  font-weight: 700;
  font-size: 0.85rem;
  color: #0f172a;
}

.comment-text-inline {
  font-size: 0.95rem;
  color: #334155;
}

.comment-meta {
  display: flex;
  gap: 15px;
  margin-top: 2px;
  margin-left: 12px;
  font-size: 0.75rem;
  color: #64748b;
}

.btn-delete-comment {
  background: none;
  border: none;
  color: #ef4444;
  cursor: pointer;
  padding: 0;
  font-size: 0.75rem;
}

.btn-delete-comment:hover {
  text-decoration: underline;
}

.comment-input-area {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.comment-input-wrapper {
  flex: 1;
  display: flex;
  background: #f1f5f9;
  border-radius: 20px;
  overflow: hidden;
  padding-right: 5px;
  border: 1px solid #cbd5e1;
}

.comment-input-wrapper input {
  flex: 1;
  background: transparent;
  border: none;
  padding: 10px 15px;
  outline: none;
  font-size: 0.95rem;
}

.comment-input-wrapper button {
  background: transparent;
  border: none;
  color: #00aa6c;
  cursor: pointer;
  padding: 0 10px;
  font-size: 1.1rem;
}

.comment-input-wrapper button:disabled {
  color: #94a3b8;
  cursor: not-allowed;
}

.loading-state,
.empty-feed {
  text-align: center;
  padding: 60px;
  background: white;
  border-radius: 12px;
  color: #64748b;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f1f5f9;
  border-top: 4px solid #00aa6c;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@media (max-width: 600px) {
  .feed-header h1 {
    font-size: 1.8rem;
  }

  .post-images {
    height: 300px;
  }
}
</style>