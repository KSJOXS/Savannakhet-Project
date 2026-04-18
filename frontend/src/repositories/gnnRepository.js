import api from '@/services/api'

export const gnnRepository = {
    // ส่ง Log การกระทำของผู้ใช้ (view, like, review)
    logInteraction(payload) {
        return api.post('/api/interactions/log', payload)
    },
    // ดึงข้อมูลแนะนำส่วนตัวด้วย GNN
    getRecommendations(userId, topK = 5) {
        return api.get(`/api/recommendations/${userId}?top_k=${topK}`)
    }
}
