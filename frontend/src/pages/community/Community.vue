<template>
  <div class="community-page">
    <Navbar />

    <div class="community-layout">
      <!-- Left Sidebar (Facebook Style) -->
      <aside class="fb-left-sidebar" v-if="user">
        <router-link to="/profile" class="fb-sidebar-item">
          <img :src="getUserAvatar(user.profile_image)" alt="avatar" class="sidebar-avatar" />
          <span class="sidebar-text">{{ user.username }}</span>
        </router-link>
        
        <router-link to="/profile?tab=trips" class="fb-sidebar-item">
          <div class="sidebar-icon-wrap" style="background: #e6f7f0; color: #00aa6c;">
            <i class="fas fa-bookmark"></i>
          </div>
          <span class="sidebar-text">{{ t('nav.myTrips', 'Saved Places') }}</span>
        </router-link>
        
        <router-link to="/profile?tab=reviews" class="fb-sidebar-item">
          <div class="sidebar-icon-wrap" style="background: #e0f2fe; color: #0284c7;">
            <i class="fas fa-history"></i>
          </div>
          <span class="sidebar-text">{{ t('nav.myReviews', 'My Reviews') }}</span>
        </router-link>
        
        <router-link to="/explore" class="fb-sidebar-item">
          <div class="sidebar-icon-wrap" style="background: #fdf4ff; color: #c026d3;">
            <i class="fas fa-compass"></i>
          </div>
          <span class="sidebar-text">{{ t('nav.exploreAll', 'Explore Places') }}</span>
        </router-link>
      </aside>

      <div class="community-container">

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
            <div class="header-right">
              <div class="place-badge" v-if="post.place_id">
                <router-link :to="`/places/${post.place_id}`">
                  <i class="fas fa-map-marker-alt"></i> {{ post.place_name }}
                </router-link>
              </div>
              <div v-if="user && user.id === post.user_id" class="post-options">
                <button @click.stop="togglePostMenu(post.id)" class="btn-dots">
                  <i class="fas fa-ellipsis-h"></i>
                </button>
                <div v-if="activePostMenu === post.id" class="options-dropdown" v-click-outside="() => activePostMenu = null">
                  <button @click.stop="openEditModal(post)"><i class="fas fa-edit"></i> Edit</button>
                  <button @click.stop="handleDeletePost(post.id)" class="text-danger"><i class="fas fa-trash"></i> Delete</button>
                </div>
              </div>
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
    </div>

    <!-- Lightbox -->
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

    <!-- Edit Post Modal (Facebook Style) -->
    <div v-if="editModal.show" class="modal-overlay" @click="closeEditModal">
      <div class="edit-modal fb-style" @click.stop>
        <div class="modal-header">
          <h3>Edit Post</h3>
          <button class="close-btn-circle" @click="closeEditModal">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="modal-body-content">
            <!-- User Profile Info -->
            <div class="modal-user-header">
              <img :src="getUserAvatar(user?.profile_image)" class="modal-avatar" />
              <div class="modal-user-info">
                <span class="modal-username">{{ user?.username }}</span>
                <div class="modal-privacy">
                  <i class="fas fa-globe-asia"></i> Public <i class="fas fa-caret-down"></i>
                </div>
              </div>
            </div>

            <!-- Rating (if applicable) -->
            <div class="modal-rating-section" v-if="editModal.post.place_id">
              <label>Rating:</label>
              <div class="ta-circle-rating">
                <i v-for="s in 5" :key="s" @click="editModal.form.rating = s"
                   :class="[editModal.form.rating >= s ? 'fas' : 'far', 'fa-circle']">
                </i>
              </div>
            </div>

            <!-- Comment Textarea -->
            <div class="modal-content-area">
              <textarea v-model="editModal.form.comment" class="fb-textarea" 
                        :placeholder="`What's on your mind, ${user?.username}?`"></textarea>
            </div>

            <!-- Image Management Area -->
            <div class="modal-image-area">
              <!-- Combined Image List -->
              <div v-if="editModal.form.existingImages.length > 0 || editModal.form.newImages.length > 0" class="modal-image-grid">
                  <!-- Old Images -->
                  <div v-for="(img, idx) in editModal.form.existingImages" :key="'old-'+idx" class="modal-img-wrap">
                    <img :src="getImageUrl(img)" />
                    <button class="btn-remove-img" @click="removeExistingImg(idx)">&times;</button>
                  </div>
                  <!-- New Images -->
                  <div v-for="(img, idx) in editModal.form.newPreviews" :key="'new-'+idx" class="modal-img-wrap">
                    <img :src="img" />
                    <button class="btn-remove-img" @click="removeNewImg(idx)">&times;</button>
                  </div>
              </div>

              <!-- Add Images Button -->
              <label class="modal-add-img-btn" v-if="editModal.form.existingImages.length + editModal.form.newImages.length < 5">
                <input type="file" multiple accept="image/*" @change="handleEditImageUpload" hidden />
                <div class="add-img-content">
                  <i class="fas fa-images"></i>
                  <span>Add Photos/Videos</span>
                </div>
              </label>
            </div>
          </div>
        </div>

        <div class="modal-footer fb-footer">
          <button class="btn-fb-save" @click="saveEdit" :disabled="saving || !editModal.form.comment.trim()">
            {{ saving ? 'Updating...' : 'Save Changes' }}
          </button>
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
const saving = ref(false)

