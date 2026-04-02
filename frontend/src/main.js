import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // ดึงไฟล์ router ที่คุณเขียนไว้มาใช้งาน
import './style.css'

const app = createApp(App)

// --- จุดสำคัญที่ต้องเพิ่ม ---
app.use(router)
// ------------------------

app.mount('#app')