<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <h1>{{ t('auth.forgot_title') }}</h1>
        <p>{{ t('auth.forgot_subtitle') }}</p>
      </div>

      <form @submit.prevent="handleForgotPassword" class="auth-form">
        <div class="form-group">
          <label>{{ t('auth.email_label') }}</label>
          <div class="input-wrapper">
            <i class="fas fa-envelope"></i>
            <input 
              v-model="email" 
              type="email" 
              :placeholder="t('auth.email_placeholder')" 
              required 
              :disabled="loading"
            />
          </div>
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          <span v-if="!loading">{{ t('auth.send_link') }}</span>
          <i v-else class="fas fa-spinner fa-spin"></i>
        </button>
      </form>

      <div v-if="message" class="alert success">
        <i class="fas fa-check-circle"></i> {{ t('auth.reset_sent_msg') }}
      </div>
      <div v-if="error" class="alert error">
        <i class="fas fa-exclamation-circle"></i> {{ error }}
      </div>

      <div class="auth-footer">
        <router-link to="/login" class="back-link">
          <i class="fas fa-arrow-left"></i> {{ t('auth.back_to_login') }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useI18n } from '@/composables/useI18n'

const { t } = useI18n()
const email = ref('')
const loading = ref(false)
const message = ref('')
const error = ref('')

const handleForgotPassword = async () => {
  loading.value = true
  message.value = ''
  error.value = ''
  
  try {
    const res = await axios.post('http://127.0.0.1:8000/forgot-password', {
      email: email.value
    })
    // เมื่อส่งสำเร็จ Backend จะตอบกลับมาเป็น { status: 'success' }
    if (res.data.status === 'success') {
      message.value = 'SUCCESS'
      email.value = ''
    }
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
  margin-top: 30px;
}

.back-link {
  text-decoration: none;
  color: #64748b;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: color 0.2s;
}

.back-link:hover {
  color: #0f172a;
}
</style>
