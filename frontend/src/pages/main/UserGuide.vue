<template>
  <div class="guide-container">
    <div class="guide-header">
      <h1>{{ t("guide.title") }}</h1>
      <p class="guide-subtitle">{{ t("guide.subtitle") }}</p>
    </div>

    <div class="guide-content">
      <section
        class="guide-section"
        v-for="(section, index) in guideSections"
        :key="index"
      >
        <div class="section-header" @click="toggleSection(index)">
          <div class="section-title">
            <i :class="section.icon"></i>
            <h2>{{ section.title }}</h2>
          </div>
          <i
            class="fas fa-chevron-down"
            :class="{ rotated: openedSections[index] }"
          ></i>
        </div>
        <transition name="slide-down">
          <div v-if="openedSections[index]" class="section-content">
            <p
              v-for="(paragraph, pIndex) in section.content"
              :key="pIndex"
              class="content-paragraph"
            >
              {{ paragraph }}
            </p>
            <ul v-if="section.steps" class="steps-list">
              <li v-for="(step, sIndex) in section.steps" :key="sIndex">
                <span class="step-number">{{ sIndex + 1 }}</span>
                <span class="step-text">{{ step }}</span>
              </li>
            </ul>
          </div>
        </transition>
      </section>
    </div>

    <div class="guide-tips">
      <h2>{{ t("guide.tips") }}</h2>
      <div class="tips-grid">
        <div class="tip-card" v-for="(tip, index) in tips" :key="index">
          <i :class="tip.icon"></i>
          <h3>{{ tip.title }}</h3>
          <p>{{ tip.description }}</p>
        </div>
      </div>
    </div>

    <div class="guide-footer">
      <h2>{{ t("guide.needMoreHelp") }}</h2>
      <p>{{ t("guide.visitContact") }}</p>
      <router-link to="/contact" class="btn-ta-solid">{{
        t("nav.contactSupport")
      }}</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useI18n } from "@/composables/useI18n";

const { t, locale } = useI18n();
const openedSections = ref({});

