<template>
  <div class="edit-page-container">
    <div class="header-section">
      <div class="header-content">
        <button class="btn-back" @click="$router.push('/admin/places')">
          <i class="fas fa-arrow-left"></i> Back
        </button>
        <div class="title-group">
          <h1>Add New Place</h1>
          <p class="subtitle">
            Enter details, coordinates, and upload images for the new location.
          </p>
        </div>
      </div>
    </div>

    <div class="main-layout">
      <form @submit.prevent="savePlace" class="form-grid">
        <div class="left-column">
          <div class="card info-card">
            <div class="card-header">
              <i class="fas fa-info-circle"></i> <span>General Info</span>
            </div>
            <div class="card-body">
              <div class="input-row">
                <div class="input-group">
                  <label>Place Name <span class="text-danger">*</span></label>
                  <input
                    v-model="form.name"
                    placeholder="Enter place name..."
                    required
                  />
                </div>
                <div class="input-group">
                  <label>Category <span class="text-danger">*</span></label>
                  <select v-model="form.category_id" required>
                    <option value="" disabled>Select category</option>
                    <option
                      v-for="cat in categories"
                      :key="cat.id"
                      :value="cat.id"
                    >
                      [{{ cat.parent_type.toUpperCase() }}] {{ cat.name }}
                    </option>
                  </select>
                </div>
              </div>

              <div
                class="input-row"
                v-if="isHotelCategory"
                style="
                  margin-top: 15px;
                  background: #f0f9ff;
                  padding: 15px;
                  border-radius: 12px;
                  border: 1px solid #bae6fd;
                "
              >
                <div
                  style="
                    grid-column: 1 / -1;
                    margin-bottom: 10px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                  "
                >
                  <label class="switch" style="margin-bottom: 0">
                    <input
                      type="checkbox"
                      v-model="showBookingLinks"
                      :disabled="form.is_published"
                    />
                    <span class="slider round"></span>
                  </label>
                  <span style="font-weight: 700; color: #0369a1"
                    >Enable Partner Booking Links (Agoda / Booking.com)</span
                  >
                </div>
                <template v-if="showBookingLinks">
                  <div class="input-group" style="margin-bottom: 0">
                    <label style="color: #0369a1; font-weight: 700"
                      ><i class="fas fa-link"></i> Booking.com URL</label
                    >
                    <input
                      v-model="form.booking_url"
                      placeholder="https://www.booking.com/hotel/..."
                    />
                  </div>
                  <div class="input-group" style="margin-bottom: 0">
                    <label style="color: #0369a1; font-weight: 700"
                      ><i class="fas fa-link"></i> Agoda URL</label
                    >
                    <input
                      v-model="form.agoda_url"
                      placeholder="https://www.agoda.com/..."
                    />
                  </div>
                </template>
              </div>

              <div class="input-group" style="margin-top: 10px">
                <label style="color: #6366f1"
                  ><i class="fas fa-paste"></i> Paste Google Maps Plus
                  Code/Address</label
                >
                <div style="display: flex; gap: 10px">
                  <input
                    v-model="addressPaste"
                    @paste="handlePasteAddress"
                    placeholder="E.g., HP4W+G5V or Place Name..."
                    style="border: 2px solid #6366f1; background: #f5f3ff"
                  />
                  <button
                    type="button"
                    @click="searchFromAddress"
                    style="
                      background: #6366f1;
                      color: white;
                      border: none;
                      padding: 0 20px;
                      border-radius: 10px;
                      cursor: pointer;
                    "
                  >
                    Detect
                  </button>
                </div>
              </div>

              <div class="input-group">
                <label>Description <span class="text-danger">*</span></label>
                <textarea
                  v-model="form.description"
                  rows="4"
                  placeholder="Place details..."
                  required
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Premium Details Card -->
          <div class="card premium-details-card">
            <div class="card-header">
              <i class="fas fa-star"></i>
              <span>Premium Details (Stats & Tags)</span>
            </div>
            <div class="card-body">
              <div class="input-row">
                <div class="input-group">
                  <label class="label-with-action">
                    <span>Best Months (Range)</span>
                    <label class="year-round-toggle">
                      <input type="checkbox" v-model="form.is_year_round" />
                      <span>Year-round</span>
                    </label>
                  </label>
                  <div
                    style="display: flex; gap: 10px; align-items: center"
                    v-if="!form.is_year_round"
                  >
                    <select
                      v-model="form.best_months_start"
                      style="
                        flex: 1;
                        padding: 10px;
                        border-radius: 8px;
                        border: 1px solid #cbd5e1;
                      "
                    >
                      <option v-for="m in months" :key="m" :value="m">
                        {{ m }}
                      </option>
                    </select>
                    <span style="color: #94a3b8; font-weight: 600">to</span>
                    <select
                      v-model="form.best_months_end"
                      style="
                        flex: 1;
                        padding: 10px;
                        border-radius: 8px;
                        border: 1px solid #cbd5e1;
                      "
                    >
                      <option v-for="m in months" :key="m" :value="m">
                        {{ m }}
                      </option>
                    </select>
                  </div>
                  <div
                    v-else
                    style="
                      padding: 10px;
                      background: #f8fafc;
                      border: 1px dashed #cbd5e1;
                      border-radius: 8px;
                      color: #64748b;
                      font-weight: 600;
                      text-align: center;
                    "
                  >
                    <i
                      class="fas fa-calendar-check"
                      style="margin-right: 8px"
                    ></i>
                    Year-round
                  </div>
                </div>
                <div class="input-group">
                  <label>Ideal Stay (e.g. 1 - 2 Days)</label>
                  <input v-model="form.ideal_stay" placeholder="2 Days" />
                </div>
              </div>
              <div class="input-row">
                <div class="input-group">
                  <label class="label-with-action">
                    <span>Daily Budget (Range in ₭)</span>
                    <label class="year-round-toggle">
                      <input type="checkbox" v-model="form.is_free" />
                      <span>Free</span>
                    </label>
                  </label>
                  <div
                    v-if="!form.is_free"
                    style="display: flex; gap: 10px; align-items: center"
                  >
                    <input
                      type="number"
                      v-model="form.budget_min"
                      placeholder="Min (e.g. 100000)"
                    />
                    <span>-</span>
                    <input
                      type="number"
                      v-model="form.budget_max"
                      placeholder="Max (e.g. 500000)"
                    />
                  </div>
                  <div
                    v-else
                    style="
                      padding: 10px;
                      background: #ecfdf5;
                      border: 1px dashed #10b981;
                      border-radius: 8px;
                      color: #047857;
                      font-weight: 700;
                      text-align: center;
                    "
                  >
                    <i class="fas fa-gift" style="margin-right: 8px"></i> Free
                    Entry / No Cost
                  </div>
                </div>
                <div class="input-group">
                  <label>Location Display Name (e.g. Savannakhet)</label>
                  <input
                    v-model="form.location_name"
                    placeholder="Savannakhet"
                  />
                </div>
              </div>

              <div class="input-group">
                <label>Best For / Best Season (Tags)</label>
                <div class="preset-tags-container">
                  <span
                    v-for="tag in predefinedBestFor"
                    :key="tag"
                    class="preset-tag"
                    :class="{ active: form.best_for.includes(tag) }"
                    @click="toggleTag('best_for', tag)"
                  >
                    <i
                      :class="
                        form.best_for.includes(tag)
                          ? 'fas fa-check'
                          : 'fas fa-plus'
                      "
                    ></i>
                    {{ tag }}
                  </span>
                </div>
                <div class="tag-input-container">
                  <div class="tag-pills">
                    <span
                      v-for="(tag, idx) in form.best_for"
                      :key="idx"
                      class="tag-pill"
                    >
                      {{ tag }}
                      <i
                        class="fas fa-times"
                        @click="removeTag('best_for', idx)"
                      ></i>
                    </span>
                  </div>
                  <input
                    @keydown.enter.prevent="addTag('best_for', $event)"
                    placeholder="Type and press Enter to add tags..."
                  />
                </div>
              </div>

              <div class="input-group">
                <label>Avoid If (Tags)</label>
                <div class="preset-tags-container">
                  <span
                    v-for="tag in predefinedAvoidIf"
                    :key="tag"
                    class="preset-tag alert"
                    :class="{ active: form.avoid_if.includes(tag) }"
                    @click="toggleTag('avoid_if', tag)"
                  >
                    <i
                      :class="
                        form.avoid_if.includes(tag)
                          ? 'fas fa-times-circle'
                          : 'fas fa-plus'
                      "
                    ></i>
                    {{ tag }}
                  </span>
                </div>
                <div class="tag-input-container">
                  <div class="tag-pills">
                    <span
                      v-for="(tag, idx) in form.avoid_if"
                      :key="idx"
                      class="tag-pill alert"
                    >
                      {{ tag }}
                      <i
                        class="fas fa-times"
                        @click="removeTag('avoid_if', idx)"
                      ></i>
                    </span>
                  </div>
                  <input
                    @keydown.enter.prevent="addTag('avoid_if', $event)"
                    placeholder="Type and press Enter to add tags..."
                  />
                </div>
              </div>
            </div>
          </div>

          <div class="card map-card">
            <div class="card-header">
              <i class="fas fa-map-marked-alt"></i> <span>Map Location</span>
              <div class="coords-display">
                <span>LAT: {{ form.location_lat }}</span>
                <span>LNG: {{ form.location_lng }}</span>
              </div>
            </div>
            <div class="card-body p-0">
              <div class="map-wrapper-large">
                <div id="map-container"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="right-column">
          <div class="card upload-card">
            <div class="card-header">
              <i class="fas fa-images"></i>
              <span>Place Images</span>
              <span class="img-count-badge">{{ images.length }} / 10</span>
            </div>
            <div class="card-body">
              <div class="gallery-grid" v-if="images.length > 0">
                <div
                  v-for="(img, index) in images"
                  :key="index"
                  class="gallery-item"
                  :class="{ 'is-cover': index === 0 }"
                >
                  <img :src="img" class="gallery-img" alt="Place image" />

                  <div v-if="index === 0" class="cover-badge">
                    <i class="fas fa-star"></i> Cover
                  </div>

                  <div class="gallery-overlay">
                    <button
                      v-if="index !== 0"
                      type="button"
                      class="img-action-btn set-cover-btn"
                      @click="setCover(index)"
                      title="Set as Cover"
                    >
                      <i class="fas fa-star"></i>
                    </button>
                    <button
                      type="button"
                      class="img-action-btn delete-img-btn"
                      @click="removeImage(index)"
                      title="Remove"
                    >
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>

                <label v-if="images.length < 10" class="gallery-add-btn">
                  <i class="fas fa-plus"></i>
                  <span>Add</span>
                  <input
                    type="file"
                    @change="onFileChange"
                    accept="image/*"
                    multiple
                    hidden
                  />
                </label>
              </div>

              <div v-else class="upload-empty-state">
                <i class="fas fa-cloud-upload-alt"></i>
                <p>No images uploaded</p>
                <label class="upload-first-btn">
                  <i class="fas fa-plus"></i> Upload Images
                  <input
                    type="file"
                    @change="onFileChange"
                    accept="image/*"
                    multiple
                    hidden
                  />
                </label>
              </div>

              <p class="upload-hint">
                <i class="fas fa-info-circle"></i>
                First image = Cover photo. Click ⭐ to set any image as cover.
                Max 10 images.
              </p>
            </div>
          </div>

          <div class="card opening-hours-card">
            <div class="card-header">
              <i class="fas fa-clock"></i> <span>Opening Hours</span>
              <div class="oh-actions">
                <button
                  type="button"
                  @click="setAllClosed(false)"
                  class="btn-oh-action"
                >
                  Open
                </button>
                <button
                  type="button"
                  @click="setAllClosed(true)"
                  class="btn-oh-action"
                >
                  Close
                </button>
                <button
                  type="button"
                  @click="copyMondayToAll"
                  class="btn-oh-action highlight"
                >
                  Copy Mon
                </button>
              </div>
            </div>
            <div class="card-body">
              <div
                v-for="day in weekDays"
                :key="day.key"
                class="oh-row"
                :class="{ 'is-closed': openingHours[day.key].closed }"
              >
                <div class="oh-day">
                  <label class="oh-switch">
                    <input
                      type="checkbox"
                      v-model="openingHours[day.key].closed"
                      :true-value="false"
                      :false-value="true"
                    />
                    <span class="oh-slider"></span>
                  </label>
                  <span class="oh-label">{{ day.label }}</span>
                </div>
                <div class="oh-times" v-if="!openingHours[day.key].closed">
                  <div class="time-box">
                    <input
                      type="time"
                      v-model="openingHours[day.key].open"
                      class="time-input"
                    />
                  </div>
                  <span class="oh-dash"
                    ><i class="fas fa-arrow-right"></i
                  ></span>
                  <div class="time-box">
                    <input
                      type="time"
                      v-model="openingHours[day.key].close"
                      class="time-input"
                    />
                  </div>
                </div>
                <div class="oh-closed-container" v-else>
                  <span class="oh-closed-badge">Closed</span>
                </div>
              </div>
            </div>
          </div>

          <div class="card status-card">
            <div class="card-header">
              <i class="fas fa-cog"></i> Publishing Status
            </div>
            <div class="card-body">
              <div
                class="status-toggle-box"
                :class="form.is_published ? 'active' : 'draft'"
              >
                <div class="toggle-info">
                  <strong>Status</strong>
                  <span>{{
                    form.is_published ? "Public (Published)" : "Draft (Hidden)"
                  }}</span>
                </div>
                <label class="switch">
                  <input type="checkbox" v-model="form.is_published" />
                  <span class="slider round"></span>
                </label>
              </div>

              <div class="btn-group-vertical">
                <button
                  type="submit"
                  class="btn-submit-full"
                  :disabled="isSaving"
                >
                  <i
                    class="fas"
                    :class="isSaving ? 'fa-spinner fa-spin' : 'fa-check-circle'"
                  ></i>
                  {{ isSaving ? "Saving..." : "Create Place" }}
                </button>
                <button
                  type="button"
                  class="btn-cancel-full"
                  @click="$router.push('/admin/places')"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
