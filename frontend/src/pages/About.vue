<template>
    <div class="about-page">
        <Navbar />

        <div class="about-header">
            <div class="header-container">
                <h1>About Savannakhet Smart Travel</h1>
                <p>Discover how we use AI to create the perfect travel experience for you.</p>
            </div>
        </div>

        <div class="main-layout">
            <div class="intro-section">
                <h2>Project Objectives & Core Features</h2>
                <p class="intro-text">
                    This project was developed to support and elevate tourism in Savannakhet Province.
                    By integrating Artificial Intelligence (AI), we analyze user preferences to recommend
                    the most suitable and personalized destinations for every traveler.
                </p>
            </div>

            <div class="features-grid">
                <div class="feature-card">
                    <div class="icon-box"><i class="fas fa-brain"></i></div>
                    <h3>GNN Integration</h3>
                    <p>Developed a smart tourism platform for Savannakhet, integrating a Graph Neural Network (GNN) to
                        deliver highly personalized travel recommendations based on user preferences.</p>
                </div>

                <div class="feature-card">
                    <div class="icon-box"><i class="fas fa-mobile-alt"></i></div>
                    <h3>User-Friendly UI</h3>
                    <p>Designed and implemented an intuitive user interface, enabling users to seamlessly explore
                        destinations, read reviews, and receive tailored travel itineraries.</p>
                </div>

                <div class="feature-card">
                    <div class="icon-box"><i class="fas fa-project-diagram"></i></div>
                    <h3>Graph Relationship Learning</h3>
                    <p>Engineered and trained a GNN model to map and analyze complex graph relationships between users,
                        locations, and interests, significantly improving recommendation accuracy.</p>
                </div>

                <div class="feature-card">
                    <div class="icon-box"><i class="fas fa-cogs"></i></div>
                    <h3>Admin Management System</h3>
                    <p>Built a comprehensive Admin Dashboard for managing tourist attractions, moderating user reviews,
                        and monitoring overall system statistics.</p>
                </div>

                <div class="feature-card">
                    <div class="icon-box"><i class="fas fa-shield-alt"></i></div>
                    <h3>Security & Scalability</h3>
                    <p>Ensured a robust system architecture with a strong focus on high availability, excellent data
                        security, and future scalability.</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

.about-page {
    background-color: #f7f9fa;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    color: #1e293b;
}

/* Header */
.about-header {
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
    max-width: 1000px;
    margin: 40px auto;
    padding: 0 20px;
}

.intro-section {
    text-align: center;
    margin-bottom: 40px;
}

.intro-section h2 {
    font-size: 1.8rem;
    font-weight: 800;
    color: #000;
    margin-bottom: 15px;
}

.intro-text {
    font-size: 1.05rem;
    color: #475569;
    line-height: 1.6;
    max-width: 800px;
    margin: 0 auto;
}

/* Grid Cards */
.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    padding-bottom: 60px;
}

.feature-card {
    background: white;
    padding: 30px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    transition: 0.3s;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    border-color: #cbd5e1;
}

.icon-box {
    width: 60px;
    height: 60px;
    background: #f1f5f9;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    color: #3498db;
    margin-bottom: 20px;
}

.feature-card h3 {
    font-size: 1.2rem;
    font-weight: 800;
    margin: 0 0 15px;
    color: #0f172a;
}

.feature-card p {
    font-size: 0.95rem;
    color: #475569;
    line-height: 1.6;
    margin: 0;
}

@media (max-width: 768px) {
    .features-grid {
        grid-template-columns: 1fr;
    }

    .header-container h1 {
        font-size: 2rem;
    }
}
</style>