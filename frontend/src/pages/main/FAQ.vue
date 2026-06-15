<template>
  <div class="faq-page-wrapper">
    <Navbar />
    
    <div class="faq-container">
      <button class="back-btn" @click="router.back()">
        <i class="fas fa-arrow-left"></i> {{ t('nav.home') || 'Back' }}
      </button>

      <div class="faq-header">
        <h1>{{ t('faq.title') }}</h1>
        <p class="faq-subtitle">{{ t('faq.subtitle') }}</p>
      </div>

    <div class="faq-content">
      <div class="faq-item" v-for="(item, index) in faqItems" :key="index">
        <div class="faq-question" @click="toggleFaq(index)">
          <span class="faq-title">{{ item.question }}</span>
          <i class="fas fa-chevron-down" :class="{ rotated: openedFaq[index] }"></i>
        </div>
        <transition name="slide-down">
          <div v-if="openedFaq[index]" class="faq-answer">
            {{ item.answer }}
          </div>
        </transition>
      </div>
    </div>

    <div class="faq-contact">
      <h2>{{ t('faq.stillNeedHelp') }}</h2>
      <p>{{ t('faq.contactUs') }}</p>
      <router-link to="/contact" class="btn-ta-solid">{{ t('nav.contactSupport') }}</router-link>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from '@/composables/useI18n'
import Navbar from '@/components/Navbar.vue'

const router = useRouter()
const { t, locale } = useI18n()
const openedFaq = ref({})

