<template>
  <div class="submit-page-container">
    <div class="header-section">
      <div class="header-content">
        <button
          class="btn-back-circle"
          @click="$router.back()"
          :title="t('submit.cancel')"
        >
          <i class="fas fa-arrow-left"></i>
        </button>
        <div class="title-group">
          <h1>
            {{ isEditMode ? t("submit.titleEdit") : t("submit.titleAdd") }}
          </h1>
          <p class="subtitle">
            {{
              isEditMode ? t("submit.subtitleEdit") : t("submit.subtitleAdd")
            }}
          </p>
        </div>
      </div>
    </div>

    <div class="main-layout">
      <!-- STATE 1: Need Permission -->
      <div v-if="permissionStatus === 'none'" class="permission-state-card">
        <div class="card permission-card">
          <div class="card-body">
            <i class="fas fa-lock-open permission-icon"></i>
            <h2>{{ t("submit.permissionTitle") }}</h2>
            <p>{{ t("submit.permissionDesc") }}</p>
            <button
              class="btn-request"
              @click="requestPermission"
              :disabled="isRequesting"
            >
              {{
                isRequesting ? t("submit.requesting") : t("submit.requestBtn")
              }}
            </button>
          </div>
        </div>
      </div>

      <!-- STATE 2: Pending Approval -->
      <div
        v-else-if="permissionStatus === 'pending'"
        class="permission-state-card"
      >
        <div class="card permission-card">
          <div class="card-body">
            <i class="fas fa-clock permission-icon pending"></i>
            <h2>{{ t("submit.waitingTitle") }}</h2>
            <p>{{ t("submit.waitingDesc") }}</p>
            <button class="btn-cancel" @click="$router.push('/')">
              {{ t("submit.returnHome") }}
            </button>
          </div>
        </div>
      </div>

      <!-- STATE 3: Approved Form -->
      <form
        v-else-if="permissionStatus === 'approved'"
        @submit.prevent="submitPlace"
        class="form-grid"
      >
        <div class="left-column">
          <div class="card info-card">
            <div class="card-header">
              <i class="fas fa-info-circle"></i>
              <span>{{ t("submit.generalInfo") }}</span>
            </div>
            <div class="card-body">
              <div class="input-row">
                <div class="input-group">
                  <label
                    >{{ t("submit.placeName") }}
                    <span class="text-danger">*</span></label
                  >
                  <input
                    v-model="form.name"
                    :placeholder="t('submit.namePlaceholder')"
                    required
                  />
                </div>
                <div class="input-group">
                  <label
                    >{{ t("submit.category") }}
                    <span class="text-danger">*</span></label
                  >
                  <select v-model="form.category_id" required>
                    <option value="" disabled>
                      {{ t("submit.selectCategory") }}
                    </option>
                    <option
                      v-for="cat in categories"
                      :key="cat.id"
                      :value="cat.id"
                    >
                      [{{
                        t(
                          "categories." + (cat.parent_type || "other"),
                        ).toUpperCase()
                      }}] {{ cat.name }}
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
                    <input type="checkbox" v-model="showBookingLinks" />
                    <span class="slider round"></span>
                  </label>
                  <span style="font-weight: 700; color: #0369a1">{{
                    t("submit.enableBooking")
                  }}</span>
                </div>
                <template v-if="showBookingLinks">
                  <div class="input-group" style="margin-bottom: 0">
                    <label style="color: #0369a1; font-weight: 700"
                      ><i class="fas fa-link"></i>
                      {{ t("submit.bookingUrl") }}</label
                    >
                    <input
                      v-model="form.booking_url"
                      placeholder="https://www.booking.com/hotel/..."
                    />
                  </div>
                  <div class="input-group" style="margin-bottom: 0">
                    <label style="color: #0369a1; font-weight: 700"
                      ><i class="fas fa-link"></i>
                      {{ t("submit.agodaUrl") }}</label
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
                  ><i class="fas fa-paste"></i>
                  {{ t("submit.pasteMap") }}</label
                >
                <div style="display: flex; gap: 10px">
                  <input
                    v-model="addressPaste"
                    @paste="handlePasteAddress"
                    :placeholder="t('submit.mapPlaceholder')"
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
                    {{ t("submit.detect") }}
                  </button>
                </div>
              </div>

              <div class="input-group">
                <label
                  >{{ t("submit.description") }}
                  <span class="text-danger">*</span></label
                >
                <textarea
                  v-model="form.description"
                  rows="4"
                  :placeholder="t('submit.descPlaceholder')"
                  required
                ></textarea>
              </div>

              <!-- ✨ Travel Guide Sections (Only in Edit Mode) -->
              <div v-if="isEditMode" class="guide-sections-editor">
                <div class="gse-header">
                  <span class="gse-title">
                    <i class="fas fa-book-open"></i>
                    {{ t("submit.guideSections") }}
                  </span>
                  <span class="gse-count" v-if="sections.length > 0">{{
                    t("submit.sectionCount", { count: sections.length })
                  }}</span>
                </div>

                <!-- Accordion list -->
                <div class="gse-list" v-if="sections.length > 0">
                  <div
                    v-for="(sec, idx) in sections"
                    :key="sec.id || idx"
                    class="gse-item"
                    :class="{
                      'is-expanded': expandedSection === sec.id,
                      'is-editing': editingSectionId === sec.id,
                    }"
                  >
                    <!-- Accordion header row -->
                    <div
                      class="gse-item-bar"
                      @click="toggleExpandSection(sec.id)"
                    >
                      <div class="gse-item-left">
                        <div class="gse-thumb-wrap">
                          <img
                            v-if="sec.image_url"
                            :src="getSectionImageUrl(sec.image_url)"
                            class="gse-thumb"
                          />
                          <div v-else class="gse-thumb-placeholder">
                            <i class="fas fa-image"></i>
                          </div>
                        </div>
                        <div class="gse-item-info">
                          <span class="gse-item-label"
                            >{{ t("submit.section") }} {{ idx + 1 }}</span
                          >
                          <span class="gse-item-desc-preview"
                            >{{
                              (sec.description || "").substring(0, 60) ||
                              t("submit.noDescription")
                            }}{{
                              (sec.description || "").length > 60 ? "..." : ""
                            }}</span
                          >
                        </div>
                      </div>
                      <div class="gse-item-right" @click.stop>
                        <button
                          type="button"
                          class="gse-btn"
                          @click="moveSectionUp(idx)"
                          :title="t('submit.moveUp')"
                        >
                          <i class="fas fa-arrow-up"></i>
                        </button>
                        <button
                          type="button"
                          class="gse-btn"
                          @click="moveSectionDown(idx)"
                          :title="t('submit.moveDown')"
                        >
                          <i class="fas fa-arrow-down"></i>
                        </button>
                        <button
                          type="button"
                          class="gse-btn edit"
                          @click="startEditSection(sec)"
                          :title="t('submit.edit')"
                        >
                          <i class="fas fa-pen"></i>
                        </button>
                        <button
                          type="button"
                          class="gse-btn danger"
                          @click="deleteSection(sec.id)"
                          :title="t('submit.delete')"
                        >
                          <i class="fas fa-trash"></i>
                        </button>
                        <button
                          type="button"
                          class="gse-btn chevron"
                          @click="toggleExpandSection(sec.id)"
                        >
                          <i
                            class="fas"
                            :class="
                              expandedSection === sec.id
                                ? 'fa-chevron-up'
                                : 'fa-chevron-down'
                            "
                          ></i>
                        </button>
                      </div>
                    </div>

                    <!-- Expanded: view mode -->
                    <div
                      v-if="
                        expandedSection === sec.id &&
                        editingSectionId !== sec.id
                      "
                      class="gse-expand-body"
                    >
                      <img
                        v-if="sec.image_url"
                        :src="getSectionImageUrl(sec.image_url)"
                        class="gse-full-img"
                      />
                      <div v-if="!sec.image_url" class="gse-no-img">
                        <i class="fas fa-image"></i>
                        {{ t("submit.noImageYet") }}
                      </div>
                      <p class="gse-desc-text">
                        {{ sec.description || t("submit.noDescription") }}
                      </p>
                    </div>

                    <!-- Expanded: edit mode -->
                    <div
                      v-if="editingSectionId === sec.id"
                      class="gse-edit-body"
                    >
                      <label
                        class="gse-upload-area"
                        :class="{
                          'has-img': editSectionPreview || sec.image_url,
                        }"
                      >
                        <img
                          v-if="editSectionPreview"
                          :src="editSectionPreview"
                          class="gse-upload-img"
                        />
                        <div
                          v-else-if="sec.image_url"
                          class="gse-upload-existing-wrap"
                        >
                          <img
                            :src="getSectionImageUrl(sec.image_url)"
                            class="gse-upload-img"
                          />
                          <span class="gse-change-hint"
                            ><i class="fas fa-camera"></i>
                            {{ t("submit.changeImage") }}</span
                          >
                        </div>
                        <div v-else class="gse-upload-ph">
                          <i class="fas fa-cloud-upload-alt"></i>
                          <span>{{ t("submit.uploadImage") }}</span>
                          <small>{{ t("submit.imgFormatHint") }}</small>
                        </div>
                        <input
                          type="file"
                          accept="image/*"
                          @change="onEditSectionImage"
                          hidden
                        />
                      </label>
                      <textarea
                        v-model="editSectionDesc"
                        rows="5"
                        :placeholder="t('submit.sectionPlaceholder')"
                        class="gse-textarea"
                      ></textarea>
                      <div class="gse-action-row">
                        <button
                          type="button"
                          class="gse-save-btn"
                          @click="saveEditSection(sec.id)"
                          :disabled="isSavingSection"
                        >
                          <i
                            class="fas"
                            :class="
                              isSavingSection
                                ? 'fa-spinner fa-spin'
                                : 'fa-check'
                            "
                          ></i>
                          {{
                            isSavingSection
                              ? t("submit.saving")
                              : t("submit.saveSection")
                          }}
                        </button>
                        <button
                          type="button"
                          class="gse-cancel-btn"
                          @click="cancelEditSection"
                        >
                          {{ t("submit.cancel") }}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Add new section inline form -->
                <div v-if="showAddSection" class="gse-add-form">
                  <div class="gse-add-title">
                    <i class="fas fa-plus-circle"></i>
                    {{ t("submit.newSection") }}
                  </div>
                  <label
                    class="gse-upload-area"
                    :class="{ 'has-img': newSectionPreview }"
                  >
                    <img
                      v-if="newSectionPreview"
                      :src="newSectionPreview"
                      class="gse-upload-img"
                    />
                    <div v-else class="gse-upload-ph">
                      <i class="fas fa-cloud-upload-alt"></i>
                      <span>{{ t("submit.uploadImage") }}</span>
                      <small>{{ t("submit.imgFormatHint") }}</small>
                    </div>
                    <input
                      type="file"
                      accept="image/*"
                      @change="onNewSectionImage"
                      hidden
                    />
                  </label>
                  <textarea
                    v-model="newSectionDesc"
                    rows="5"
                    :placeholder="t('submit.sectionPlaceholder')"
                    class="gse-textarea"
                  ></textarea>
                  <div class="gse-action-row">
                    <button
                      type="button"
                      class="gse-save-btn"
                      @click="addSection"
                      :disabled="isSavingSection"
                    >
                      <i
                        class="fas"
                        :class="
                          isSavingSection ? 'fa-spinner fa-spin' : 'fa-check'
                        "
                      ></i>
                      {{
                        isSavingSection
                          ? t("submit.adding")
                          : t("submit.addSection")
                      }}
                    </button>
                    <button
                      type="button"
                      class="gse-cancel-btn"
                      @click="
                        showAddSection = false;
                        newSectionPreview = null;
                        newSectionDesc = '';
                      "
                    >
                      {{ t("submit.cancel") }}
                    </button>
                  </div>
                </div>

                <!-- + Add Section trigger button -->
                <button
                  v-if="!showAddSection"
                  type="button"
                  class="gse-add-trigger"
                  @click="
                    showAddSection = true;
                    expandedSection = null;
                  "
                >
                  <i class="fas fa-plus"></i>
                  <span>{{ t("submit.addSection") }}</span>
                </button>
              </div>
              <div v-else class="sections-placeholder">
                <i class="fas fa-book-open"></i>
                <p>{{ t("submit.sectionsPlaceholder") }}</p>
              </div>
            </div>
          </div>

          <div class="card premium-details-card">
            <div class="card-header">
              <i class="fas fa-star"></i>
              <span>{{ t("submit.premiumDetails") }}</span>
            </div>
            <div class="card-body">
              <div class="input-row">
                <div class="input-group">
                  <label class="label-with-action">
                    <span>{{ t("submit.bestMonths") }}</span>
                    <label class="year-round-toggle">
                      <input type="checkbox" v-model="form.is_year_round" />
                      <span>{{ t("submit.yearRound") }}</span>
                    </label>
                  </label>
                  <div
                    v-if="!form.is_year_round"
                    class="month-range fade-in"
                    style="display: flex; gap: 10px; align-items: center"
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
                        {{ t("common." + m) }}
                      </option>
                    </select>
                    <span style="color: #94a3b8; font-weight: 600">{{
                      t("submit.to")
                    }}</span>
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
                        {{ t("common." + m) }}
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
                    {{ t("submit.yearRound") }}
                  </div>
                </div>
                <div class="input-group">
                  <label>{{ t("submit.idealStay") }}</label>
                  <input
                    v-model="form.ideal_stay"
                    :placeholder="t('submit.idealStayPlaceholder')"
                  />
                </div>
              </div>
              <div class="input-row">
                <div class="input-group">
                  <label class="label-with-action">
                    <span>{{ t("submit.dailyBudget") }}</span>
                    <label class="year-round-toggle">
                      <input type="checkbox" v-model="form.is_free" />
                      <span>{{ t("submit.free") }}</span>
                    </label>
                  </label>
                  <div
                    v-if="!form.is_free"
                    style="display: flex; gap: 10px; align-items: center"
                  >
                    <input
                      type="number"
                      v-model="form.budget_min"
                      :placeholder="t('submit.min')"
                    />
                    <span>-</span>
                    <input
                      type="number"
                      v-model="form.budget_max"
                      :placeholder="t('submit.max')"
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
                    <i class="fas fa-gift" style="margin-right: 8px"></i>
                    {{ t("submit.freeEntry") }}
                  </div>
                </div>
                <div class="input-group">
                  <label>{{ t("submit.locationName") }}</label>
                  <input
                    v-model="form.location_name"
                    :placeholder="t('submit.locationPlaceholder')"
                  />
                </div>
              </div>

              <div class="input-group">
                <label>{{ t("submit.bestFor") }}</label>
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
                    :placeholder="t('submit.tagPlaceholder')"
                  />
                </div>
              </div>

              <div class="input-group">
                <label>{{ t("submit.avoidIf") }}</label>
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
                    :placeholder="t('submit.tagPlaceholder')"
                  />
                </div>
              </div>
            </div>
          </div>

          <div class="card map-card">
            <div class="card-header">
              <i class="fas fa-map-marked-alt"></i>
              <span>{{ t("submit.mapLocation") }}</span>
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
              <span>{{ t("submit.placeImages") }}</span>
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
                    <i class="fas fa-star"></i> {{ t("submit.cover") }}
                  </div>

                  <div class="gallery-overlay">
                    <button
                      v-if="index !== 0"
                      type="button"
                      class="img-action-btn set-cover-btn"
                      @click="setCover(index)"
                      :title="t('submit.setCover')"
                    >
                      <i class="fas fa-star"></i>
                    </button>
                    <button
                      type="button"
                      class="img-action-btn delete-img-btn"
                      @click="removeImage(index)"
                      :title="t('submit.delete')"
                    >
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>

                <label v-if="images.length < 10" class="gallery-add-btn">
                  <i class="fas fa-plus"></i>
                  <span>{{ t("submit.add") }}</span>
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
                <p>{{ t("submit.noImages") }}</p>
                <label class="upload-first-btn">
                  <i class="fas fa-plus"></i> {{ t("submit.uploadImages") }}
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
                {{ t("submit.uploadHint") }}
              </p>
            </div>
          </div>

          <div class="card opening-hours-card">
            <div class="card-header">
              <i class="fas fa-clock"></i>
              <span>{{ t("submit.openingHours") }}</span>
              <div class="oh-actions">
                <button
                  type="button"
                  @click="setAllClosed(false)"
                  class="btn-oh-action"
                >
                  {{ t("submit.open") }}
                </button>
                <button
                  type="button"
                  @click="setAllClosed(true)"
                  class="btn-oh-action"
                >
                  {{ t("submit.close") }}
                </button>
                <button
                  type="button"
                  @click="copyMondayToAll"
                  class="btn-oh-action highlight"
                >
                  {{ t("submit.copyMon") }}
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
                  <span class="oh-label">{{ t("common." + day.key) }}</span>
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
                  <span class="oh-closed-badge">{{ t("submit.closed") }}</span>
                </div>
              </div>
            </div>
          </div>

          <div v-if="isEditMode" class="card status-card">
            <div class="card-header">
              <i class="fas fa-cog"></i> {{ t("submit.statusCard") }}
            </div>
            <div class="card-body">
              <div
                class="status-toggle-box"
                :class="form.is_published ? 'active' : 'draft'"
              >
                <div class="toggle-info">
                  <strong>{{ t("submit.statusLabel") }}</strong>
                  <span>{{
                    form.is_published
                      ? t("submit.statusPublic")
                      : t("submit.statusDraft")
                  }}</span>
                </div>
                <label class="switch">
                  <input type="checkbox" v-model="form.is_published" />
                  <span class="slider round"></span>
                </label>
              </div>

              <div
                v-if="isEditMode && form.status === 'pending'"
                class="status-note-pending"
              >
                <i class="fas fa-clock"></i> {{ t("submit.pendingNote") }}
              </div>

              <p class="info-note" v-if="!isEditMode">
                <i class="fas fa-shield-alt"></i> {{ t("submit.approvalNote") }}
              </p>

              <div class="btn-group-vertical">
                <button
                  type="submit"
                  class="btn-submit-full"
                  :disabled="isSaving"
                >
                  <i
                    class="fas"
                    :class="
                      isSaving
                        ? 'fa-spinner fa-spin'
                        : isEditMode
                          ? 'fa-save'
                          : 'fa-paper-plane'
                    "
                  ></i>
                  {{
                    isSaving
                      ? isEditMode
                        ? t("submit.updating")
                        : t("submit.submitting")
                      : isEditMode
                        ? t("submit.updateBtn")
                        : t("submit.submitBtn")
                  }}
                </button>
                <button
                  type="button"
                  class="btn-cancel-full"
                  @click="$router.push('/')"
                >
                  {{ t("submit.cancel") }}
                </button>
              </div>
            </div>
          </div>
          <div v-else class="card status-card">
            <div class="card-body">
              <div class="btn-group-vertical">
                <button
                  type="submit"
                  class="btn-submit-full"
                  :disabled="isSaving"
                >
                  <i
                    class="fas"
                    :class="isSaving ? 'fa-spinner fa-spin' : 'fa-paper-plane'"
                  ></i>
                  {{
                    isSaving ? t("submit.submitting") : t("submit.submitBtn")
                  }}
                </button>
                <button
                  type="button"
                  class="btn-cancel-full"
                  @click="$router.push('/')"
                >
                  {{ t("submit.cancel") }}
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
import { useRouter, useRoute } from "vue-router";
import { placeRepository } from "@/repositories/placeRepository";
import { categoryRepository } from "@/repositories/categoryRepository";
import { userRepository } from "@/repositories/userRepository";
import { useAuth } from "@/composables/useAuth";
import { useI18n } from "@/composables/useI18n";

