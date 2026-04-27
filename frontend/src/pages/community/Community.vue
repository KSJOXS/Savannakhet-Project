<template>
  <div class="community-page">
    <Navbar />
    
    <div class="community-container">
      <div class="feed-header">
        <h1>{{ t('nav.communityFeed') || 'Community Feed' }}</h1>
        <p>{{ t('recommend.hero_subtitle') }}</p>
      </div>

      <!-- Write Post Box -->
      <div v-if="user" class="write-post-card">
        <div class="write-post-header">
          <img :src="getUserAvatar(user.profile_image)" alt="avatar" class="mini-avatar" />
          <div class="fake-input" @click="showPostModal = true">
            {{ t('place.writeReviewPlaceholder') || "What's on your mind?" }}
          </div>
        </div>
        <div class="write-post-footer">
          <button class="btn-action" @click="showPostModal = true">
            <i class="fas fa-camera text-success"></i> Photo/Video
          </button>
          <button class="btn-action" @click="showPostModal = true">
            <i class="fas fa-map-marker-alt text-danger"></i> Check In
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
            <p class="comment-text">{{ post.comment }}</p>
          </div>

          <!-- Image Gallery -->
          <div v-if="post.images && post.images.length > 0" class="post-images">
            <div class="image-grid" :class="`images-${Math.min(post.images.length, 3)}`">
              <div v-for="(img, idx) in post.images.slice(0, 3)" :key="idx" class="img-wrapper" @click="openLightbox(post.images, idx)">
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

          <!-- Comments Section -->
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
                    <button v-if="user && user.username === c.username" @click="deleteComment(post.id, c.id)" class="btn-delete-comment">Delete</button>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="user" class="comment-input-area">
              <img :src="getUserAvatar(user.profile_image)" alt="avatar" class="comment-avatar" />
              <div class="comment-input-wrapper">
                <input type="text" v-model="newCommentTexts[post.id]" placeholder="Write a comment..." @keyup.enter="submitComment(post)" />
                <button @click="submitComment(post)" :disabled="!newCommentTexts[post.id]?.trim()"><i class="fas fa-paper-plane"></i></button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Post Modal -->
    <div v-if="showPostModal" class="modal-overlay" @click="showPostModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ t('nav.writePost') || 'Create Post' }}</h2>
          <button class="close-btn" @click="showPostModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <!-- Place Search -->
          <div class="form-group">
            <label><i class="fas fa-map-marker-alt"></i> Tag a Place (Optional)</label>
            <div class="search-place-wrapper">
              <input type="text" v-model="placeSearchQuery" @input="searchPlaces" placeholder="Search a place to tag..." />
              <div v-if="searchResults.length > 0" class="search-results">
                <div v-for="p in searchResults" :key="p.id" class="search-item" @click="selectPlace(p)">
                  {{ p.name }}
                </div>
              </div>
              <div v-if="selectedPlace" class="selected-place-badge">
                {{ selectedPlace.name }} <i class="fas fa-times" @click="selectedPlace = null"></i>
              </div>
            </div>
          </div>

          <!-- Rating -->
          <div class="form-group" v-if="selectedPlace">
            <label>Rating</label>
            <div class="rating-picker">
              <i v-for="s in 5" :key="s" @click="newPost.rating = s" :class="[newPost.rating >= s ? 'fas' : 'far', 'fa-star']"></i>
            </div>
          </div>

          <!-- Comment -->
          <div class="form-group">
            <textarea v-model="newPost.comment" placeholder="Describe your experience..."></textarea>
          </div>

          <!-- Images -->
          <div class="form-group">
            <label class="btn-upload">
              <i class="fas fa-images"></i> Add Photos
              <input type="file" multiple accept="image/*" @change="handleImageUpload" hidden />
            </label>
            <div class="image-previews">
              <div v-for="(src, idx) in imagePreviews" :key="idx" class="preview-thumb">
                <img :src="src" />
                <button @click="removeImage(idx)">&times;</button>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-post" :disabled="submitting || !newPost.comment" @click="submitPost">
            {{ submitting ? 'Posting...' : 'Post' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Simple Lightbox -->
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
import Navbar from '@/components/Navbar.vue'
import { placeRepository } from '@/repositories/placeRepository'
import { useI18n } from '@/composables/useI18n'
import { useAuth } from '@/composables/useAuth'

const { t } = useI18n()
const { user } = useAuth()
const loading = ref(true)
const feed = ref([])
const showPostModal = ref(false)
const submitting = ref(false)

const placeSearchQuery = ref('')
const searchResults = ref([])
const selectedPlace = ref(null)

const newPost = ref({
  rating: 5,
  comment: ''
})
const postImages = ref([])
const imagePreviews = ref([])

const searchPlaces = async () => {
  if (placeSearchQuery.value.length < 2) {
    searchResults.value = []
    return
  }
  try {
    const res = await placeRepository.getAll()
    searchResults.value = res.data.filter(p => 
      p.name.toLowerCase().includes(placeSearchQuery.value.toLowerCase())
    ).slice(0, 5)
  } catch (err) { console.error(err) }
}

const selectPlace = (p) => {
  selectedPlace.value = p
  placeSearchQuery.value = ''
  searchResults.value = []
}

const handleImageUpload = (e) => {
  const files = Array.from(e.target.files)
  files.forEach(file => {
    postImages.value.push(file)
    imagePreviews.value.push(URL.createObjectURL(file))
  })
}

const removeImage = (idx) => {
  postImages.value.splice(idx, 1)
  imagePreviews.value.splice(idx, 1)
}

const submitPost = async () => {
  if (!user.value || !newPost.value.comment) return
  submitting.value = true
  try {
    const fd = new FormData()
    if (selectedPlace.value) {
      fd.append('place_id', selectedPlace.value.id)
      fd.append('rating', newPost.value.rating)
    }
    fd.append('user_id', user.value.id)
    fd.append('comment_text', newPost.value.comment)
    postImages.value.forEach(img => fd.append('images', img))

    await placeRepository.addComment(fd)
    
    // Reset and close
    showPostModal.value = false
    selectedPlace.value = null
    newPost.value = { rating: 5, comment: '' }
    postImages.value = []
    imagePreviews.value = []
    fetchFeed()
  } catch (err) {
    console.error("Post failed:", err)
    alert("Failed to post. Please try again.")
  } finally {
    submitting.value = false
  }
}

const lightbox = ref({
  show: false,
  images: [],
  index: 0
})

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

const isLiked = (post) => {
  return user.value && post.liked_by.includes(user.value.id)
}

const handleLike = async (post) => {
  if (!user.value) return alert('Please login to like posts')
  try {
    const res = await placeRepository.toggleLike(post.id, user.value.id)
    if (res.data.status === 'liked') {
      post.liked_by.push(user.value.id)
    } else {
      post.liked_by = post.liked_by.filter(id => id !== user.value.id)
    }
  } catch (err) {
    console.error("Like failed:", err)
  }
}

const showCommentsFor = ref(null)
const newCommentTexts = ref({})

const toggleComments = (postId) => {
  showCommentsFor.value = showCommentsFor.value === postId ? null : postId
}

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
  } catch (err) {
    console.error("Failed to post comment", err)
  }
}

