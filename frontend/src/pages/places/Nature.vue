<template>
  <div class="nature-page">
    <Navbar />

    <div class="nature-header">
      <div class="header-container">
        <h1>{{ t("nature.title") || "Nature & Parks in Savannakhet" }}</h1>
        <p class="subtitle">
          {{
            t("nature.subtitle") ||
            "Discover serene landscapes, lush forests, and outdoor adventures."
          }}
        </p>

        <div class="quick-filters" v-if="natureCategories.length > 0">
          <button
            class="filter-pill"
            :class="{ active: selectedCategories.length === 0 }"
            @click="selectedCategories = []"
          >
            <i class="fas fa-th-large"></i> {{ t("landmarks.all") || "All" }}
          </button>
          <button
            v-for="cat in natureCategories.slice(0, 6)"
            :key="cat.id"
            class="filter-pill"
            @click="toggleCategory(cat.name.toLowerCase())"
            :class="{
              active: selectedCategories.includes(cat.name.toLowerCase()),
            }"
          >
            <i :class="getIconForNature(cat.name)"></i> {{ cat.name }}
          </button>
        </div>
      </div>
    </div>

    <div class="main-layout">
      <aside class="filter-sidebar">
        <div class="map-preview" @click="showMapModal = true">
          <img
            src="https://images.unsplash.com/photo-1524661135-423995f22d0b?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"
            alt="Map View"
          />
          <button class="btn-view-map">
            <i class="fas fa-map"></i>
            {{ t("common.viewOnMap") || "View on map" }}
          </button>
        </div>

        <!-- Search -->
        <div class="filter-group">
          <div class="search-input-wrap">
            <i class="fas fa-search"></i>
            <input
              v-model="searchQuery"
              type="text"
              :placeholder="
                t('searchPlaceholder') !== 'searchPlaceholder'
                  ? t('searchPlaceholder')
                  : 'Search...'
              "
            />
          </div>
        </div>

        <div class="filter-group">
          <h3>{{ t("landmarks.filterCategory") || "Category" }}</h3>
          <label
            class="filter-checkbox"
            :class="{ active: selectedCategories.length === 0 }"
            @click="selectedCategories = []"
            style="cursor: pointer; font-weight: 700"
          >
            <input
              type="checkbox"
              :checked="selectedCategories.length === 0"
              readonly
            />
            <span>{{ t("landmarks.all") || "All" }}</span>
          </label>
          <label
            v-for="cat in natureCategories"
            :key="'sidebar-' + cat.id"
            class="filter-checkbox"
          >
            <input
              type="checkbox"
              :value="cat.name.toLowerCase()"
              v-model="selectedCategories"
            />
            <span>{{ cat.name }}</span>
          </label>
        </div>
      </aside>

      <main class="nature-list-area">
        <div class="list-header">
          <h2>
            {{ filteredNature.length }}
            {{
              filteredNature.length !== 1
                ? t("landmarks.foundLabelPlural") || "nature spots"
                : t("landmarks.foundLabel") || "nature spot"
            }}
            {{ t("landmarks.found") || "found" }}
          </h2>
          <div class="sort-by">
            <span>{{ t("landmarks.sortBy") || "Sort by:" }}</span>
            <select v-model="sortBy">
              <option value="default">
                {{ t("landmarks.sortDefault") || "Recommended" }}
              </option>
              <option value="name">
                {{ t("landmarks.sortName") || "Name" }}
              </option>
              <option value="rating">
                {{ t("landmarks.sortRating") || "Rating" }}
              </option>
            </select>
          </div>
        </div>

        <div v-if="loading" class="loading-box">
          <div class="spinner"></div>
          <p>{{ t("landmarks.loading") || "Loading nature's beauty..." }}</p>
        </div>

        <div v-else-if="filteredNature.length === 0" class="empty-box">
          <i class="fas fa-leaf"></i>
          <p>
            {{
              t("landmarks.noResults") ||
              "No nature spots found matching your search."
            }}
          </p>
          <button
            @click="resetFilters()"
            class="btn-details"
            style="margin-top: 15px"
          >
            {{ t("landmarks.clearFilters") || "Clear Filters" }}
          </button>
        </div>

        <!-- Immersive Cards Grid -->
        <div v-else class="nature-grid">
          <div
            v-for="(place, index) in sortedNature"
            :key="place.id"
            class="nature-card"
            @click="goToDetail(place.id)"
          >
            <div class="card-img-wrapper">
              <img
                :src="getCoverImage(place)"
                :alt="place.name"
                @error="handleImgError"
              />
              <button
                class="btn-heart"
                :class="{ active: isFavorite(place.id) }"
                @click.stop="toggleHeart(place.id)"
              >
                <i class="fas fa-heart"></i>
              </button>
            </div>

            <div class="card-info">
              <span class="category-tag">{{
                getCategoryName(place.category_id)
              }}</span>
              <h3 class="place-name">{{ place.name }}</h3>

              <div class="rating-row">
                <span class="bubbles">
                  <i
                    v-for="s in 5"
                    :key="s"
                    :class="[
                      (place.rating_avg || 0) >= s ? 'fas' : 'far',
                      'fa-circle',
                    ]"
                  ></i>
                </span>
                <span class="review-count">{{
                  place.rating_avg || "0.0"
                }}</span>
              </div>

              <div class="description-snippet">
                <p>
                  {{
                    place.description ||
                    "Explore the untouched beauty of this natural wonder in Savannakhet."
                  }}
                </p>
              </div>

              <div class="card-footer">
                <span class="location-tag"
                  >✨ {{ t("landmarks.verified") || "Verified" }}</span
                >
                <span class="btn-details"
                  >{{ t("landmarks.openGuide") || "View Details" }} →</span
                >
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <SectionDivider icon="fas fa-leaf" />

    <MapOverlay
      :is-open="showMapModal"
      :places="places"
      :categories="categories"
      initial-filter="nature"
      title="Nature & Parks"
      @close="showMapModal = false"
    />

    <RecentlyViewed />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { placeRepository } from "@/repositories/placeRepository";