const { t } = useI18n();
const router = useRouter();
const route = useRoute();
const { user, login } = useAuth();
const categories = ref([]);
const map = ref(null);
const marker = ref(null);
const addressPaste = ref("");
const isSaving = ref(false);
const isSavingSection = ref(false);

const permissionStatus = ref("loading");
const isRequesting = ref(false);

const sections = ref([]);
const showAddSection = ref(false);
const editingSectionId = ref(null);
const expandedSection = ref(null);

const newSectionDesc = ref("");
const newSectionFile = ref(null);
const newSectionPreview = ref(null);

const editSectionDesc = ref("");
const editSectionFile = ref(null);
const editSectionPreview = ref(null);

const images = ref([]);
const rawFiles = ref([]);

const isEditMode = computed(() => !!route.params.id);
const showBookingLinks = ref(false);

const months = [
  "jan",
  "feb",
  "mar",
  "apr",
  "may",
  "jun",
  "jul",
  "aug",
  "sep",
  "oct",
  "nov",
  "dec",
];

const form = ref({
  name: "",
  category_id: "",
  description: "",
  location_lat: 16.5662, // Savannakhet starting coordinates
  location_lng: 104.7525,
  best_months: "",
  best_months_start: "Nov",
  best_months_end: "Feb",
  is_year_round: false,
  ideal_stay: "",
  budget_min: 150000,
  budget_max: 500000,
  is_free: false,
  location_name: "",
  best_for: [],
  avoid_if: [],
  booking_url: "",
  agoda_url: "",
  is_published: true,
  status: "pending",
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

const weekDays = [
  { key: "mon", label: "mon" },
  { key: "tue", label: "tue" },
  { key: "wed", label: "wed" },
  { key: "thu", label: "thu" },
  { key: "fri", label: "fri" },
  { key: "sat", label: "sat" },
  { key: "sun", label: "sun" },
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
  const urlMatch = input.match(/@(-?\d+\.\d+),(-?\d+\.\d+)/);
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

  const geocoder = L.Control.Geocoder.nominatim();
  geocoder.geocode(input, (results) => {
    if (results && results.length > 0) {
      const { center } = results[0];
      map.value.setView(center, 17);
      updateMarkerPosition(center.lat, center.lng);
    } else {
      alert(
        t(
          "submit.errLocationNotFound",
          "Location not found. Try copying exact coordinates.",
        ),
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

const onFileChange = (e) => {
  const files = Array.from(e.target.files);
  files.forEach((file) => {
    if (images.value.length >= 10) return;

    if (file.size > 5 * 1024 * 1024) {
      alert(
        t(
          "submit.errFileTooLarge",
          `File ${file.name} is too large (Max 5MB).`,
        ).replace("{name}", file.name),
      );
      return;
    }

    rawFiles.value.push(file);

    const reader = new FileReader();
    reader.onload = (ev) => {
      images.value.push(ev.target.result);
    };
    reader.readAsDataURL(file);
  });
  e.target.value = "";
};

const removeImage = (index) => {
  images.value.splice(index, 1);
  rawFiles.value.splice(index, 1);
};

const setCover = (index) => {
  const [img] = images.value.splice(index, 1);
  images.value.unshift(img);

  const [file] = rawFiles.value.splice(index, 1);
  rawFiles.value.unshift(file);
};

const submitPlace = async () => {
  if (!form.value.name || !form.value.category_id || !form.value.description) {
    alert(
      t(
        "submit.errFillRequired",
        "Please fill in Name, Category, and Description.",
      ),
    );
    return;
  }

  if (!user.value || !user.value.id) {
    alert(
      t("submit.errMustBeLoggedIn", "You must be logged in to submit a place."),
    );
    router.push("/login");
    return;
  }

  isSaving.value = true;
  try {
    const formData = new FormData();
    formData.append("name", form.value.name);
    formData.append("description", form.value.description);
    formData.append("category_id", form.value.category_id);
    formData.append("location_lat", form.value.location_lat);
    formData.append("location_lng", form.value.location_lng);
    formData.append("user_id", user.value.id);
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
    formData.append("is_published", form.value.is_published ? 1 : 0);

    rawFiles.value.forEach((file) => {
      formData.append("images", file);
    });

    if (isEditMode.value) {
      await placeRepository.update(route.params.id, formData);
      alert(t("submit.successUpdate", "✅ Place updated successfully!"));
    } else {
      await placeRepository.submit(formData);
      alert(
        t(
          "submit.successSubmit",
          "🎉 Place submitted successfully! Waiting for admin approval.",
        ),
      );
    }

    router.push("/profile?tab=places");
  } catch (error) {
    console.error("Submit Error:", error);
    alert(t("submit.errSubmit", "❌ Failed to submit place."));
  } finally {
    isSaving.value = false;
  }
};

const requestPermission = async () => {
  isRequesting.value = true;
  try {
    await userRepository.requestPostPermission(user.value.id);
    permissionStatus.value = "pending";

    // Update local user state
    const updatedUser = { ...user.value, post_permission_status: "pending" };
    login(updatedUser, localStorage.getItem("access_token"));

    alert(
      t("submit.successPermission", "Permission request sent successfully!"),
    );
  } catch (error) {
    console.error(error);
    alert(t("submit.errPermission", "Failed to request permission."));
  } finally {
    isRequesting.value = false;
  }
};

onMounted(async () => {
  if (!user.value) {
    router.push("/login");
    return;
  }

  // Fetch fresh profile to get latest status
  try {
    const profileRes = await userRepository.getProfile(user.value.id);
    const profileData = profileRes.data;

    // Admins should always have approved status
    if (profileData.role === "admin") {
      permissionStatus.value = "approved";
    } else {
      permissionStatus.value = profileData.post_permission_status || "none";
    }

    // Update local context
    login(profileData, localStorage.getItem("access_token"));
  } catch (e) {
    console.error("Could not fetch user profile", e);
    // Check if user object already has admin role as fallback
    if (user.value && user.value.role === "admin") {
      permissionStatus.value = "approved";
    } else {
      permissionStatus.value = "none";
    }
  }

  if (permissionStatus.value === "approved" || isEditMode.value) {
    try {
      const res = await categoryRepository.getAll();
      categories.value = res.data;

      if (isEditMode.value) {
        await loadPlaceData();
      }

      await nextTick();
      initMap();
    } catch (error) {
      console.error("Failed to load categories:", error);
    }
  }
});

const loadPlaceData = async () => {
  try {
    const res = await placeRepository.getById(route.params.id);
    const p = res.data;

    form.value.name = p.name;
    form.value.category_id = p.category_id;
    form.value.description = p.description;
    form.value.location_lat = p.location_lat || 16.5662;
    form.value.location_lng = p.location_lng || 104.7525;
    form.value.location_name = p.location_name || "";
    form.value.ideal_stay = p.ideal_stay || "";
    form.value.booking_url = p.booking_url || "";
    form.value.agoda_url = p.agoda_url || "";
    form.value.is_published = !!p.is_published;
    form.value.status = p.status || "pending";
    form.value.best_for = Array.isArray(p.best_for) ? p.best_for : [];
    form.value.avoid_if = Array.isArray(p.avoid_if) ? p.avoid_if : [];

    if (p.best_months) {
      if (p.best_months === "Year-round") {
        form.value.is_year_round = true;
      } else {
        const parts = p.best_months.split(" - ");
        if (parts.length === 2) {
          form.value.best_months_start = parts[0];
          form.value.best_months_end = parts[1];
        }
      }
    }

    if (p.daily_budget) {
      if (
        p.daily_budget === "Free" ||
        p.daily_budget?.toLowerCase().includes("free")
      ) {
        form.value.is_free = true;
      } else {
        const match = p.daily_budget.match(/₭ (\d+k?) - (\d+k?)/);
        if (match) {
          const parseVal = (v) =>
            v.endsWith("k") ? parseInt(v) * 1000 : parseInt(v);
          form.value.budget_min = parseVal(match[1]);
          form.value.budget_max = parseVal(match[2]);
        }
      }
    }

    if (p.opening_hours) {
      Object.keys(p.opening_hours).forEach((day) => {
        if (openingHours.value[day]) {
          openingHours.value[day] = { ...p.opening_hours[day] };
        }
      });
    }

    if (p.image_url) {
      try {
        const imgUrls = JSON.parse(p.image_url);
        images.value = imgUrls.map((url) => `http://127.0.0.1:8000${url}`);
      } catch (e) {
        console.warn("Could not parse image_url", e);
      }
    }

    if (form.value.booking_url || form.value.agoda_url) {
      showBookingLinks.value = true;
    }

    await fetchSections();
  } catch (e) {
    console.error("Error loading place data:", e);
    alert("Failed to load place information.");
  }
};

// ══════════════════════════════════════════════
// 📖 TRAVEL GUIDE SECTIONS METHODS
// ══════════════════════════════════════════════
const fetchSections = async () => {
  const id = route.params.id;
  if (!id) return;
  try {
    const res = await placeRepository.getSections(id);
    sections.value = res.data;
  } catch (e) {
    sections.value = [];
  }
};

const getSectionImageUrl = (url) => {
  if (!url) return "";
  if (url.startsWith("http") || url.startsWith("data:")) return url;
  return `http://127.0.0.1:8000${url.startsWith("/") ? "" : "/"}${url}`;
};

const toggleExpandSection = (id) => {
  expandedSection.value = expandedSection.value === id ? null : id;
};

const onNewSectionImage = (e) => {
  const file = e.target.files[0];
  if (!file) return;
  newSectionFile.value = file;
  newSectionPreview.value = URL.createObjectURL(file);
  e.target.value = "";
};

const onEditSectionImage = (e) => {
  const file = e.target.files[0];
  if (!file) return;
  editSectionFile.value = file;
  editSectionPreview.value = URL.createObjectURL(file);
  e.target.value = "";
};

const addSection = async () => {
  const id = route.params.id;
  if (!id) return;
  isSavingSection.value = true;
  try {
    const fd = new FormData();
    fd.append("description", newSectionDesc.value);
    fd.append("order_index", sections.value.length);
    if (newSectionFile.value) fd.append("image", newSectionFile.value);
    await placeRepository.addSection(id, fd);
    newSectionDesc.value = "";
    newSectionFile.value = null;
    newSectionPreview.value = null;
    showAddSection.value = false;
    await fetchSections();
  } catch (e) {
    alert("❌ Failed to add section.");
  } finally {
    isSavingSection.value = false;
  }
};

const startEditSection = (sec) => {
  editingSectionId.value = sec.id;
  expandedSection.value = sec.id;
  editSectionDesc.value = sec.description || "";
  editSectionFile.value = null;
  editSectionPreview.value = null;
};

const cancelEditSection = () => {
  editingSectionId.value = null;
  editSectionDesc.value = "";
  editSectionFile.value = null;
  editSectionPreview.value = null;
};

const saveEditSection = async (sectionId) => {
  const id = route.params.id;
  isSavingSection.value = true;
  try {
    const fd = new FormData();
    fd.append("description", editSectionDesc.value);
    if (editSectionFile.value) fd.append("image", editSectionFile.value);
    await placeRepository.updateSection(id, sectionId, fd);
    cancelEditSection();
    await fetchSections();
  } catch (e) {
    alert("❌ Failed to update section.");
  } finally {
    isSavingSection.value = false;
  }
};

const deleteSection = async (sectionId) => {
  if (!confirm("Delete this section?")) return;
  const id = route.params.id;
  try {
    await placeRepository.deleteSection(id, sectionId);
    await fetchSections();
  } catch (e) {
    alert("❌ Failed to delete section.");
  }
};

const moveSectionUp = async (idx) => {
  if (idx === 0) return;
  const id = route.params.id;
  const sec = sections.value[idx];
  const prev = sections.value[idx - 1];
  try {
    const fd1 = new FormData();
    fd1.append("order_index", idx - 1);
    const fd2 = new FormData();
    fd2.append("order_index", idx);
    await Promise.all([
      placeRepository.updateSection(id, sec.id, fd1),
      placeRepository.updateSection(id, prev.id, fd2),
    ]);
    await fetchSections();
  } catch (e) {
    console.error(e);
  }
};

const moveSectionDown = async (idx) => {
  if (idx === sections.value.length - 1) return;
  const id = route.params.id;
  const sec = sections.value[idx];
  const next = sections.value[idx + 1];
  try {
    const fd1 = new FormData();
    fd1.append("order_index", idx + 1);
    const fd2 = new FormData();
    fd2.append("order_index", idx);
    await Promise.all([
      placeRepository.updateSection(id, sec.id, fd1),
      placeRepository.updateSection(id, next.id, fd2),
    ]);
    await fetchSections();
  } catch (e) {
    console.error(e);
  }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap");

.submit-page-container {
  background: #f1f5f9;
  min-height: 100vh;
  font-family: "Kanit", sans-serif;
  color: #1e293b;
  padding-bottom: 50px;
}

.text-danger {
  color: #e74c3c;
}

.header-section {
  background: white;
  padding: 20px 30px;
  border-bottom: 1px solid #e2e8f0;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 20px;
}

.btn-back-circle {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  border: 1px solid #e2e8f0;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1.1rem;
}

.btn-back-circle:hover {
  background: #f8fafc;
  color: #1e293b;
  border-color: #cbd5e1;
  transform: translateX(-3px);
}

.title-group h1 {
  font-size: 1.8rem;
  margin: 0 0 5px 0;
  color: #0f172a;
}

.subtitle {
  font-size: 1rem;
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
  overflow: hidden; /* Ensure content doesn't spill out */
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
  height: 400px;
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

.info-note {
  background: #eff6ff;
  color: #1e3a8a;
  padding: 15px;
  border-radius: 10px;
  font-size: 0.9rem;
  margin-bottom: 20px;
  border-left: 4px solid #3b82f6;
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
  font-size: 1.1rem;
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

/* Status Card */
.status-toggle-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px;
  border-radius: 12px;
  margin-bottom: 20px;
  transition: all 0.3s;
}

.status-toggle-box.active {
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
}

.status-toggle-box.draft {
  background: #fff1f2;
  border: 1px solid #fecdd3;
}

.toggle-info {
  display: flex;
  flex-direction: column;
}

.toggle-info strong {
  font-size: 0.95rem;
  color: #1e293b;
}

.toggle-info span {
  font-size: 0.8rem;
  color: #64748b;
}

.status-note-pending {
  background: #fffbeb;
  border: 1px solid #fef3c7;
  color: #92400e;
  padding: 12px;
  border-radius: 10px;
  font-size: 0.8rem;
  margin-bottom: 20px;
  display: flex;
  gap: 8px;
  line-height: 1.4;
}

.status-note-pending i {
  margin-top: 2px;
}

.btn-group-vertical {
  display: flex;
  flex-direction: column;
}

/* Premium Details Card */
.tag-input-container {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  padding: 10px;
}

.tag-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

.tag-pill {
  background: #eff6ff;
  color: #2563eb;
  padding: 4px 12px;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}

.tag-pill.alert {
  background: #fff1f2;
  color: #e11d48;
}

.tag-pill i {
  cursor: pointer;
  font-size: 0.75rem;
}

.tag-input-container input {
  border: none;
  background: transparent;
  padding: 5px;
  font-size: 0.9rem;
}

.tag-input-container input:focus {
  box-shadow: none;
}

/* Opening Hours Card */
.oh-actions {
  margin-left: auto;
  display: flex;
  gap: 8px;
}

.btn-oh-action {
  padding: 4px 10px;
  font-size: 0.75rem;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  background: white;
  cursor: pointer;
  font-weight: 600;
  color: #64748b;
  transition: 0.2s;
}

.btn-oh-action.highlight {
  background: #6366f1;
  color: white;
  border-color: #6366f1;
}

.oh-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;
}

.oh-row:last-child {
  border-bottom: none;
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

.oh-times {
  display: flex;
  align-items: center;
  gap: 5px;
}

.time-box {
  width: 95px;
}

.time-input {
  padding: 6px 5px;
  font-size: 0.8rem;
  text-align: center;
  border: 1px solid #e2e8f0;
}

.oh-dash {
  color: #94a3b8;
  font-size: 0.8rem;
}

.oh-closed-badge {
  background: #f1f5f9;
  color: #94a3b8;
  padding: 6px 20px;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
}

.is-closed .oh-label {
  color: #94a3b8;
}

/* Switch Styles */
.switch,
.oh-switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 22px;
}

.switch input,
.oh-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider,
.oh-slider {
  position: absolute;
  cursor: pointer;
  inset: 0;
  background-color: #cbd5e1;
  transition: 0.4s;
  border-radius: 34px;
}

.slider:before,
.oh-slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

input:checked + .slider,
input:checked + .oh-slider {
  background-color: #3b82f6;
}

input:checked + .slider:before,
input:checked + .oh-slider:before {
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

/* 📖 TRAVEL GUIDE SECTIONS EDITOR */
.guide-sections-editor {
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  background: #ffffff;
  overflow: hidden;
  margin-top: 20px;
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

.gse-expand-body,
.gse-edit-body {
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
  background: rgba(0, 0, 0, 0.4);
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

.sections-placeholder {
  padding: 30px;
  text-align: center;
  background: #f8fafc;
  border-radius: 16px;
  border: 2px dashed #e2e8f0;
  color: #94a3b8;
  margin-top: 20px;
}

.sections-placeholder i {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #cbd5e1;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Permission State Cards */
.permission-state-card {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
  animation: fadeInDown 0.5s ease-out;
}

.permission-card {
  max-width: 500px;
  width: 100%;
  text-align: center;
  padding: 20px;
  background: #ffffff;
  border-radius: 24px;
  box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(226, 232, 240, 0.8);
  position: relative;
  overflow: hidden;
}

.permission-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
}

.permission-card .card-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px 20px;
}

.permission-icon {
  font-size: 3.5rem;
  color: #3b82f6;
  margin-bottom: 20px;
  background: #eff6ff;
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.15);
}

.permission-icon.pending {
  color: #f59e0b;
  background: #fffbeb;
  box-shadow: 0 8px 20px rgba(245, 158, 11, 0.15);
}

.permission-card h2 {
  font-size: 1.6rem;
  color: #1e293b;
  margin-bottom: 12px;
  font-weight: 700;
}

.permission-card p {
  color: #64748b;
  font-size: 1.05rem;
  line-height: 1.6;
  margin-bottom: 30px;
}

.btn-request {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  padding: 14px 30px;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
  width: 100%;
  font-family: "Kanit", sans-serif;
}

.btn-request:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4);
}

.btn-request:disabled {
  background: #94a3b8;
  box-shadow: none;
  cursor: not-allowed;
  transform: none;
}

.btn-cancel {
  background: white;
  color: #64748b;
  border: 2px solid #e2e8f0;
  padding: 12px 30px;
  border-radius: 12px;
  font-size: 1.05rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  font-family: "Kanit", sans-serif;
}

.btn-cancel:hover {
  background: #f8fafc;
  color: #0f172a;
  border-color: #cbd5e1;
}
</style>
