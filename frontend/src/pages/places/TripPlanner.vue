<template>
  <div class="trip-planner-page">
    <!-- Back Button -->
    <button class="btn-back-floating" @click="goBack">
      <i class="fas fa-arrow-left"></i>
      <span>{{ t("common.back") || "Back" }}</span>
    </button>

    <section class="planner-hero">
      <div class="hero-bg">
        <img src="/images/planner_bg.png" alt="Travel Background" />
        <div class="hero-overlay"></div>
      </div>

      <div class="hero-content">
        <div class="header-badge">
          <i class="fas fa-sparkles"></i>
          <span>{{ t("tripPlanner.badge") }}</span>
        </div>
        <h1 class="display-title">{{ t("tripPlanner.title") }}</h1>
        <p class="subtitle">{{ t("tripPlanner.subtitle") }}</p>
      </div>
    </section>

    <div class="planner-container" :class="{ 'has-itinerary': itinerary }">
      <!-- Input Form -->
      <div class="search-bar-wrapper" v-if="!itinerary">
        <div class="search-bar">
          <!-- Month Section -->
          <div
            class="search-section"
            @click.stop="
              showMonthDropdown = !showMonthDropdown;
              showDaysDropdown = false;
              showInterestDropdown = false;
              showBudgetDropdown = false;
            "
          >
            <div class="section-icon"><i class="fas fa-calendar-alt"></i></div>
            <div class="section-content">
              <div class="section-label">{{ t("tripPlanner.month") }}</div>
              <div class="section-value has-value">
                {{ selectedMonthName }}
              </div>
            </div>

            <div
              class="dropdown-menu month-dropdown"
              v-if="showMonthDropdown"
              @click.stop
            >
              <div class="dropdown-header">
                {{ t("tripPlanner.selectMonth") }}
              </div>
              <div class="month-grid">
                <div
                  class="month-item"
                  v-for="m in months"
                  :key="m.id"
                  :class="{ active: selectedMonth === m.id }"
                  @click="
                    selectedMonth = m.id;
                    showMonthDropdown = false;
                  "
                >
                  {{ m.name }}
                </div>
              </div>
            </div>
          </div>

          <div class="divider"></div>

          <!-- Budget Section -->
          <div
            class="search-section"
            @click.stop="
              showBudgetDropdown = !showBudgetDropdown;
              showDaysDropdown = false;
              showMonthDropdown = false;
              showInterestDropdown = false;
            "
          >
            <div class="section-icon"><i class="fas fa-wallet"></i></div>
            <div class="section-content">
              <div class="section-label">{{ t("tripPlanner.budget") }}</div>
              <div class="section-value has-value">
                {{ selectedBudgetText }}
              </div>
            </div>

            <div
              class="dropdown-menu budget-dropdown"
              v-if="showBudgetDropdown"
              @click.stop
            >
              <div class="dropdown-header">
                {{ t("tripPlanner.selectBudget") }}
              </div>
              <div class="dropdown-list">
                <div
                  class="pref-item"
                  v-for="b in budgets"
                  :key="b.id"
                  :class="{ active: selectedBudget === b.id }"
                  @click="
                    selectedBudget = b.id;
                    showBudgetDropdown = false;
                  "
                >
                  <i v-if="b.id === 'any'" class="fas fa-coins"></i>
                  <i v-else-if="b.id === 'low'" class="fas fa-wallet"></i>
                  <i
                    v-else-if="b.id === 'moderate'"
                    class="fas fa-credit-card"
                  ></i>
                  <i v-else class="fas fa-crown"></i>
                  <span>{{ b.label }}</span>
                  <i
                    class="fas fa-check check-icon"
                    v-if="selectedBudget === b.id"
                  ></i>
                </div>
              </div>
            </div>
          </div>

          <div class="divider"></div>

          <!-- Interests Section -->
          <div
            class="search-section"
            @click.stop="
              showInterestDropdown = !showInterestDropdown;
              showDaysDropdown = false;
              showMonthDropdown = false;
              showBudgetDropdown = false;
            "
          >
            <div class="section-icon"><i class="fas fa-heart"></i></div>
            <div class="section-content">
              <div class="section-label">{{ t("tripPlanner.interests") }}</div>
              <div
                class="section-value"
                :class="{ 'has-value': selectedPreferences.length > 0 }"
              >
                {{ selectedPreferencesText }}
              </div>
            </div>

            <div class="dropdown-menu" v-if="showInterestDropdown" @click.stop>
              <div class="dropdown-header">
                {{ t("tripPlanner.selectInterests") }}
              </div>
              <div class="dropdown-list">
                <div
                  class="pref-item"
                  v-for="pref in availablePreferences"
                  :key="pref.id"
                  :class="{ active: selectedPreferences.includes(pref.id) }"
                  @click="togglePreference(pref.id)"
                >
                  <i :class="pref.icon"></i>
                  <span>{{ pref.label }}</span>
                  <i
                    class="fas fa-check check-icon"
                    v-if="selectedPreferences.includes(pref.id)"
                  ></i>
                </div>
              </div>
            </div>
          </div>

          <div class="divider"></div>

          <!-- Days Section -->
          <div
            class="search-section"
            @click.stop="
              showDaysDropdown = !showDaysDropdown;
              showInterestDropdown = false;
              showMonthDropdown = false;
              showBudgetDropdown = false;
            "
          >
            <div class="section-icon"><i class="fas fa-clock"></i></div>
            <div class="section-content">
              <div class="section-label">{{ t("tripPlanner.duration") }}</div>
              <div class="section-value has-value">
                {{ days }}
                {{ days === 1 ? t("tripPlanner.day") : t("tripPlanner.days") }}
              </div>
            </div>

            <div
              class="dropdown-menu days-dropdown"
              v-if="showDaysDropdown"
              @click.stop
            >
              <div class="dropdown-header">{{ t("tripPlanner.duration") }}</div>
              <div class="dropdown-list">
                <div
                  class="pref-item"
                  v-for="d in 5"
                  :key="d"
                  :class="{ active: days === d }"
                  @click="
                    days = d;
                    showDaysDropdown = false;
                  "
                >
                  <i class="fas fa-calendar-day"></i>
                  <span
                    >{{ d }}
                    {{
                      d === 1 ? t("tripPlanner.day") : t("tripPlanner.days")
                    }}</span
                  >
                  <i class="fas fa-check check-icon" v-if="days === d"></i>
                </div>
              </div>
            </div>
          </div>

          <!-- Generate Button -->
          <div class="search-action">
            <button
              class="btn-generate-bar"
              @click="generateItinerary"
              :disabled="loading"
            >
              <i class="fas fa-spinner fa-spin" v-if="loading"></i>
              <span v-else>{{ t("tripPlanner.generate") }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Itinerary Result -->
      <div class="itinerary-result" v-else>
        <div class="result-header">
          <div class="result-title-group">
            <span class="result-eyebrow">{{ t("tripPlanner.badge") }}</span>
            <h2>{{ t("tripPlanner.yourItinerary", { days }) }}</h2>
          </div>
          <div class="action-buttons">
            <button
              v-if="user"
              class="btn-save"
              @click="saveItinerary"
              :disabled="saving"
            >
              <i class="fas fa-spinner fa-spin" v-if="saving"></i>
              <i class="fas fa-bookmark" v-else></i>
              <span>{{
                saving ? t("tripPlanner.saving") : t("tripPlanner.saveToTrips")
              }}</span>
            </button>
            <button class="btn-outline" @click="resetPlanner">
              <i class="fas fa-redo"></i>
              <span>{{ t("tripPlanner.planAnother") }}</span>
            </button>
          </div>
        </div>

        <div v-if="saveSuccess" class="save-success-alert">
          <i class="fas fa-check-circle"></i>
          <span>{{ t("tripPlanner.saveSuccess") }}</span>
        </div>

        <div class="timeline-container">
          <div
            class="day-section"
            v-for="(plan, dayLabel) in itinerary"
            :key="dayLabel"
          >
            <div
              class="day-header"
              style="
                display: flex;
                justify-content: space-between;
                align-items: center;
              "
            >
              <h3>{{ dayLabel }}</h3>
              <button
                class="btn-delete-day"
                @click="deleteDay(dayLabel)"
                :title="t('tripPlanner.deleteDay')"
              >
                <i class="fas fa-trash-alt"></i>
              </button>
            </div>

            <div class="timeline">
              <div
                class="timeline-item"
                v-for="(slot, index) in plan"
                :key="index"
              >
                <div class="time-marker">
                  <span class="time">{{ slot.time }}</span>
                  <div class="marker-dot"></div>
                  <div
                    class="marker-line"
                    v-if="index !== plan.length - 1"
                  ></div>
                </div>

                <div class="timeline-content">
                  <div class="slot-header-flex">
                    <div class="slot-label">
                      <i
                        v-if="slot.time_slot === 'Morning'"
                        class="fas fa-sun"
                        style="color: #f59e0b"
                      ></i>
                      <i
                        v-else-if="slot.time_slot === 'Afternoon'"
                        class="fas fa-cloud-sun"
                        style="color: #f97316"
                      ></i>
                      <i v-else class="fas fa-moon" style="color: #6366f1"></i>
                      {{
                        t(`tripPlanner.${slot.time_slot.toLowerCase()}`) ||
                        slot.time_slot
                      }}
                    </div>
                    <button
                      class="btn-swap"
                      @click="swapPlace(dayLabel, index, slot)"
                      :title="t('tripPlanner.changePlace') || 'Change Place'"
                    >
                      <i
                        class="fas fa-sync-alt"
                        :class="{
                          'fa-spin':
                            isSwapping &&
                            swappingSlot === `${dayLabel}-${index}`,
                        }"
                      ></i>
                    </button>
                  </div>

                  <div class="place-card" @click="goToDetail(slot.place.id)">
                    <button
                      class="btn-remove-place"
                      @click.stop="removePlace(dayLabel, index)"
                      :title="t('tripPlanner.removePlace') || 'Remove Place'"
                    >
                      <i class="fas fa-times"></i>
                    </button>
                    <div class="place-img">
                      <img
                        :src="getCoverImage(slot.place.image_url)"
                        :alt="slot.place.name"
                        @error="handleImgError"
                      />
                      <div class="match-badge" v-if="slot.is_preferred">
                        🔥
                        {{ t("tripPlanner.perfectMatch") || "Perfect Match" }}
                      </div>
                    </div>
                    <div class="place-info">
                      <div
                        style="
                          display: flex;
                          justify-content: space-between;
                          align-items: flex-start;
                        "
                      >
                        <h4>{{ slot.place.name }}</h4>
                        <div
                          v-if="getDisplaySeason(slot)"
                          class="season-badge"
                          :style="{
                            backgroundColor: getDisplaySeason(slot).bg,
                            color: getDisplaySeason(slot).color,
                          }"
                          :title="getDisplaySeason(slot).name"
                        >
                          <i :class="getDisplaySeason(slot).icon"></i>
                          <span class="season-badge-name">{{
                            getDisplaySeason(slot).name
                          }}</span>
                        </div>
                      </div>
                      <div class="rating-cat">
                        <span class="rating"
                          ><i class="fas fa-star" style="color: #f59e0b"></i>
                          {{ slot.place.rating_avg || "New" }}</span
                        >
                        <span class="dot">•</span>
                        <span class="cat">{{ slot.category_name }}</span>
                      </div>
                      <p class="desc">{{ slot.place.description }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Add Place Actions -->
            <div class="add-place-footer">
              <div class="add-chips-label">{{ t("tripPlanner.addPlace") }}</div>
              <div class="add-chips-group">
                <button
                  class="add-chip"
                  @click="addPlace(dayLabel, 'Morning')"
                  :disabled="isAddingPlace"
                >
                  <i
                    class="fas fa-plus"
                    v-if="
                      !isAddingPlace || addingSlot !== `${dayLabel}-Morning`
                    "
                  ></i>
                  <i class="fas fa-spinner fa-spin" v-else></i>
                  <span>{{ t("tripPlanner.addMorning") }}</span>
                </button>
                <button
                  class="add-chip"
                  @click="addPlace(dayLabel, 'Afternoon')"
                  :disabled="isAddingPlace"
                >
                  <i
                    class="fas fa-plus"
                    v-if="
                      !isAddingPlace || addingSlot !== `${dayLabel}-Afternoon`
                    "
                  ></i>
                  <i class="fas fa-spinner fa-spin" v-else></i>
                  <span>{{ t("tripPlanner.addAfternoon") }}</span>
                </button>
                <button
                  class="add-chip"
                  @click="addPlace(dayLabel, 'Evening')"
                  :disabled="isAddingPlace"
                >
                  <i
                    class="fas fa-plus"
                    v-if="
                      !isAddingPlace || addingSlot !== `${dayLabel}-Evening`
                    "
                  ></i>
                  <i class="fas fa-spinner fa-spin" v-else></i>
                  <span>{{ t("tripPlanner.addEvening") }}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuth } from "@/composables/useAuth";
