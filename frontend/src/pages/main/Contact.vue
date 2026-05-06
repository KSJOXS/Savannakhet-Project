<template>
    <div class="contact-page">
        <Navbar />

        <div class="contact-header">
            <div class="header-container">
                <h1>{{ t('contact.title') || 'Contact Us' }}</h1>
                <p>{{ t('contact.subtitle') || "Have questions, feedback, or need assistance? We'd love to hear from you." }}</p>
            </div>
        </div>

        <div class="main-layout">
            <div class="contact-grid">
                
                <div class="contact-info">
                    <h2>{{ t('contact.getInTouch') || 'Get in Touch' }}</h2>
                    <p class="subtitle">
                        {{ t('contact.description') || 'ไม่ว่าคุณจะมีข้อสงสัยเกี่ยวกับการใช้งานระบบแนะนำสถานที่ AI, ต้องการแจ้งปัญหา, หรือมีข้อเสนอแนะใดๆ ทีมงาน Savannakhet Smart Travel ยินดีให้บริการครับ' }}
                    </p>

                    <div class="info-cards">
                        <div class="info-card">
                            <div class="icon-box"><i class="fas fa-envelope"></i></div>
                            <div class="info-text">
                                <h4>{{ t('contact.emailLabel') || 'Email Address' }}</h4>
                                <p><a href="mailto:jo.xaysongkham99@gmail.com">jo.xaysongkham99@gmail.com</a></p>
                            </div>
                        </div>

                        <div class="info-card">
                            <div class="icon-box"><i class="fas fa-phone-alt"></i></div>
                            <div class="info-text">
                                <h4>{{ t('contact.phoneLabel') || 'Phone Number' }}</h4>
                                <p><a href="tel:0209374933">020-9374933</a></p>
                            </div>
                        </div>

                        <div class="info-card">
                            <div class="icon-box"><i class="fas fa-map-marker-alt"></i></div>
                            <div class="info-text">
                                <h4>{{ t('contact.locationLabel') || 'Location' }}</h4>
                                <p>Kaysone Phomvihane City,<br>Savannakhet Province, Laos</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="contact-form-card">
                    <h3>{{ t('contact.formTitle') || 'Send a Message' }}</h3>
                    <p class="form-desc">{{ t('contact.formDesc') || 'ส่งข้อความหาเราโดยตรงผ่านฟอร์มด้านล่างนี้' }}</p>
                    
                    <form @submit.prevent="submitForm">
                        <div class="form-group">
                            <label>{{ t('contact.yourName') || 'Your Name' }}</label>
                            <input type="text" v-model="form.name" required :placeholder="t('contact.namePlaceholder') || 'ชื่อของคุณ'" />
                        </div>

                        <div class="form-group">
                            <label>{{ t('contact.yourEmail') || 'Email Address' }}</label>
                            <input type="email" v-model="form.email" required :placeholder="t('contact.emailPlaceholder') || 'อีเมลของคุณ'" />
                        </div>

                        <div class="form-group">
                            <label>{{ t('contact.subject') || 'Subject' }}</label>
                            <input type="text" v-model="form.subject" required :placeholder="t('contact.subjectPlaceholder') || 'หัวข้อที่ต้องการติดต่อ'" />
                        </div>

                        <div class="form-group">
                            <label>{{ t('contact.message') || 'Message' }}</label>
                            <textarea v-model="form.message" required rows="5" :placeholder="t('contact.messagePlaceholder') || 'พิมพ์ข้อความของคุณที่นี่...'"></textarea>
                        </div>

                        <button type="submit" class="btn-submit" :disabled="isSubmitting">
                            <span v-if="isSubmitting"><i class="fas fa-spinner fa-spin"></i> {{ t('contact.sending') || 'กำลังส่งข้อความ...' }}</span>
                            <span v-else><i class="fas fa-paper-plane"></i> {{ t('contact.sendBtn') || 'ส่งข้อความ (Send Message)' }}</span>
                        </button>

                        <transition name="fade">
                            <div v-if="showSuccess" class="success-message">
                                <i class="fas fa-check-circle"></i> {{ t('contact.successMsg') || 'ส่งข้อความสำเร็จ! เราจะติดต่อกลับโดยเร็วที่สุด' }}
                            </div>
                        </transition>
                    </form>
                </div>

            </div>
        </div>


    </div>
</template>

<script setup>
import { ref } from 'vue'
import Navbar from '@/components/Navbar.vue'
import { useI18n } from '@/composables/useI18n'
import api from '@/services/api'

const { t } = useI18n()