import { categoryRepository } from "@/repositories/categoryRepository";
import { favoriteRepository } from "@/repositories/favoriteRepository";
import { useAuth } from "@/composables/useAuth";
import { useI18n } from "@/composables/useI18n";
import Navbar from "@/components/Navbar.vue";
import MapOverlay from "@/components/MapOverlay.vue";
import SectionDivider from "@/components/SectionDivider.vue";
import RecentlyViewed from "@/components/RecentlyViewed.vue";
import axios from "axios";

const router = useRouter();
const { user } = useAuth();
const { t } = useI18n();
const places = ref([]);
const categories = ref([]);
const favoriteIds = ref([]);
const loading = ref(true);
const selectedCategories = ref([]);
const searchQuery = ref("");
const showMapModal = ref(false);
const sortBy = ref("default");

const fetchData = async () => {
  loading.value = true;
  try {
    const [resPlaces, resCats] = await Promise.all([
      placeRepository.getAll(),
      categoryRepository.getAll(),
    ]);
    places.value = resPlaces.data;
    categories.value = resCats.data;
    loading.value = false;

    if (user.value) {
      favoriteRepository
        .getUserFavorites(user.value.id)
        .then((favRes) => {
          favoriteIds.value = favRes.data.map((f) => f.place_id);
        })
        .catch((err) => console.error("Error fetching favorites:", err));
    }
  } catch (err) {
    console.error("Error fetching places:", err);
    loading.value = false;
  }
};

const natureCategories = computed(() => {
  return categories.value.filter((c) => {
    const pType = c.parent_type?.toLowerCase() || "";
    return ["nature", "park", "forest", "waterfall", "mountain"].includes(
      pType,
    );
  });
});

const filteredNature = computed(() => {
  let results = places.value.filter((p) => {
    const cat = categories.value.find((c) => c.id == p.category_id);
    const pType = cat?.parent_type?.toLowerCase() || "";
    return ["nature", "park", "forest", "waterfall", "mountain"].includes(
      pType,
    );
  });

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase();
    results = results.filter(
      (p) =>
        p.name?.toLowerCase().includes(q) ||
        p.description?.toLowerCase().includes(q),
    );
  }

  if (selectedCategories.value.length > 0) {
    results = results.filter((p) => {
      const cat = categories.value.find((c) => c.id === p.category_id);
      return cat && selectedCategories.value.includes(cat.name.toLowerCase());
    });
  }
  return results;
});

const sortedNature = computed(() => {
  const list = [...filteredNature.value];
  if (sortBy.value === "name")
    return list.sort((a, b) => a.name.localeCompare(b.name));
  if (sortBy.value === "rating")
    return list.sort((a, b) => (b.rating_avg || 0) - (a.rating_avg || 0));
  return list;
});

const toggleCategory = (name) => {
  name = name.toLowerCase();
  if (selectedCategories.value.includes(name)) {
    selectedCategories.value = selectedCategories.value.filter(
      (c) => c !== name,
    );
  } else {
    selectedCategories.value.push(name);
  }
};

const resetFilters = () => {
  selectedCategories.value = [];
  searchQuery.value = "";
  sortBy.value = "default";
};