import { useI18n } from "@/composables/useI18n";
import api from "@/services/api";

const router = useRouter();
const route = useRoute();
const { user } = useAuth();
const { t } = useI18n();

const goBack = () => {
  router.back();
};

const days = ref(2);
const loading = ref(false);
const saving = ref(false);
const saveSuccess = ref(false);
const itinerary = ref(null);

const selectedMonth = ref(new Date().getMonth() + 1);
const showMonthDropdown = ref(false);

const selectedBudget = ref("any");
const showBudgetDropdown = ref(false);

const budgets = computed(() => [
  { id: "any", label: t("tripPlanner.budgetAny") || "Any Budget" },
  { id: "low", label: t("tripPlanner.budgetLow") || "Low Budget" },
  { id: "moderate", label: t("tripPlanner.budgetModerate") || "Moderate" },
  { id: "luxury", label: t("tripPlanner.budgetLuxury") || "Luxury" },
]);

const selectedBudgetText = computed(() => {
  return (
    budgets.value.find((b) => b.id === selectedBudget.value)?.label ||
    t("tripPlanner.budgetAny") ||
    "Any Budget"
  );
});

const months = computed(() => [
  { id: 1, name: t("common.january") || "January" },
  { id: 2, name: t("common.february") || "February" },
  { id: 3, name: t("common.march") || "March" },
  { id: 4, name: t("common.april") || "April" },
  { id: 5, name: t("common.may") || "May" },
  { id: 6, name: t("common.june") || "June" },
  { id: 7, name: t("common.july") || "July" },
  { id: 8, name: t("common.august") || "August" },
  { id: 9, name: t("common.september") || "September" },
  { id: 10, name: t("common.october") || "October" },
  { id: 11, name: t("common.november") || "November" },
  { id: 12, name: t("common.december") || "December" },
]);

