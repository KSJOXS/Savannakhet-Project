<template>
    <div class="admin-dashboard">
        <header class="dashboard-header">
            <h2><i class="fas fa-chart-line"></i> Dashboard Overview</h2>
            <p>Welcome back, Admin. ข้อมูลอัปเดตจากระบบ</p>
        </header>

        <div v-if="loading" class="loading-state">
            <div class="spinner"></div>
            <p>กำลังโหลดข้อมูลสถิติ...</p>
        </div>

        <div v-else>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon user-bg"><i class="fas fa-users"></i></div>
                    <div class="stat-info">
                        <h3>Total Users</h3>
                        <p class="stat-number">{{ dashboardData.total_users || 0 }}</p>
                        <span class="stat-change positive">Registered</span>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon location-bg"><i class="fas fa-map-marker-alt"></i></div>
                    <div class="stat-info">
                        <h3>Locations</h3>
                        <p class="stat-number">{{ dashboardData.total_places || 0 }}</p>
                        <span class="stat-change">Active Destinations</span>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon review-bg"><i class="fas fa-star"></i></div>
                    <div class="stat-info">
                        <h3>Total Reviews</h3>
                        <p class="stat-number">{{ dashboardData.total_reviews || 0 }}</p>
                        <span class="stat-change positive">Interactions</span>
                    </div>
                </div>
            </div>

            <div class="dashboard-content">
                <div class="content-card">
                    <h3><i class="fas fa-heart"></i> Category Distribution</h3>
                    <div class="category-stats" v-if="dashboardData.categories.length > 0">
                        <div v-for="(cat, idx) in dashboardData.categories" :key="idx" class="progress-item">
                            <div class="progress-label">
                                <span>{{ cat.name }}</span>
                                <span>{{ cat.count }} places</span>
                            </div>
                            <div class="progress-bar-bg">
                                <div class="progress-bar-fill"
                                    :style="{ width: (cat.count / dashboardData.total_places * 100) + '%', background: '#3498db' }">
                                </div>
                            </div>
                        </div>
                    </div>
                    <p v-else class="no-data">ยังไม่มีข้อมูลหมวดหมู่</p>
                </div>

                <div class="content-card">
                    <h3><i class="fas fa-award"></i> Top Rated Locations</h3>
                    <table class="mini-table">
                        <thead>
                            <tr>
                                <th>Place Name</th>
                                <th>Rating</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="p in dashboardData.top_places" :key="p.id">
                                <td><strong>{{ p.name }}</strong></td>
                                <td><i class="fas fa-star text-warning"></i> {{ p.rating }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const loading = ref(true)
const dashboardData = ref({
    total_users: 0,
    total_places: 0,
    total_reviews: 0,
    categories: [],
    top_places: []
})

const fetchStats = async () => {
    loading.value = true
    try {
        const response = await axios.get('http://localhost:8000/admin/stats')
        console.log("API Result:", response.data) // เช็คใน Console (F12)
        dashboardData.value = response.data
    } catch (error) {
        console.error("Dashboard Error:", error)
        alert("เซิร์ฟเวอร์เกิดข้อผิดพลาด (500) กรุณาเช็ค Backend Terminal")
    } finally {
        loading.value = false
    }
}

onMounted(fetchStats)
</script>

<style scoped>
.admin-dashboard {
    padding: 25px;
    background: #f8fafc;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.stat-card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
}

.stat-icon {
    width: 55px;
    height: 55px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
}

.user-bg {
    background: #e0f2fe;
    color: #0369a1;
}

.location-bg {
    background: #f0fdf4;
    color: #166534;
}

.review-bg {
    background: #fefce8;
    color: #854d0e;
}

.stat-number {
    font-size: 1.8rem;
    font-weight: 800;
    margin: 5px 0;
    color: #0f172a;
}

.dashboard-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 25px;
}

.content-card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
}

.progress-item {
    margin-bottom: 15px;
}

.progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    margin-bottom: 5px;
    font-weight: 600;
}

.progress-bar-bg {
    background: #f1f5f9;
    height: 8px;
    border-radius: 10px;
    overflow: hidden;
}

.progress-bar-fill {
    height: 100%;
    transition: width 0.5s ease;
}

.mini-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}

.mini-table th {
    text-align: left;
    font-size: 0.75rem;
    color: #94a3b8;
    text-transform: uppercase;
    padding-bottom: 10px;
}

.mini-table td {
    padding: 12px 0;
    border-bottom: 1px solid #f8fafc;
    font-size: 0.9rem;
}

.text-warning {
    color: #f59e0b;
}

.loading-state {
    text-align: center;
    padding: 100px;
}

.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}
</style>
