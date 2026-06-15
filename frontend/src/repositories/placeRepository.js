import api from "@/services/api";

export const placeRepository = {
  getAll(includeDrafts = false) {
    return api.get(`/places${includeDrafts ? "?include_drafts=true" : ""}`);
  },
  getById(id) {
    return api.get(`/places/${id}`);
  },

  // 🛠️ ส่ง FormData ผ่าน POST ได้ปกติ
  create(data) {
    return api.post("/admin/places", data, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },

  // User submit place
  submit(data) {
    return api.post("/places/submit", data, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },

  getPendingPlaces() {
    return api.get("/admin/places/pending");
  },

  updateStatus(id, status) {
    const fd = new FormData();
    fd.append("status", status);
    return api.put(`/admin/places/${id}/status`, fd, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },

  // 🛠️ สำหรับ FastAPI สามารถส่ง FormData ผ่าน PUT ได้โดยตรงเลยครับ 🎉
  update(id, data) {
    const isFormData = data instanceof FormData;

    return api.put(`/admin/places/${id}`, data, {
      headers: isFormData ? { "Content-Type": "multipart/form-data" } : {},
    });
  },

  delete(id) {
    return api.delete(`/admin/places/${id}`);
  },
  getComments(placeId) {
    return api.get(`/places/${placeId}/comments`);
  },
  addComment(data) {
    // data should be FormData
    return api.post("/reviews", data, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  getCommunityFeed() {
    return api.get("/community/feed");
  },
  toggleLike(reviewId, userId) {
    return api.post(`/reviews/${reviewId}/like?user_id=${userId}`);
  },
  getAllComments() {
    return api.get("/admin/all-comments");
  },
  deleteComment(id) {
    return api.delete(`/admin/comments/${id}`);
  },
  updateUserReview(reviewId, data) {
    return api.put(`/reviews/${reviewId}`, data, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  deleteUserReview(reviewId, userId) {
    return api.delete(`/reviews/${reviewId}?user_id=${userId}`);
  },
  addPostComment(reviewId, data) {
    return api.post(`/reviews/${reviewId}/comments`, data, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  deletePostComment(commentId, userId) {
    return api.delete(`/reviews/comments/${commentId}?user_id=${userId}`);
  },
  // 🤖 GNN Interaction Logging — records user behavior for AI learning
  logInteraction(userId, placeId, actionType, score = null) {
    return api.post("/interactions/log", {
      user_id: userId,
      place_id: placeId,
      action_type: actionType, // 'view', 'like', 'review'
      score: score,
    });
  },
  // 🤖 GNN Recommendations — fetch personalized places from AI
  getGnnRecommendations(userId, topK = 8) {
    return api.get(`/api/recommendations/${userId}?top_k=${topK}`);
  },

  // 📖 Place Sections (image + description blocks)
  getSections(placeId) {
    return api.get(`/places/${placeId}/sections`);
  },
  addSection(placeId, formData) {
    return api.post(`/admin/places/${placeId}/sections`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  updateSection(placeId, sectionId, formData) {
    return api.put(`/admin/places/${placeId}/sections/${sectionId}`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  deleteSection(placeId, sectionId) {
    return api.delete(`/admin/places/${placeId}/sections/${sectionId}`);
  },
};