const currentSeason = computed(() => {
  const m = selectedMonth.value;
  if ([11, 12, 1, 2].includes(m)) {
    return {
      id: "cool",
      name: t("tripPlanner.seasonCool"),
      icon: "fas fa-snowflake",
      color: "#3b82f6",
      bg: "#eff6ff",
      desc: t("tripPlanner.seasonCoolDesc"),
    };
  } else if ([3, 4, 5].includes(m)) {
    return {
      id: "hot",
      name: t("tripPlanner.seasonHot"),
      icon: "fas fa-sun",
      color: "#ef4444",
      bg: "#fef2f2",
      desc: t("tripPlanner.seasonHotDesc"),
    };
  } else {
    return {
      id: "rainy",
      name: t("tripPlanner.seasonRainy"),
      icon: "fas fa-cloud-showers-heavy",
      color: "#10b981",
      bg: "#ecfdf5",
      desc: t("tripPlanner.seasonRainyDesc"),
    };
  }
});

const getDisplaySeason = (slot) => {
  if (!slot || !slot.place) return null;

  // 1. Get the months string and trim it
  let bestMonthsStr = (slot.place.best_months || "").toLowerCase().trim();

  // 2. If no months specified or invalid data, don't show any badge
  if (
    !bestMonthsStr ||
    bestMonthsStr === "undefined" ||
    bestMonthsStr === "null" ||
    bestMonthsStr.includes("undefined") ||
    bestMonthsStr.includes("none")
  ) {
    return null;
  }

  // 3. Check if Year Round / All Season (First priority)
  const allSeasonKeywords = [
    "1-12",
    "year round",
    "year-round",
    "all year",
    "all season",
    "all seasons",
    "ທຸກລະດູ",
    "ທັງປີ",
    "ຕະຫຼອດປີ",
    "ทุกฤดู",
    "ทังปี",
    "ตลอดปี",
    "ทังละดู",
    "ทັງລະດู",
    "quanh năm",
    "suốt năm",
  ];
  if (allSeasonKeywords.some((k) => bestMonthsStr.includes(k))) {
    return {
      name:
        t("tripPlanner.allSeason") &&
        t("tripPlanner.allSeason") !== "tripPlanner.allSeason"
          ? t("tripPlanner.allSeason")
          : "All Season",
      icon: "fas fa-infinity",
      color: "#6366f1",
      bg: "#eef2ff",
    };
  }

  // 4. Identify the inherent season using stricter matching
  // Cool Season (Nov-Feb)
  const coolKeywords = [
    "jan",
    "feb",
    "nov",
    "dec",
    "ມັງກອນ",
    "ກຸມພາ",
    "ພະຈິກ",
    "ທັນວາ",
    "ม.ค",
    "ก.พ",
    "พ.ย",
    "ธ.ค",
  ];
  const coolNums = ["1", "2", "11", "12"];

  // Check if any month name matches OR if a lone number matches
  const hasCool =
    coolKeywords.some((k) => bestMonthsStr.includes(k)) ||
    coolNums.some((n) => new RegExp(`\\b${n}\\b`).test(bestMonthsStr));

  if (hasCool) {
    return {
      name: t("tripPlanner.seasonCool"),
      icon: "fas fa-snowflake",
      color: "#3b82f6",
      bg: "#eff6ff",
    };
  }

  // Hot Season (Mar-May)
  const hotKeywords = [
    "mar",
    "apr",
    "may",
    "ມັດສະ",
    "ເມສາ",
    "ພຶດສະພາ",
    "มี.ค",
    "เม.ย",
    "พ.ค",
  ];
  const hotNums = ["3", "4", "5"];
  const hasHot =
    hotKeywords.some((k) => bestMonthsStr.includes(k)) ||
    hotNums.some((n) => new RegExp(`\\b${n}\\b`).test(bestMonthsStr));

  if (hasHot) {
    return {
      name: t("tripPlanner.seasonHot"),
      icon: "fas fa-sun",
      color: "#ef4444",
      bg: "#fef2f2",
    };
  }

  // Rainy Season (Jun-Oct)
  const rainyKeywords = [
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "มิ.ย",
    "ก.ค",
    "ส.ค",
    "ก.ย",
    "ต.ค",
  ];
  const rainyNums = ["6", "7", "8", "9", "10"];
  const hasRainy =
    rainyKeywords.some((k) => bestMonthsStr.includes(k)) ||
    rainyNums.some((n) => new RegExp(`\\b${n}\\b`).test(bestMonthsStr));

  if (hasRainy) {
    return {
      name: t("tripPlanner.seasonRainy"),
      icon: "fas fa-cloud-showers-heavy",
      color: "#10b981",
      bg: "#ecfdf5",
    };
  }

  // 5. Fallback to specific boost only if months was somehow missed
  if (slot.season_boost) {
    return currentSeason.value;
  }

  return null;
};

