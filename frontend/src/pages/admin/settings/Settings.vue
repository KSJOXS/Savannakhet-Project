<template>
    <div class="admin-page">
        <transition name="toast">
            <div v-if="toast.show" :class="['toast', toast.type]">
                <i :class="toast.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
                {{ toast.message }}
            </div>
        </transition>

        <div class="header-content">
            <div class="title-section">
                <h3><i class="fas fa-sliders-h"></i> Master Website Settings</h3>
                <p class="subtitle">Manage global configurations, contact details, and banner images across the platform.</p>
            </div>
        </div>

        <div class="settings-layout">
            <div class="card settings-card">
                <div class="card-header">
                    <h4><i class="fas fa-address-card"></i> General & Contact Information</h4>
                </div>
                <div class="card-body">
                    <div class="form-row">
                        <div class="form-group half">
                            <label>Contact Phone Number</label>
                            <div class="input-wrapper">
                                <i class="fas fa-phone-alt"></i>
                                <input type="text" v-model="settings.contact_phone" placeholder="e.g. 020-999-8888" />
                            </div>
                        </div>
                        <div class="form-group half">
                            <label>Contact Email</label>
                            <div class="input-wrapper">
                                <i class="fas fa-envelope"></i>
                                <input type="email" v-model="settings.contact_email" placeholder="e.g. info@savannakhet.com" />
                            </div>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Footer Text (Copyright)</label>
                        <div class="input-wrapper">
                            <i class="fas fa-copyright"></i>
                            <input type="text" v-model="settings.footer_text" placeholder="e.g. 🌴 Savannakhet Smart Travel © 2026" />
                        </div>
                    </div>
                </div>
            </div>

            <div class="card settings-card hero-card">
                <div class="card-header">
                    <div class="header-row">
                        <h4><i class="fas fa-images"></i> Manage Website Images</h4>
                    </div>
                    <p class="card-subtitle">Upload backgrounds for specific pages. (Images auto-save upon upload)</p>
                </div>
                
                <div class="card-body">
                    <div class="tabs-container">
                        <button :class="['tab-btn', { active: activeTab === 'home' }]" @click="activeTab = 'home'">
                            <i class="fas fa-home"></i> Homepage (Explore)
                        </button>
                        <button :class="['tab-btn', { active: activeTab === 'recommend' }]" @click="activeTab = 'recommend'">
                            <i class="fas fa-star"></i> Recommend List
                        </button>
                    </div>

                    <div class="tab-content">
                        <div class="tab-header-info">
                            <h5>Background Images for: <strong>{{ activeTabName }}</strong></h5>
                            <span class="image-count-badge" :class="{ full: activeImagesList.length >= 10 }">
                                {{ activeImagesList.length }} / 10
                            </span>
                        </div>

                        <div v-if="activeImagesList.length > 0" class="image-gallery">
                            <div v-for="(url, index) in activeImagesList" :key="index" class="gallery-item">
                                <img :src="url" :alt="`Image ${index + 1}`" />
                                <div class="gallery-overlay"><span class="img-index">{{ index + 1 }}</span></div>
                                <button @click="removeImage(url)" class="btn-remove-gallery" :disabled="removingUrl === url">
                                    <i v-if="removingUrl === url" class="fas fa-spinner fa-spin"></i>
                                    <i v-else class="fas fa-times"></i>
                                </button>
                            </div>

                            <div v-if="activeImagesList.length < 10" class="gallery-item add-slot" @click="triggerFileInput">
                                <div class="add-slot-inner">
                                    <i class="fas fa-plus-circle"></i>
                                    <span>Add Image</span>
                                </div>
                            </div>
                        </div>

                        <div v-else class="upload-box" @click="triggerFileInput">
                            <div class="upload-icon-wrap"><i class="fas fa-cloud-upload-alt"></i></div>
                            <p>Click to upload images for {{ activeTabName }}</p>
                            <span>Up to 10 images · JPG, PNG, WEBP · Recommended 1920×1080</span>
                        </div>

                        <div v-if="isUploading" class="upload-progress">
                            <div class="progress-bar"><div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div></div>
                            <span>Uploading {{ currentUploadIndex }} of {{ totalToUpload }}...</span>
                        </div>
                    </div>
                </div>
            </div>

            <input type="file" ref="fileInput" class="hidden-input" accept="image/jpeg,image/png,image/webp" multiple @change="onFilesSelected"/>
        </div>

        <div class="master-action-bar">
            <div class="save-info">
                <i class="fas fa-info-circle"></i> <span>Images are saved automatically. Press save to apply text changes.</span>
            </div>
            <button @click="saveAllSettings" class="btn-master-save" :disabled="isSaving">
                <i v-if="isSaving" class="fas fa-spinner fa-spin"></i>
                <i v-else class="fas fa-save"></i>
                {{ isSaving ? 'Saving Changes...' : 'Save All Settings' }}
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from 'vue';
import settingRepository from '@/repositories/settingRepository';