const deleteComment = async (postId, commentId) => {
  if (!confirm('Delete this comment?')) return
  try {
    await placeRepository.deletePostComment(commentId, user.value.id)
    fetchFeed()
  } catch (err) {
    console.error("Failed to delete comment", err)
  }
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

const handleShare = (post) => {
  const url = `${window.location.origin}/#/places/${post.place_id}`
  navigator.clipboard.writeText(url)
  alert('Link to place copied to clipboard!')
}

const openLightbox = (images, index) => {
  lightbox.value = { show: true, images, index }
}

const nextImg = () => {
  lightbox.value.index = (lightbox.value.index + 1) % lightbox.value.images.length
}

const prevImg = () => {
  lightbox.value.index = (lightbox.value.index - 1 + lightbox.value.images.length) % lightbox.value.images.length
}

onMounted(fetchFeed)
</script>

<style scoped>
.community-page {
  background: #f0f2f5;
  min-height: 100vh;
}

.community-container {
  max-width: 700px;
  margin: 40px auto;
  padding: 0 15px;
}

/* Write Post Card */
.write-post-card {
  background: white;
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
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

.text-success { color: #45bd62; }
.text-danger { color: #f3425f; }

/* Modal Styles */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(5px);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-content {
  background: white;
  width: 100%;
  max-width: 550px;
  border-radius: 12px;
  box-shadow: 0 12px 28px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
  max-height: 90vh;
}

.modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #e4e6eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  font-size: 1.25rem;
  font-weight: 700;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  color: #1c1e21;
}

.search-place-wrapper {
  position: relative;
}

.search-place-wrapper input {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-top: 5px;
  z-index: 10;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.search-item {
  padding: 10px 15px;
  cursor: pointer;
}

.search-item:hover {
  background: #f0f2f5;
}

.selected-place-badge {
  margin-top: 10px;
  background: #e7f3ff;
  color: #1877f2;
  padding: 8px 15px;
  border-radius: 8px;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}

.selected-place-badge i {
  cursor: pointer;
}

.rating-picker {
  display: flex;
  gap: 10px;
  font-size: 1.5rem;
  color: #f5c330;
}

.rating-picker i {
  cursor: pointer;
}

.modal-body textarea {
  width: 100%;
  height: 120px;
  border: none;
  font-size: 1.1rem;
  resize: none;
  outline: none;
}

.btn-upload {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

.image-previews {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  flex-wrap: wrap;
}

.preview-thumb {
  position: relative;
  width: 80px;
  height: 80px;
}

.preview-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.preview-thumb button {
  position: absolute;
  top: -5px;
  right: -5px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.modal-footer {
  padding: 15px 20px;
  border-top: 1px solid #e4e6eb;
}

.btn-post {
  width: 100%;
  background: #1877f2;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
}

.btn-post:disabled {
  background: #e4e6eb;
  color: #bcc0c4;
  cursor: not-allowed;
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

.post-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
  margin-bottom: 20px;
  padding: 15px;
  transition: 0.3s;
}

.post-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
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
  background: #e7f3ff;
  color: #1877f2;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  text-decoration: none;
  transition: 0.2s;
}

.place-badge a:hover {
  background: #dbeafe;
}

.post-content {
  margin-bottom: 15px;
}

.rating-stars {
  color: #f5c330;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.comment-text {
  color: #050505;
  line-height: 1.5;
  font-size: 1rem;
  white-space: pre-wrap;
}

/* Image Gallery Styles */
.post-images {
  margin: 0 -15px 15px;
  background: #f0f2f5;
}

.image-grid {
  display: grid;
  gap: 2px;
  height: 400px;
}

.images-1 { grid-template-columns: 1fr; }
.images-2 { grid-template-columns: 1fr 1fr; }
.images-3 { grid-template-columns: 2fr 1fr; grid-template-rows: 1fr 1fr; }

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
  background: rgba(0,0,0,0.5);
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
  border-top: 1px solid #f0f2f5;
}

.btn-like, .btn-share {
  flex: 1;
  background: none;
  border: none;
  padding: 8px;
  border-radius: 6px;
  color: #65676b;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: 0.2s;
}

.btn-like:hover, .btn-share:hover {
  background: #f2f2f2;
}

.btn-like.liked {
  color: #e0245e;
}

.btn-like.liked i {
  animation: heartBeat 0.3s ease-in-out;
}

@keyframes heartBeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.3); }
  100% { transform: scale(1); }
}

/* Lightbox */
.lightbox-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.9);
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
  background: rgba(255,255,255,0.2);
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
  background: rgba(255,255,255,0.5);
}