// Edit Modal State
const editModal = ref({ 
  show: false, 
  post: {}, 
  form: { 
    rating: 0, 
    comment: '',
    existingImages: [],
    newImages: [],
    newPreviews: []
  } 
})

const closeEditModal = () => {
  editModal.value.show = false
}

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
  return `http://127.0.0.1:8000/${url.startsWith('/') ? url.slice(1) : url}`;
}

const getUserAvatar = (url) => {
  if (url) return getImageUrl(url);
  return 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23ccc"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/></svg>';
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

// Post Menu (Edit/Delete)
const activePostMenu = ref(null)
const togglePostMenu = (postId) => {
  activePostMenu.value = activePostMenu.value === postId ? null : postId
}

const handleDeletePost = async (postId) => {
  if (!confirm('Are you sure you want to delete this post?')) return
  try {
    await placeRepository.deleteUserReview(postId, user.value.id)
    fetchFeed()
  } catch (err) {
    console.error("Delete failed:", err)
    alert("Failed to delete post")
  }
}

const openEditModal = (post) => {
  editModal.value = {
    show: true,
    post: post,
    form: {
      rating: post.rating || 0,
      comment: post.comment || '',
      existingImages: [...(post.images || [])],
      newImages: [],
      newPreviews: []
    }
  }
  activePostMenu.value = null
}

const handleEditImageUpload = (e) => {
  const files = Array.from(e.target.files)
  files.forEach(file => {
    editModal.value.form.newImages.push(file)
    editModal.value.form.newPreviews.push(URL.createObjectURL(file))
  })
}

const removeExistingImg = (idx) => {
  editModal.value.form.existingImages.splice(idx, 1)
}

const removeNewImg = (idx) => {
  editModal.value.form.newImages.splice(idx, 1)
  editModal.value.form.newPreviews.splice(idx, 1)
}

const saveEdit = async () => {
  if (!editModal.value.form.comment.trim()) return
  saving.value = true
  try {
    const fd = new FormData()
    fd.append('user_id', user.value.id)
    fd.append('rating', editModal.value.form.rating)
    fd.append('comment_text', editModal.value.form.comment)
    fd.append('existing_images', JSON.stringify(editModal.value.form.existingImages))
    
    // Append new images
    editModal.value.form.newImages.forEach(img => {
      fd.append('new_images', img)
    })
    
    await placeRepository.updateUserReview(editModal.value.post.id, fd)
    editModal.value.show = false
    fetchFeed()
  } catch (err) {
    console.error("Edit failed:", err)
    alert("Failed to update post")
  } finally {
    saving.value = false
  }
}

// Custom directive for clicking outside
const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event);
      }
    };
    document.addEventListener('click', el.clickOutsideEvent);
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent);
  },
}

onMounted(fetchFeed)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

.community-page {
  background: #f0f2f5;
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
}

.community-layout {
  display: flex;
  max-width: 1200px;
  margin: 20px auto;
  gap: 20px;
  padding: 0 15px;
}

.fb-left-sidebar {
  width: 280px;
  position: sticky;
  top: 100px;
  height: max-content;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

@media (max-width: 900px) {
  .fb-left-sidebar {
    display: none;
  }
}

.fb-sidebar-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px;
  border-radius: 8px;
  text-decoration: none;
  color: #050505;
  font-weight: 600;
  transition: 0.2s;
}

.fb-sidebar-item:hover {
  background: #e4e6eb;
}