const guideDataEn = [
  {
    title: "Getting Started",
    icon: "fas fa-rocket",
    content: [
      "Welcome to Savannakhet Smart Travel! Here's how to make the most of our platform and start discovering amazing places in Savannakhet.",
      "Our platform is designed to be user-friendly and intuitive. Whether you're a first-time visitor or a frequent traveler, we've got you covered with personalized recommendations.",
    ],
    steps: [
      "Visit our homepage and explore featured destinations",
      "Create an account to unlock personalized features",
      "Browse hotels, restaurants, and attractions",
      "Save your favorite places to your collection",
    ],
  },
  {
    title: "Creating Your Account",
    icon: "fas fa-user-plus",
    content: [
      "Creating an account is free and takes just a few minutes. Having an account allows you to save places, write reviews, and receive personalized recommendations.",
      "All you need is a valid email address and you're ready to go!",
    ],
    steps: [
      'Click "Sign in" button in the top navigation',
      'Click "Register" to create a new account',
      "Enter your email, username, and password",
      "Verify your email by clicking the link in the confirmation email",
      "Start using all premium features!",
    ],
  },
  {
    title: "Exploring Places",
    icon: "fas fa-map-location-dot",
    content: [
      "Savannakhet has so much to offer! Use our smart search and filter features to find exactly what you're looking for.",
      "Whether you're interested in hotels, restaurants, natural attractions, or cultural landmarks, we've got comprehensive information for each location.",
    ],
    steps: [
      "Use the search bar or browse by category",
      "Filter by price, rating, and distance",
      "Click on any place to see detailed information",
      "Check opening hours, contact info, and location on map",
      "Read reviews from other travelers",
    ],
  },
  {
    title: "Saving & Managing Favorites",
    icon: "fas fa-heart",
    content: [
      "Save places you love to your personal collection. This helps our AI learn your preferences and provide better recommendations in the future.",
      "You can access all your saved places anytime from your profile.",
    ],
    steps: [
      "Click the heart icon on any place card",
      'The place is added to your "Saves" collection',
      "Go to your profile to view all saved places",
      "Organize your saves into custom collections",
      "Share your favorite places with friends",
    ],
  },
  {
    title: "Writing Reviews",
    icon: "fas fa-pen-nib",
    content: [
      "Your reviews help other travelers make informed decisions. Share your honest experiences and help the community!",
      "Be descriptive and helpful - mention what you loved or didn't love about the place.",
    ],
    steps: [
      "Visit a place detail page",
      "Scroll to the reviews section",
      'Click "Write Review"',
      "Add a title and rating",
      "Write your detailed review",
      "Add up to 5 photos from your visit",
      "Click submit and your review goes live!",
    ],
  },
  {
    title: "Personalized Recommendations",
    icon: "fas fa-sparkles",
    content: [
      "Our AI engine learns from your behavior to provide increasingly better recommendations over time.",
      "The more you interact with our platform - browsing, saving, and rating places - the smarter our recommendations become.",
    ],
    steps: [
      "Browse and save places you like",
      "Rate places using our rating system",
      "Write reviews to share your opinions",
      'Check out the "Recommended for You" section',
      "AI learns your preferences and improves suggestions",
    ],
  },
  {
    title: "Language Settings",
    icon: "fas fa-globe",
    content: [
      "We support multiple languages to make your experience better. You can switch languages anytime using the language selector in the navigation bar.",
      "Currently supported languages: English, Thai, Lao, and Vietnamese.",
    ],
    steps: [
      "Look for the language icon in the top right",
      "Click the globe icon",
      "Select your preferred language",
      "The entire interface updates instantly",
      "Your preference is saved for future visits",
    ],
  },
  {
    title: "Mobile-Friendly Features",
    icon: "fas fa-mobile-alt",
    content: [
      "Our platform is fully optimized for mobile devices. Use it on the go to find restaurants, hotels, and attractions on your phone or tablet.",
      "All features are accessible from mobile, including browsing, saving, and writing reviews.",
    ],
    steps: [
      "Visit our site from any mobile device",
      "Everything is responsive and touch-friendly",
      "Use the search function to find places nearby",
      "View maps and directions on your phone",
      "Write reviews and take photos on the go",
    ],
  },
];