const selectedMonthName = computed(() => {
  return (
    months.value.find((m) => m.id === selectedMonth.value)?.name ||
    t("tripPlanner.selectMonth")
  );
});

const isSwapping = ref(false);
const swappingSlot = ref("");

const swapPlace = async (dayLabel, index, slot) => {
  if (isSwapping.value) return;
  isSwapping.value = true;
  swappingSlot.value = `${dayLabel}-${index}`;

  try {
    const usedIds = [];
    Object.values(itinerary.value).forEach((plan) => {
      plan.forEach((item) => usedIds.push(item.place.id));
    });

    const payload = {
      current_place_id: slot.place.id,
      time_slot: slot.time_slot,
      month: selectedMonth.value,
      preferences:
        selectedPreferences.value.length > 0 ? selectedPreferences.value : null,
      budget: selectedBudget.value !== "any" ? selectedBudget.value : null,
      used_place_ids: usedIds,
    };

    const response = await api.post("/api/itinerary/swap", payload);
    itinerary.value[dayLabel][index] = response.data;
  } catch (error) {
    console.error("Error swapping place:", error);
    alert(
      t("tripPlanner.swapError") || "ไม่สามารถหาสถานที่อื่นมาแทนได้ในขณะนี้",
    );
  } finally {
    isSwapping.value = false;
    swappingSlot.value = "";
  }
};

const deleteDay = (dayLabel) => {
  if (!confirm(`${t("tripPlanner.deleteDay")} ${dayLabel}?`)) return;

  delete itinerary.value[dayLabel];

  const newItinerary = {};
  let d = 1;
  for (const key in itinerary.value) {
    newItinerary[`Day ${d}`] = itinerary.value[key];
    d++;
  }

  itinerary.value = newItinerary;
  days.value = Object.keys(newItinerary).length;

  if (days.value === 0) {
    itinerary.value = null;
    days.value = 1;
  }
};

const removePlace = (dayLabel, index) => {
  itinerary.value[dayLabel].splice(index, 1);
};

const isAddingPlace = ref(false);
const addingSlot = ref("");