const form = ref({
    name: '',
    email: '',
    subject: '',
    message: ''
})

const isSubmitting = ref(false)
const showSuccess = ref(false)

const submitForm = async () => {
    isSubmitting.value = true
    showSuccess.value = false

    try {
        await api.post('/api/contact', form.value)
        isSubmitting.value = false
        showSuccess.value = true
        
        // เคลียร์ฟอร์ม
        form.value = {
            name: '',
            email: '',
            subject: '',
            message: ''
        }

        // ปิดข้อความแจ้งเตือนหลังผ่านไป 5 วินาที
        setTimeout(() => {
            showSuccess.value = false
        }, 5000)
    } catch (error) {
        console.error('Failed to submit contact form:', error)
        alert('Failed to send message. Please try again later.')
        isSubmitting.value = false
    }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

.contact-page {
    background-color: #f7f9fa;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    color: #1e293b;
    display: flex;
    flex-direction: column;
}

/* Header */
.contact-header {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    padding: 60px 20px;
    text-align: center;
    color: white;
}

.header-container h1 {
    font-size: 2.5rem;
    font-weight: 900;
    margin: 0 0 10px;
}

.header-container p {
    font-size: 1.1rem;
    color: #94a3b8;
    max-width: 600px;
    margin: 0 auto;
}

/* Main Content */
.main-layout {
    flex: 1;
    max-width: 1100px;
    width: 100%;
    margin: 60px auto;
    padding: 0 20px;
}

.contact-grid {
    display: grid;
    grid-template-columns: 1fr 1.3fr;
    gap: 60px;
    align-items: start;
}

/* ฝั่งซ้าย: ข้อมูลติดต่อ */
.contact-info h2 {
    font-size: 2.2rem;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 15px;
}

.subtitle {
    font-size: 1.05rem;
    color: #475569;
    line-height: 1.7;
    margin-bottom: 40px;
}

.info-cards {
    display: flex;
    flex-direction: column;
    gap: 25px;
}

.info-card {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
    transition: 0.3s;
}

.info-card:hover {
    transform: translateX(5px);
    border-color: #cbd5e1;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
}

.icon-box {
    width: 50px;
    height: 50px;
    background: #f0f9ff;
    color: #206fa3;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
}

.info-text h4 {
    margin: 0 0 5px;
    font-size: 1.1rem;
    font-weight: 700;
    color: #1e293b;
}

.info-text p, .info-text a {
    margin: 0;
    color: #64748b;
    font-size: 1rem;
    line-height: 1.5;
    text-decoration: none;
    transition: 0.2s;
}

.info-text a:hover {
    color: #206fa3;
    text-decoration: underline;
}

/* ฝั่งขวา: ฟอร์มติดต่อ */
.contact-form-card {
    background: white;
    padding: 40px;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.06);
}

.contact-form-card h3 {
    font-size: 1.8rem;
    font-weight: 800;
    margin: 0 0 8px;
    color: #0f172a;
}

.form-desc {
    color: #64748b;
    font-size: 0.95rem;
    margin-bottom: 30px;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    font-weight: 600;
    color: #475569;
    margin-bottom: 8px;
    font-size: 0.95rem;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 14px 16px;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    background: #f8fafc;
    font-family: inherit;
    font-size: 1rem;
    color: #1e293b;
    transition: all 0.2s ease;
    box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #206fa3;
    background: #ffffff;
    box-shadow: 0 0 0 3px rgba(32, 111, 163, 0.1);
}

.form-group textarea {
    resize: vertical;
    min-height: 120px;
}

.btn-submit {
    width: 100%;
    background: #206fa3; /* สีน้ำเงินพรีเมียม */
    color: white;
    border: none;
    padding: 16px;
    border-radius: 10px;
    font-size: 1.05rem;
    font-weight: 700;
    cursor: pointer;
    transition: 0.3s;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
}

.btn-submit:hover:not(:disabled) {
    background: #1a5c8a;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(32, 111, 163, 0.3);
}

.btn-submit:disabled {
    background: #94a3b8;
    cursor: not-allowed;
}

.success-message {
    margin-top: 20px;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #166534;
    padding: 15px;
    border-radius: 10px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 10px;
}

.success-message i {
    font-size: 1.2rem;
    color: #22c55e;
}

/* Animations */
.fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}

/* Footer */


/* Responsive */
@media (max-width: 992px) {
    .contact-grid {
        grid-template-columns: 1fr;
        gap: 40px;
    }
    
    .contact-form-card {
        padding: 30px 20px;
    }
}
</style>