const getIconForNature = (name) => {
  name = name.toLowerCase();
  if (name.includes("park") || name.includes("garden")) return "fas fa-tree";
  if (
    name.includes("waterfall") ||
    name.includes("river") ||
    name.includes("lake")
  )
    return "fas fa-water";
  if (name.includes("mountain") || name.includes("cave"))
    return "fas fa-mountain";
  if (name.includes("wildlife") || name.includes("animal")) return "fas fa-paw";
  return "fas fa-leaf";
};

// --- Image Carousel Logic ---
const currentImageIndices = ref({});

const getPlaceImagesArray = (place) => {
  const noImageUrl =
    "data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22400%22%20height%3D%22300%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20fill%3D%22%23e2e8f0%22%2F%3E%3Ctext%20x%3D%2250%25%22%20y%3D%2250%25%22%20fill%3D%22%2364748b%22%20font-family%3D%22sans-serif%22%20font-size%3D%2220%22%20text-anchor%3D%22middle%22%20dy%3D%22.3em%22%3ENo%20Image%3C%2Ftext%3E%3C%2Fsvg%3E";
  let urls = [];

  if (place.images && Array.isArray(place.images) && place.images.length > 0) {
    urls = place.images.map((img) => img.image_url || img.url || img);
  } else if (place.image_url) {
    if (
      typeof place.image_url === "string" &&
      place.image_url.trim().startsWith("[")
    ) {
      try {
        urls = JSON.parse(place.image_url);
      } catch (e) {
        urls = [
          place.image_url.replace(/^\["?|"?\]$/g, "").replace(/\\"/g, ""),
        ];
      }
    } else {
      urls = [place.image_url];
    }
  }
  if (urls.length === 0) return [noImageUrl];
  return urls.map((url) => {
    if (!url) return noImageUrl;
    if (
      url.startsWith("https://") ||
      url.startsWith("http://") ||
      url.startsWith("data:")
    )
      return url;
    return `http://127.0.0.1:8000${url.startsWith("/") ? "" : "/"}${url}`;
  });
};

const getCoverImage = (place) => {
  const images = getPlaceImagesArray(place);
  const index = currentImageIndices.value[place.id] || 0;
  return images[index] || images[0];
};

const handleImgError = (e) => {
  e.target.src =
    "https://images.unsplash.com/photo-1469474968028-56623f02e42e?q=80&w=600";
};

const getCategoryName = (id) =>
  categories.value.find((c) => c.id === id)?.name || "Nature";

const isFavorite = (id) => favoriteIds.value.includes(id);
const toggleHeart = async (placeId) => {
  if (!user.value) return router.push("/login");
  try {
    const res = await favoriteRepository.toggleFavorite(user.value.id, placeId);
    if (res.data.status === "added") {
      favoriteIds.value.push(placeId);
      await axios.post("http://127.0.0.1:8000/api/interactions/", {
        place_id: placeId,
        rating: 5,
        interaction_type: "like",
      });
    } else {
      favoriteIds.value = favoriteIds.value.filter((id) => id !== placeId);
    }
  } catch (err) {
    console.error(err);
  }
};

const goToDetail = (id) => router.push(`/places/${id}`);

onMounted(fetchData);
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:wght@700;800;900&display=swap");

.nature-page {
  background-color: #faf9f6;
  min-height: 100vh;
  font-family: "Inter", sans-serif;
  color: #1e293b;
}

/* Header */
.nature-header {
  background: white;
  padding: 30px 20px;
  border-bottom: 1px solid #e2e8f0;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
}
.header-container h1 {
  font-size: 2.2rem;
  font-weight: 800;
  margin: 0 0 5px;
  color: #000;
}
.subtitle {
  color: #475569;
  font-size: 1rem;
  margin-bottom: 20px;
}

/* Quick Filters */
.quick-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.filter-pill {
  background: white;
  border: 1px solid #cbd5e1;
  padding: 9px 20px;
  border-radius: 50px;
  font-weight: 600;
  font-size: 0.88rem;
  color: #475569;
  cursor: pointer;
  transition: 0.2s;
  display: flex;
  align-items: center;
  gap: 7px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}
.filter-pill i {
  color: #64748b;
  font-size: 1rem;
}
.filter-pill:hover {
  border-color: #000;
  background: #f8fafc;
  color: #000;
}
.filter-pill.active {
  background: #000;
  color: #fff;
  border-color: #000;
}
.filter-pill.active i {
  color: #fff;
}

/* Layout */
.main-layout {
  max-width: 1200px;
  margin: 30px auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 30px;
}

/* Sidebar */
.map-preview {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  height: 130px;
  border: 1px solid #cbd5e1;
  cursor: pointer;
  margin-bottom: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
.map-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.btn-view-map {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  border: 1px solid #000;
  color: #000;
  padding: 10px 18px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  pointer-events: none;
}

/* Search */
.search-input-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  padding: 10px 14px;
  margin-bottom: 20px;
  background: #f8fafc;
  transition: border-color 0.2s;
}
.search-input-wrap:focus-within {
  border-color: #000;
  background: white;
}
.search-input-wrap i {
  color: #94a3b8;
  font-size: 0.9rem;
}
.search-input-wrap input {
  border: none;
  background: transparent;
  outline: none;
  font-size: 0.9rem;
  color: #1e293b;
  width: 100%;
  font-family: "Inter", sans-serif;
}

.filter-group h3 {
  font-size: 1rem;
  font-weight: 800;
  margin: 0 0 14px;
  color: #000;
}
.filter-checkbox {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 11px;
  cursor: pointer;
  font-size: 0.9rem;
  color: #475569;
  transition: color 0.15s;
}
.filter-checkbox:hover {
  color: #000;
}
.filter-checkbox input {
  width: 16px;
  height: 16px;
  cursor: pointer;
  accent-color: #000;
}
.filter-divider {
  height: 1px;
  background: #cbd5e1;
  margin: 22px 0;
}

/* Main Content List */
.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 22px;
}
.list-header h2 {
  font-size: 1.45rem;
  font-weight: 800;
  margin: 0;
  color: #000;
  display: flex;
  align-items: center;
  gap: 10px;
}
.sort-by {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.88rem;
  font-weight: 600;
  color: #475569;
}
.sort-by select {
  padding: 8px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-weight: 600;
  outline: none;
  cursor: pointer;
  background: white;
  color: #000;
  transition: border-color 0.2s;
}
.sort-by select:focus {
  border-color: #000;
}