// Compute an auto-incremented time so places in the same slot never share the same time.
// Each additional place in the same slot gets +90 minutes from the base time.
const getNextTimeForSlot = (dayLabel, timeSlot) => {
  const baseMinutes = { Morning: 9 * 60, Afternoon: 14 * 60, Evening: 19 * 60 };
  const base = baseMinutes[timeSlot] ?? 9 * 60;
  const count = (itinerary.value[dayLabel] || []).filter(
    (p) => p.time_slot === timeSlot,
  ).length;
  const totalMinutes = base + count * 90;
  const h = Math.floor(totalMinutes / 60) % 24;
  const m = totalMinutes % 60;
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
};

const addPlace = async (dayLabel, timeSlot) => {
  if (isAddingPlace.value) return;
  isAddingPlace.value = true;
  addingSlot.value = `${dayLabel}-${timeSlot}`;

  try {
    const usedIds = [];
    Object.values(itinerary.value).forEach((plan) => {
      plan.forEach((item) => usedIds.push(item.place.id));
    });

    const payload = {
      current_place_id: null,
      time_slot: timeSlot,
      month: selectedMonth.value,
      preferences:
        selectedPreferences.value.length > 0 ? selectedPreferences.value : null,
      budget: selectedBudget.value !== "any" ? selectedBudget.value : null,
      used_place_ids: usedIds,
    };

    const response = await api.post("/api/itinerary/swap", payload);
    const newPlace = response.data;

    // Override the time returned by the server with a unique incremented time
    newPlace.time = getNextTimeForSlot(dayLabel, timeSlot);

    if (timeSlot === "Morning") {
      const lastMorningIdx = itinerary.value[dayLabel].findLastIndex(
        (p) => p.time_slot === "Morning",
      );
      itinerary.value[dayLabel].splice(
        lastMorningIdx !== -1 ? lastMorningIdx + 1 : 0,
        0,
        newPlace,
      );
    } else if (timeSlot === "Afternoon") {
      const lastAfternoonIdx = itinerary.value[dayLabel].findLastIndex(
        (p) => p.time_slot === "Afternoon",
      );
      if (lastAfternoonIdx !== -1) {
        itinerary.value[dayLabel].splice(lastAfternoonIdx + 1, 0, newPlace);
      } else {
        const firstEveningIdx = itinerary.value[dayLabel].findIndex(
          (p) => p.time_slot === "Evening",
        );
        itinerary.value[dayLabel].splice(
          firstEveningIdx !== -1
            ? firstEveningIdx
            : itinerary.value[dayLabel].length,
          0,
          newPlace,
        );
      }
    } else {
      itinerary.value[dayLabel].push(newPlace);
    }
  } catch (error) {
    console.error("Error adding place:", error);
    alert(
      t("tripPlanner.swapError") || "ไม่สามารถหาสถานที่อื่นมาแทนได้ในขณะนี้",
    );
  } finally {
    isAddingPlace.value = false;
    addingSlot.value = "";
  }
};

const availablePreferences = computed(() => [
  {
    id: "nature",
    label: t("categories.nature") || "Nature",
    icon: "fas fa-tree",
  },
  {
    id: "culture",
    label: t("categories.culture") || "Culture & Temple",
    icon: "fas fa-vihara",
  },
  {
    id: "local_food",
    label: t("categories.localFood") || "Local Food",
    icon: "fas fa-utensils",
  },
  {
    id: "cafe",
    label: t("categories.cafe") || "Cafe & Sweets",
    icon: "fas fa-coffee",
  },
  {
    id: "landmark",
    label: t("categories.landmark") || "Landmarks",
    icon: "fas fa-camera",
  },
]);
const selectedPreferences = ref([]);

const togglePreference = (id) => {
  const index = selectedPreferences.value.indexOf(id);
  if (index > -1) {
    selectedPreferences.value.splice(index, 1);
  } else {
    selectedPreferences.value.push(id);
  }
};

const showInterestDropdown = ref(false);
const showDaysDropdown = ref(false);

const closeDropdowns = () => {
  showInterestDropdown.value = false;
  showDaysDropdown.value = false;
  showMonthDropdown.value = false;
  showBudgetDropdown.value = false;
};

onMounted(() => {
  document.addEventListener("click", closeDropdowns);
});

onUnmounted(() => {
  document.removeEventListener("click", closeDropdowns);
});

const selectedPreferencesText = computed(() => {
  if (selectedPreferences.value.length === 0)
    return t("tripPlanner.anyInterests") || "Any Interests";
  if (selectedPreferences.value.length === 1) {
    return availablePreferences.value.find(
      (p) => p.id === selectedPreferences.value[0],
    ).label;
  }
  return `${selectedPreferences.value.length} ${t("tripPlanner.selected") || "Selected"}`;
});

const generateItinerary = async () => {
  if (loading.value) return;
  loading.value = true;
  try {
    const payload = {
      days: days.value || 2,
      preferences:
        selectedPreferences.value && selectedPreferences.value.length > 0
          ? selectedPreferences.value
          : null,
      month: selectedMonth.value || new Date().getMonth() + 1,
      budget: selectedBudget.value !== "any" ? selectedBudget.value : null,
    };

    if (user.value && user.value.id) {
      payload.user_id = user.value.id;
    }

    console.log("Generating with payload:", payload);
    const response = await api.post("/api/itinerary/generate", payload);

    if (response.data) {
      itinerary.value = response.data;
      // Scroll to result after a short delay to allow DOM update
      setTimeout(() => {
        const el = document.querySelector(".itinerary-result");
        if (el) el.scrollIntoView({ behavior: "smooth" });
      }, 100);
    } else {
      throw new Error("No data received");
    }
  } catch (error) {
    console.error("Error generating itinerary:", error);
    alert(
      t("tripPlanner.generateError") ||
        "ไม่สามารถสร้างแผนการเดินทางได้ในขณะนี้ กรุณาลองใหม่อีกครั้ง",
    );
  } finally {
    loading.value = false;
  }
};