/* global L */
import { ref, onMounted, nextTick, computed } from "vue";
import { useRouter } from "vue-router";
import { placeRepository } from "@/repositories/placeRepository";
import { categoryRepository } from "@/repositories/categoryRepository";

const router = useRouter();
const categories = ref([]);
const map = ref(null);
const marker = ref(null);
const addressPaste = ref("");
const isSaving = ref(false);
const showBookingLinks = ref(false);

// 💡 สร้าง 2 Array:
// 1. images ไว้เก็บ Base64 โชว์ให้แอดมินดูหน้าเว็บ
// 2. rawFiles ไว้เก็บก้อนไฟล์ดิบๆ สำหรับยิงไปหา FastAPI
const images = ref([]);
const rawFiles = ref([]);

const months = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
];

const predefinedBestFor = [
  "Hot Season",
  "Rainy Season",
  "Cool Season",
  "All Seasons",
  "Photography",
  "Nature",
  "Spirituality",
  "Relaxation",
  "Family",
  "Couples",
  "Adventure",
  "Food",
];
const predefinedAvoidIf = [
  "Rainy Season",
  "Hot Season",
  "Crowds",
  "Inappropriate Attire",
  "Mobility Issues",
  "Noisy",
];

const form = ref({
  name: "",
  category_id: "",
  description: "",
  location_lat: 16.5662, // พิกัดเริ่มต้นที่สะหวันนะเขต
  location_lng: 104.7525,
  is_published: true,
  best_months: "",
  best_months_start: "Nov",
  best_months_end: "Feb",
  is_year_round: false,
  ideal_stay: "",
  daily_budget: "",
  budget_min: 150000,
  budget_max: 500000,
  is_free: false,
  location_name: "",
  best_for: [],
  avoid_if: [],
  booking_url: "",
  agoda_url: "",
});