.sidebar-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
}

.sidebar-icon-wrap {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
}

.sidebar-text {
  font-size: 0.95rem;
}

.community-container {
  flex: 1;
  max-width: 780px;
  width: 100%;
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
  align-items: center;
  margin-bottom: 15px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.post-options {
  position: relative;
}

.btn-dots {
  background: none;
  border: none;
  color: #65676b;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
  transition: 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-dots:hover {
  background: #f0f2f5;
}

.options-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  z-index: 100;
  width: 150px;
  overflow: hidden;
  border: 1px solid #e4e6eb;
}

.options-dropdown button {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 15px;
  border: none;
  background: none;
  font-size: 0.9rem;
  font-weight: 600;
  color: #050505;
  cursor: pointer;
  text-align: left;
}

.options-dropdown button:hover {
  background: #f2f2f2;
}

.options-dropdown button.text-danger {
  color: #f3425f;
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

/* Modals & Overlay */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 11000;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(4px);
}

/* Facebook Style Edit Modal */
.fb-style {
  width: 95%;
  max-width: 600px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 12px 28px 0 rgba(0, 0, 0, 0.2), 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  max-height: 90vh;
  position: relative;
  overflow: hidden;
}

.modal-header {
  padding: 18px 20px;
  border-bottom: 1px solid #e4e6eb;
  position: relative;
  text-align: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #050505;
}

.close-btn-circle {
  position: absolute;
  top: 12px;
  right: 15px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #e4e6eb;
  border: none;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #606770;
  transition: background 0.2s;
}

.close-btn-circle:hover {
  background: #d8dadf;
}

.modal-body {
  padding: 16px;
  overflow-y: auto;
}

.modal-body-content {
  padding: 0 4px;
}

.modal-user-header {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 18px;
}

.modal-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #e4e6eb;
}

.modal-username {
  font-weight: 700;
  font-size: 1.05rem;
  color: #050505;
  display: block;
}

.modal-privacy {
  background: #e4e6eb;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #050505;
  margin-top: 2px;
}

.modal-content-area {
  margin-bottom: 20px;
}

.fb-textarea {
  width: 100%;
  min-height: 150px;
  border: none;
  font-family: inherit;
  font-size: 1.4rem;
  outline: none;
  resize: none;
  color: #050505;
  padding: 5px 0;
}

.modal-rating-section {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 18px;
  padding: 12px;
  background: #f7f8fa;
  border-radius: 8px;
}

.modal-rating-section label {
  font-weight: 700;
  font-size: 1rem;
  color: #65676b;
}

.ta-circle-rating {
  display: flex;
  gap: 10px;
  color: #00aa6c;
  font-size: 1.8rem;
}

.ta-circle-rating i {
  cursor: pointer;
  transition: transform 0.1s;
}

.ta-circle-rating i:hover {
  transform: scale(1.1);
}

.modal-image-area {
  border: 1px solid #ced0d4;
  border-radius: 12px;
  padding: 12px;
  margin-bottom: 5px;
}

.modal-image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 10px;
  margin-bottom: 12px;
}

.modal-img-wrap {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}

.modal-img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.btn-remove-img {
  position: absolute;
  top: 6px;
  right: 6px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  transition: 0.2s;
}

.btn-remove-img:hover {
  background: white;
  transform: scale(1.1);
}

.modal-add-img-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f2f5;
  border-radius: 10px;
  padding: 40px;
  cursor: pointer;
  transition: 0.2s;
  border: 2px dashed #ced0d4;
}

.modal-add-img-btn:hover {
  background: #e4e6eb;
  border-color: #bcc0c4;
}

.add-img-content {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.add-img-content i {
  font-size: 2rem;
  color: #45bd62;
}

.add-img-content span {
  font-weight: 700;
  font-size: 1.1rem;
  color: #050505;
}

.fb-footer {
  padding: 16px 20px 20px;
}

.btn-fb-save {
  width: 100%;
  background: #00aa6c;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-fb-save:hover:not(:disabled) {
  background: #008f5a;
}

.btn-fb-save:disabled {
  background: #e4e6eb;
  color: #bcc0c4;
  cursor: not-allowed;
}

.text-primary { color: #1877f2; }
.text-warning { color: #f7b928; }
.text-danger { color: #f02849; }
.text-success { color: #45bd62; }

@media (max-width: 600px) {
  .edit-modal.fb-style {
    width: 95%;
  }
}
</style>