const faqData = {
  en: [
    {
      question: 'What is Savannakhet Smart Travel?',
      answer: 'Savannakhet Smart Travel is an intelligent travel guide platform that helps you discover the best places to visit, hotels to stay, and restaurants to eat in Savannakhet city using AI-powered recommendations.'
    },
    {
      question: 'How do I create an account?',
      answer: 'To create an account, click the "Sign in" button in the top right corner of the page. Then click "Register" and fill in your email, username, and password. You\'ll receive a confirmation email to verify your account.'
    },
    {
      question: 'How does the recommendation system work?',
      answer: 'Our AI system analyzes your preferences, past visits, and interests to provide personalized recommendations. The more you use the platform and rate places, the better the recommendations become.'
    },
    {
      question: 'Can I save my favorite places?',
      answer: 'Yes! You can save any place to your favorites by clicking the heart icon. Your saved places will appear in the "Saves" section of your profile.'
    },
    {
      question: 'How do I write a review?',
      answer: 'First, visit the place detail page and scroll to the reviews section. Click "Write Review" to share your experience with other travelers. You can rate the place and add photos.'
    },
    {
      question: 'Is the app available in multiple languages?',
      answer: 'Yes! Our platform supports English, Thai, Lao, and Vietnamese. You can change the language using the language selector in the top navigation bar.'
    },
    {
      question: 'How do I report an issue?',
      answer: 'If you encounter any bugs or issues, please use the "Report Issue" option in the Help menu or go to the Contact page to get in touch with our support team.'
    },
    {
      question: 'Is my personal data safe?',
      answer: 'We take data privacy seriously. All your personal information is encrypted and stored securely. We never share your data with third parties without your consent.'
    }
  ],
  th: [
    {
      question: 'Savannakhet Smart Travel คืออะไร?',
      answer: 'Savannakhet Smart Travel เป็นแพลตฟอร์มท่องเที่ยวอัจฉริยะที่ช่วยคุณค้นพบสถานที่ที่ดีที่สุด โรงแรม และร้านอาหารในเมืองสะหวันนะเขด โดยใช้ระบบแนะนำที่ขับเคลื่อนด้วย AI'
    },
    {
      question: 'ฉันจะสร้างบัญชีได้อย่างไร?',
      answer: 'ในการสร้างบัญชี ให้คลิกปุ่ม "เข้าสู่ระบบ" ที่มุมบนขวาของหน้า จากนั้นคลิก "สมัครสมาชิก" และกรอกอีเมล ชื่อผู้ใช้ และรหัสผ่าน คุณจะได้รับอีเมลยืนยันการสมัครสมาชิก'
    },
    {
      question: 'ระบบแนะนำทำงานอย่างไร?',
      answer: 'ระบบ AI ของเราวิเคราะห์ความชอบของคุณ การเยี่ยมชมในอดีต และความสนใจเพื่อให้คำแนะนำที่ปรับแต่งให้เหมาะสม ยิ่งคุณใช้แพลตฟอร์มมากขึ้นและให้คะแนนสถานที่มากขึ้น คำแนะนำก็จะดีขึ้น'
    },
    {
      question: 'ฉันสามารถบันทึกสถานที่ที่ชอบได้หรือไม่?',
      answer: 'ได้! คุณสามารถบันทึกสถานที่ใดๆ ไปยังรายการที่ชอบโดยคลิกไอคอนหัวใจ สถานที่ที่บันทึกไว้ของคุณจะปรากฏในส่วน "รายการที่บันทึก" ของโปรไฟล์ของคุณ'
    },
    {
      question: 'ฉันจะเขียนรีวิวได้อย่างไร?',
      answer: 'ก่อนอื่น ให้ไปที่หน้ารายละเอียดสถานที่และเลื่อนไปที่ส่วนรีวิว คลิก "เขียนรีวิว" เพื่อแบ่งปันประสบการณ์ของคุณกับนักท่องเที่ยวอื่นๆ คุณสามารถให้คะแนนสถานที่และเพิ่มรูปภาพ'
    },
    {
      question: 'แอปพลิเคชันใช้ได้กับหลายภาษาหรือไม่?',
      answer: 'ได้! แพลตฟอร์มของเรารองรับภาษาอังกฤษ ไทย ลาว และเวียดนาม คุณสามารถเปลี่ยนภาษาโดยใช้ตัวเลือกเลือกภาษาในแถบนำทางด้านบน'
    },
    {
      question: 'ฉันจะรายงานปัญหาได้อย่างไร?',
      answer: 'หากคุณพบข้อผิดพลาดหรือปัญหาใดๆ โปรดใช้ตัวเลือก "รายงานปัญหา" ในเมนูช่วยเหลือ หรือไปที่หน้าติดต่อเพื่อติดต่อทีมสนับสนุน'
    },
    {
      question: 'ข้อมูลส่วนตัวของฉันปลอดภัยหรือไม่?',
      answer: 'เราให้ความสำคัญกับความเป็นส่วนตัวของข้อมูล ข้อมูลส่วนตัวของคุณทั้งหมดจะถูกเข้ารหัสและจัดเก็บอย่างปลอดภัย เราจะไม่เปิดเผยข้อมูลของคุณให้กับบุคคลที่สามโดยไม่ได้รับความยินยอม'
    }
  ],
  la: [
    {
      question: 'ສະວັນນະເຂດສະມາດ ທຣາວເວລ ແມ່ນຫຍັງ?',
      answer: 'Savannakhet Smart Travel ແມ່ນແພລັດຟອມການທ່ອງທ່ຽວທີ່ສະຫລາດທີ່ຊ່ວຍໃຫ້ທ່ານຄົ້ນພົບສະຖານທີ່ທີ່ດີທີ່ສຸດ, ໂຮງແຮມ ແລະຮ້ານອາຫານໃນນະຄອນສະວັນນະເຂດໂດຍໃຊ້ລະບົບຄຳແນະນຳທີ່ຂັບເຄື່ອນໂດຍ AI'
    },
    {
      question: 'ຂ້ອຍຈະສ້າງບັນຊີໄດ້ແນວໃດ?',
      answer: 'ເພື່ອສ້າງບັນຊີ, ໃຫ້ຄລິກປຸ່ມ "ເຂົ້າສູ່ລະບົບ" ຢູ່ທີ່ມຸມເທິງຂວາຂອງໜ້າ ຫຼັງຈາກນັ້ນ ໃຫ້ຄລິກ "ລົງທະບຽນ" ແລະ ຕື່ມ E-mail, ຊື່ຜູ້ໃຊ້ ແລະ ລະຫັດຜ່ານ ທ່ານຈະໄດ້ຮັບອີເມວຢືນຢັນ'
    },
    {
      question: 'ລະບົບຄຳແນະນຳເຮັດວຽກແນວໃດ?',
      answer: 'ລະບົບ AI ຂອງພວກເຮົາວິເຄາະຄວາມມັກຂອງທ່ານ, ການຢ້ຽມຢາມທີ່ຜ່ານມາ ແລະ ຄວາມສົນໃຈເພື່ອໃຫ້ຄຳແນະນຳສ່ວນບຸກຄົນ. ຍິ່ງທ່ານໃຊ້ແພລັດຟອມຫຼາຍຂື້ນ ແລະ ໃຫ້ຄະແນນສະຖານທີ່ຫຼາຍຂື້ນ ຄຳແນະນຳກໍ່ຈະດີຂື້ນ'
    },
    {
      question: 'ຂ້ອຍສາມາດບັນທຶກສະຖານທີ່ທີ່ມັກໄດ້ບໍ?',
      answer: 'ໄດ້! ທ່ານສາມາດບັນທຶກສະຖານທີ່ໃດໜຶ່ງໄປຍັງສະຖານທີ່ທີ່ມັກໂດຍຄລິກໄອຄອນຫົວໃຈ ສະຖານທີ່ທີ່ທ່ານບັນທຶກໄວ້ຈະປາກົດຢູ່ໃນພາກ "ລາຍການທີ່ບັນທຶກ" ຂອງໂປຣໄຟລ໌ຂອງທ່ານ'
    },
    {
      question: 'ຂ້ອຍຈະຂຽນບົດວິຈານໄດ້ແນວໃດ?',
      answer: 'ກ່ອນອື່ນ ໃຫ້ໄປຫາໜ້າລາຍລະອຽດສະຖານທີ່ ແລະ ເລື່ອນລົງໄປຍັງພາກບົດວິຈານ ຄລິກ "ຂຽນບົດວິຈານ" ເພື່ອແບ່ງປັນປະສົບການຂອງທ່ານ ທ່ານສາມາດໃຫ້ຄະແນນສະຖານທີ່ ແລະ ເພີ່ມຮູບຖ່າຍ'
    },
    {
      question: 'ແອັບພລິເຄຊັນມີຫຼາຍພາສາບໍ?',
      answer: 'ໄດ້! ແພລັດຟອມຂອງພວກເຮົາສະໜັບສະໜູນພາສາອັງກິດ, ໄທ, ລາວ ແລະ ວຽດນາມ ທ່ານສາມາດປ່ຽນພາສາໂດຍໃຊ້ຕົວເລືອກຕົວເລືອກພາສາໃນແຖບນຳທາງເທິງ'
    },
    {
      question: 'ຂ້ອຍຈະລາຍງານບັນຫາໄດ້ແນວໃດ?',
      answer: 'ຫາກທ່ານພົບຂໍ້ຜິດພາດ ຫຼື ບັນຫາໃດໆ ກະລຸນາໃຊ້ຕົວເລືອກ "ລາຍງານບັນຫາ" ໃນເມນູຊ່ວຍເຫຼືອ ຫຼື ໄປຫາໜ້າຕິດຕໍ່ເພື່ອຕິດຕໍ່ທີມສະໜັບສະໜູນ'
    },
    {
      question: 'ຂໍ້ມູນສ່ວນໂຕຂອງຂ້ອຍປອດໄພບໍ?',
      answer: 'ພວກເຮົາໃຫ້ຄວາມສຳຄັນກັບຄວາມເປັນສ່ວນຕົວຂອງຂໍ້ມູນ ຂໍ້ມູນສ່ວນໂຕທັງໝົດຂອງທ່ານຖືກເຂົ້າລະຫັດ ແລະ ເກັບຮັກສາຢ່າງປອດໄພ ພວກເຮົາຈະບໍ່ເປີດເຜີຍຂໍ້ມູນຂອງທ່ານໃຫ້ບຸກຄົນທີ່ສາມໂດຍບໍ່ໄດ້ຮັບການອະນຸມັດ'
    }
  ],
  vi: [
    {
      question: 'Du lịch thông minh Savannakhet là gì?',
      answer: 'Savannakhet Smart Travel là một nền tảng du lịch thông minh giúp bạn khám phá những nơi tốt nhất để thăm, khách sạn để ở và nhà hàng để ăn ở thành phố Savannakhet bằng cách sử dụng các khuyến nghị được hỗ trợ bởi AI.'
    },
    {
      question: 'Làm cách nào tôi có thể tạo một tài khoản?',
      answer: 'Để tạo tài khoản, hãy nhấp vào nút "Đăng nhập" ở góc trên bên phải của trang. Sau đó nhấp vào "Đăng ký" và điền email, tên người dùng và mật khẩu của bạn. Bạn sẽ nhận được email xác nhận để xác minh tài khoản của bạn.'
    },
    {
      question: 'Hệ thống đề xuất hoạt động như thế nào?',
      answer: 'Hệ thống AI của chúng tôi phân tích sở thích, các chuyến thăm quá khứ và sở thích của bạn để cung cấp các khuyến nghị được cá nhân hóa. Bạn sử dụng nền tảng nhiều hơn và đánh giá các địa điểm, các khuyến nghị sẽ trở nên tốt hơn.'
    },
    {
      question: 'Tôi có thể lưu các địa điểm yêu thích của mình không?',
      answer: 'Có! Bạn có thể lưu bất kỳ nơi nào vào các địa điểm yêu thích của bạn bằng cách nhấp vào biểu tượng trái tim. Các địa điểm đã lưu của bạn sẽ xuất hiện trong phần "Đã lưu" của hồ sơ của bạn.'
    },
    {
      question: 'Làm cách nào tôi có thể viết một bài đánh giá?',
      answer: 'Đầu tiên, hãy truy cập trang chi tiết địa điểm và cuộn xuống phần đánh giá. Nhấp vào "Viết đánh giá" để chia sẻ trải nghiệm của bạn với các du khách khác. Bạn có thể đánh giá địa điểm và thêm ảnh.'
    },
    {
      question: 'Ứng dụng có sẵn bằng nhiều ngôn ngữ không?',
      answer: 'Có! Nền tảng của chúng tôi hỗ trợ tiếng Anh, tiếng Thái, tiếng Lào và tiếng Việt. Bạn có thể thay đổi ngôn ngữ bằng trình chọn ngôn ngữ trong thanh điều hướng trên cùng.'
    },
    {
      question: 'Làm cách nào tôi có thể báo cáo một vấn đề?',
      answer: 'Nếu bạn gặp phải bất kỳ lỗi nào hoặc vấn đề, vui lòng sử dụng tùy chọn "Báo cáo sự cố" trong menu Trợ giúp hoặc truy cập trang Liên hệ để liên hệ với nhóm hỗ trợ của chúng tôi.'
    },
    {
      question: 'Dữ liệu cá nhân của tôi có an toàn không?',
      answer: 'Chúng tôi coi trọng quyền riêng tư của dữ liệu. Tất cả thông tin cá nhân của bạn được mã hóa và lưu trữ an toàn. Chúng tôi không bao giờ chia sẻ dữ liệu của bạn với các bên thứ ba mà không có sự đồng ý của bạn.'
    }
  ]
}

