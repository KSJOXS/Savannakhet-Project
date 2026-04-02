<template>
    <div class="auth-page">
        <div class="auth-card">
            <button @click="router.push('/')" class="btn-back">← กลับหน้าหลัก</button>

            <div class="auth-header">
                <h2>สมัครสมาชิก</h2>
                <p>สร้างบัญชีเพื่อเริ่มต้นใช้งานระบบแนะนำท่องเที่ยว</p>
            </div>

            <form @submit.prevent="handleRegister" class="auth-form">
                <div class="input-group">
                    <label>ชื่อผู้ใช้ (Username)</label>
                    <input v-model="form.username" type="text" placeholder="ระบุชื่อผู้ใช้" required>
                </div>

                <div class="input-group">
                    <label>อีเมล (Email)</label>
                    <input v-model="form.email" type="email" placeholder="example@gmail.com" required>
                </div>

                <div class="input-group">
                    <label>รหัสผ่าน (Password)</label>
                    <input v-model="form.password" type="password" placeholder="อย่างน้อย 6 ตัวอักษร" required>
                </div>

                <button type="submit" :disabled="loading" class="btn-submit">
                    {{ loading ? 'กำลังสร้างบัญชี...' : 'สมัครสมาชิกตอนนี้' }}
                </button>
            </form>

            <div class="auth-footer">
                <span>มีบัญชีอยู่แล้ว? </span>
                <router-link to="/login">เข้าสู่ระบบที่นี่</router-link>
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

// อัปเดตให้มี email ตามที่ Backend ต้องการ
const form = ref({
    username: '',
    email: '',
    password: ''
})

const handleRegister = async () => {
    loading.value = true
    try {
        // ยิงไปที่ Endpoint /register ผ่าน repository
        await authRepository.register(form.value)
        alert("สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ")
        router.push('/login')
    } catch (err) {
        // แสดงข้อความ Error จาก Backend (เช่น Username ซ้ำ หรือ Email ไม่ถูกต้อง)
        const errorMsg = err.response?.data?.detail || "เกิดข้อผิดพลาด โปรดลองอีกครั้ง"
        alert(errorMsg)
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
@import "../assets/auth.css";
</style>