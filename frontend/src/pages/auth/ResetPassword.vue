<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <h1>{{ t('auth.reset_title') }}</h1>
        <p>{{ t('auth.reset_subtitle') }}</p>
      </div>

      <form @submit.prevent="handleResetPassword" class="auth-form" v-if="!success">
        <div class="form-group">
          <label>{{ t('auth.new_password') }}</label>
          <div class="input-wrapper">
            <i class="fas fa-lock"></i>
            <input 
              v-model="password" 
              type="password" 
              placeholder="Minimum 6 characters" 
              required 
              minlength="6"
              :disabled="loading"
            />
          </div>
        </div>

        <div class="form-group">
          <label>{{ t('auth.confirm_password') }}</label>
          <div class="input-wrapper">
            <i class="fas fa-shield-alt"></i>
            <input 
              v-model="confirmPassword" 
              type="password" 
              :placeholder="t('auth.confirm_placeholder')" 
              required 
              :disabled="loading"
            />
          </div>
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          <span v-if="!loading">{{ t('auth.update_btn') }}</span>
          <i v-else class="fas fa-spinner fa-spin"></i>
        </button>
      </form>

      <div v-if="message" class="alert success">
        <i class="fas fa-check-circle"></i> {{ t('auth.update_success') }}
      </div>
      <div v-if="error" class="alert error">
        <i class="fas fa-exclamation-circle"></i> {{ error }}
      </div>

      <div class="auth-footer" v-if="success">
        <router-link to="/login" class="btn-secondary">
          {{ t('nav.signIn') }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useI18n } from '@/composables/useI18n'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()

const token = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const message = ref('')
const error = ref('')
const success = ref(false)

onMounted(() => {
  // ดึง token จาก URL query
  token.value = route.query.token
  if (!token.value) {
    error.value = 'Invalid or missing token.'
  }
})

const handleResetPassword = async () => {
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.'
    return
  }

  loading.value = true
  message.value = ''
  error.value = ''
  
  try {
    const res = await axios.post('http://localhost:8000/reset-password', {
      token: token.value,
      new_password: password.value
    })
    message.value = 'SUCCESS'
    success.value = true
    // ไปหน้า Login หลังจาก 3 วินาที
    setTimeout(() => {
        if (success.value) router.push('/login')
    }, 3000)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Something went wrong.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@import "@/assets/auth.css";

.auth-page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.auth-card {
  background: white;
  padding: 40px;
  border-radius: 24px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.05);
  width: 100%;
  max-width: 450px;
  text-align: center;
}

.auth-header h1 {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #0f172a;
}

.auth-header p {
  color: #64748b;
  margin-bottom: 30px;
}

.form-group {
  text-align: left;
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #334155;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper i {
  position: absolute;
  left: 16px;
  color: #94a3b8;
}

.input-wrapper input {
  width: 100%;
  padding: 14px 14px 14px 48px;
  border: 2px solid #f1f5f9;
  border-radius: 14px;
  outline: none;
  transition: all 0.2s;
}

.input-wrapper input:focus {
  border-color: #00aa6c;
  background: #f0fdf4;
}

.btn-primary {
  width: 100%;
  padding: 14px;
  background: #0f172a;
  color: white;
  border: none;
  border-radius: 14px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary:hover {
  background: #00aa6c;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 170, 108, 0.3);
}

.alert {
  margin-top: 20px;
  padding: 12px;
  border-radius: 12px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.alert.success {
  background: #f0fdf4;
  color: #166534;
}

.alert.error {
  background: #fef2f2;
  color: #991b1b;
}

.auth-footer {
  margin-top: 24px;
}

.btn-secondary {
    display: block;
    text-decoration: none;
    color: #00aa6c;
    font-weight: 700;
    padding: 12px;
    border: 2px solid #00aa6c;
    border-radius: 14px;
    transition: all 0.2s;
}

.btn-secondary:hover {
    background: #00aa6c;
    color: white;
}
</style>