const faqItems = computed(() => faqData[locale.value] || faqData.en)

const toggleFaq = (index) => {
  openedFaq.value[index] = !openedFaq.value[index]
}
</script>

<style scoped>
.faq-page-wrapper {
  background-color: #f7f9fa;
  min-height: 100vh;
}

.faq-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 20px;
  min-height: calc(100vh - 300px);
}

.back-btn {
  background: transparent;
  border: none;
  color: #3498db;
  font-size: 1.05rem;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: color 0.2s;
}

.back-btn:hover {
  color: #2980b9;
}

.faq-header {
  text-align: center;
  margin-bottom: 50px;
}

.faq-header h1 {
  font-size: 2.5rem;
  color: #333;
  margin: 0 0 10px 0;
}

.faq-subtitle {
  font-size: 1.1rem;
  color: #666;
  margin: 0;
}

.faq-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 60px;
}

.faq-item {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.faq-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-color: #3498db;
}

.faq-question {
  padding: 20px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f9f9f9;
  transition: all 0.3s ease;
}

.faq-question:hover {
  background-color: #f0f8ff;
}

.faq-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.faq-question i {
  font-size: 0.9rem;
  color: #3498db;
  transition: transform 0.3s ease;
}

.faq-question i.rotated {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 20px;
  background-color: #fff;
  color: #555;
  line-height: 1.6;
  border-top: 1px solid #e0e0e0;
}

.faq-contact {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  padding: 40px;
  border-radius: 8px;
  text-align: center;
}

.faq-contact h2 {
  font-size: 1.8rem;
  margin: 0 0 10px 0;
}

.faq-contact p {
  font-size: 1.1rem;
  margin: 0 0 20px 0;
  opacity: 0.9;
}

.faq-contact .btn-ta-solid {
  background-color: white;
  color: #3498db;
  border: none;
  padding: 12px 30px;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
}

.faq-contact .btn-ta-solid:hover {
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
  .faq-container {
    padding: 20px;
  }

  .faq-header h1 {
    font-size: 2rem;
  }

  .faq-question {
    padding: 15px;
  }

  .faq-title {
    font-size: 1rem;
  }
}
</style>