const isHotelCategory = computed(() => {
  if (!form.value.category_id || !categories.value.length) return false;
  const cat = categories.value.find((c) => c.id === form.value.category_id);
  return (
    cat &&
    (cat.parent_type?.toLowerCase() === "hotel" ||
      cat.name.toLowerCase().includes("hotel"))
  );
});

const addTag = (field, event) => {
  const val = event.target.value.trim();
  if (val && !form.value[field].includes(val)) {
    form.value[field].push(val);
    event.target.value = "";
  }
};

const removeTag = (field, index) => {
  form.value[field].splice(index, 1);
};

const toggleTag = (field, tag) => {
  const idx = form.value[field].indexOf(tag);
  if (idx === -1) {
    form.value[field].push(tag);
  } else {
    form.value[field].splice(idx, 1);
  }
};

const weekDays = [
  { key: "mon", label: "Monday" },
  { key: "tue", label: "Tuesday" },
  { key: "wed", label: "Wednesday" },
  { key: "thu", label: "Thursday" },
  { key: "fri", label: "Friday" },
  { key: "sat", label: "Saturday" },
  { key: "sun", label: "Sunday" },
];

const defaultDayHours = () => ({
  open: "08:00",
  close: "17:00",
  closed: false,
});

const openingHours = ref({
  mon: defaultDayHours(),
  tue: defaultDayHours(),
  wed: defaultDayHours(),
  thu: defaultDayHours(),
  fri: defaultDayHours(),
  sat: defaultDayHours(),
  sun: defaultDayHours(),
});

