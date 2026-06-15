<template>
  <div class="history-page">
    <Navbar />

    <section class="hero-section">
      <div class="hero-bg">
        <img src="/images/heritage/main.png" alt="Savannakhet Hero" />
        <div class="hero-gradient"></div>
      </div>
      <div class="hero-content">
        <span class="badge">{{ t("history.hero_badge") }}</span>
        <h1 class="display-title">{{ t("history.hero_title") }}</h1>
        <p class="subtitle">
          {{ t("history.hero_subtitle") }}
        </p>
      </div>
    </section>

    <main class="main-container">
      <section class="story-block intro-block">
        <div class="text-wrapper text-center">
          <h2 class="section-title">{{ t("history.intro_title") }}</h2>
          <p class="lead-text">
            {{ t("history.intro_lead") }}
          </p>
          <p>
            {{ t("history.intro_desc") }}
          </p>
        </div>
      </section>

      <section class="story-block split-block">
        <div class="split-image">
          <img src="/images/heritage/culture.png" alt="Colonial Architecture" />
          <div class="img-caption">{{ t("history.colonial_caption") }}</div>
        </div>
        <div class="split-text">
          <h2 class="section-title">{{ t("history.colonial_title") }}</h2>
          <p>
            {{ t("history.colonial_desc1") }}
          </p>
          <p>
            {{ t("history.colonial_desc2") }}
          </p>
        </div>
      </section>

      <section class="story-block split-block reverse">
        <div class="split-image">
          <img
            src="https://images.unsplash.com/photo-1542385151-efd9000785a0?q=80&w=2069&auto=format&fit=crop"
            alt="Local Culture"
          />
          <div class="img-caption">{{ t("history.culture_caption") }}</div>
        </div>
        <div class="split-text">
          <h2 class="section-title">{{ t("history.culture_title") }}</h2>
          <p>
            {{ t("history.culture_desc") }}
          </p>
          <div class="quote-box">
            <i class="fas fa-quote-left quote-icon"></i>
            <p>{{ t("history.culture_quote") }}</p>
          </div>
        </div>
      </section>

      <section class="landmarks-highlight">
        <div class="text-center mb-10">
          <span class="sub-heading">{{ t("history.landmarks_eyebrow") }}</span>
          <h2 class="section-title">{{ t("history.landmarks_title") }}</h2>
          <p class="lead-text">{{ t("history.landmarks_subtitle") }}</p>
        </div>

        <div class="landmark-cards">
          <div class="l-card" @click="router.push('/explore')">
            <div class="l-card-img">
              <img src="/images/history/ing_hang.png" alt="That Ing Hang" />
            </div>
            <div class="l-card-content">
              <h3>{{ t("history.card_inghang_title") }}</h3>
              <p>{{ t("history.card_inghang_desc") }}</p>
              <span class="explore-btn"
                >Explore <i class="fas fa-arrow-right"></i
              ></span>
            </div>
          </div>

          <div class="l-card" @click="router.push('/explore')">
            <div class="l-card-img">
              <img
                src="/images/history/st_teresa.png"
                alt="St. Teresa Church"
              />
            </div>
            <div class="l-card-content">
              <h3>{{ t("history.card_teresa_title") }}</h3>
              <p>{{ t("history.card_teresa_desc") }}</p>
              <span class="explore-btn"
                >Explore <i class="fas fa-arrow-right"></i
              ></span>
            </div>
          </div>

          <div class="l-card" @click="router.push('/explore')">
            <div class="l-card-img">
              <img
                src="/images/history/old_town.png"
                alt="Old Town Savannakhet"
              />
            </div>
            <div class="l-card-content">
              <h3>{{ t("history.card_oldtown_title") }}</h3>
              <p>{{ t("history.card_oldtown_desc") }}</p>
              <span class="explore-btn"
                >Explore <i class="fas fa-arrow-right"></i
              ></span>
            </div>
          </div>
        </div>
      </section>
    </main>

    <section class="history-cta">
      <div class="cta-content">
        <h2>{{ t("history.cta_title") }}</h2>
        <button class="btn-primary-large" @click="router.push('/explore')">
          <i class="fas fa-compass"></i> {{ t("history.cta_btn") }}
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import Navbar from "@/components/Navbar.vue";
import { useI18n } from "@/composables/useI18n";

const router = useRouter();
const { t } = useI18n();
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap");

.history-page {
  background-color: #ffffff;
  min-height: 100vh;
  font-family: "Inter", sans-serif;
  color: #0f172a;
}

/* ==========================================================================
   Modern Hero Section
   ========================================================================== */
.hero-section {
  position: relative;
  height: 70vh;
  min-height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  overflow: hidden;
  margin-bottom: 60px;
}

.hero-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.hero-bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scale(1.05);
  /* Slight scale to hide edges during load */
}

