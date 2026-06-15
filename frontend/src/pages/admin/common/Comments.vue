<template>
  <div class="admin-page">
    <div class="page-header">
      <h2><i class="fas fa-comments"></i> Review Management</h2>
      <div class="stats-badge" v-if="comments.length > 0">
        Total: {{ comments.length }} Reviews
      </div>
    </div>

    <div class="filter-bar">
      <div class="search-box">
        <i class="fas fa-search"></i>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by user, comment or place..."
        />
      </div>
      <button @click="fetchComments" class="btn-refresh">
        <i class="fas fa-sync"></i> Refresh Data
      </button>
    </div>

    <div class="table-container">
      <table class="admin-table">
        <thead>
          <tr>
            <th style="width: 220px">Location</th>
            <th style="width: 150px">User</th>
            <th>Review Details</th>
            <th style="width: 100px">Actions</th>
          </tr>
        </thead>
        <tbody v-if="!loading">
          <tr v-for="comment in filteredComments" :key="comment.id">
            <td>
              <div class="place-cell">
                <img
                  :src="getThumbnail(comment.place_image || comment.image_url)"
                  class="place-thumb"
                  @error="(e) => (e.target.src = PLACEHOLDER)"
                />
                <div class="place-name-group">
                  <span class="place-name">{{
                    comment.place_name ||
                    "Place ID: " + (comment.place_id || "Unknown")
                  }}</span>
                  <button
                    class="btn-view-link"
                    @click="viewPublicPlace(comment.place_id)"
                  >
                    View Site <i class="fas fa-external-link-alt"></i>
                  </button>
                </div>
              </div>
            </td>

            <td>
              <div class="user-info">
                <div class="user-icon">
                  {{ (comment.username || "U").charAt(0).toUpperCase() }}
                </div>
                <strong>{{ comment.username || "Traveler" }}</strong>
              </div>
            </td>

            <td>
              <div class="rating-bubbles">
                <i
                  v-for="s in 5"
                  :key="s"
                  :class="[comment.rating >= s ? 'fas' : 'far', 'fa-circle']"
                ></i>
                <span class="rating-num">({{ comment.rating }}/5)</span>
              </div>
              <p class="comment-text">
                {{ comment.comment_text || comment.comment }}
              </p>
              <small class="comment-date">ID: #{{ comment.id }}</small>
            </td>

            <td>
              <button
                @click="handleDelete(comment.id)"
                class="btn-delete-action"
              >
                <i class="fas fa-trash-alt"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading reviews from database...</p>
      </div>

      <div v-if="!loading && filteredComments.length === 0" class="empty-state">
        <i class="fas fa-comment-slash"></i>
        <p>No reviews found. Try checking your backend API.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { placeRepository } from "@/repositories/placeRepository";

const router = useRouter();
const comments = ref([]);
const loading = ref(true);
const searchQuery = ref("");

const PLACEHOLDER = `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='70'%3E%3Crect width='100' height='70' fill='%23f1f5f9'/%3E%3C/svg%3E`;

const fetchComments = async () => {
  loading.value = true;
  try {
    // 🚨 สำคัญ: ลองเช็คที่ไฟล์ placeRepository ว่า getAllComments() ส่งค่ากลับมาไหม
    const res = await placeRepository.getAllComments();
    console.log("Debug Admin Reviews:", res.data); // ดูค่าที่ส่งมาจาก DB ใน Console (F12)
    comments.value = res.data;
  } catch (err) {
    console.error("Error fetching admin comments:", err);
    alert("Cannot fetch review data. Please check your API connection.");
  } finally {
    loading.value = false;
  }
};

const handleDelete = async (id) => {
  if (
    confirm(
      "Are you sure you want to delete this review? This action cannot be undone.",
    )
  ) {
    try {
      await placeRepository.deleteComment(id);
      fetchComments(); // รีโหลดข้อมูลใหม่
    } catch (err) {
      alert("Failed to delete review.");
    }
  }
};

