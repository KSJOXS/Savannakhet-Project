import api from '@/services/api'

export const placeRepository = {
    getAll(includeDrafts = false) {
        return api.get(`/places${includeDrafts ? '?include_drafts=true' : ''}`)
    },
    getById(id) {
        return api.get(`/places/${id}`)
    },
    create(data) {
        return api.post('/places', data)
    },
    update(id, data) {
        return api.put(`/places/${id}`, data)
    },
    delete(id) {
        return api.delete(`/admin/places/${id}`)
    },
    getComments(placeId) {
        return api.get(`/places/${placeId}/comments`)
    },
    addComment(placeId, data) {
        return api.post(`/places/${placeId}/comments`, data)
    },
    getAllComments() {
        return api.get('/admin/all-comments')
    },
    deleteComment(id) {
        return api.delete(`/comments/${id}`)
    }
}
