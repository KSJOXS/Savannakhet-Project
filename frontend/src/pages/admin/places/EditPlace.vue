<template>
    <div class="edit-page-container">
        <div class="header-section">
            <div class="header-content">
                <button class="btn-back" @click="$router.push('/admin/places')">
                    <i class="fas fa-arrow-left"></i> Back
                </button>
                <div class="title-group">
                    <h1>Edit Place</h1>
                    <p class="subtitle">Manage details, coordinates, and images for this location.</p>
                </div>
            </div>
        </div>

        <div class="main-layout">
            <form @submit.prevent="updatePlace" class="form-grid">
                <div class="left-column">
                    <div class="card info-card" :class="{ 'is-locked': form.is_published }">
                        <div class="card-header">
                            <i class="fas fa-edit"></i> <span>General Info</span>
                            <div v-if="form.is_published" class="lock-badge">
                                <i class="fas fa-lock"></i> Locked (Change to Draft to edit)
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="input-row">
                                <div class="input-group">
                                    <label>Place Name</label>
                                    <input v-model="form.name" :disabled="form.is_published"
                                        placeholder="Enter place name..." required>
                                </div>
                                <div class="input-group">
                                    <label>Category</label>
                                    <select v-model="form.category_id" :disabled="form.is_published">
                                        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                                            [{{ cat.parent_type.toUpperCase() }}] {{ cat.name }}
                                        </option>
                                    </select>
                                </div>
                            </div>

                             <div class="input-row" v-if="isHotelCategory" style="margin-top: 15px; background: #f0f9ff; padding: 15px; border-radius: 12px; border: 1px solid #bae6fd;">
                                <div style="grid-column: 1 / -1; margin-bottom: 10px; display: flex; align-items: center; gap: 10px;">
                                    <label class="switch" style="margin-bottom: 0;">
                                        <input type="checkbox" v-model="showBookingLinks" :disabled="form.is_published">
                                        <span class="slider round"></span>
                                    </label>
                                    <span style="font-weight: 700; color: #0369a1;">Enable Partner Booking Links (Agoda / Booking.com)</span>
                                </div>
                                <template v-if="showBookingLinks">
                                    <div class="input-group" style="margin-bottom: 0;">
                                        <label style="color: #0369a1; font-weight: 700;"><i class="fas fa-link"></i> Booking.com URL</label>
                                        <input v-model="form.booking_url" :disabled="form.is_published" placeholder="https://www.booking.com/hotel/...">
                                    </div>
                                    <div class="input-group" style="margin-bottom: 0;">
                                        <label style="color: #0369a1; font-weight: 700;"><i class="fas fa-link"></i> Agoda URL</label>
                                        <input v-model="form.agoda_url" :disabled="form.is_published" placeholder="https://www.agoda.com/...">
                                    </div>
                                </template>
                             </div>

                            <div class="input-group" v-if="!form.is_published" style="margin-top: 10px;">
                                <label style="color: #6366f1;"><i class="fas fa-paste"></i> Paste Google Maps Plus Code/Address</label>
                                <div style="display: flex; gap: 10px;">
                                    <input v-model="addressPaste" @paste="handlePasteAddress"
                                        placeholder="E.g., HP4W+G5V or Place Name..."
                                        style="border: 2px solid #6366f1; background: #f5f3ff;">
                                    <button type="button" @click="searchFromAddress"
                                        style="background: #6366f1; color: white; border: none; padding: 0 20px; border-radius: 10px; cursor: pointer;">
                                        Detect
                                    </button>
                                </div>
                            </div>

                            <div class="input-group">
                                <label>Description</label>
                                <textarea v-model="form.description" :disabled="form.is_published" rows="4"
                                    placeholder="Place details..."></textarea>
                            </div>

                            <!-- ✨ Travel Guide Sections — inline below Description -->
                            <div class="guide-sections-editor">
                                <div class="gse-header">
                                    <span class="gse-title">
                                        <i class="fas fa-book-open"></i>
                                        Travel Guide Sections
                                    </span>
                                    <span class="gse-count" v-if="sections.length > 0">{{ sections.length }} section{{ sections.length !== 1 ? 's' : '' }}</span>
                                </div>

                                <!-- Accordion list -->
                                <div class="gse-list" v-if="sections.length > 0">
                                    <div
                                        v-for="(sec, idx) in sections"
                                        :key="sec.id || idx"
                                        class="gse-item"
                                        :class="{ 'is-expanded': expandedSection === sec.id, 'is-editing': editingSectionId === sec.id }"
                                    >
                                        <!-- Accordion header row -->
                                        <div class="gse-item-bar" @click="toggleExpandSection(sec.id)">
                                            <div class="gse-item-left">
                                                <div class="gse-thumb-wrap">
                                                    <img v-if="sec.image_url" :src="getSectionImageUrl(sec.image_url)" class="gse-thumb" />
                                                    <div v-else class="gse-thumb-placeholder"><i class="fas fa-image"></i></div>
                                                </div>
                                                <div class="gse-item-info">
                                                    <span class="gse-item-label">Section {{ idx + 1 }}</span>
                                                    <span class="gse-item-desc-preview">{{ (sec.description || '').substring(0, 60) || 'No description' }}{{ (sec.description || '').length > 60 ? '...' : '' }}</span>
                                                </div>
                                            </div>
                                            <div class="gse-item-right" @click.stop>
                                                <button type="button" class="gse-btn" @click="moveSectionUp(idx)" :disabled="idx === 0 || form.is_published" title="Move Up"><i class="fas fa-arrow-up"></i></button>
                                                <button type="button" class="gse-btn" @click="moveSectionDown(idx)" :disabled="idx === sections.length - 1 || form.is_published" title="Move Down"><i class="fas fa-arrow-down"></i></button>
                                                <button type="button" class="gse-btn edit" @click="startEditSection(sec)" :disabled="form.is_published" title="Edit"><i class="fas fa-pen"></i></button>
                                                <button type="button" class="gse-btn danger" @click="deleteSection(sec.id)" :disabled="form.is_published" title="Delete"><i class="fas fa-trash"></i></button>
                                                <button type="button" class="gse-btn chevron" @click="toggleExpandSection(sec.id)">
                                                    <i class="fas" :class="expandedSection === sec.id ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
                                                </button>
                                            </div>
                                        </div>

                                        <!-- Expanded: view mode -->
                                        <div v-if="expandedSection === sec.id && editingSectionId !== sec.id" class="gse-expand-body">
                                            <img v-if="sec.image_url" :src="getSectionImageUrl(sec.image_url)" class="gse-full-img" />
                                            <div v-if="!sec.image_url" class="gse-no-img"><i class="fas fa-image"></i> No image yet</div>
                                            <p class="gse-desc-text">{{ sec.description || '(No description)' }}</p>
                                        </div>

                                        <!-- Expanded: edit mode -->
                                        <div v-if="editingSectionId === sec.id" class="gse-edit-body">
                                            <label class="gse-upload-area" :class="{ 'has-img': editSectionPreview || sec.image_url }">
                                                <img v-if="editSectionPreview" :src="editSectionPreview" class="gse-upload-img" />
                                                <div v-else-if="sec.image_url" class="gse-upload-existing-wrap">
                                                    <img :src="getSectionImageUrl(sec.image_url)" class="gse-upload-img" />
                                                    <span class="gse-change-hint"><i class="fas fa-camera"></i> Click to change image</span>
                                                </div>
                                                <div v-else class="gse-upload-ph">
                                                    <i class="fas fa-cloud-upload-alt"></i>
                                                    <span>Click to upload image</span>
                                                    <small>JPG / PNG / WebP</small>
                                                </div>
                                                <input type="file" accept="image/*" @change="onEditSectionImage" hidden />
                                            </label>
                                            <textarea v-model="editSectionDesc" rows="5" placeholder="Write a detailed description for this section..." class="gse-textarea"></textarea>
                                            <div class="gse-action-row">
                                                <button type="button" class="gse-save-btn" @click="saveEditSection(sec.id)" :disabled="isSavingSection">
                                                    <i class="fas" :class="isSavingSection ? 'fa-spinner fa-spin' : 'fa-check'"></i>
                                                    {{ isSavingSection ? 'Saving...' : 'Save Section' }}
                                                </button>
                                                <button type="button" class="gse-cancel-btn" @click="cancelEditSection">Cancel</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Add new section inline form -->
                                <div v-if="showAddSection" class="gse-add-form">
                                    <div class="gse-add-title"><i class="fas fa-plus-circle"></i> New Section</div>
                                    <label class="gse-upload-area" :class="{ 'has-img': newSectionPreview }">
                                        <img v-if="newSectionPreview" :src="newSectionPreview" class="gse-upload-img" />
                                        <div v-else class="gse-upload-ph">
                                            <i class="fas fa-cloud-upload-alt"></i>
                                            <span>Click to upload image</span>
                                            <small>JPG / PNG / WebP · Max 5MB</small>
                                        </div>
                                        <input type="file" accept="image/*" @change="onNewSectionImage" hidden />
                                    </label>
                                    <textarea v-model="newSectionDesc" rows="5" placeholder="Write a detailed description for this section (travel article style)..." class="gse-textarea"></textarea>
                                    <div class="gse-action-row">
                                        <button type="button" class="gse-save-btn" @click="addSection" :disabled="isSavingSection">
                                            <i class="fas" :class="isSavingSection ? 'fa-spinner fa-spin' : 'fa-check'"></i>
                                            {{ isSavingSection ? 'Adding...' : 'Add Section' }}
                                        </button>
                                        <button type="button" class="gse-cancel-btn" @click="showAddSection = false; newSectionPreview = null; newSectionDesc = ''">Cancel</button>
                                    </div>
                                </div>

                                <!-- + Add Section trigger button -->
                                <button v-if="!showAddSection" type="button" class="gse-add-trigger" @click="showAddSection = true; expandedSection = null" :disabled="form.is_published">
                                    <i class="fas fa-plus"></i>
                                    <span>Add Section</span>
                                </button>
                            </div>

                        </div>
                    </div>

                    <!-- Premium Details Card -->
                    <div class="card premium-details-card" :class="{ 'is-locked': form.is_published }">
                        <div class="card-header">
                            <i class="fas fa-star"></i> <span>Premium Details (Stats & Tags)</span>
                        </div>
                        <div class="card-body">
                            <div class="input-row">
                                <div class="input-group">
                                    <label class="label-with-action">
                                        <span>Best Months (Range)</span>
                                        <label class="year-round-toggle">
                                            <input type="checkbox" v-model="form.is_year_round" :disabled="form.is_published"> 
                                            <span>Year-round</span>
                                        </label>
                                    </label>
                                    <div style="display: flex; gap: 10px; align-items: center;" v-if="!form.is_year_round">
                                        <select v-model="form.best_months_start" :disabled="form.is_published" style="flex: 1; padding: 10px; border-radius: 8px; border: 1px solid #cbd5e1;">
                                            <option v-for="m in months" :key="m" :value="m">{{ m }}</option>
                                        </select>
                                        <span style="color: #94a3b8; font-weight: 600;">to</span>
                                        <select v-model="form.best_months_end" :disabled="form.is_published" style="flex: 1; padding: 10px; border-radius: 8px; border: 1px solid #cbd5e1;">
                                            <option v-for="m in months" :key="m" :value="m">{{ m }}</option>
                                        </select>
                                    </div>
                                    <div v-else style="padding: 10px; background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; color: #64748b; font-weight: 600; text-align: center;">
                                        <i class="fas fa-calendar-check" style="margin-right: 8px;"></i> Year-round
                                    </div>
                                </div>
                                <div class="input-group">
                                    <label>Ideal Stay (e.g. 1 - 2 Days)</label>
                                    <input v-model="form.ideal_stay" :disabled="form.is_published" placeholder="2 Days">
                                </div>
                            </div>
                            <div class="input-row">
                                <div class="input-group">
                                    <label class="label-with-action">
                                        <span>Daily Budget (Range in ₭)</span>
                                        <label class="year-round-toggle">
                                            <input type="checkbox" v-model="form.is_free" :disabled="form.is_published"> 
                                            <span>Free</span>
                                        </label>
                                    </label>
                                    <div v-if="!form.is_free" style="display: flex; gap: 10px; align-items: center;">
                                        <input type="number" v-model="form.budget_min" :disabled="form.is_published" placeholder="Min (e.g. 100000)">
                                        <span>-</span>
                                        <input type="number" v-model="form.budget_max" :disabled="form.is_published" placeholder="Max (e.g. 500000)">
                                    </div>
                                    <div v-else style="padding: 10px; background: #ecfdf5; border: 1px dashed #10b981; border-radius: 8px; color: #047857; font-weight: 700; text-align: center;">
                                        <i class="fas fa-gift" style="margin-right: 8px;"></i> Free Entry / No Cost
                                    </div>
                                </div>
                                <div class="input-group">
                                    <label>Location Display Name (e.g. Savannakhet)</label>
                                    <input v-model="form.location_name" :disabled="form.is_published" placeholder="Savannakhet">
                                </div>
                            </div>

                            <div class="input-group">
                                <label>Best For / Best Season (Tags)</label>
                                <div class="preset-tags-container" v-if="!form.is_published">
                                    <span v-for="tag in predefinedBestFor" :key="tag" 
                                          class="preset-tag" :class="{'active': form.best_for.includes(tag)}"
                                          @click="toggleTag('best_for', tag)">
                                        <i :class="form.best_for.includes(tag) ? 'fas fa-check' : 'fas fa-plus'"></i> {{ tag }}
                                    </span>
                                </div>
                                <div class="tag-input-container" :class="{ disabled: form.is_published }">
                                    <div class="tag-pills">
                                        <span v-for="(tag, idx) in form.best_for" :key="idx" class="tag-pill">
                                            {{ tag }}
                                            <i v-if="!form.is_published" class="fas fa-times" @click="removeTag('best_for', idx)"></i>
                                        </span>
                                    </div>
                                    <input v-if="!form.is_published" @keydown.enter.prevent="addTag('best_for', $event)" 
                                        placeholder="Type and press Enter to add tags...">
                                </div>
                            </div>

                            <div class="input-group">
                                <label>Avoid If (Tags)</label>
                                <div class="preset-tags-container" v-if="!form.is_published">
                                    <span v-for="tag in predefinedAvoidIf" :key="tag" 
                                          class="preset-tag alert" :class="{'active': form.avoid_if.includes(tag)}"
                                          @click="toggleTag('avoid_if', tag)">
                                        <i :class="form.avoid_if.includes(tag) ? 'fas fa-times-circle' : 'fas fa-plus'"></i> {{ tag }}
                                    </span>
                                </div>
                                <div class="tag-input-container" :class="{ disabled: form.is_published }">
                                    <div class="tag-pills">
                                        <span v-for="(tag, idx) in form.avoid_if" :key="idx" class="tag-pill alert">
                                            {{ tag }}
                                            <i v-if="!form.is_published" class="fas fa-times" @click="removeTag('avoid_if', idx)"></i>
                                        </span>
                                    </div>
                                    <input v-if="!form.is_published" @keydown.enter.prevent="addTag('avoid_if', $event)" 
                                        placeholder="Type and press Enter to add tags...">
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
                                <div v-if="form.is_published" class="map-overlay-locked">
                                    <div class="overlay-msg">
                                        <i class="fas fa-info-circle"></i> Change to Draft to edit coordinates
                                    </div>
                                </div>
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
                                <div v-for="(img, index) in images" :key="index"
                                    class="gallery-item"
                                    :class="{ 'is-cover': index === 0 }">
                                    <img :src="img" class="gallery-img" alt="Place image">

                                    <div v-if="index === 0" class="cover-badge">
                                        <i class="fas fa-star"></i> Cover
                                    </div>

                                    <div v-if="!form.is_published" class="gallery-overlay">
                                        <button v-if="index !== 0" type="button"
                                            class="img-action-btn set-cover-btn"
                                            @click="setCover(index)"
                                            title="Set as Cover">
                                            <i class="fas fa-star"></i>
                                        </button>
                                        <button type="button"
                                            class="img-action-btn delete-img-btn"
                                            @click="removeImage(index)"
                                            title="Remove">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </div>
                                </div>

                                <label v-if="!form.is_published && images.length < 10" class="gallery-add-btn">
                                    <i class="fas fa-plus"></i>
                                    <span>Add</span>
                                    <input type="file" @change="onFileChange" accept="image/*" multiple hidden>
                                </label>
                            </div>

                            <div v-else class="upload-empty-state">
                                <i class="fas fa-cloud-upload-alt"></i>
                                <p>No images uploaded</p>
                                <label v-if="!form.is_published" class="upload-first-btn">
                                    <i class="fas fa-plus"></i> Upload Images
                                    <input type="file" @change="onFileChange" accept="image/*" multiple hidden>
                                </label>
                                <span v-else class="locked-hint">Change to Draft to upload images</span>
                            </div>

                            <p class="upload-hint">
                                <i class="fas fa-info-circle"></i>
                                First image = Cover photo. Click ⭐ to set any image as cover. Max 10 images.
                            </p>
                        </div>
                    </div>

                    <div class="card opening-hours-card">
                        <div class="card-header">
                            <i class="fas fa-clock"></i> <span>Opening Hours</span>
                            <div class="oh-actions">
                                <button type="button" @click="setAllClosed(false)" class="btn-oh-action">Open</button>
                                <button type="button" @click="setAllClosed(true)" class="btn-oh-action">Close</button>
                                <button type="button" @click="copyMondayToAll" class="btn-oh-action highlight">Copy Mon</button>
                            </div>
                        </div>
                        <div class="card-body">
                            <div v-for="day in weekDays" :key="day.key" class="oh-row" :class="{'is-closed': openingHours[day.key].closed}">
                                <div class="oh-day">
                                    <label class="oh-switch">
                                        <input type="checkbox" v-model="openingHours[day.key].closed" :true-value="false" :false-value="true" />
                                        <span class="oh-slider"></span>
                                    </label>
                                    <span class="oh-label">{{ day.label }}</span>
                                </div>
                                <div class="oh-times" v-if="!openingHours[day.key].closed">
                                    <div class="time-box">
                                        <input type="time" v-model="openingHours[day.key].open" class="time-input" />
                                    </div>
                                    <span class="oh-dash"><i class="fas fa-arrow-right"></i></span>
                                    <div class="time-box">
                                        <input type="time" v-model="openingHours[day.key].close" class="time-input" />
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
                            <div class="status-toggle-box" :class="form.is_published ? 'active' : 'draft'">
                                <div class="toggle-info">
                                    <strong>Status</strong>
                                    <span>{{ form.is_published ? 'Public (Published)' : 'Draft (Hidden)' }}</span>
                                </div>
                                <label class="switch">
                                    <input type="checkbox" v-model="form.is_published">
                                    <span class="slider round"></span>
                                </label>
                            </div>

                            <div class="btn-group-vertical">
                                <button type="submit" class="btn-submit-full" :disabled="isSaving">
                                    <i class="fas" :class="isSaving ? 'fa-spinner fa-spin' : 'fa-check-circle'"></i>
                                    {{ isSaving ? 'Saving...' : 'Save All Changes' }}
                                </button>
                                <button type="button" class="btn-cancel-full" @click="$router.push('/admin/places')">
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
import { ref, onMounted, nextTick, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { placeRepository } from '@/repositories/placeRepository'
import { categoryRepository } from '@/repositories/categoryRepository'

const route = useRoute()
const router = useRouter()
const categories = ref([])
const removingUrl = ref(null)

const predefinedBestFor = [
    'Hot Season', 'Rainy Season', 'Cool Season', 'All Seasons',
    'Photography', 'Nature', 'Spirituality', 'Relaxation', 'Family', 'Couples', 'Adventure', 'Food'
]
const predefinedAvoidIf = [
    'Rainy Season', 'Hot Season', 'Crowds', 'Inappropriate Attire', 'Mobility Issues', 'Noisy'
]

const map = ref(null)
const marker = ref(null)
const addressPaste = ref('')
const isSaving = ref(false)
const showBookingLinks = ref(false)

const weekDays = [
    { key: 'mon', label: 'Monday' },
    { key: 'tue', label: 'Tuesday' },
    { key: 'wed', label: 'Wednesday' },
    { key: 'thu', label: 'Thursday' },
    { key: 'fri', label: 'Friday' },
    { key: 'sat', label: 'Saturday' },
    { key: 'sun', label: 'Sunday' },
]

const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

const defaultDayHours = () => ({ open: '08:00', close: '17:00', closed: false })

const openingHours = ref({
    mon: defaultDayHours(),
    tue: defaultDayHours(),
    wed: defaultDayHours(),
    thu: defaultDayHours(),
    fri: defaultDayHours(),
    sat: defaultDayHours(),
    sun: defaultDayHours(),
})

const setAllClosed = (isClosed) => {
    weekDays.forEach(day => {
        openingHours.value[day.key].closed = isClosed
    })
}

const copyMondayToAll = () => {
    const mon = openingHours.value.mon
    weekDays.forEach(day => {
        if (day.key !== 'mon') {
            openingHours.value[day.key] = { ...mon }
        }
    })
}

// images = array ของ URL (เก่า) หรือ base64 (ใหม่) สำหรับโชว์เท่านั้น
const images = ref([])
// existingUrls = URL ของรูปเก่าที่อยู่บน server (string)
const existingUrls = ref([])
// newFiles = File object ที่เพิ่งเลือกใหม่ (File) พร้อม preview base64
const newFiles = ref([]) // [{ file: File, preview: string }]

const form = ref({
    name: '',
    category_id: 1,
    description: '',
    location_lat: 16.5662,
    location_lng: 104.7525,
    is_published: true,
    best_months: '',
    best_months_start: 'Nov',
    best_months_end: 'Feb',
    is_year_round: false,
    ideal_stay: '',
    daily_budget: '',
    budget_min: 150000,
    budget_max: 500000,
    is_free: false,
    location_name: '',
    best_for: [],
    avoid_if: [],
    booking_url: '',
    agoda_url: ''
})

const isHotelCategory = computed(() => {
    if (!form.value.category_id || !categories.value.length) return false
    const cat = categories.value.find(c => c.id === form.value.category_id)
    return cat && (cat.parent_type?.toLowerCase() === 'hotel' || cat.name.toLowerCase().includes('hotel'))
})

const addTag = (field, event) => {
    const val = event.target.value.trim()
    if (val && !form.value[field].includes(val)) {
        form.value[field].push(val)
        event.target.value = ''
    }
}

const removeTag = (field, index) => {
    if (form.value.is_published) return
    form.value[field].splice(index, 1)
}

const toggleTag = (field, tag) => {
    if (form.value.is_published) return
    const idx = form.value[field].indexOf(tag)
    if (idx === -1) {
        form.value[field].push(tag)
    } else {
        form.value[field].splice(idx, 1)
    }
}

// --- Parse image_url: ดึงข้อมูลจาก DB แล้วเติม localhost:8000 ให้อัตโนมัติ ---
const parseImages = (imageUrl) => {
    if (!imageUrl) return []
    
    let arr = []
    if (typeof imageUrl === 'string' && imageUrl.trim().startsWith('[')) {
        try { 
            arr = JSON.parse(imageUrl) 
        } catch { 
            arr = [imageUrl.replace(/^\["?|"?\]$/g, '').replace(/\\"/g, '')] 
        }
    } else {
        arr = [imageUrl]
    }

    return arr.map(url => {
        if (!url) return null;
        if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) {
            return url;
        }
        return `http://127.0.0.1:8000${url.startsWith('/') ? '' : '/'}${url}`;
    }).filter(Boolean);
}

watch(() => form.value.is_published, (newVal) => {
    if (marker.value) {
        if (newVal) marker.value.dragging.disable()
        else marker.value.dragging.enable()
    }
})

const initMap = () => {
    if (map.value) return;
    const lat = parseFloat(form.value.location_lat) || 16.5662
    const lng = parseFloat(form.value.location_lng) || 104.7525

    map.value = L.map('map-container', { zoomControl: false }).setView([lat, lng], 15)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map.value)
    L.control.zoom({ position: 'bottomright' }).addTo(map.value);

    marker.value = L.marker([lat, lng], { draggable: !form.value.is_published }).addTo(map.value)

    map.value.on('click', (e) => {
        if (!form.value.is_published) updateMarkerPosition(e.latlng.lat, e.latlng.lng)
    })

    marker.value.on('dragend', () => {
        const pos = marker.value.getLatLng()
        updateMarkerPosition(pos.lat, pos.lng)
    })
}

const handlePasteAddress = (e) => {
    const pasteData = e.clipboardData.getData('text')
    addressPaste.value = pasteData
    setTimeout(() => searchFromAddress(), 100)
}

const searchFromAddress = () => {
    if (!addressPaste.value) return

    const input = addressPaste.value.trim()

    // 1. ตรวจสอบว่าเป็นการวางลิงก์ Google Maps ที่มีพิกัด (เช่น /@16.5401,104.7570,15z)
    const urlMatch = input.match(/@(-?\d+\.\d+),(-?\d+\.\d+)/)
    
    // 2. ตรวจสอบว่าเป็นการวางพิกัดตรงๆ (เช่น 16.5401, 104.7570)
    const coordMatch = input.match(/^(-?\d+\.\d+)[\s,]+(-?\d+\.\d+)$/)

    let lat = null
    let lng = null

    if (urlMatch) {
        lat = parseFloat(urlMatch[1])
        lng = parseFloat(urlMatch[2])
    } else if (coordMatch) {
        lat = parseFloat(coordMatch[1])
        lng = parseFloat(coordMatch[2])
    }

    if (lat !== null && lng !== null) {
        map.value.setView([lat, lng], 17)
        updateMarkerPosition(lat, lng)
        return
    }

    // 3. Fallback ไปใช้ระบบค้นหาชื่อฟรีด้วย Nominatim (อาจจะไม่เจอชื่อที่เป๊ะแบบ Google Maps)
    const geocoder = L.Control.Geocoder.nominatim()
    geocoder.geocode(input, (results) => {
        if (results && results.length > 0) {
            const { center } = results[0]
            map.value.setView(center, 17)
            updateMarkerPosition(center.lat, center.lng)
        } else {
            alert('Location not found in free database.\n\nTip: Copy the whole Google Maps Link (URL) or exact coordinates (e.g., 16.540, 104.757) instead!')
        }
    })
}

const updateMarkerPosition = (lat, lng) => {
    const fixedLat = isNaN(lat) ? 16.5662 : parseFloat(parseFloat(lat).toFixed(6))
    const fixedLng = isNaN(lng) ? 104.7525 : parseFloat(parseFloat(lng).toFixed(6))
    if (marker.value) marker.value.setLatLng([fixedLat, fixedLng])
    form.value.location_lat = fixedLat
    form.value.location_lng = fixedLng
}

// --- Multi-image handlers ---
// images = existingUrls + newFiles preview (ใช้โชว์ใน UI)
const rebuildImages = () => {
    images.value = [
        ...existingUrls.value,
        ...newFiles.value.map(f => f.preview)
    ]
}

const onFileChange = (e) => {
    const files = Array.from(e.target.files)
    files.forEach(file => {
        if (images.value.length >= 10) return
        
        // เช็คขนาดไฟล์ (5MB)
        if (file.size > 5 * 1024 * 1024) {
            alert(`File ${file.name} is too large (Max 5MB).`)
            return
        }

        const reader = new FileReader()
        reader.onload = (ev) => {
            newFiles.value.push({ file, preview: ev.target.result })
            rebuildImages()
        }
        reader.readAsDataURL(file)
    })
    e.target.value = '' // reset
}

const removeImage = (index) => {
    const oldCount = existingUrls.value.length
    if (index < oldCount) {
        // ลบรูปเก่า (URL บน server)
        existingUrls.value.splice(index, 1)
    } else {
        // ลบรูปใหม่ (File ที่เพิ่งเลือก)
        newFiles.value.splice(index - oldCount, 1)
    }
    rebuildImages()
}

const setCover = (index) => {
    const oldCount = existingUrls.value.length
    if (index < oldCount) {
        // รูปเก่า: เลื่อน URL มาหน้า
        const [url] = existingUrls.value.splice(index, 1)
        existingUrls.value.unshift(url)
    } else {
        // รูปใหม่: เลื่อน File มาหน้า newFiles ก่อน
        const newIdx = index - oldCount
        const [entry] = newFiles.value.splice(newIdx, 1)
        newFiles.value.unshift(entry)
    }
    rebuildImages()
}

const fetchDetails = async () => {
    const id = route.params.id
    try {
        const [resPlace, resCats] = await Promise.all([
            placeRepository.getById(id),
            categoryRepository.getAll()
        ])
        const data = resPlace.data
        form.value = {
            ...data,
            location_lat: parseFloat(data.location_lat) || 16.5662,
            location_lng: parseFloat(data.location_lng) || 104.7525,
            is_published: !!data.is_published
        }
        
        // Auto-show booking links if they exist
        const hasBooking = data.booking_url && data.booking_url.trim().length > 0;
        const hasAgoda = data.agoda_url && data.agoda_url.trim().length > 0;
        if (hasBooking || hasAgoda) {
            showBookingLinks.value = true;
        }
        
        // Load opening hours if present
        if (data.opening_hours && typeof data.opening_hours === 'object') {
            weekDays.forEach(d => {
                if (data.opening_hours[d.key]) {
                    openingHours.value[d.key] = { ...defaultDayHours(), ...data.opening_hours[d.key] }
                }
            })
        }

        // Load premium details tags
        form.value.best_for = Array.isArray(data.best_for) ? data.best_for : []
        form.value.avoid_if = Array.isArray(data.avoid_if) ? data.avoid_if : []

        // Parse Best Months Range
        if (data.best_months === 'Year-round' || data.best_months === 'ตลอดทั้งปี') {
            form.value.is_year_round = true
        } else if (data.best_months && data.best_months.includes(' - ')) {
            const parts = data.best_months.split(' - ')
            if (parts.length === 2) {
                form.value.best_months_start = parts[0]
                form.value.best_months_end = parts[1]
                form.value.is_year_round = false
            }
        }

        // Parse Budget Range (e.g. ₭ 150k - 500k) or 'Free'
        if (data.daily_budget) {
            if (data.daily_budget === 'Free' || data.daily_budget?.toLowerCase().includes('free')) {
                form.value.is_free = true
            } else {
                const budgetStr = data.daily_budget.replace('₭ ', '')
                const parts = budgetStr.split(' - ')
                if (parts.length === 2) {
                    const min = parts[0].replace('k', '000').replace(/[^0-9]/g, '')
                    const max = parts[1].replace('k', '000').replace(/[^0-9]/g, '')
                    form.value.budget_min = parseInt(min) || 0
                    form.value.budget_max = parseInt(max) || 0
                    form.value.is_free = false
                }
            }
        }

        // โหลดรูปเก่ามาแสดง
        existingUrls.value = parseImages(data.image_url)
        newFiles.value = []
        rebuildImages() 

        categories.value = resCats.data
        await nextTick()
        initMap()
    } catch (error) {
        console.error("Error:", error)
    }
}

// --- บันทึกข้อมูลด้วย FormData (เหมือนหน้า Add) ---
const updatePlace = async () => {
    const id = route.params.id
    isSaving.value = true

    try {
        const formData = new FormData()
        formData.append('name', form.value.name)
        formData.append('description', form.value.description)
        formData.append('category_id', form.value.category_id)
        formData.append('is_published', form.value.is_published ? 1 : 0)
        formData.append('location_lat', form.value.location_lat)
        formData.append('location_lng', form.value.location_lng)

        formData.append('opening_hours', JSON.stringify(openingHours.value))

        // Premium Details
        const bestMonthsStr = form.value.is_year_round ? 'Year-round' : `${form.value.best_months_start} - ${form.value.best_months_end}`
        
        // Format budget as ₭ 100k - 300k style or just raw numbers
        const formatBudget = (val) => {
            if (!val) return '0'
            if (val >= 1000) return (val / 1000) + 'k'
            return val
        }
        const budgetStr = form.value.is_free ? 'Free' : `₭ ${formatBudget(form.value.budget_min)} - ${formatBudget(form.value.budget_max)}`

        formData.append('best_months', bestMonthsStr)
        formData.append('ideal_stay', form.value.ideal_stay || '')
        formData.append('daily_budget', budgetStr)
        formData.append('location_name', form.value.location_name || '')
        formData.append('best_for', JSON.stringify(form.value.best_for || []))
        formData.append('avoid_if', JSON.stringify(form.value.avoid_if || []))
        formData.append('booking_url', form.value.booking_url || '')
        formData.append('agoda_url', form.value.agoda_url || '')

        // ส่ง URL ของรูปเก่าที่ยังเหลืออยู่ให้ Backend รู้ว่าต้องเก็บรูปไหนไว้
        formData.append('existing_image_urls', JSON.stringify(existingUrls.value))

        // ส่งเฉพาะ File ใหม่ที่เพิ่งเลือก
        newFiles.value.forEach(({ file }) => {
            formData.append('images', file)
        })

        // ถ้าไม่มีรูปใหม่เลย จะส่งแค่ข้อมูลทั่วไป (FastAPI จะรู้ว่าไม่ต้องอัปเดตไฟล์)
        if (newFiles.value.length === 0) {
            // เราอาจจะต้องทำระบบส่งรูปเก่าไปบอก FastAPI ด้วย แต่ในเบื้องต้นส่งแค่นี้ก่อน
        }

        await placeRepository.update(id, formData)
        
        alert('✅ Saved successfully')
        router.push('/admin/places')
    } catch (error) {
        console.error("Update Error:", error)
        alert('❌ Failed to save. ' + (error.response?.data?.detail || ''))
    } finally {
        isSaving.value = false
    }
}

onMounted(fetchDetails)

// ══════════════════════════════════════════════
// 📖 TRAVEL GUIDE SECTIONS
// ══════════════════════════════════════════════
const sections = ref([])
const showAddSection = ref(false)
const isSavingSection = ref(false)

// New section state
const newSectionDesc = ref('')
const newSectionFile = ref(null)
const newSectionPreview = ref(null)

// Edit section state
const editingSectionId = ref(null)
const editSectionDesc = ref('')
const editSectionFile = ref(null)
const editSectionPreview = ref(null)

const expandedSection = ref(null)
const toggleExpandSection = (id) => {
    if (expandedSection.value === id) {
        expandedSection.value = null
    } else {
        expandedSection.value = id
    }
}

const getSectionImageUrl = (url) => {
    if (!url) return ''
    if (url.startsWith('http')) return url
    return `http://127.0.0.1:8000${url.startsWith('/') ? '' : '/'}${url}`
}

const fetchSections = async () => {
    const id = route.params.id
    try {
        const res = await placeRepository.getSections(id)
        sections.value = res.data
    } catch (e) {
        sections.value = []
    }
}

const onNewSectionImage = (e) => {
    const file = e.target.files[0]
    if (!file) return
    newSectionFile.value = file
    newSectionPreview.value = URL.createObjectURL(file)
    e.target.value = ''
}

const onEditSectionImage = (e) => {
    const file = e.target.files[0]
    if (!file) return
    editSectionFile.value = file
    editSectionPreview.value = URL.createObjectURL(file)
    e.target.value = ''
}

const addSection = async () => {
    const id = route.params.id
    isSavingSection.value = true
    try {
        const fd = new FormData()
        fd.append('description', newSectionDesc.value)
        fd.append('order_index', sections.value.length)
        if (newSectionFile.value) fd.append('image', newSectionFile.value)
        await placeRepository.addSection(id, fd)
        newSectionDesc.value = ''
        newSectionFile.value = null
        newSectionPreview.value = null
        showAddSection.value = false
        await fetchSections()
    } catch (e) {
        alert('❌ Failed to add section.')
    } finally {
        isSavingSection.value = false
    }
}

const startEditSection = (sec) => {
    editingSectionId.value = sec.id
    expandedSection.value = sec.id // Expand when editing
    editSectionDesc.value = sec.description || ''
    editSectionFile.value = null
    editSectionPreview.value = null
}

const cancelEditSection = () => {
    editingSectionId.value = null
    editSectionDesc.value = ''
    editSectionFile.value = null
    editSectionPreview.value = null
}

const saveEditSection = async (sectionId) => {
    const id = route.params.id
    isSavingSection.value = true
    try {
        const fd = new FormData()
        fd.append('description', editSectionDesc.value)
        if (editSectionFile.value) fd.append('image', editSectionFile.value)
        await placeRepository.updateSection(id, sectionId, fd)
        cancelEditSection()
        await fetchSections()
    } catch (e) {
        alert('❌ Failed to update section.')
    } finally {
        isSavingSection.value = false
    }
}

const deleteSection = async (sectionId) => {
    if (!confirm('Delete this section?')) return
    const id = route.params.id
    try {
        await placeRepository.deleteSection(id, sectionId)
        await fetchSections()
    } catch (e) {
        alert('❌ Failed to delete section.')
    }
}

const moveSectionUp = async (idx) => {
    if (idx === 0) return
    const id = route.params.id
    const sec = sections.value[idx]
    const prev = sections.value[idx - 1]
    try {
        const fd1 = new FormData(); fd1.append('order_index', idx - 1)
        const fd2 = new FormData(); fd2.append('order_index', idx)
        await Promise.all([
            placeRepository.updateSection(id, sec.id, fd1),
            placeRepository.updateSection(id, prev.id, fd2),
        ])
        await fetchSections()
    } catch (e) { console.error(e) }
}

const moveSectionDown = async (idx) => {
    if (idx === sections.value.length - 1) return
    const id = route.params.id
    const sec = sections.value[idx]
    const next = sections.value[idx + 1]
    try {
        const fd1 = new FormData(); fd1.append('order_index', idx + 1)
        const fd2 = new FormData(); fd2.append('order_index', idx)
        await Promise.all([
            placeRepository.updateSection(id, sec.id, fd1),
            placeRepository.updateSection(id, next.id, fd2),
        ])
        await fetchSections()
    } catch (e) { console.error(e) }
}

onMounted(fetchSections)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap');

.edit-page-container {
    background: #f1f5f9;
    min-height: 100vh;
    font-family: 'Kanit', sans-serif;
    color: #1e293b;
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

.card {
    background: white;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    margin-bottom: 25px;
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
.preset-tag:hover { background: #e2e8f0; }
.preset-tag.active { background: #dcfce7; color: #15803d; border-color: #22c55e; }
.preset-tag.alert.active { background: #fee2e2; color: #b91c1c; border-color: #ef4444; }

input, select, textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    outline: none;
    font-family: 'Kanit', sans-serif;
    box-sizing: border-box;
}

.map-wrapper-large {
    height: 600px;
    position: relative;
    border-radius: 0 0 20px 20px;
    overflow: hidden;
}

#map-container { height: 100%; width: 100%; }

.coords-display {
    margin-left: auto;
    font-size: 0.8rem;
    background: #e2e8f0;
    padding: 4px 12px;
    border-radius: 15px;
    display: flex;
    gap: 12px;
}

.map-overlay-locked {
    position: absolute;
    inset: 0;
    background: rgba(255, 255, 255, 0.4);
    z-index: 999;
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(1px);
}

.overlay-msg {
    background: #1e293b;
    color: white;
    padding: 10px 20px;
    border-radius: 30px;
    font-size: 0.9rem;
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

.gallery-item:hover .gallery-overlay { opacity: 1; }

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

.set-cover-btn { background: #f59e0b; color: white; }
.set-cover-btn:hover { background: #d97706; transform: scale(1.1); }

.delete-img-btn { background: #f43f5e; color: white; }
.delete-img-btn:hover { background: #e11d48; transform: scale(1.1); }

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

.gallery-add-btn i { font-size: 1.4rem; }

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

.upload-empty-state i { font-size: 2.5rem; }
.upload-empty-state p { margin: 0; font-weight: 500; }

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
    font-family: 'Kanit', sans-serif;
    transition: 0.2s;
}
.upload-first-btn:hover { background: #2563eb; }

.locked-hint { font-size: 0.85rem; color: #94a3b8; }

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
.status-toggle-box.active { background: #ecfdf5; border: 1px solid #a7f3d0; }
.status-toggle-box.draft  { background: #fff1f2; border: 1px solid #fecdd3; }

.btn-submit-full {
    background: #10b981;
    color: white;
    border: none;
    padding: 15px;
    border-radius: 12px;
    width: 100%;
    font-weight: 700;
    font-family: 'Kanit', sans-serif;
    cursor: pointer;
    transition: 0.2s;
}
.btn-submit-full:hover:not(:disabled) { background: #059669; }
.btn-submit-full:disabled { opacity: 0.7; cursor: not-allowed; }

.btn-cancel-full {
    background: white;
    border: 1px solid #cbd5e1;
    padding: 12px;
    border-radius: 12px;
    color: #64748b;
    cursor: pointer;
    margin-top: 10px;
    width: 100%;
    font-family: 'Kanit', sans-serif;
    transition: 0.2s;
}
.btn-cancel-full:hover { background: #f8fafc; }

.btn-group-vertical { display: flex; flex-direction: column; }

/* Switch Toggle */
.switch { position: relative; width: 50px; height: 26px; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider {
    position: absolute; cursor: pointer; inset: 0;
    background: #cbd5e1; transition: .4s; border-radius: 34px;
}
.slider:before {
    position: absolute; content: "";
    height: 18px; width: 18px;
    left: 4px; bottom: 4px;
    background: white; transition: .4s; border-radius: 50%;
}
input:checked + .slider { background: #10b981; }
input:checked + .slider:before { transform: translateX(24px); }

/* Lock badge */
.lock-badge {
    margin-left: auto;
    font-size: 0.78rem;
    background: #fff7ed;
    color: #c2410c;
    padding: 3px 10px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 5px;
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
    font-family: 'Kanit', sans-serif;
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
    gap: 12px;
    flex-shrink: 0;
}

.oh-label {
    font-weight: 700;
    font-size: 0.85rem;
    color: #1e293b;
    width: 80px;
}

.oh-row.is-closed .oh-label {
    color: #94a3b8;
}

.oh-times {
    display: flex;
    align-items: center;
    gap: 5px;
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
    font-family: 'Kanit', sans-serif;
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
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: #e2e8f0;
    transition: .4s;
    border-radius: 34px;
}
.oh-slider:before {
    position: absolute;
    content: "";
    height: 14px;
    width: 14px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.oh-switch input:checked + .oh-slider {
    background-color: #10b981;
}
.oh-switch input:checked + .oh-slider:before {
    transform: translateX(18px);
}

/* Common Toggle Switch Styles */
.switch {
  position: relative;
  display: inline-block;
  width: 46px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #cbd5e1;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
}

input:checked + .slider {
  background-color: #3b82f6;
}

input:checked + .slider:before {
  transform: translateX(22px);
}

.slider.round {
  border-radius: 24px;
}

.slider.round:before {
  border-radius: 50%;
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

.tag-input-container.disabled {
    background: #f8fafc;
    border-color: #e2e8f0;
    cursor: not-allowed;
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

/* ══════════════════════════════════════
   TRAVEL GUIDE SECTIONS CARD
══════════════════════════════════════ */
.sections-card { overflow: hidden; }

.sections-body { display: flex; flex-direction: column; gap: 14px; }

.sections-hint {
    font-size: 0.82rem;
    color: #64748b;
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    border-radius: 8px;
    padding: 8px 12px;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ---- Sections list ---- */
.sections-list { display: flex; flex-direction: column; gap: 10px; }

.section-item {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
    background: #fafafa;
    transition: box-shadow 0.2s;
}
.section-item.editing {
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12);
}

.section-item-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background: #f1f5f9;
    border-bottom: 1px solid #e2e8f0;
}
.section-number {
    font-size: 0.8rem;
    font-weight: 700;
    color: #6366f1;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.section-actions { display: flex; gap: 4px; }

.btn-sec-action {
    width: 28px;
    height: 28px;
    border: 1px solid #e2e8f0;
    background: white;
    border-radius: 6px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
    color: #64748b;
    transition: all 0.15s;
}
.btn-sec-action:hover:not(:disabled) { background: #f1f5f9; color: #1e293b; }
.btn-sec-action:disabled { opacity: 0.35; cursor: default; }
.btn-sec-action.edit:hover { background: #eff6ff; color: #3b82f6; border-color: #93c5fd; }
.btn-sec-action.danger:hover { background: #fef2f2; color: #dc2626; border-color: #fca5a5; }

/* ---- Preview ---- */
.section-preview { padding: 10px 12px; }
.section-preview-img {
    width: 100%;
    height: 120px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 8px;
    display: block;
}
.section-no-img {
    width: 100%;
    height: 80px;
    background: #f1f5f9;
    border: 2px dashed #cbd5e1;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #94a3b8;
    font-size: 0.85rem;
    gap: 6px;
    margin-bottom: 8px;
}
.section-preview-text {
    font-size: 0.83rem;
    color: #475569;
    margin: 0;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* ---- Edit / Add form ---- */
.section-edit-form { padding: 12px; display: flex; flex-direction: column; gap: 10px; }
.add-section-form {
    border: 2px dashed #c7d2fe;
    border-radius: 12px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    background: #fafafe;
}
.add-section-title {
    font-weight: 700;
    color: #6366f1;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Upload area */
.sec-upload-area {
    display: block;
    border: 2px dashed #cbd5e1;
    border-radius: 10px;
    overflow: hidden;
    cursor: pointer;
    transition: border-color 0.2s;
    min-height: 130px;
    position: relative;
}
.sec-upload-area:hover { border-color: #6366f1; }
.sec-upload-area.has-img { border-style: solid; border-color: #6366f1; }

.sec-upload-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 24px 16px;
    color: #94a3b8;
    font-size: 0.85rem;
    min-height: 130px;
}
.sec-upload-placeholder i { font-size: 1.8rem; color: #cbd5e1; }
.sec-upload-placeholder small { font-size: 0.75rem; color: #b8c4d2; }

.sec-upload-preview {
    width: 100%;
    height: 160px;
    object-fit: cover;
    display: block;
}
.sec-upload-existing {
    position: relative;
}
.sec-upload-existing span {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0,0,0,0.45);
    color: white;
    font-size: 0.85rem;
    font-weight: 600;
    opacity: 0;
    transition: opacity 0.2s;
}
.sec-upload-area:hover .sec-upload-existing span { opacity: 1; }

/* Textarea */
.sec-textarea {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-family: 'Kanit', sans-serif;
    font-size: 0.9rem;
    resize: vertical;
    min-height: 90px;
    box-sizing: border-box;
    line-height: 1.6;
    color: #1e293b;
    transition: border-color 0.2s;
}
.sec-textarea:focus { outline: none; border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }

.sec-edit-actions { display: flex; gap: 8px; }

.btn-sec-save {
    flex: 1;
    padding: 9px 16px;
    background: #6366f1;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 700;
    font-size: 0.88rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    transition: background 0.2s;
}
.btn-sec-save:hover:not(:disabled) { background: #4f46e5; }
.btn-sec-save:disabled { opacity: 0.6; cursor: default; }

.btn-sec-cancel {
    padding: 9px 14px;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.88rem;
    color: #64748b;
    font-weight: 600;
    transition: background 0.2s;
}
.btn-sec-cancel:hover { background: #f8fafc; }

/* Add Section button */
.btn-add-section {
    width: 100%;
    padding: 11px;
    background: white;
    border: 2px dashed #c7d2fe;
    border-radius: 10px;
    color: #6366f1;
    font-weight: 700;
    font-size: 0.9rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: all 0.2s;
    font-family: 'Kanit', sans-serif;
}
.btn-add-section:hover {
    background: #f0f0ff;
    border-color: #6366f1;
}

/* ══════════════════════════════════════
   NEW: GUIDE SECTIONS EDITOR (GSE)
   Inline professional accordion look
══════════════════════════════════════ */
.guide-sections-editor {
    margin-top: 25px;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    background: #ffffff;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.gse-header {
    background: #f8fafc;
    padding: 14px 20px;
    border-bottom: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.gse-title {
    font-weight: 700;
    color: #1e293b;
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    gap: 10px;
}

.gse-title i {
    color: #6366f1;
}

.gse-count {
    font-size: 0.75rem;
    background: #e0e7ff;
    color: #4338ca;
    padding: 2px 8px;
    border-radius: 999px;
    font-weight: 600;
}

.gse-list {
    display: flex;
    flex-direction: column;
}

.gse-item {
    border-bottom: 1px solid #f1f5f9;
    transition: all 0.2s;
}

.gse-item:last-child {
    border-bottom: none;
}

.gse-item.is-expanded {
    background: #fcfdfe;
}

.gse-item.is-editing {
    background: #f5f7ff;
}

/* Item Bar (Accordion Header) */
.gse-item-bar {
    padding: 12px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    user-select: none;
}

.gse-item-bar:hover {
    background: #f8fafc;
}

.gse-item-left {
    display: flex;
    align-items: center;
    gap: 15px;
    flex: 1;
    min-width: 0;
}

.gse-thumb-wrap {
    width: 48px;
    height: 48px;
    border-radius: 8px;
    overflow: hidden;
    background: #f1f5f9;
    flex-shrink: 0;
    border: 1px solid #e2e8f0;
}

.gse-thumb {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.gse-thumb-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #cbd5e1;
}

.gse-item-info {
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.gse-item-label {
    font-size: 0.85rem;
    font-weight: 700;
    color: #475569;
}

.gse-item-desc-preview {
    font-size: 0.8rem;
    color: #94a3b8;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.gse-item-right {
    display: flex;
    align-items: center;
    gap: 6px;
}

.gse-btn {
    width: 32px;
    height: 32px;
    border: 1px solid #e2e8f0;
    background: #fff;
    color: #64748b;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 0.8rem;
    transition: all 0.15s;
}

.gse-btn:hover:not(:disabled) {
    background: #f1f5f9;
    color: #1e293b;
    border-color: #cbd5e1;
}

.gse-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
}

.gse-btn.edit:hover {
    background: #eff6ff;
    color: #3b82f6;
    border-color: #93c5fd;
}

.gse-btn.danger:hover {
    background: #fef2f2;
    color: #dc2626;
    border-color: #fca5a5;
}

.gse-btn.chevron {
    border: none;
    background: transparent;
}

/* Expanded Bodies */
.gse-expand-body, .gse-edit-body {
    padding: 0 20px 20px 20px;
    animation: fadeInDown 0.3s ease-out;
}

.gse-full-img {
    width: 100%;
    max-height: 250px;
    object-fit: cover;
    border-radius: 12px;
    margin-bottom: 15px;
    border: 1px solid #e2e8f0;
}

.gse-no-img {
    width: 100%;
    height: 120px;
    background: #f8fafc;
    border: 2px dashed #e2e8f0;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #94a3b8;
    font-size: 0.9rem;
    gap: 10px;
    margin-bottom: 15px;
}

.gse-desc-text {
    font-size: 0.95rem;
    line-height: 1.6;
    color: #334155;
    white-space: pre-line;
    margin: 0;
}

/* Edit Body / Forms */
.gse-edit-body {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.gse-upload-area {
    display: block;
    width: 100%;
    height: 180px;
    border: 2px dashed #cbd5e1;
    border-radius: 12px;
    overflow: hidden;
    cursor: pointer;
    position: relative;
    transition: all 0.2s;
}

.gse-upload-area:hover {
    border-color: #6366f1;
    background: #f5f7ff;
}

.gse-upload-area.has-img {
    border-style: solid;
    border-color: #6366f1;
}

.gse-upload-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.gse-upload-existing-wrap {
    width: 100%;
    height: 100%;
    position: relative;
}

.gse-change-hint {
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.4);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    font-weight: 600;
    opacity: 0;
    transition: opacity 0.2s;
}

.gse-upload-area:hover .gse-change-hint {
    opacity: 1;
}

.gse-upload-ph {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    color: #94a3b8;
}

.gse-upload-ph i {
    font-size: 2rem;
    color: #cbd5e1;
}

.gse-upload-ph small {
    font-size: 0.75rem;
    opacity: 0.8;
}

.gse-textarea {
    width: 100%;
    padding: 15px;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    font-family: inherit;
    font-size: 0.95rem;
    line-height: 1.6;
    color: #1e293b;
    resize: vertical;
    min-height: 120px;
    box-sizing: border-box;
}

.gse-textarea:focus {
    outline: none;
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.gse-action-row {
    display: flex;
    gap: 12px;
}

.gse-save-btn {
    flex: 1;
    background: #6366f1;
    color: #fff;
    border: none;
    padding: 12px;
    border-radius: 10px;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    transition: background 0.2s;
}

.gse-save-btn:hover:not(:disabled) {
    background: #4f46e5;
}

.gse-save-btn:disabled {
    opacity: 0.7;
}

.gse-cancel-btn {
    padding: 12px 20px;
    background: #fff;
    border: 1px solid #e2e8f0;
    color: #64748b;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
}

.gse-cancel-btn:hover {
    background: #f8fafc;
    color: #1e293b;
}

/* Add Form Specifics */
.gse-add-form {
    padding: 20px;
    background: #fafafe;
    border-top: 1px solid #e2e8f0;
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.gse-add-title {
    font-weight: 700;
    color: #6366f1;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Add Trigger Button */
.gse-add-trigger {
    width: 100%;
    padding: 15px;
    background: #fff;
    border: none;
    color: #6366f1;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    border-top: 1px solid #f1f5f9;
    transition: all 0.2s;
}

.gse-add-trigger:hover {
    background: #f5f7ff;
    color: #4f46e5;
}

input:checked + .slider:before, input:checked + .oh-slider:before {
    transform: translateX(18px);
}

.label-with-action {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.year-round-toggle {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #6366f1;
    font-size: 0.8rem;
    cursor: pointer;
    font-weight: 600;
}

.year-round-toggle input {
    width: auto;
    cursor: pointer;
}
</style>