const resetPlanner = () => {
  itinerary.value = null;
  days.value = 2;
  saveSuccess.value = false;
  sessionStorage.removeItem("tripPlannerState");
  if (route.query.id) {
    router.push("/trip-planner");
  }
};

const saveItinerary = async () => {
  if (!user.value) {
    router.push("/login");
    return;
  }

  saving.value = true;
  try {
    const items = [];
    // Convert itinerary object into flat array for saving
    Object.entries(itinerary.value).forEach(([dayLabel, plan]) => {
      const dayNum = parseInt(dayLabel.replace("Day ", ""));
      plan.forEach((slot) => {
        items.push({
          day: dayNum,
          time_slot: slot.time_slot,
          time: slot.time,
          place_id: slot.place.id,
        });
      });
    });

    const payload = {
      user_id: user.value.id,
      title: `My ${days.value}-Day Trip to Savannakhet`,
      days: days.value,
      items: items,
    };

    await api.post("/api/itinerary/save", payload);
    saveSuccess.value = true;
    setTimeout(() => {
      saveSuccess.value = false;
    }, 5000);
  } catch (error) {
    console.error("Error saving itinerary:", error);
    alert("Failed to save itinerary. Please try again.");
  } finally {
    saving.value = false;
  }
};

const goToDetail = (id) => {
  router.push(`/places/${id}`);
};

const loadSavedItinerary = async (id) => {
  loading.value = true;
  try {
    const response = await api.get(`/api/itinerary/user/${user.value.id}`);
    const saved = response.data.find((it) => it.id === parseInt(id));
    if (saved) {
      days.value = saved.days;
      const formatted = {};
      for (let d = 1; d <= saved.days; d++) {
        formatted[`Day ${d}`] = [];
      }

      saved.items.forEach((item) => {
        if (item.place) {
          formatted[`Day ${item.day}`].push({
            time_slot: item.time_slot,
            time: item.time,
            place: item.place,
            category_name: item.place.category_name || "Place",
            is_preferred: false,
          });
        }
      });
      itinerary.value = formatted;
    }
  } catch (error) {
    console.error("Error loading saved itinerary:", error);
    alert("Could not load the saved trip.");
  } finally {
    loading.value = false;
  }
};

const saveStateToStorage = () => {
  if (!itinerary.value) return;
  const state = {
    days: days.value,
    itinerary: itinerary.value,
    selectedMonth: selectedMonth.value,
    selectedPreferences: selectedPreferences.value,
  };
  sessionStorage.setItem("tripPlannerState", JSON.stringify(state));
};

const loadStateFromStorage = () => {
  const stored = sessionStorage.getItem("tripPlannerState");
  if (stored) {
    try {
      const state = JSON.parse(stored);
      if (state.itinerary) {
        days.value = state.days || 2;
        itinerary.value = state.itinerary;
        selectedMonth.value = state.selectedMonth || new Date().getMonth() + 1;
        selectedPreferences.value = state.selectedPreferences || [];
        return true;
      }
    } catch (e) {
      console.error("Error loading stored planner state", e);
    }
  }
  return false;
};

watch(
  [days, itinerary, selectedMonth, selectedPreferences],
  () => {
    saveStateToStorage();
  },
  { deep: true },
);

onMounted(() => {
  if (route.query.id && user.value) {
    loadSavedItinerary(route.query.id);
  } else {
    loadStateFromStorage();
  }
});

