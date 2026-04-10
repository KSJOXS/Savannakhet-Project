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
                <h2>Sign In</h2>
                <p>Welcome back! Please enter your credentials.</p>
            </div>

            <form @submit.prevent="handleLogin" class="auth-form">
                <div class="input-group">
                    <label>Username</label>
                    <div class="input-with-icon">
                        <i class="fas fa-user"></i>
                        <input v-model="form.username" type="text" placeholder="Enter your username" required>
                    </div>
                </div>
                <div class="input-group">
                    <label>Password</label>
                    <div class="input-with-icon">
                        <i class="fas fa-lock"></i>
                        <input v-model="form.password" type="password" placeholder="Enter your password" required>
                    </div>
                </div>
                <p v-if="error" class="error-msg">⚠️ {{ error }}</p>
                <button type="submit" :disabled="loading" class="btn-submit">
                    {{ loading ? 'Signing in...' : 'Sign In' }}
                </button>
            </form>

            <div class="auth-footer">
                <span>Don't have an account?</span>
                <router-link to="/register">Create one free</router-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { authRepository } from '@/repositories/authRepository'
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'

const router = useRouter()
const error = ref('')
const loading = ref(false)
const form = ref({ username: '', password: '' })

const handleLogin = async () => {
    loading.value = true
    error.value = ''
    try {
        const res = await authRepository.login(form.value)
        const { login } = useAuth()
        login(res.data.user, res.data.access_token)
        if (res.data.user.role === 'admin') {
            router.push('/admin/places')
        } else {
            router.push('/explore')
        }
    } catch (err) {
        error.value = err.response?.data?.detail || 'Invalid username or password'
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
@import "@/assets/auth.css";
</style>
