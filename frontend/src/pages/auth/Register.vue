<template>
    <div class="auth-page">
        <div class="auth-card">
            <div class="auth-brand">
                <span class="auth-brand-icon">🌴</span>
                <span class="auth-brand-name">Savannakhet Smart Travel</span>
            </div>

            <button @click="router.push('/')" class="btn-back">
                <i class="fas fa-chevron-left"></i> Back to Home
            </button>

            <div class="auth-header">
                <h2>Create Account</h2>
                <p>Join us and start exploring Savannakhet.</p>
            </div>

            <form @submit.prevent="handleRegister" class="auth-form">
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

                <p v-if="errorMsg" class="error-msg">⚠️ {{ errorMsg }}</p>

                <button type="submit" :disabled="loading" class="btn-submit">
                    {{ loading ? 'Creating account...' : 'Create Account' }}
                </button>
            </form>

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
const loading = ref(false)
const errorMsg = ref('')

const form = ref({
    username: '',
    email: '',
    password: ''
})

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