const viewPublicPlace = (id) => {
  if (!id) return;
  const url = router.resolve({ name: "PlaceDetail", params: { id: id } }).href;
  window.open(url, "_blank");
};

// ระบบค้นหาที่รองรับทั้งชื่อคน, ข้อความ, และชื่อสถานที่
const filteredComments = computed(() => {
  if (!searchQuery.value) return comments.value;
  const query = searchQuery.value.toLowerCase();
  return comments.value.filter((c) => {
    return (
      c.username?.toLowerCase().includes(query) ||
      c.comment_text?.toLowerCase().includes(query) ||
      c.comment?.toLowerCase().includes(query) ||
      c.place_name?.toLowerCase().includes(query)
    );
  });
});

const getThumbnail = (imageUrl) => {
  if (!imageUrl || imageUrl === "[]" || imageUrl === "0") return PLACEHOLDER;
  let url = imageUrl;
  if (typeof url === "string" && url.startsWith("[")) {
    try {
      url = JSON.parse(url)[0];
    } catch (e) {
      url = url.replace(/[\[\]"]/g, "");
    }
  }
  if (url.startsWith("data:") || url.startsWith("http")) return url;
  return `http://127.0.0.1:8000/${url.startsWith("/") ? url.slice(1) : url}`;
};

onMounted(fetchComments);
</script>

<style scoped>
.admin-page {
  padding: 25px;
  background: #f8fafc;
  min-height: 100vh;
  font-family: "Inter", sans-serif;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.page-header h2 {
  font-weight: 800;
  color: #0f172a;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-header h2 i {
  color: #f59e0b;
}

.stats-badge {
  background: #334155;
  color: white;
  padding: 6px 14px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.8rem;
}

.filter-bar {
  display: flex;
  justify-content: space-between;
  gap: 15px;
  margin-bottom: 20px;
}

.search-box {
  position: relative;
  flex: 1;
  max-width: 500px;
}

.search-box i {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
}

.search-box input {
  width: 100%;
  padding: 12px 12px 12px 45px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  outline: none;
  background: white;
  transition: 0.2s;
}

.search-box input:focus {
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.btn-refresh {
  background: white;
  border: 1px solid #e2e8f0;
  padding: 0 20px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-refresh:hover {
  background: #f1f5f9;
}

.table-container {
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
}

.admin-table th {
  background: #f8fafc;
  padding: 16px;
  text-align: left;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
  border-bottom: 1px solid #e2e8f0;
}

.admin-table td {
  padding: 16px;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: top;
}

.place-cell {
  display: flex;
  gap: 12px;
}

.place-thumb {
  width: 60px;
  height: 45px;
  border-radius: 6px;
  object-fit: cover;
  background: #f1f5f9;
  border: 1px solid #eee;
}

.place-name {
  display: block;
  font-weight: 700;
  color: #1e293b;
  font-size: 0.9rem;
  margin-bottom: 4px;
}

.btn-view-link {
  background: none;
  border: none;
  color: #3498db;
  font-size: 0.7rem;
  font-weight: 700;
  cursor: pointer;
  padding: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-icon {
  width: 32px;
  height: 32px;
  background: #00aa6c;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 800;
}

.rating-bubbles {
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 3px;
}

.rating-bubbles i {
  color: #00aa6c;
  font-size: 0.7rem;
}

.rating-num {
  font-size: 0.75rem;
  font-weight: 700;
  color: #94a3b8;
  margin-left: 6px;
}

.comment-text {
  color: #334155;
  line-height: 1.5;
  font-size: 0.9rem;
  margin: 0;
}

.comment-date {
  color: #94a3b8;
  font-size: 0.7rem;
  margin-top: 5px;
  display: block;
}

.btn-delete-action {
  background: #fef2f2;
  color: #ef4444;
  border: 1px solid #fee2e2;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s;
}

.btn-delete-action:hover {
  background: #ef4444;
  color: white;
  border-color: #ef4444;
}

.loading-state,
.empty-state {
  padding: 80px;
  text-align: center;
  color: #64748b;
}

.spinner {
  width: 35px;
  height: 35px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
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
