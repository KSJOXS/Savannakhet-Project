<template>
    <div class="auth-page">
        <LanguageSwitcherAuth />
        
        <div class="auth-card">
            <div class="auth-brand">
                <span class="auth-brand-icon">🌴</span>
                <span class="auth-brand-name">Savannakhet Smart Travel</span>
            </div>

            <button @click="router.push('/')" class="btn-back">
                <i class="fas fa-chevron-left"></i> {{ t('auth.back_home') }}
            </button>

            <div class="auth-header">
                <h2>{{ t('auth.login_title') }}</h2>
                <p>{{ t('auth.login_subtitle') }}</p>
            </div>

            <form @submit.prevent="handleLogin" class="auth-form">
                <div class="input-group">
                    <label>{{ t('auth.username') }}</label>
                    <div class="input-with-icon">
                        <i class="fas fa-user"></i>
                        <input v-model="form.username" type="text" :placeholder="t('auth.username_placeholder')" required>
                    </div>
                </div>
                <div class="input-group">
                    <label>{{ t('auth.password') }}</label>
                    <div class="input-with-icon">
                        <i class="fas fa-lock"></i>
                        <input v-model="form.password" type="password" :placeholder="t('auth.password_placeholder')" required>
                    </div>
                    <div class="forgot-pwd-wrap">
                        <router-link to="/forgot-password" class="forgot-link">{{ t('auth.forgot_password') }}</router-link>
                    </div>
                </div>
                <p v-if="error" class="error-msg">⚠️ {{ error }}</p>
                <button type="submit" :disabled="loading" class="btn-submit">
                    <span v-if="loading"><i class="fas fa-spinner fa-spin mr-2"></i> {{ t('auth.signing_in') }}</span>
                    <span v-else>{{ t('auth.sign_in_btn') }}</span>
                </button>
            </form>

            <div class="auth-footer">
                <span>{{ t('auth.no_account') }}</span>
                <router-link to="/register">{{ t('auth.create_free') }}</router-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { authRepository } from '@/repositories/authRepository'
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'
import { useI18n } from '@/composables/useI18n'
import LanguageSwitcherAuth from '@/components/LanguageSwitcherAuth.vue'

const { t } = useI18n()
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
            router.push('/history')
        }
    } catch (err) {
        error.value = err.response?.data?.detail || t('common.error')
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
@import "@/assets/auth.css";

.mr-2 {
    margin-right: 8px;
}
</style>