// General Settings State
const settings = reactive({ 
    contact_phone: '', 
    contact_email: '',
    footer_text: ''
});

// Image States for Tabs
const activeTab = ref('home'); // 'home' | 'recommend' | 'admin'
const imagesHome = ref([]);
const imagesRecommend = ref([]);

// UI States
const isSaving = ref(false);
const isUploading = ref(false);
const uploadProgress = ref(0);
const currentUploadIndex = ref(0);
const totalToUpload = ref(0);
const removingUrl = ref(null);
const fileInput = ref(null);

const toast = reactive({ show: false, message: '', type: 'success' });
const showToast = (message, type = 'success') => {
    toast.message = message; toast.type = type; toast.show = true;
    setTimeout(() => { toast.show = false; }, 3500);
};

// Map Tabs to UI text and DB Keys
const activeTabName = computed(() => {
    if (activeTab.value === 'home') return 'Homepage (Explore)';
    if (activeTab.value === 'recommend') return 'Recommend List Page';
    return '';
});

const activeSettingKey = computed(() => {
    if (activeTab.value === 'home') return 'hero_images_public';
    if (activeTab.value === 'recommend') return 'hero_images_recommend';
    return '';
});

// Dynamic List based on active tab
const activeImagesList = computed({
    get: () => {
        if (activeTab.value === 'home') return imagesHome.value;
        if (activeTab.value === 'recommend') return imagesRecommend.value;
        return [];
    },
    set: (val) => {
        if (activeTab.value === 'home') imagesHome.value = val;
        else if (activeTab.value === 'recommend') imagesRecommend.value = val;
    }
});

const getFullImageUrl = (url) => {
    if (!url) return '';
    if (url.startsWith('http') || url.startsWith('data:')) return url;
    return `http://127.0.0.1:8000/${url.startsWith('/') ? url.slice(1) : url}`;
};

// Load all configurations
const loadSettings = async () => {
    try {
        const res = await settingRepository.getAll();
        res.data.forEach(s => {
            // Text Settings
            if (s.key_name === 'contact_phone') settings.contact_phone = s.value || '';
            if (s.key_name === 'contact_email') settings.contact_email = s.value || '';
            if (s.key_name === 'footer_text') settings.footer_text = s.value || '';
            
            // Image Settings
            if (['hero_images_public', 'hero_images_recommend', 'hero_images_admin', 'hero_images'].includes(s.key_name)) {
                try {
                    const parsed = JSON.parse(s.value || '[]');
                    const fullUrls = parsed.map(url => getFullImageUrl(url));
                    
                    if (s.key_name === 'hero_images_public' || s.key_name === 'hero_images') imagesHome.value = fullUrls;
                    if (s.key_name === 'hero_images_recommend') imagesRecommend.value = fullUrls;
                } catch (e) { console.error(e) }
            }
        });
    } catch (err) { console.error('Failed to load settings:', err); }
};

// 💾 Master Save Function
const saveAllSettings = async () => {
    isSaving.value = true;
    try {
        await Promise.all([
            settingRepository.upsert('contact_phone', { value: settings.contact_phone }),
            settingRepository.upsert('contact_email', { value: settings.contact_email }),
            settingRepository.upsert('footer_text', { value: settings.footer_text })
        ]);
        showToast('Website settings saved successfully!', 'success');
    } catch (error) {
        showToast('Failed to save settings.', 'error');
    } finally {
        isSaving.value = false;
    }
};

