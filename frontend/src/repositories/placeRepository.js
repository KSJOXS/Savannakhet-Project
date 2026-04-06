import api from '@/services/api'

export const placeRepository = {
    getAll(includeDrafts = false) {
        return api.get(`/places${includeDrafts ? '?include_drafts=true' : ''}`)
    },
    getById(id) {
        return api.get(`/places/${id}`)
    },

    // 🛠️ ส่ง FormData ผ่าน POST ได้ปกติ
    create(data) {
        return api.post('/admin/places', data, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
    },

    // 🛠️ สำหรับ FastAPI สามารถส่ง FormData ผ่าน PUT ได้โดยตรงเลยครับ 🎉
    update(id, data) {
        const isFormData = data instanceof FormData;

        return api.put(`/admin/places/${id}`, data, {
            headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : {}
        })
    },

    delete(id) {
        return api.delete(`/admin/places/${id}`)
    },
    getComments(placeId) {
        return api.get(`/places/${placeId}/comments`)
    },
    addComment(placeId, data) {
        return api.post('/reviews', { place_id: parseInt(placeId), ...data })
    },
    getAllComments() {
        return api.get('/admin/all-comments')
    },
    deleteComment(id) {
        return api.delete(`/comments/${id}`)
    }
}