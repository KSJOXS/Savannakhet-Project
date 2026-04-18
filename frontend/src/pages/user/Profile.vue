<template>
    <div class="profile-page">
        <Navbar />
        
        <div class="profile-container">
            <div class="profile-card">
                <div class="profile-header">
                    <h2>⚙️ Account Settings</h2>
                    <p>View and update your personal information</p>
                </div>
                
                <div v-if="loading" class="loading-state">
                    <div class="spinner"></div>
                    <p>Loading your profile...</p>
                </div>
                
                <form v-else @submit.prevent="handleUpdate" class="profile-form">
                    
                    <div class="avatar-section">
                        <div class="avatar-wrapper" :class="{ 'is-editing': isEditing }" @click="isEditing && triggerImageUpload()">
                            <img :src="currentProfileImage" alt="Profile Avatar" class="avatar-img" />
                            <div v-if="isEditing" class="avatar-overlay">
                                <i class="fas fa-camera"></i>
                            </div>
                        </div>
                        <p v-if="isEditing" class="avatar-hint">Click the image to change</p>
                        
                        <input 
                            type="file" 
                            ref="fileInput" 
                            class="hidden-input" 
                            accept="image/jpeg,image/png,image/webp" 
                            @change="onImageSelected" 
                        />
                    </div>

                    <div class="input-group">
                        <label>Username</label>
                        <input v-model="form.username" type="text" placeholder="Username" :disabled="!isEditing" />
                    </div>
                    
                    <div class="input-group">
                        <label>Email Address</label>
                        <input v-model="form.email" type="email" placeholder="Email address" :disabled="!isEditing" />
                    </div>
                    
                    <div class="input-group" v-if="isEditing">
                        <label>New Password <span style="color:#94a3b8; font-weight:400;">(optional)</span></label>
                        <input v-model="form.password" type="password" placeholder="Leave blank to keep current" />
                    </div>
                    
                    <div class="form-actions">
                        <p v-if="successMsg" class="success-msg">{{ successMsg }}</p>
                        <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

                        <div class="btn-group-profile">
                            <button v-if="!isEditing" type="button" class="btn-edit" @click="isEditing = true">
                                <i class="fas fa-edit"></i> Edit Profile
                            </button>
                            
                            <template v-else>
                                <button type="button" class="btn-cancel" @click="cancelEdit" :disabled="saving">
                                    Cancel
                                </button>
                                <button type="submit" class="btn-save" :disabled="saving">
                                    <i class="fas fa-save"></i> {{ saving ? 'Saving...' : 'Save Changes' }}
                                </button>
                            </template>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import { userRepository } from '@/repositories/userRepository'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { user } = useAuth()
const loading = ref(true)
const saving = ref(false)
const isEditing = ref(false)
const successMsg = ref('')
const errorMsg = ref('')

const originalData = ref({})
const fileInput = ref(null)
const selectedFile = ref(null)
const imagePreview = ref(null)

const form = ref({
    username: '',
    email: '',
    password: '',
    profile_image: ''
})

// 📸 คำนวณรูปภาพที่จะแสดง (ถ้าเลือกรูปใหม่โชว์ Preview / ถ้าไม่มีใช้รูปจำลองจากชื่อ)
const currentProfileImage = computed(() => {
    if (imagePreview.value) return imagePreview.value;
    
    if (form.value.profile_image) {
        const url = form.value.profile_image;
        if (url.startsWith('http') || url.startsWith('data:')) return url;
        return `http://localhost:8000/${url.startsWith('/') ? url.slice(1) : url}`;
    }
    
    // รูปภาพ Default แบบ Generate จากชื่อ
    return `https://ui-avatars.com/api/?name=${form.value.username || 'User'}&background=3498db&color=fff&size=150`;
})

// 📸 สั่งคลิก Input File
const triggerImageUpload = () => {
    fileInput.value.click()
}

// 📸 จัดการเมื่อผู้ใช้เลือกไฟล์
const onImageSelected = (e) => {
    const file = e.target.files[0];
    if (file) {
        selectedFile.value = file;
        imagePreview.value = URL.createObjectURL(file);
    }
}

const cancelEdit = () => {
    isEditing.value = false
    form.value = { ...originalData.value, password: '' }
    selectedFile.value = null
    imagePreview.value = null
    errorMsg.value = ''
    successMsg.value = ''
}

const fetchProfile = async () => {
    if (!user.value) {
        router.push('/login')
        return
    }
    
    loading.value = true
    try {
        const res = await userRepository.getProfile(user.value.id)
        form.value.username = res.data.username
        form.value.email = res.data.email
        form.value.profile_image = res.data.profile_image // ดึงรูปโปรไฟล์มาเก็บ
        originalData.value = { 
            username: res.data.username, 
            email: res.data.email, 
            profile_image: res.data.profile_image 
        }
    } catch (err) {
        console.error("Error fetching profile:", err)
        errorMsg.value = "ไม่สามารถดึงข้อมูลโปรไฟล์ได้"
    } finally {
        loading.value = false
    }
}