const setAllClosed = (isClosed) => {
  weekDays.forEach((day) => {
    openingHours.value[day.key].closed = isClosed;
  });
};

const copyMondayToAll = () => {
  const mon = openingHours.value.mon;
  weekDays.forEach((day) => {
    if (day.key !== "mon") {
      openingHours.value[day.key] = { ...mon };
    }
  });
};
// --- จัดการแผนที่ (Map) ---
const initMap = () => {
  if (map.value) return;
  const lat = parseFloat(form.value.location_lat);
  const lng = parseFloat(form.value.location_lng);

  map.value = L.map("map-container", { zoomControl: false }).setView(
    [lat, lng],
    15,
  );
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(
    map.value,
  );
  L.control.zoom({ position: "bottomright" }).addTo(map.value);

  // ตอนสร้างใหม่ ให้ Marker ลากได้เสมอ
  marker.value = L.marker([lat, lng], { draggable: true }).addTo(map.value);

  map.value.on("click", (e) => {
    updateMarkerPosition(e.latlng.lat, e.latlng.lng);
  });

  marker.value.on("dragend", () => {
    const pos = marker.value.getLatLng();
    updateMarkerPosition(pos.lat, pos.lng);
  });
};

const handlePasteAddress = (e) => {
  const pasteData = e.clipboardData.getData("text");
  addressPaste.value = pasteData;
  setTimeout(() => searchFromAddress(), 100);
};