const triggerFileInput = () => {
    if (activeImagesList.value.length >= 10) {
        showToast('Maximum 10 images reached.', 'error'); return;
    }
    fileInput.value.click();
};

const onFilesSelected = async (e) => {
    const files = Array.from(e.target.files);
    if (!files.length) return;

    const remaining = 10 - activeImagesList.value.length;
    const filesToUpload = files.slice(0, remaining);
    
    isUploading.value = true;
    totalToUpload.value = filesToUpload.length;
    currentUploadIndex.value = 0;

    for (let i = 0; i < filesToUpload.length; i++) {
        currentUploadIndex.value = i + 1;
        try {
            // 🚨 อัปโหลดรูป พร้อมส่งชื่อ Tab (Key) ไปด้วย
            const res = await settingRepository.uploadHeroImage(filesToUpload[i], activeSettingKey.value);
            if (res.data && res.data.all_images) {
                activeImagesList.value = res.data.all_images.map(url => getFullImageUrl(url));
            }
        } catch (err) {
            showToast('Upload failed', 'error'); break;
        }
        uploadProgress.value = Math.round(((i + 1) / filesToUpload.length) * 100);
    }

    isUploading.value = false; e.target.value = '';
    showToast(`${filesToUpload.length} image(s) uploaded!`, 'success');
};

const removeImage = async (url) => {
    removingUrl.value = url;
    try {
        const pathOnly = url.replace('http://127.0.0.1:8000', '');
        // 🚨 ลบรูป พร้อมส่งชื่อ Tab (Key) ไปด้วย
        const res = await settingRepository.removeHeroImage(pathOnly, activeSettingKey.value);
        if (res.data && res.data.all_images) {
            activeImagesList.value = res.data.all_images.map(img => getFullImageUrl(img));
        }
        showToast('Image removed.', 'success');
    } catch (err) {
        showToast('Failed to remove image.', 'error');
    } finally {
        removingUrl.value = null;
    }
};

onMounted(loadSettings);
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap');