const handleUpdate = async () => {
    saving.value = true
    successMsg.value = ''
    errorMsg.value = ''
    
    // 📦 ใช้ FormData เพราะมีการอัปโหลดไฟล์รูปภาพ
    const formData = new FormData()
    if (form.value.username) formData.append('username', form.value.username)
    if (form.value.email) formData.append('email', form.value.email)
    if (form.value.password) formData.append('password', form.value.password)
    
    // แนบไฟล์รูปถ้ามีการเลือกรูปใหม่
    if (selectedFile.value) {
        formData.append('profile_image', selectedFile.value)
    }
    
    try {
        // 🚨 หมายเหตุ: Backend ของคุณต้องรองรับการรับค่าแบบ form-data ใน Endpoint นี้นะครับ
        const res = await userRepository.updateProfile(user.value.id, formData)
        successMsg.value = "Profile updated successfully!"
        
        // Update local storage
        const currentData = JSON.parse(localStorage.getItem('user') || '{}')
        currentData.username = res.data.username
        currentData.profile_image = res.data.profile_image // อัปเดตรูปใหม่ใน LocalStorage
        localStorage.setItem('user', JSON.stringify(currentData))
        
        // Update user state
        user.value.username = res.data.username 
        if (res.data.profile_image) user.value.profile_image = res.data.profile_image
        
        // Update form state
        form.value.profile_image = res.data.profile_image
        originalData.value = { ...form.value }
        
        isEditing.value = false
        form.value.password = ''
        selectedFile.value = null
        imagePreview.value = null
    } catch (err) {
        errorMsg.value = err.response?.data?.detail || "Something went wrong. Please try again."
    } finally {
        saving.value = false
    }
}

onMounted(fetchProfile)
</script>

<style scoped>
.profile-page {
    background: linear-gradient(135deg, #1e5799 0%, #2989d8 50%, #207cca 100%) !important;
    min-height: 100vh;
    width: 100%;
}

.profile-container {
    max-width: 600px;
    margin: 60px auto;
    padding: 0 20px;
}

.profile-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.2);
}

.profile-header {
    text-align: center;
    margin-bottom: 30px;
}

.profile-header h2 {
    color: #1e293b;
    margin: 0 0 10px;
    font-size: 1.8rem;
}

.profile-header p {
    color: #64748b;
    font-size: 0.95rem;
}

/* 📸 Avatar Styles */
.avatar-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 25px;
}

.avatar-wrapper {
    position: relative;
    width: 110px;
    height: 110px;
    border-radius: 50%;
    overflow: hidden;
    border: 4px solid white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: 0.3s;
}

.avatar-wrapper.is-editing {
    cursor: pointer;
}

.avatar-wrapper.is-editing:hover {
    box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
    transform: translateY(-2px);
}

.avatar-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-overlay {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-size: 1.8rem;
    opacity: 0;
    transition: 0.3s;
}

.avatar-wrapper.is-editing:hover .avatar-overlay {
    opacity: 1;
}

.avatar-hint {
    font-size: 0.8rem;
    color: #94a3b8;
    margin-top: 10px;
}

.hidden-input {
    display: none;
}

/* Form Styles */
.profile-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.input-group label {
    display: block;
    font-weight: 700;
    color: #334155;
    margin-bottom: 8px;
    font-size: 0.9rem;
}

.input-group input {
    width: 100%;
    padding: 12px 15px;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    background: #f8fafc;
    color: #1e293b;
    transition: 0.3s;
    box-sizing: border-box;
}

.input-group input:disabled {
    background: #e2e8f0;
    color: #64748b;
    cursor: not-allowed;
    border-color: #cbd5e1;
}

.input-group input:focus {
    border-color: #3498db;
    outline: none;
    background: white;
}

.btn-group-profile {
    display: flex;
    gap: 15px;
    margin-top: 10px;
}

.btn-edit, .btn-cancel, .btn-save {
    flex: 1;
    padding: 12px;
    border-radius: 50px;
    border: none;
    font-weight: bold;
    font-size: 1rem;
    cursor: pointer;
    transition: 0.3s;
    color: white;
}

.btn-edit {
    background: #f59e0b;
}

.btn-edit:hover {
    background: #d97706;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(245, 158, 11, 0.3);
}

.btn-cancel {
    background: #94a3b8;
}

.btn-cancel:hover {
    background: #64748b;
}

.btn-save {
    background: #3498db;
    margin-top: 10px;
}

.btn-save:hover:not(:disabled) {
    background: #2980b9;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
}

.btn-save:disabled {
    background: #94a3b8;
    cursor: not-allowed;
}

.success-msg { color: #10b981; text-align: center; margin-bottom: 10px; font-weight: bold; }
.error-msg { color: #ef4444; text-align: center; margin-bottom: 10px; font-weight: bold; }
.loading-state { text-align: center; padding: 40px 0; color: #64748b; }

.spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 0 auto 15px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>