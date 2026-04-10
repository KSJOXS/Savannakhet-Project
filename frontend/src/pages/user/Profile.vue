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
import { ref, onMounted } from 'vue'
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

const form = ref({
    username: '',
    email: '',
    password: ''
})

const cancelEdit = () => {
    isEditing.value = false
    form.value = { ...originalData.value, password: '' }
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
        originalData.value = { username: res.data.username, email: res.data.email }
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
    
    const dataToSend = {}
    if (form.value.username) dataToSend.username = form.value.username
    if (form.value.email) dataToSend.email = form.value.email
    if (form.value.password) dataToSend.password = form.value.password
    
    try {
        const res = await userRepository.updateProfile(user.value.id, dataToSend)
        successMsg.value = "Profile updated successfully!"
        // Note: re-login required if password changed
        
        // Update local user context dynamically
        const currentData = JSON.parse(localStorage.getItem('user') || '{}')
        currentData.username = res.data.username
        localStorage.setItem('user', JSON.stringify(currentData))
        user.value.username = res.data.username // update reactive composable
        
        originalData.value = { username: res.data.username, email: res.data.email }
        isEditing.value = false
        form.value.password = ''
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

.btn-edit {
    flex: 1;
    background: #f59e0b;
    color: white;
    padding: 12px;
    border-radius: 50px;
    border: none;
    font-weight: bold;
    font-size: 1rem;
    cursor: pointer;
    transition: 0.3s;
}

.btn-edit:hover {
    background: #d97706;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(245, 158, 11, 0.3);
}

.btn-cancel {
    flex: 1;
    background: #94a3b8;
    color: white;
    padding: 12px;
    border-radius: 50px;
    border: none;
    font-weight: bold;
    font-size: 1rem;
    cursor: pointer;
    transition: 0.3s;
}

.btn-cancel:hover {
    background: #64748b;
}

.btn-save {
    flex: 1;
    background: #3498db;
    color: white;
    padding: 12px;
    border-radius: 50px;
    border: none;
    font-weight: bold;
    font-size: 1rem;
    cursor: pointer;
    transition: 0.3s;
    margin-top: 10px;
}

.btn-save:hover {
    background: #2980b9;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
}

.btn-save:disabled {
    background: #94a3b8;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}

.success-msg {
    color: #10b981;
    text-align: center;
    margin-bottom: 10px;
    font-size: 0.9rem;
    font-weight: bold;
}

.error-msg {
    color: #ef4444;
    text-align: center;
    margin-bottom: 10px;
    font-size: 0.9rem;
    font-weight: bold;
}

.loading-state {
    text-align: center;
    padding: 40px 0;
    color: #64748b;
}

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