/* Comments Section */
.comments-section {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #f0f2f5;
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
  background: #f0f2f5;
  padding: 8px 12px;
  border-radius: 18px;
  display: flex;
  flex-direction: column;
  word-break: break-word;
}

.comment-username {
  font-weight: 700;
  font-size: 0.85rem;
  color: #050505;
}

.comment-text-inline {
  font-size: 0.95rem;
  color: #050505;
}

.comment-meta {
  display: flex;
  gap: 15px;
  margin-top: 2px;
  margin-left: 12px;
  font-size: 0.75rem;
  color: #65676b;
}

.btn-delete-comment {
  background: none;
  border: none;
  color: #65676b;
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
  background: #f0f2f5;
  border-radius: 20px;
  overflow: hidden;
  padding-right: 5px;
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
  color: #1877f2;
  cursor: pointer;
  padding: 0 10px;
  font-size: 1.1rem;
}

.comment-input-wrapper button:disabled {
  color: #bcc0c4;
  cursor: not-allowed;
}

@media (max-width: 600px) {
  .feed-header h1 {
    font-size: 2rem;
  }
}

.loading-state, .empty-feed {
  text-align: center;
  padding: 60px;
  background: white;
  border-radius: 12px;
  color: #65676b;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #1877f2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 600px) {
  .feed-header h1 { font-size: 1.8rem; }
  .post-images { height: 300px; }
}
</style>
