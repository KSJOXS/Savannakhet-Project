<template>
    <div class="admin-page">
        <h3><i class="fas fa-star"></i> Review Management</h3>
        <div class="table-container">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>User</th>
                        <th>Comment</th>
                        <th>Rating</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="comment in comments" :key="comment.id">
                        <td><strong>{{ comment.username || 'User' }}</strong></td>
                        <td>{{ comment.comment_text }}</td>
                        <td><i class="fas fa-star text-warning"></i> {{ comment.rating }}</td>
                        <td>
                            <button @click="deleteComment(comment.id)" class="btn-delete">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div v-if="comments.length === 0" class="no-data">No reviews found.</div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { placeRepository } from '@/repositories/placeRepository'

const comments = ref([])

const fetchComments = async () => {
    try {
        // หมายเหตุ: คุณต้องสร้าง API Endpoint นี้ที่ฝั่ง Backend (Laravel/FastAPI) ด้วย
        const res = await placeRepository.getAllComments()
        comments.value = res.data
    } catch (err) {
        console.error("Error fetching comments:", err)
        comments.value = []
    }
}

const deleteComment = async (id) => {
    if (confirm('Delete this review?')) {
        await placeRepository.deleteComment(id)
        fetchComments()
    }
}

onMounted(fetchComments)
</script>