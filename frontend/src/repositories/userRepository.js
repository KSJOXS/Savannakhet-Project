import api from '@/services/api'

export const userRepository = {
    getAll() {
        return api.get('/users')
    },
    getProfile(id) {
        return api.get(`/users/${id}`)
    },
    updateProfile(id, data) {
        return api.patch(`/users/${id}`, data)
    },
    update(id, data) {
        return api.put(`/users/${id}`, data)
    },
    softDelete(id) {
        return api.patch(`/users/${id}/soft-delete`)
    },
    restore(id) {
        return api.patch(`/users/${id}/restore`)
    },
    requestPostPermission(id) {
        return api.post(`/users/${id}/request-post-permission`)
    },
    getPendingPermissions() {
        return api.get('/admin/users/pending-permissions')
    },
    updatePostPermission(id, status) {
        const fd = new FormData();
        fd.append('status', status);
        return api.put(`/admin/users/${id}/post-permission-status`, fd, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
    },
    getUserReviews(id) {
        return api.get(`/users/${id}/reviews`)
    },
    getUserPlaces(id) {
        return api.get(`/users/${id}/places`)
    },
    getItineraries(userId) {
        return api.get(`/api/itinerary/user/${userId}`)
    },
    deleteItinerary(id) {
        return api.delete(`/api/itinerary/${id}`)
    }
}