const searchFromAddress = () => {
  if (!addressPaste.value) return;

  const input = addressPaste.value.trim();

  // 1. ตรวจสอบว่าเป็นการวางลิงก์ Google Maps ที่มีพิกัด (เช่น /@16.5401,104.7570,15z)
  const urlMatch = input.match(/@(-?\d+\.\d+),(-?\d+\.\d+)/);

  // 2. ตรวจสอบว่าเป็นการวางพิกัดตรงๆ (เช่น 16.5401, 104.7570)
  const coordMatch = input.match(/^(-?\d+\.\d+)[\s,]+(-?\d+\.\d+)$/);

  let lat = null;
  let lng = null;

  if (urlMatch) {
    lat = parseFloat(urlMatch[1]);
    lng = parseFloat(urlMatch[2]);
  } else if (coordMatch) {
    lat = parseFloat(coordMatch[1]);
    lng = parseFloat(coordMatch[2]);
  }

  if (lat !== null && lng !== null) {
    map.value.setView([lat, lng], 17);
    updateMarkerPosition(lat, lng);
    return;
  }

  // 3. Fallback ไปใช้ระบบค้นหาชื่อฟรีด้วย Nominatim (อาจจะไม่เจอชื่อที่เป๊ะแบบ Google Maps)
  const geocoder = L.Control.Geocoder.nominatim();
  geocoder.geocode(input, (results) => {
    if (results && results.length > 0) {
      const { center } = results[0];
      map.value.setView(center, 17);
      updateMarkerPosition(center.lat, center.lng);
    } else {
      alert(
        "Location not found in free database.\n\nTip: Copy the whole Google Maps Link (URL) or exact coordinates (e.g., 16.540, 104.757) instead!",
      );
    }
  });
};

const updateMarkerPosition = (lat, lng) => {
  const fixedLat = isNaN(lat)
    ? 16.5662
    : parseFloat(parseFloat(lat).toFixed(6));
  const fixedLng = isNaN(lng)
    ? 104.7525
    : parseFloat(parseFloat(lng).toFixed(6));
  if (marker.value) marker.value.setLatLng([fixedLat, fixedLng]);
  form.value.location_lat = fixedLat;
  form.value.location_lng = fixedLng;
};

// --- จัดการรูปภาพ (Gallery) ---
const onFileChange = (e) => {
  const files = Array.from(e.target.files);
  files.forEach((file) => {
    if (images.value.length >= 10) return;

    // เช็คขนาด 5MB
    if (file.size > 5 * 1024 * 1024) {
      alert(`File ${file.name} is too large (Max 5MB).`);
      return;
    }

    // 1. เก็บไฟล์ดิบไว้ส่ง API
    rawFiles.value.push(file);

    // 2. แปลงเป็น Base64 ไว้โชว์พรีวิว
    const reader = new FileReader();
    reader.onload = (ev) => {
      images.value.push(ev.target.result);
    };
    reader.readAsDataURL(file);
  });
  e.target.value = ""; // Reset input
};

