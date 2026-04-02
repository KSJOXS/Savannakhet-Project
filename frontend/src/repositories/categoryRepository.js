import api from '@/services/api'

export const categoryRepository = {
    getAll() {
        return api.get('/categories')
    },
    create(data) {
        return api.post('/categories', data)
    },
    delete(id) {
        return api.delete(`/categories/${id}`)
    }
}
