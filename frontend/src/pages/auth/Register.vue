<template>
    <div class="auth-page">
        <div class="auth-card">
            <div class="auth-brand">
                <span class="auth-brand-icon">🌴</span>
                <span class="auth-brand-name">Savannakhet Smart Travel</span>
            </div>

            <button v-if="step === 1" @click="router.push('/')" class="btn-back">
                <i class="fas fa-chevron-left"></i> Back to Home
            </button>
            <button v-else @click="step = 1" class="btn-back">
                <i class="fas fa-chevron-left"></i> Back to Account Info
            </button>

            <div class="step-indicator">
                <div class="step-dot" :class="{ active: step === 1 }"></div>
                <div class="step-dot" :class="{ active: step === 2 }"></div>
            </div>

            <div v-if="step === 1">
                <div class="auth-header">
                    <h2>Create Account</h2>
                    <p>Join us and start exploring Savannakhet.</p>
                </div>

                <form @submit.prevent="step = 2" class="auth-form">
                    <div class="input-group">
                        <label>Username</label>
                        <div class="input-with-icon">
                            <i class="fas fa-user"></i>
                            <input v-model="form.username" type="text" placeholder="Choose a username" required>
                        </div>
                    </div>

                    <div class="input-group">
                        <label>Email Address</label>
                        <div class="input-with-icon">
                            <i class="fas fa-envelope"></i>
                            <input v-model="form.email" type="email" placeholder="example@gmail.com" required>
                        </div>
                    </div>

                    <div class="input-group">
                        <label>Password</label>
                        <div class="input-with-icon">
                            <i class="fas fa-lock"></i>
                            <input v-model="form.password" type="password" placeholder="At least 6 characters" required>
                        </div>
                    </div>

                    <button type="submit" class="btn-submit">
                        Next: Personalize Interests <i class="fas fa-arrow-right" style="margin-left: 8px;"></i>
                    </button>
                </form>
            </div>

            <div v-else>
                <div class="auth-header">
                    <h2>Your Interests</h2>
                    <p>Tell us what you like to help AI recommend better.</p>
                </div>

                <div class="interests-grid">
                    <div v-for="interest in availableInterests" :key="interest.id" class="interest-item"
                        :class="{ selected: form.preferences.includes(interest.id) }" @click="toggleInterest(interest.id)">
                        <i :class="interest.icon"></i>
                        <span>{{ interest.name }}</span>
                    </div>
                </div>

                <p v-if="errorMsg" class="error-msg">⚠️ {{ errorMsg }}</p>

                <button @click="handleRegister" :disabled="loading" class="btn-submit">
                    {{ loading ? 'Creating account...' : 'Complete Registration' }}
                </button>
            </div>

            <div class="auth-footer">
                <span>Already have an account?</span>
                <router-link to="/login">Sign in here</router-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { authRepository } from '@/repositories/authRepository'
import { useRouter } from 'vue-router'

const router = useRouter()
const step = ref(1)
const loading = ref(false)
const errorMsg = ref('')

const form = ref({
    username: '',
    email: '',
    password: '',
    preferences: []
})

const availableInterests = [
    { id: 'nature', name: 'ธรรมชาติ & ภูเขา', icon: 'fas fa-mountain' },
    { id: 'culture', name: 'วัด & ประวัติศาสตร์', icon: 'fas fa-vihara' },
    { id: 'cafe', name: 'คาเฟ่ & ของหวาน', icon: 'fas fa-coffee' },
    { id: 'local_food', name: 'อาหารท้องถิ่น', icon: 'fas fa-bowl-food' },
    { id: 'landmark', name: 'จุดถ่ายรูปสวย', icon: 'fas fa-camera' },
    { id: 'chill', name: 'เดินเล่นชิลๆ', icon: 'fas fa-walking' }
]

const toggleInterest = (id) => {
    const index = form.value.preferences.indexOf(id)
    if (index === -1) {
        form.value.preferences.push(id)
    } else {
        form.value.preferences.splice(index, 1)
    }
}

const handleRegister = async () => {
    loading.value = true
    errorMsg.value = ''
    try {
        await authRepository.register(form.value)
        router.push('/login?registered=1')
    } catch (err) {
        errorMsg.value = err.response?.data?.detail || 'Registration failed. Please try again.'
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
@import "@/assets/auth.css";
</style>