const removeImage = (index) => {
  images.value.splice(index, 1); // ลบพรีวิว
  rawFiles.value.splice(index, 1); // ลบไฟล์จริงที่จะส่ง
};

const setCover = (index) => {
  // สลับพรีวิวมาไว้ตำแหน่งแรก (Cover)
  const [img] = images.value.splice(index, 1);
  images.value.unshift(img);

  // สลับไฟล์ดิบมาไว้ตำแหน่งแรกด้วย (เพื่อส่งให้ API ตามลำดับ)
  const [file] = rawFiles.value.splice(index, 1);
  rawFiles.value.unshift(file);
};

// --- ฟังก์ชันบันทึกข้อมูล ---
const savePlace = async () => {
  if (!form.value.name || !form.value.category_id || !form.value.description) {
    alert("Please fill in Name, Category, and Description.");
    return;
  }

  isSaving.value = true;
  try {
    // ใช้ FormData ส่งไป FastAPI
    const formData = new FormData();
    formData.append("name", form.value.name);
    formData.append("description", form.value.description);
    formData.append("category_id", form.value.category_id);
    formData.append("is_published", form.value.is_published ? 1 : 0);
    formData.append("location_lat", form.value.location_lat);
    formData.append("location_lng", form.value.location_lng);
    formData.append("opening_hours", JSON.stringify(openingHours.value));

    // Premium Details
    const bestMonthsStr = form.value.is_year_round
      ? "Year-round"
      : `${form.value.best_months_start} - ${form.value.best_months_end}`;
    const formatBudget = (val) => {
      if (!val) return "0";
      if (val >= 1000) return val / 1000 + "k";
      return val;
    };
    const budgetStr = form.value.is_free
      ? "Free"
      : `₭ ${formatBudget(form.value.budget_min)} - ${formatBudget(form.value.budget_max)}`;

    formData.append("best_months", bestMonthsStr);
    formData.append("ideal_stay", form.value.ideal_stay || "");
    formData.append("daily_budget", budgetStr);
    formData.append("location_name", form.value.location_name || "");
    formData.append("best_for", JSON.stringify(form.value.best_for || []));
    formData.append("avoid_if", JSON.stringify(form.value.avoid_if || []));
    formData.append("booking_url", form.value.booking_url || "");
    formData.append("agoda_url", form.value.agoda_url || "");

    // ยัดไฟล์ทั้งหมดใส่ Key 'images' ให้ FastAPI แปลงเป็น List[UploadFile]
    rawFiles.value.forEach((file) => {
      formData.append("images", file);
    });

    await placeRepository.create(formData);

    alert("✅ Place added successfully!");
    router.push("/admin/places"); // กลับไปหน้าตาราง
  } catch (error) {
    console.error("Save Error:", error);
    alert("❌ Failed to save place. " + (error.response?.data?.detail || ""));
  } finally {
    isSaving.value = false;
  }
};

onMounted(async () => {
  try {
    const res = await categoryRepository.getAll();
    categories.value = res.data;
    await nextTick();
    initMap();
  } catch (error) {
    console.error("Failed to load categories:", error);
  }
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap");

.edit-page-container {
  background: #f1f5f9;
  min-height: 100vh;
  font-family: "Kanit", sans-serif;
  color: #1e293b;
}

.text-danger {
  color: #e74c3c;
}

.header-section {
  background: white;
  padding: 20px 30px;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 20px;
}

.btn-back {
  padding: 10px 15px;
  border-radius: 10px;
  border: 1px solid #cbd5e1;
  background: white;
  cursor: pointer;
}

.title-group h1 {
  font-size: 1.4rem;
  margin: 0;
}

.subtitle {
  font-size: 0.85rem;
  color: #64748b;
  margin: 0;
}

.main-layout {
  max-width: 1400px;
  margin: 30px auto;
  padding: 0 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 25px;
}

@media (max-width: 1024px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}

.card {
  background: white;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  margin-bottom: 25px;
  overflow: hidden;
}

.card-header {
  padding: 15px 25px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  border-radius: 20px 20px 0 0;
}

.img-count-badge {
  margin-left: auto;
  background: #e2e8f0;
  color: #64748b;
  font-size: 0.78rem;
  padding: 2px 10px;
  border-radius: 20px;
  font-weight: 500;
}

.card-body {
  padding: 25px;
}

.input-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 15px;
}

@media (max-width: 600px) {
  .input-row {
    grid-template-columns: 1fr;
  }
}

.input-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 5px;
  color: #475569;
}