.admin-page { font-family: 'Kanit', sans-serif; color: #334155; padding: 30px 40px 100px; max-width: 1300px; margin: 0; min-height: 100vh; background-color: #f1f5f9; }
.toast { position: fixed; top: 24px; right: 24px; z-index: 9999; padding: 14px 22px; border-radius: 12px; font-size: 0.95rem; font-weight: 500; display: flex; align-items: center; gap: 10px; box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12); }
.toast.success { background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }
.toast.error { background: #fff1f2; color: #9f1239; border: 1px solid #fecdd3; }

.header-content { margin-bottom: 30px; border-left: 5px solid #0f172a; padding-left: 20px; }
.title-section h3 { font-size: 1.8rem; font-weight: 700; color: #0f172a; margin: 0; display: flex; align-items: center; gap: 12px; }
.subtitle { color: #64748b; font-size: 1rem; margin-top: 4px; }
.settings-layout { display: flex; flex-direction: column; gap: 24px; }

.card { background: white; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border: 1px solid #e2e8f0; overflow: hidden; }
.card-header { background: #f8fafc; padding: 16px 24px; border-bottom: 1px solid #e2e8f0; }
.card-header h4 { margin: 0; font-weight: 700; color: #1e293b; font-size: 1.15rem; display: flex; align-items: center; gap: 10px; }
.card-subtitle { margin: 6px 0 0 32px; font-size: 0.85rem; color: #64748b; }
.card-body { padding: 24px; }

/* Forms */
.form-row { display: flex; gap: 20px; }
.form-group.half { flex: 1; }
.form-group { margin-bottom: 20px; }
.form-group label { display: block; font-size: 0.95rem; font-weight: 600; color: #475569; margin-bottom: 8px; }
.input-wrapper { position: relative; }
.input-wrapper i { position: absolute; left: 16px; top: 50%; transform: translateY(-50%); color: #94a3b8; }
.input-wrapper input { width: 100%; padding: 12px 12px 12px 48px; border: 1.5px solid #e2e8f0; border-radius: 10px; font-size: 0.95rem; background: #f8fafc; transition: 0.2s; box-sizing: border-box; }
.input-wrapper input:focus { background: white; border-color: #3b82f6; outline: none; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1); }

/* Tabs */
.tabs-container { display: flex; gap: 10px; border-bottom: 2px solid #f1f5f9; padding-bottom: 15px; margin-bottom: 20px; }
.tab-btn { background: #f8fafc; border: 1px solid #e2e8f0; padding: 10px 20px; font-size: 0.95rem; font-weight: 600; color: #64748b; cursor: pointer; border-radius: 8px; transition: 0.2s; display: flex; align-items: center; gap: 8px; }
.tab-btn:hover { background: #f1f5f9; color: #0f172a; }
.tab-btn.active { background: #0f172a; color: white; border-color: #0f172a; }

.tab-header-info { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.tab-header-info h5 { margin: 0; font-size: 1.05rem; color: #334155; font-weight: 500;}
.image-count-badge { background: #dbeafe; color: #1e40af; font-size: 0.8rem; font-weight: 700; padding: 4px 12px; border-radius: 50px; }

/* Gallery */
.image-gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
.gallery-item { position: relative; aspect-ratio: 16/9; border-radius: 12px; overflow: hidden; background: #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: 0.2s; }
.gallery-item:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.15); }
.gallery-item img { width: 100%; height: 100%; object-fit: cover; }
.gallery-overlay { position: absolute; top: 8px; left: 8px; }
.img-index { background: rgba(0,0,0,0.6); color: white; font-size: 0.75rem; padding: 2px 8px; border-radius: 20px; }
.btn-remove-gallery { position: absolute; top: 8px; right: 8px; width: 30px; height: 30px; border-radius: 50%; background: rgba(255,255,255,0.95); color: #ef4444; border: none; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,0.2); opacity: 0; transition: 0.2s; }
.gallery-item:hover .btn-remove-gallery { opacity: 1; }

.gallery-item.add-slot { border: 2px dashed #cbd5e1; background: #f8fafc; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.add-slot-inner { text-align: center; color: #94a3b8; font-weight: 600; }
.add-slot-inner i { font-size: 2rem; display: block; margin-bottom: 5px; }

.upload-box { border: 2px dashed #cbd5e1; border-radius: 16px; padding: 60px 20px; text-align: center; cursor: pointer; background: #f8fafc; }
.upload-box:hover { background: #f1f5f9; border-color: #94a3b8; }
.upload-icon-wrap { font-size: 3.5rem; color: #94a3b8; margin-bottom: 16px; }
.upload-box p { font-size: 1.1rem; font-weight: 600; color: #475569; margin: 0 0 6px; }
.hidden-input { display: none; }

/* Progress */
.upload-progress { margin-top: 16px; }
.progress-bar { width: 100%; height: 8px; background: #e2e8f0; border-radius: 50px; overflow: hidden; margin-bottom: 8px; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #3b82f6, #60a5fa); border-radius: 50px; transition: width 0.3s ease; }

/* 💾 Master Action Bar */
.master-action-bar {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: white;
    padding: 16px 40px;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.05);
    display: flex;
    justify-content: flex-end;
    align-items: center;
    z-index: 100;
    border-top: 1px solid #e2e8f0;
}
.save-info { color: #64748b; font-size: 0.9rem; margin-right: 24px; display: flex; align-items: center; gap: 8px;}
.save-info i { color: #3b82f6; }
.btn-master-save {
    background: #0f172a; color: white; border: none; padding: 14px 32px;
    border-radius: 50px; font-weight: 700; font-size: 1rem; cursor: pointer;
    display: flex; align-items: center; gap: 10px; box-shadow: 0 4px 15px rgba(15, 23, 42, 0.2);
    transition: 0.2s; font-family: 'Kanit', sans-serif;
}
.btn-master-save:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(15, 23, 42, 0.3); }
.btn-master-save:disabled { background: #94a3b8; cursor: not-allowed; box-shadow: none; }

@media (max-width: 768px) {
    .form-row { flex-direction: column; gap: 0; }
    .master-action-bar { flex-direction: column; gap: 15px; padding: 15px; text-align: center; }
    .save-info { margin-right: 0; font-size: 0.8rem; }
    .btn-master-save { width: 100%; justify-content: center; }
    .admin-page { padding: 20px 20px 150px; }
}
</style>