const getCoverImage = (imgData) => {
  const noImageUrl =
    "data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22400%22%20height%3D%22300%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20fill%3D%22%23e2e8f0%22%2F%3E%3Ctext%20x%3D%2250%25%22%20y%3D%2250%25%22%20fill%3D%22%2364748b%22%20font-family%3D%22sans-serif%22%20font-size%3D%2220%22%20text-anchor%3D%22middle%22%20dy%3D%22.3em%22%3ENo%20Image%3C%2Ftext%3E%3C%2Fsvg%3E";

  if (
    !imgData ||
    imgData === "[]" ||
    imgData === "null" ||
    imgData === "undefined"
  )
    return noImageUrl;

  let urls = [];
  if (typeof imgData === "string" && imgData.trim().startsWith("[")) {
    try {
      const parsed = JSON.parse(imgData);
      if (Array.isArray(parsed) && parsed.length > 0) urls = parsed;
      else return noImageUrl;
    } catch (e) {
      urls = [imgData.replace(/^\["?|"?\]$/g, "").replace(/\\"/g, "")];
    }
  } else if (Array.isArray(imgData)) {
    urls = imgData;
  } else if (typeof imgData === "string") {
    urls = [imgData];
  } else {
    return noImageUrl;
  }

  if (!Array.isArray(urls) || urls.length === 0) return noImageUrl;
  const url = urls[0];

  if (!url || typeof url !== "string" || url === "null" || url === "undefined")
    return noImageUrl;
  if (
    url.startsWith("http://") ||
    url.startsWith("https://") ||
    url.startsWith("data:")
  )
    return url;

  const backendUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
  return `${backendUrl}${url.startsWith("/") ? "" : "/"}${url}`;
};

const handleImgError = (e) => {
  e.target.src =
    "data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22400%22%20height%3D%22300%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20fill%3D%22%23e2e8f0%22%2F%3E%3Ctext%20x%3D%2250%25%22%20y%3D%2250%25%22%20fill%3D%22%2364748b%22%20font-family%3D%22sans-serif%22%20font-size%3D%2220%22%20text-anchor%3D%22middle%22%20dy%3D%22.3em%22%3ENo%20Image%3C%2Ftext%3E%3C%2Fsvg%3E";
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap");

.trip-planner-page {
  background-color: #fcfcfd;
  min-height: 100vh;
  font-family: "Plus Jakarta Sans", sans-serif;
  color: #0f172a;
  position: relative;
}

/* Hero Section */
.planner-hero {
  position: relative;
  height: 550px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.hero-bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scale(1.05);
  filter: brightness(0.65) saturate(1.2);
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to bottom,
    rgba(15, 23, 42, 0.4),
    rgba(15, 23, 42, 0.8)
  );
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 900px;
  padding: 0 20px;
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  color: white;
  padding: 10px 24px;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 700;
  margin-bottom: 30px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

.display-title {
  font-family: "Playfair Display", serif;
  font-size: 4rem;
  font-weight: 900;
  margin-bottom: 20px;
  line-height: 1.1;
  text-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.subtitle {
  font-size: 1.35rem;
  color: rgba(255, 255, 255, 0.9);
  max-width: 700px;
  margin: 0 auto;
  font-weight: 500;
  line-height: 1.6;
}

.planner-container {
  max-width: 1000px;
  margin: -60px auto 60px;
  padding: 0 20px;
  position: relative;
  z-index: 10;
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.planner-container.has-itinerary {
  margin-top: 50px;
}

/* Concierge Bar Style */
.search-bar-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 50px;
}

.search-bar {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 30px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
  border: 1px solid #e2e8f0;
  padding: 12px;
  width: 100%;
  max-width: 900px;
  position: relative;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.search-bar:hover {
  box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.2);
  transform: translateY(-5px);
}

.search-section {
  flex: 1;
  padding: 12px 20px;
  cursor: pointer;
  border-radius: 20px;
  transition: 0.2s;
  position: relative;
  display: flex;
  align-items: center;
  gap: 15px;
}

.search-section:hover {
  background: #f8fafc;
}

.section-icon {
  width: 40px;
  height: 40px;
  background: #f1f5f9;
  color: #64748b;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  transition: 0.3s;
}

.search-section:hover .section-icon {
  background: #3b82f6;
  color: white;
  transform: scale(1.1);
}

.section-label {
  font-size: 0.7rem;
  font-weight: 800;
  color: #94a3b8;
  margin-bottom: 2px;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.section-value {
  font-size: 0.95rem;
  color: #64748b;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.section-value.has-value {
  color: #0f172a;
}

.divider {
  width: 1px;
  height: 50px;
  background: #f1f5f9;
  margin: 0 5px;
}

.search-action {
  padding-left: 15px;
}

.btn-generate-bar {
  background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
  color: white;
  border: none;
  padding: 16px 40px;
  border-radius: 20px;
  font-size: 1.05rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 10px 20px rgba(37, 99, 235, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 160px;
}

.btn-generate-bar:hover {
  background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
  transform: scale(1.05);
  box-shadow: 0 15px 30px rgba(37, 99, 235, 0.35);
}

.btn-generate-bar:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.btn-back-floating {
  position: fixed;
  top: 30px;
  left: 30px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 12px 24px;
  border-radius: 50px;
  font-weight: 700;
  color: #0f172a;
  cursor: pointer;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  align-items: center;
  gap: 10px;
  z-index: 1000;
}

.btn-back-floating:hover {
  background: white;
  transform: translateX(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
}

/* Dropdowns */
.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 15px;
  background: white;
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
  border: 1px solid #f1f5f9;
  width: 350px;
  z-index: 100;
  padding: 25px;
  cursor: default;
  animation: slideDown 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.days-dropdown,
.budget-dropdown {
  width: 280px;
  left: auto;
  right: 0;
}

.month-dropdown {
  width: 400px;
}

.month-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.month-item {
  padding: 12px;
  font-size: 0.9rem;
  text-align: center;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 700;
  color: #64748b;
  background: #f8fafc;
  transition: 0.2s;
}

.month-item:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.month-item.active {
  background: #3b82f6;
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.dropdown-header {
  font-size: 0.85rem;
  font-weight: 800;
  color: #94a3b8;
  margin-bottom: 20px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.dropdown-list {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.pref-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  font-weight: 600;
  color: #475569;
  gap: 12px;
}

.pref-item i:not(.check-icon) {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  border-radius: 10px;
  font-size: 0.9rem;
  color: #64748b;
  transition: 0.2s;
}

.pref-item:hover {
  background: #f8fafc;
  color: #0f172a;
}

.pref-item:hover i:not(.check-icon) {
  background: #e2e8f0;
  color: #0f172a;
}

.pref-item.active {
  background: #eff6ff;
  color: #3b82f6;
}

.pref-item.active i:not(.check-icon) {
  background: #3b82f6;
  color: white;
}

.check-icon {
  margin-left: auto;
  font-size: 0.8rem;
  color: #3b82f6;
}

.result-title-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.result-eyebrow {
  font-size: 0.85rem;
  font-weight: 800;
  color: #3b82f6;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.has-itinerary .result-eyebrow {
  color: #3b82f6;
}

.result-header h2 {
  font-family: "Playfair Display", serif;
  font-size: 2.8rem;
  font-weight: 900;
  margin: 0;
  color: #0f172a;
}

.has-itinerary .result-header h2 {
  color: #0f172a;
  text-shadow: none;
}

.action-buttons {
  display: flex;
  gap: 15px;
}

.btn-save {
  background: #10b981;
  color: white;
  border: none;
  padding: 14px 28px;
  border-radius: 50px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 10px 20px rgba(16, 185, 129, 0.2);
}

.btn-save:hover {
  background: #059669;
  transform: translateY(-3px);
  box-shadow: 0 15px 30px rgba(16, 185, 129, 0.3);
}

.btn-outline {
  background: white;
  border: 1px solid #e2e8f0;
  padding: 14px 28px;
  border-radius: 50px;
  font-weight: 800;
  color: #475569;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-outline:hover {
  border-color: #0f172a;
  color: #0f172a;
  background: #f8fafc;
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

/* Timeline Container */
.timeline-container {
  background: white;
  border-radius: 40px;
  padding: 60px;
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.04);
  border: 1px solid #f1f5f9;
}

.day-section {
  margin-bottom: 80px;
  position: relative;
}

.itinerary-result {
  margin-top: 20px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 40px;
  padding: 0 10px;
}

.day-header {
  margin-bottom: 40px;
  position: relative;
  z-index: 5;
}

.day-header h3 {
  font-family: "Playfair Display", serif;
  font-size: 2.2rem;
  font-weight: 900;
  color: #0f172a;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 20px;
}

.btn-delete-day {
  background: #fff1f2;
  color: #e11d48;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: 0.2s;
}

.btn-delete-day:hover {
  background: #e11d48;
  color: white;
  transform: rotate(10deg);
}

.day-header h3::after {
  content: "";
  flex: 1;
  height: 2px;
  background: linear-gradient(to right, #f1f5f9, transparent);
}

.timeline {
  padding-left: 10px;
}

.timeline-item {
  display: flex;
  gap: 30px;
  position: relative;
  margin-bottom: 40px;
}

.timeline-item:last-child {
  margin-bottom: 0;
}

.time-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 70px;
  flex-shrink: 0;
}

.time {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-weight: 800;
  font-size: 0.9rem;
  color: #0f172a;
  background: white;
  border: 1px solid #e2e8f0;
  padding: 8px 14px;
  border-radius: 12px;
  margin-bottom: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
}

.marker-dot {
  width: 20px;
  height: 20px;
  background: white;
  border: 5px solid #3b82f6;
  border-radius: 50%;
  z-index: 2;
  box-shadow: 0 0 0 5px rgba(59, 130, 246, 0.1);
}

.marker-line {
  position: absolute;
  top: 60px;
  bottom: -60px;
  left: 35px;
  width: 3px;
  background: linear-gradient(to bottom, #3b82f6, #f1f5f9);
  z-index: 1;
}

.timeline-content {
  flex: 1;
}

.slot-header-flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.slot-label {
  font-size: 0.75rem;
  font-weight: 800;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.place-card {
  display: flex;
  background: white;
  border: 1px solid #f1f5f9;
  border-radius: 24px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.02);
}

.place-card:hover {
  transform: translateX(10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.06);
  border-color: #3b82f6;
}

.place-img {
  width: 220px;
  height: 180px;
  flex-shrink: 0;
  position: relative;
}

.place-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.place-info {
  padding: 30px;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.place-info h4 {
  margin: 0 0 10px;
  font-family: "Playfair Display", serif;
  font-size: 1.6rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.2;
}

.rating-cat {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.85rem;
  color: #64748b;
  margin-bottom: 15px;
  font-weight: 600;
}

.match-badge {
  position: absolute;
  bottom: 15px;
  left: 15px;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(8px);
  color: white;
  padding: 6px 14px;
  border-radius: 50px;
  font-weight: 800;
  font-size: 0.7rem;
  letter-spacing: 0.5px;
  z-index: 2;
}

.season-badge {
  padding: 6px 12px;
  border-radius: 10px;
  font-size: 0.7rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 6px;
  text-transform: uppercase;
}

.desc {
  font-size: 0.9rem;
  color: #64748b;
  line-height: 1.6;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.btn-remove-place {
  position: absolute;
  top: 15px;
  right: 15px;
  width: 30px;
  height: 30px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #e11d48;
  cursor: pointer;
  z-index: 5;
  opacity: 0;
  transform: scale(0.8);
  transition: 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.place-card:hover .btn-remove-place {
  opacity: 1;
  transform: scale(1);
}

.btn-remove-place:hover {
  background: #e11d48;
  color: white;
}

.btn-swap {
  background: #f1f5f9;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  cursor: pointer;
  transition: 0.3s;
}

.btn-swap:hover {
  background: #3b82f6;
  color: white;
  transform: rotate(180deg);
}

/* Add Place Actions */
.add-place-footer {
  margin-top: 40px;
  padding: 30px;
  background: #f8fafc;
  border-radius: 24px;
  border: 1px dashed #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.add-chips-label {
  font-size: 0.8rem;
  font-weight: 800;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.add-chips-group {
  display: flex;
  gap: 12px;
}

.add-chip {
  background: white;
  border: 1px solid #e2e8f0;
  padding: 10px 20px;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 700;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.add-chip:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.add-chip:active {
  transform: scale(0.95);
}

@media (max-width: 768px) {
  .display-title {
    font-size: 2.5rem;
  }
  .search-bar {
    flex-direction: column;
    border-radius: 20px;
  }
  .divider {
    width: 100%;
    height: 1px;
  }
  .place-card {
    flex-direction: column;
  }
  .place-img {
    width: 100%;
    height: 200px;
  }
}
</style>