const guideDataTh = [
  {
    title: "เริ่มต้นใช้งาน",
    icon: "fas fa-rocket",
    content: [
      "ยินดีต้อนรับสู่ Savannakhet Smart Travel! นี่คือวิธีการสูงสุดของแพลตฟอร์มของเราและเริ่มค้นพบสถานที่ที่น่าตื่นตาในเมืองสะหวันนะเขด",
      "แพลตฟอร์มของเราออกแบบมาให้เป็นมิตรกับผู้ใช้และโดยตรง ไม่ว่าคุณจะเป็นผู้เยี่ยมชมครั้งแรกหรือนักท่องเที่ยวชำนาญการ เรามีคำแนะนำที่ปรับแต่งให้เหมาะสมสำหรับคุณ",
    ],
    steps: [
      "ไปที่หน้าแรกและสำรวจสถานที่ท่องเที่ยวที่แนะนำ",
      "สร้างบัญชีเพื่อปลดล็อคฟีเจอร์ที่ปรับแต่งให้เหมาะสม",
      "เรียกดูโรงแรม ร้านอาหาร และสถานที่ท่องเที่ยว",
      "บันทึกสถานที่ที่ชอบของคุณลงในคอลเลกชันของคุณ",
    ],
  },
  {
    title: "การสร้างบัญชีของคุณ",
    icon: "fas fa-user-plus",
    content: [
      "การสร้างบัญชีเป็นแบบฟรีและใช้เวลาเพียงไม่กี่นาที การมีบัญชีช่วยให้คุณบันทึกสถานที่ เขียนรีวิว และรับคำแนะนำที่ปรับแต่งให้เหมาะสม",
      "สิ่งที่คุณต้องคือที่อยู่อีเมลที่ถูกต้องและคุณก็พร้อมไป!",
    ],
    steps: [
      'คลิกปุ่ม "เข้าสู่ระบบ" ในการนำทางด้านบน',
      'คลิก "สมัครสมาชิก" เพื่อสร้างบัญชีใหม่',
      "ป้อนอีเมล ชื่อผู้ใช้ และรหัสผ่าน",
      "ยืนยันอีเมลของคุณโดยคลิกลิงก์ในอีเมลยืนยัน",
      "เริ่มใช้ฟีเจอร์พรีเมียมทั้งหมด!",
    ],
  },
  {
    title: "สำรวจสถานที่",
    icon: "fas fa-map-location-dot",
    content: [
      "สะหวันนะเขดมีอะไรมากมายให้เสนอ! ใช้ฟีเจอร์ค้นหาและตัวกรองที่ชาญฉลาดของเราเพื่อค้นหาสิ่งที่คุณกำลังมองหา",
      "ไม่ว่าคุณจะสนใจโรงแรม ร้านอาหาร สถานที่ท่องเที่ยวในธรรมชาติ หรือสถานที่เก่าแก่ทางวัฒนธรรม เรามีข้อมูลที่ครอบคลุมสำหรับแต่ละสถานที่",
    ],
    steps: [
      "ใช้แถบค้นหาหรือเรียกดูตามหมวดหมู่",
      "ตัวกรองตามราคา คะแนน และระยะทาง",
      "คลิกที่สถานที่ใดก็ได้เพื่อดูข้อมูลโดยละเอียด",
      "ตรวจสอบเวลาเปิด ข้อมูลติดต่อ และที่ตั้งบนแผนที่",
      "อ่านรีวิวจากนักท่องเที่ยวคนอื่นๆ",
    ],
  },
  {
    title: "การบันทึกและการจัดการรายการโปรด",
    icon: "fas fa-heart",
    content: [
      "บันทึกสถานที่ที่คุณรักลงในคอลเลกชันส่วนตัวของคุณ สิ่งนี้ช่วยให้ AI เรียนรู้ความชอบของคุณและให้คำแนะนำที่ดีขึ้นในอนาคต",
      "คุณสามารถเข้าถึงสถานที่ที่บันทึกไว้ของคุณได้ตลอดเวลาจากโปรไฟล์ของคุณ",
    ],
    steps: [
      "คลิกไอคอนหัวใจบนไพ่สถานที่ใด ๆ",
      'สถานที่จะถูกเพิ่มลงในคอลเลกชัน "บันทึก" ของคุณ',
      "ไปที่โปรไฟล์ของคุณเพื่อดูสถานที่ที่บันทึกไว้ทั้งหมด",
      "จัดระเบียบการบันทึกของคุณเป็นคอลเลกชันที่กำหนดเอง",
      "แชร์สถานที่ที่ชื่นชอบกับเพื่อน",
    ],
  },
];

const guideSections = computed(() => {
  if (locale.value === "th") return guideDataTh;
  return guideDataEn;
});

const tips = computed(() => {
  if (locale.value === "th") {
    return [
      {
        icon: "fas fa-lightbulb",
        title: "ใช้ตัวกรอง",
        description:
          "ใช้ตัวกรองเพื่อหาสถานที่ที่ตรงกับงบประมาณและความสนใจของคุณ",
      },
      {
        icon: "fas fa-star",
        title: "ให้คะแนน",
        description: "ให้คะแนนสถานที่ที่คุณไป AI ของเราจะเรียนรู้ความชอบของคุณ",
      },
      {
        icon: "fas fa-share",
        title: "แชร์กับเพื่อน",
        description: "แชร์การบันทึกของคุณกับเพื่อนและครอบครัว",
      },
      {
        icon: "fas fa-mobile-alt",
        title: "ใช้บนมือถือ",
        description: "เข้าถึงแพลตฟอร์มของเราได้ง่ายบนอุปกรณ์มือถือใด ๆ",
      },
    ];
  }
  return [
    {
      icon: "fas fa-lightbulb",
      title: "Use Filters",
      description:
        "Use filters to find places that match your budget and interests",
    },
    {
      icon: "fas fa-star",
      title: "Rate Places",
      description:
        "Rate the places you visit so our AI can learn your preferences",
    },
    {
      icon: "fas fa-share",
      title: "Share with Friends",
      description: "Share your saves with friends and family",
    },
    {
      icon: "fas fa-mobile-alt",
      title: "Use on Mobile",
      description: "Access our platform easily on any mobile device",
    },
  ];
});

