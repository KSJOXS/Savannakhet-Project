<template>
  <div class="auth-page">
    <LanguageSwitcherAuth />

    <div class="auth-card">
      <div class="auth-brand">
        <span class="auth-brand-icon">🌴</span>
        <span class="auth-brand-name">Savannakhet Smart Travel</span>
      </div>

      <button v-if="step === 1" @click="router.push('/')" class="btn-back">
        <i class="fas fa-chevron-left"></i> {{ t("auth.back_home") }}
      </button>
      <button v-else @click="step = 1" class="btn-back">
        <i class="fas fa-chevron-left"></i> {{ t("auth.back_account") }}
      </button>

      <div class="step-indicator">
        <div class="step-dot" :class="{ active: step === 1 }"></div>
        <div class="step-dot" :class="{ active: step === 2 }"></div>
      </div>

      <div v-if="step === 1">
        <div class="auth-header">
          <h2>{{ t("auth.register_title") }}</h2>
          <p>{{ t("auth.register_subtitle") }}</p>
        </div>

        <form @submit.prevent="step = 2" class="auth-form">
          <div class="input-group">
            <label>{{ t("auth.username") }}</label>
            <div class="input-with-icon">
              <i class="fas fa-user"></i>
              <input
                v-model="form.username"
                type="text"
                :placeholder="t('auth.username_placeholder')"
                required
              />
            </div>
          </div>

          <div class="input-group">
            <label>{{ t("auth.email") }}</label>
            <div class="input-with-icon">
              <i class="fas fa-envelope"></i>
              <input
                v-model="form.email"
                type="email"
                :placeholder="t('auth.email_placeholder')"
                required
              />
            </div>
          </div>

          <div class="input-group">
            <label>{{ t("auth.password") }}</label>
            <div class="input-with-icon">
              <i class="fas fa-lock"></i>
              <input
                v-model="form.password"
                type="password"
                :placeholder="t('auth.password_hint')"
                required
              />
            </div>
          </div>

          <div class="terms-group">
            <label class="checkbox-container">
              <input type="checkbox" v-model="form.acceptedTerms" required />
              <span class="checkmark"></span>
              <span class="terms-text">
                {{ t("auth.accept_terms_prefix") }}
                <a href="/terms" target="_blank" class="terms-link">{{
                  t("auth.terms_link")
                }}</a>
                {{ t("auth.accept_terms_mid") }}
                <a href="/privacy" target="_blank" class="terms-link">{{
                  t("auth.privacy_link")
                }}</a>
              </span>
            </label>
          </div>

          <button
            type="submit"
            class="btn-submit"
            :disabled="!form.acceptedTerms"
          >
            {{ t("auth.next_interests") }}
            <i class="fas fa-arrow-right" style="margin-left: 8px"></i>
          </button>
        </form>
      </div>

      <div v-else>
        <div class="auth-header">
          <h2>{{ t("auth.interests_title") }}</h2>
          <p>{{ t("auth.interests_subtitle") }}</p>
        </div>

        <div class="interests-grid">
          <div
            v-for="interest in availableInterests"
            :key="interest.id"
            class="interest-item"
            :class="{ selected: form.preferences.includes(interest.id) }"
            @click="toggleInterest(interest.id)"
          >
            <i :class="interest.icon"></i>
            <span>{{ t(interest.key) }}</span>
          </div>
        </div>

        <p v-if="errorMsg" class="error-msg">⚠️ {{ errorMsg }}</p>

        <button @click="handleRegister" :disabled="loading" class="btn-submit">
          <span v-if="loading"
            ><i class="fas fa-spinner fa-spin mr-2"></i>
            {{ t("auth.creating_account") }}</span
          >
          <span v-else>{{ t("auth.complete_reg") }}</span>
        </button>
      </div>

      <div class="auth-footer">
        <span>{{ t("auth.already_have_account") }}</span>
        <router-link to="/login">{{ t("auth.sign_in_here") }}</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { authRepository } from "@/repositories/authRepository";
import { useRouter } from "vue-router";
import { useI18n } from "@/composables/useI18n";
import LanguageSwitcherAuth from "@/components/LanguageSwitcherAuth.vue";

const { t } = useI18n();
const router = useRouter();
const step = ref(1);
const loading = ref(false);
const errorMsg = ref("");

const form = ref({
  username: "",
  email: "",
  password: "",
  preferences: [],
  acceptedTerms: false,
});

const availableInterests = [
  { id: "nature", key: "auth.interest_nature", icon: "fas fa-mountain" },
  { id: "culture", key: "auth.interest_culture", icon: "fas fa-vihara" },
  { id: "cafe", key: "auth.interest_cafe", icon: "fas fa-coffee" },
  {
    id: "local_food",
    key: "auth.interest_local_food",
    icon: "fas fa-bowl-food",
  },
  { id: "landmark", key: "auth.interest_landmark", icon: "fas fa-camera" },
  { id: "chill", key: "auth.interest_chill", icon: "fas fa-walking" },
];

const toggleInterest = (id) => {
  const index = form.value.preferences.indexOf(id);
  if (index === -1) {
    form.value.preferences.push(id);
  } else {
    form.value.preferences.splice(index, 1);
  }
};

const handleRegister = async () => {
  loading.value = true;
  errorMsg.value = "";
  try {
    await authRepository.register(form.value);
    router.push("/login?registered=1");
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || t("common.error");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@import "@/assets/auth.css";

.mr-2 {
  margin-right: 8px;
}
</style>