.hero-gradient {
  position: absolute;
  inset: 0;
  /* Modern soft gradient: dark at bottom, slightly clear at top */
  background: linear-gradient(
    180deg,
    rgba(15, 23, 42, 0.3) 0%,
    rgba(15, 23, 42, 0.8) 100%
  );
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 800px;
  padding: 0 20px;
  color: #ffffff;
  animation: fadeUp 1s ease-out forwards;
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.badge {
  display: inline-block;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.4);
  color: white;
  padding: 8px 20px;
  border-radius: 30px;
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 25px;
}

.display-title {
  font-size: 4.5rem;
  font-weight: 900;
  margin: 0 0 20px;
  line-height: 1.1;
  letter-spacing: -1px;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.subtitle {
  font-size: 1.25rem;
  font-weight: 400;
  color: #f8fafc;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
}

/* ==========================================================================
   Main Content Layout
   ========================================================================== */
.main-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 20px 80px;
}

.section-title {
  font-size: 2.2rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 25px;
  line-height: 1.3;
  letter-spacing: -0.5px;
}

.sub-heading {
  display: block;
  font-size: 0.9rem;
  font-weight: 700;
  color: #00aa6c;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 10px;
}

.lead-text {
  font-size: 1.25rem;
  color: #334155;
  line-height: 1.8;
  margin-bottom: 20px;
}

.story-block {
  margin-bottom: 100px;
}

.story-block p {
  font-size: 1.1rem;
  color: #475569;
  line-height: 1.8;
  margin-bottom: 20px;
}

/* Intro Text Block */
.intro-block .text-wrapper {
  max-width: 800px;
  margin: 0 auto;
}

.text-center {
  text-align: center;
}

/* Split Blocks (Text + Image side by side) */
.split-block {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

.split-block.reverse {
  direction: rtl;
  /* Flip layout */
}

.split-block.reverse > * {
  direction: ltr;
  /* Reset text direction inside */
}

.split-image {
  position: relative;
}

.split-image img {
  width: 100%;
  height: 450px;
  object-fit: cover;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  transition: transform 0.5s ease;
}

.split-image:hover img {
  transform: translateY(-10px);
}

.img-caption {
  margin-top: 12px;
  font-size: 0.85rem;
  color: #94a3b8;
  text-align: center;
  font-style: italic;
}

/* Quote Box */
.quote-box {
  background: #f8fafc;
  border-left: 4px solid #00aa6c;
  padding: 30px;
  border-radius: 0 16px 16px 0;
  margin-top: 30px;
  position: relative;
}

.quote-icon {
  font-size: 1.5rem;
  color: #cbd5e1;
  margin-bottom: 10px;
}

.quote-box p {
  font-size: 1.2rem;
  font-style: italic;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
  line-height: 1.6;
}

/* ==========================================================================
   Landmarks Highlight Cards
   ========================================================================== */
.landmarks-highlight {
  margin-top: 120px;
  padding-top: 80px;
  border-top: 1px solid #f1f5f9;
}

.mb-10 {
  margin-bottom: 50px;
}

.landmark-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.l-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.l-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
  border-color: #cbd5e1;
}

.l-card-img {
  height: 220px;
  width: 100%;
  overflow: hidden;
}

.l-card-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.l-card:hover .l-card-img img {
  transform: scale(1.05);
}

.l-card-content {
  padding: 25px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.l-card-content h3 {
  font-size: 1.25rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 10px;
}

.l-card-content p {
  font-size: 0.95rem;
  color: #64748b;
  line-height: 1.6;
  margin: 0 0 20px;
  flex: 1;
}

.explore-btn {
  font-size: 0.9rem;
  font-weight: 700;
  color: #00aa6c;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: gap 0.2s;
}

.l-card:hover .explore-btn {
  gap: 12px;
  /* Arrow moves slightly to right on hover */
}

/* ==========================================================================
   Footer Action Area
   ========================================================================== */
.history-cta {
  background: #0f172a;
  color: white;
  text-align: center;
  padding: 100px 20px;
}

.cta-content {
  max-width: 800px;
  margin: 0 auto;
}

.cta-content h2 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 40px;
  font-family: "Playfair Display", serif;
}

.btn-primary-large {
  background: #00aa6c;
  color: white;
  border: none;
  padding: 18px 45px;
  font-size: 1.15rem;
  font-weight: 700;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 15px 30px rgba(0, 170, 108, 0.25);
  display: inline-flex;
  align-items: center;
  gap: 12px;
}

.btn-primary-large:hover {
  background: #00ca80;
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 170, 108, 0.35);
}

/* ==========================================================================
   Responsive Design
   ========================================================================== */
@media (max-width: 992px) {
  .display-title {
    font-size: 3.5rem;
  }

  .split-block {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .split-block.reverse {
    direction: ltr;
  }

  .split-image img {
    height: 350px;
  }

  .landmark-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .display-title {
    font-size: 2.8rem;
  }

  .hero-section {
    height: 60vh;
    min-height: 400px;
  }

  .section-title {
    font-size: 1.8rem;
  }

  .lead-text {
    font-size: 1.1rem;
  }

  .landmark-cards {
    grid-template-columns: 1fr;
  }

  .footer-content h2 {
    font-size: 1.8rem;
  }
}
</style>