const toggleSection = (index) => {
  openedSections.value[index] = !openedSections.value[index];
};
</script>

<style scoped>
.guide-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
  min-height: calc(100vh - 300px);
}

.guide-header {
  text-align: center;
  margin-bottom: 50px;
}

.guide-header h1 {
  font-size: 2.5rem;
  color: #333;
  margin: 0 0 10px 0;
}

.guide-subtitle {
  font-size: 1.1rem;
  color: #666;
  margin: 0;
}

.guide-content {
  margin-bottom: 60px;
}

.guide-section {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  margin-bottom: 15px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.guide-section:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-color: #3498db;
}

.section-header {
  padding: 20px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f9f9f9;
  transition: all 0.3s ease;
}

.section-header:hover {
  background-color: #f0f8ff;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 15px;
  flex: 1;
}

.section-title i {
  font-size: 1.5rem;
  color: #3498db;
}

.section-title h2 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

.section-header i.fa-chevron-down {
  font-size: 0.9rem;
  color: #3498db;
  transition: transform 0.3s ease;
}

.section-header i.rotated {
  transform: rotate(180deg);
}

.section-content {
  padding: 20px;
  background-color: #fff;
  border-top: 1px solid #e0e0e0;
}

.content-paragraph {
  margin: 0 0 15px 0;
  color: #555;
  line-height: 1.6;
  font-size: 1rem;
}

.steps-list {
  list-style: none;
  padding: 0;
  margin: 20px 0 0 0;
}

.steps-list li {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 5px;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  background-color: #3498db;
  color: white;
  border-radius: 50%;
  font-weight: 600;
  margin-right: 15px;
  flex-shrink: 0;
}

.step-text {
  color: #555;
  line-height: 1.5;
}

.guide-tips {
  margin-bottom: 60px;
}

.guide-tips h2 {
  font-size: 2rem;
  color: #333;
  text-align: center;
  margin-bottom: 30px;
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.tip-card {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  padding: 30px;
  border-radius: 8px;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
}

.tip-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
}

.tip-card i {
  font-size: 2.5rem;
  margin-bottom: 15px;
}

.tip-card h3 {
  font-size: 1.3rem;
  margin: 15px 0;
}

.tip-card p {
  margin: 0;
  opacity: 0.9;
  line-height: 1.5;
}

.guide-footer {
  background: linear-gradient(135deg, #2ecc71, #27ae60);
  color: white;
  padding: 40px;
  border-radius: 8px;
  text-align: center;
}

.guide-footer h2 {
  font-size: 1.8rem;
  margin: 0 0 10px 0;
}

.guide-footer p {
  font-size: 1.1rem;
  margin: 0 0 20px 0;
  opacity: 0.9;
}

.guide-footer .btn-ta-solid {
  background-color: white;
  color: #2ecc71;
  border: none;
  padding: 12px 30px;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
}

.guide-footer .btn-ta-solid:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px);
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from {
  opacity: 0;
  max-height: 0;
}

.slide-down-leave-to {
  opacity: 0;
  max-height: 0;
}

@media (max-width: 768px) {
  .guide-container {
    padding: 20px;
  }

  .guide-header h1 {
    font-size: 2rem;
  }

  .section-header {
    padding: 15px;
  }

  .section-title h2 {
    font-size: 1.1rem;
  }

  .tips-grid {
    grid-template-columns: 1fr;
  }
}
</style>