.preset-tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.preset-tag {
  font-size: 0.8rem;
  background: #f1f5f9;
  color: #64748b;
  border: 1px solid #cbd5e1;
  padding: 4px 10px;
  border-radius: 15px;
  cursor: pointer;
  transition: 0.2s;
  user-select: none;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}
.preset-tag:hover {
  background: #e2e8f0;
}
.preset-tag.active {
  background: #dcfce7;
  color: #15803d;
  border-color: #22c55e;
}
.preset-tag.alert.active {
  background: #fee2e2;
  color: #b91c1c;
  border-color: #ef4444;
}

input,
select,
textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  outline: none;
  font-family: "Kanit", sans-serif;
  box-sizing: border-box;
}

input:focus,
select:focus,
textarea:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.map-wrapper-large {
  height: 500px;
  position: relative;
  border-radius: 0 0 20px 20px;
  overflow: hidden;
}

#map-container {
  height: 100%;
  width: 100%;
}

.coords-display {
  margin-left: auto;
  font-size: 0.8rem;
  background: #e2e8f0;
  padding: 4px 12px;
  border-radius: 15px;
  display: flex;
  gap: 12px;
}

/* ===================== GALLERY STYLES ===================== */
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 14px;
}

.gallery-item {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  aspect-ratio: 4/3;
  border: 2px solid #e2e8f0;
  cursor: pointer;
  transition: 0.2s;
}

.gallery-item.is-cover {
  border-color: #f59e0b;
  box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.2);
}

.gallery-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.cover-badge {
  position: absolute;
  top: 6px;
  left: 6px;
  background: #f59e0b;
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.gallery-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  opacity: 0;
  transition: 0.25s;
}

.gallery-item:hover .gallery-overlay {
  opacity: 1;
}

.img-action-btn {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  transition: 0.2s;
}

.set-cover-btn {
  background: #f59e0b;
  color: white;
}

.set-cover-btn:hover {
  background: #d97706;
  transform: scale(1.1);
}

.delete-img-btn {
  background: #f43f5e;
  color: white;
}

.delete-img-btn:hover {
  background: #e11d48;
  transform: scale(1.1);
}

.gallery-add-btn {
  aspect-ratio: 4/3;
  border: 2px dashed #cbd5e1;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;
  color: #94a3b8;
  font-size: 0.85rem;
  transition: 0.2s;
  font-weight: 500;
}

.gallery-add-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  background: #eff6ff;
}

.gallery-add-btn i {
  font-size: 1.4rem;
}

/* ===================== OPENING HOURS STYLES ===================== */
.opening-hours-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.oh-actions {
  display: flex;
  gap: 5px;
}

.btn-oh-action {
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  color: #475569;
  font-size: 0.65rem;
  padding: 3px 8px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 700;
  transition: 0.2s;
  font-family: "Kanit", sans-serif;
  white-space: nowrap;
}

.btn-oh-action:hover {
  background: #e2e8f0;
  color: #1e293b;
}

.btn-oh-action.highlight {
  background: #eff6ff;
  border-color: #bfdbfe;
  color: #3b82f6;
}

.opening-hours-card .card-body {
  padding: 10px 15px 15px;
}

.oh-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 8px;
  margin: 0 -8px;
  border-radius: 10px;
  border-bottom: 1px solid #f1f5f9;
  transition: 0.2s;
}

.oh-row:hover {
  background: #f8fafc;
}

.oh-row.is-closed {
  opacity: 0.6;
}

.oh-row:last-child {
  border-bottom: none;
  padding-bottom: 12px;
}

.oh-day {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100px;
}

.oh-label {
  font-weight: 600;
  color: #334155;
  font-size: 0.85rem;
}

.oh-row.is-closed .oh-label {
  color: #94a3b8;
}

.oh-times {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  justify-content: flex-end;
}

.time-box {
  position: relative;
}

.time-input {
  padding: 6px 5px;
  font-size: 0.8rem;
  text-align: center;
  border: 1px solid #e2e8f0;
  width: 95px;
  border-radius: 8px;
  background: white;
  color: #0f172a;
  font-family: "Kanit", sans-serif;
  font-weight: 700;
  outline: none;
  transition: 0.2s;
}