/* 🍃 Immersive Card Style (Matches Hotels) */
.nature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
}

.nature-card {
  position: relative;
  background: #0f172a;
  border-radius: 6px;
  overflow: hidden;
  height: 480px;
  transition: all 0.45s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.nature-card:hover {
  transform: translateY(-6px) scale(1.01);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.card-img-wrapper {
  position: absolute;
  inset: 0;
  height: 100%;
  overflow: hidden;
  z-index: 0;
}

.card-img-wrapper::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0) 0%,
    rgba(0, 0, 0, 0.15) 35%,
    rgba(0, 0, 0, 0.75) 75%,
    rgba(0, 0, 0, 0.95) 100%
  );
  z-index: 1;
}

.card-img-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.45s ease;
}
.nature-card:hover .card-img-wrapper img {
  transform: scale(1.06);
}

.btn-heart {
  position: absolute;
  top: 14px;
  right: 14px;
  background: rgba(255, 255, 255, 0.92);
  border: none;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #94a3b8;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: 0.2s;
  z-index: 50;
}
.btn-heart.active {
  color: #ef4444;
}
.btn-heart:hover {
  transform: scale(1.1);
  background: white;
}

/* Info */
.card-info {
  position: relative;
  z-index: 2;
  padding: 24px 20px;
  margin-top: auto;
  color: white;
  display: flex;
  flex-direction: column;
}

.category-tag {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.63rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 6px;
}

.place-name {
  font-size: 1.6rem;
  font-weight: 800;
  font-family: "Playfair Display", serif;
  color: white;
  line-height: 1.15;
  margin: 0 0 8px;
}
.nature-card:hover .place-name {
  color: #93c5fd;
}

.rating-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}
.bubbles i {
  color: #00aa6c;
  font-size: 0.8rem;
  margin-right: 2px;
}
.review-count {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 600;
}

.description-snippet {
  font-size: 0.82rem;
  color: rgba(255, 255, 255, 0.65);
  line-height: 1.55;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 12px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}
.location-tag {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.68rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.btn-details {
  color: white;
  font-weight: 800;
  font-size: 0.75rem;
  letter-spacing: 0.5px;
  transition: 0.2s;
}
.nature-card:hover .btn-details {
  color: #00aa6c;
}

/* States */
.loading-box,
.empty-box {
  text-align: center;
  padding: 60px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}
.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #000;
  border-radius: 50%;
  width: 40px;
  height: 40px;
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
.empty-box i {
  font-size: 2.5rem;
  color: #cbd5e1;
  margin-bottom: 15px;
}
.empty-box p {
  color: #64748b;
  font-size: 1rem;
}

@media (max-width: 1024px) {
  .main-layout {
    grid-template-columns: 1fr;
  }
  .filter-sidebar {
    display: none;
  }
}
</style>
