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
    }
}
