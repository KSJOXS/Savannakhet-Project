import api from '@/services/api'

export const userRepository = {
    getAll() {
        return api.get('/users')
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