.time-input:focus {
  border-color: #3b82f6;
  background: #f0f7ff;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.oh-dash {
  color: #cbd5e1;
  font-size: 0.7rem;
  display: flex;
  align-items: center;
}

.oh-closed-container {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}

.oh-closed-badge {
  color: #94a3b8;
  font-weight: 700;
  font-size: 0.75rem;
  background: #f1f5f9;
  padding: 4px 12px;
  border-radius: 20px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

/* Custom switch for Opening Hours */
.oh-switch {
  position: relative;
  display: inline-block;
  width: 38px;
  height: 20px;
}

.oh-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.oh-slider {
  position: absolute;
  cursor: pointer;
  inset: 0;
  background: #e2e8f0;
  border-radius: 999px;
  transition: 0.3s;
}

.oh-slider:before {
  content: "";
  position: absolute;
  height: 14px;
  width: 14px;
  left: 3px;
  top: 3px;
  background: white;
  border-radius: 50%;
  transition: 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.oh-switch input:checked + .oh-slider {
  background: #10b981;
}

.oh-switch input:checked + .oh-slider:before {
  transform: translateX(18px);
}

/* Empty upload state */
.upload-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background: #f8fafc;
  border: 2px dashed #cbd5e1;
  border-radius: 15px;
  color: #94a3b8;
  margin-bottom: 14px;
  gap: 12px;
}

.upload-empty-state i {
  font-size: 2.5rem;
}

.upload-empty-state p {
  margin: 0;
  font-weight: 500;
}

.upload-first-btn {
  background: #3b82f6;
  color: white;
  padding: 10px 22px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: "Kanit", sans-serif;
  transition: 0.2s;
}

.upload-first-btn:hover {
  background: #2563eb;
}

.upload-hint {
  font-size: 0.8rem;
  color: #94a3b8;
  margin: 0;
  display: flex;
  align-items: flex-start;
  gap: 6px;
  line-height: 1.5;
}

/* ===================== STATUS CARD ===================== */
.status-toggle-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px;
  border-radius: 12px;
  margin-bottom: 20px;
}

.status-toggle-box.active {
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
}

.status-toggle-box.draft {
  background: #fff1f2;
  border: 1px solid #fecdd3;
}

.btn-submit-full {
  background: #10b981;
  color: white;
  border: none;
  padding: 15px;
  border-radius: 12px;
  width: 100%;
  font-weight: 700;
  font-family: "Kanit", sans-serif;
  cursor: pointer;
  transition: 0.2s;
}

.btn-submit-full:hover:not(:disabled) {
  background: #059669;
}

.btn-submit-full:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-cancel-full {
  background: white;
  border: 1px solid #cbd5e1;
  padding: 12px;
  border-radius: 12px;
  color: #64748b;
  cursor: pointer;
  margin-top: 10px;
  width: 100%;
  font-family: "Kanit", sans-serif;
  transition: 0.2s;
}

.btn-cancel-full:hover {
  background: #f8fafc;
}

/* Switch Toggle */
.switch {
  position: relative;
  width: 50px;
  height: 26px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  inset: 0;
  background: #cbd5e1;
  transition: 0.4s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 4px;
  bottom: 4px;
  background: white;
  transition: 0.4s;
  border-radius: 50%;
}

input:checked + .slider {
  background: #10b981;
}

input:checked + .slider:before {
  transform: translateX(24px);
}

/* Tag Input Styles */
.tag-input-container {
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  padding: 10px;
  background: white;
  min-height: 45px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  transition: 0.2s;
}

.tag-input-container:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.tag-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-pill {
  background: #eff6ff;
  color: #1d4ed8;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  border: 1px solid #dbeafe;
}

.tag-pill.alert {
  background: #fff1f2;
  color: #e11d48;
  border-color: #ffe4e6;
}

.tag-pill i {
  cursor: pointer;
  font-size: 0.75rem;
  opacity: 0.6;
  transition: 0.2s;
}

.tag-pill i:hover {
  opacity: 1;
  transform: scale(1.2);
}

.tag-input-container input {
  flex: 1;
  min-width: 150px;
  border: none !important;
  padding: 4px !important;
  font-size: 0.85rem !important;
  background: transparent !important;
}

.tag-input-container input:focus {
  outline: none !important;
}
</style>
