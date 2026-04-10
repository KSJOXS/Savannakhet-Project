import api from '@/services/api';

const settingRepository = {
    // Get all settings
    getAll() {
        return api.get('/api/settings');
    },
    // Get specific setting
    getByKey(key_name) {
        return api.get(`/api/settings/${key_name}`);
    },
    // Create or update setting (text values)
    upsert(key_name, data) {
        return api.put(`/api/settings/${key_name}`, data);
    },

    // 🚨 อัปเดต: เพิ่มการรับค่า keyName เพื่อแยกหน้า (Home, Recommend, Admin)
    uploadHeroImage(file, keyName) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('key_name', keyName); // บอก Backend ว่ารูปนี้ของคีย์อะไร
        return api.post('/api/settings/hero-images/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
    },

    // 🚨 อัปเดต: ส่ง keyName ไปตอนลบด้วย
    removeHeroImage(imageUrl, keyName) {
        return api.delete(`/api/settings/hero-images/remove?image_url=${encodeURIComponent(imageUrl)}&key_name=${keyName}`);
    }
};

export default settingRepository;