<template>
    <footer class="smart-travel-footer">
        <div class="footer-container">
            <div class="footer-left">
                <div class="footer-logo-row">
                    <div class="logo-icon">
                        <i class="fas fa-map-marked-alt"></i>
                    </div>
                    <span class="copyright-text">{{ t('footer.copyright') }}</span>
                </div>
                <div class="footer-links">
                    <a href="#">{{ t('footer.terms') }}</a>
                    <a href="#">{{ t('footer.cookiePolicy') }}</a>
                    <a href="#">{{ t('footer.cookieConsent') }}</a>
                    <a href="#">{{ t('footer.sitemap') }}</a>
                    <a href="#">{{ t('footer.howItWorks') }}</a>
                    <router-link to="/contact">{{ t('footer.contactUs') }}</router-link>
                </div>
                <div class="footer-disclaimer">
                    {{ t('footer.disclaimer') }}
                    <br><br>
                    {{ t('footer.disclaimer2') }}
                </div>
                
                <div v-if="contactPhone || contactEmail" class="footer-contact-info">
                    <p><strong>{{ t('footer.contactLabel') }}</strong> 
                        <span v-if="contactPhone"><i class="fas fa-phone-alt"></i> {{ contactPhone }}</span>
                        <span v-if="contactEmail" class="ml-2"><i class="fas fa-envelope"></i> {{ contactEmail }}</span>
                    </p>
                </div>
            </div>
            
            <div class="footer-right">
                <div class="language-dropdown-wrapper">
                    <select class="language-select" :value="locale" @change="setLocale($event.target.value)">
                        <option v-for="loc in supportedLocales" :key="loc.code" :value="loc.code">
                            {{ loc.flag }} {{ loc.label }}
                        </option>
                    </select>
                    <i class="fas fa-chevron-down arrow-icon"></i>
                </div>
            </div>
        </div>
    </footer>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import settingRepository from '@/repositories/settingRepository';
import { useI18n } from '@/composables/useI18n';

const { t, setLocale, locale, supportedLocales } = useI18n();

const contactPhone = ref('');
const contactEmail = ref('');

onMounted(async () => {
    try {
        const res = await settingRepository.getAll();
        res.data.forEach(setting => {
            if (setting.key_name === 'contact_phone') contactPhone.value = setting.value;
            if (setting.key_name === 'contact_email') contactEmail.value = setting.value;
        });
    } catch (error) {
        console.error('Failed to load footer settings:', error);
    }
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.smart-travel-footer {
    background-color: #f8fafc;
    padding: 30px 40px;
    border-top: 1px solid #e2e8f0;
    font-family: 'Inter', 'Prompt', sans-serif;
    color: #334155;
    margin-top: 50px;
}

.footer-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    gap: 40px;
}

.footer-left {
    flex: 1;
}

.footer-logo-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}

.logo-icon {
    width: 32px;
    height: 32px;
    background-color: #00aa6c;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.1rem;
}

.copyright-text {
    font-size: 0.85rem;
    font-weight: 500;
    color: #475569;
}

.footer-links {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 16px;
}

.footer-links a {
    color: #0f172a;
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 700;
}

.footer-links a:hover {
    text-decoration: underline;
}

.footer-disclaimer {
    font-size: 0.75rem;
    line-height: 1.5;
    color: #64748b;
    max-width: 850px;
}

.footer-contact-info {
    margin-top: 16px;
    font-size: 0.85rem;
    color: #475569;
}

.footer-contact-info p {
    margin: 0;
}

.footer-contact-info i {
    color: #3b82f6;
    margin-right: 4px;
}

.ml-2 {
    margin-left: 12px;
}

.footer-right {
    display: flex;
    align-items: flex-start;
}

.language-dropdown-wrapper {
    position: relative;
    width: 180px;
}

.language-select {
    width: 100%;
    appearance: none;
    background-color: white;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 10px 30px 10px 14px;
    font-size: 0.9rem;
    font-weight: 600;
    color: #0f172a;
    cursor: pointer;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.language-select:focus {
    outline: none;
    border-color: #94a3b8;
}

.arrow-icon {
    position: absolute;
    right: 14px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 0.8rem;
    color: #0f172a;
    pointer-events: none;
}

@media (max-width: 768px) {
    .footer-container {
        flex-direction: column;
        gap: 20px;
    }
    .smart-travel-footer {
        padding: 20px;
    }
}
</style>