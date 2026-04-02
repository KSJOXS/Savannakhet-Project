<template>
    <div class="auth-page">
        <div class="auth-card">
            <button @click="router.push('/')" class="btn-back">← กลับหน้าหลัก</button>
            <div class="auth-header">
                <h2>เข้าสู่ระบบ</h2>
                <p>ยินดีต้อนรับสู่ Savannakhet Smart Travel</p>
            </div>

            <form @submit.prevent="handleLogin" class="auth-form">
                <div class="input-group">
                    <label>ชื่อผู้ใช้</label>
                    <input v-model="form.username" type="text" placeholder="ระบุชื่อผู้ใช้" required>
                </div>
                <div class="input-group">
                    <label>รหัสผ่าน</label>
                    <input v-model="form.password" type="password" placeholder="ระบุรหัสผ่าน" required>
                </div>
                <button type="submit" :disabled="loading" class="btn-submit">
                    {{ loading ? 'กำลังเข้าสู่ระบบ...' : 'เข้าสู่ระบบ' }}
                </button>
            </form>

            <p v-if="error" class="error-msg">⚠️ {{ error }}</p>
            <div class="auth-footer">
                <span>ยังไม่มีบัญชี? </span>
                <router-link to="/register">สมัครสมาชิกฟรี</router-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const error = ref('')
const loading = ref(false)
const form = ref({ username: '', password: '' }) // ใช้ชื่อ form ให้ตรงกับ v-model

const handleLogin = async () => {
    loading.value = true
    error.value = ''
    try {
        const res = await axios.post('http://127.0.0.1:8000/login', form.value)

        // บันทึกข้อมูลลงเครื่อง
        localStorage.setItem('user', JSON.stringify(res.data.user))
        localStorage.setItem('access_token', res.data.access_token)

        // เช็คสิทธิ์ Admin
        if (res.data.user.role === 'admin') {
            router.push('/admin/places') // ไปหน้าหลังบ้าน
        } else {
            router.push('/') // ไปหน้าแรก
        }
    } catch (err) {
        error.value = err.response?.data?.detail || 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
@import "../assets/auth.css";
</style>