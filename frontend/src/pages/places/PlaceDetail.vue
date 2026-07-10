<template>
  <div class="ta-detail-page">
    <!-- Removed standard Navbar for immersive experience -->

    <div v-if="place">
      <div class="premium-hero-wrapper">
        <header
          class="premium-hero"
          :style="{ backgroundImage: `url(${galleryImages[0]})` }"
        >
          <div class="hero-overlay"></div>

          <!-- Immersive Hero Navbar -->
          <nav class="hero-nav">
            <div class="nav-left">
              <div class="logo" @click="router.push('/')">
                <span class="logo-main">Savannakhet</span
                ><span class="logo-sub">.travel</span>
              </div>
            </div>
            <div class="nav-right">
              <div class="nav-items">
                <a @click="router.push('/landmarks')">{{
                  t("nav.destinations")
                }}</a>
                <a @click="router.push('/trip-planner')">{{
                  t("nav.tools")
                }}</a>
                <a @click="router.push('/hotels')">{{ t("nav.hotels") }}</a>
                <a @click="router.push('/nature')">{{ t("nav.nature") }}</a>
              </div>
              <button class="btn-plan" @click="router.push('/trip-planner')">
                {{ t("nav.planYourTrip") }}
              </button>
            </div>
          </nav>

          <div class="hero-content">
            <div class="top-row">
              <button @click="handleBack" class="btn-back-minimal">
                <i class="fas fa-chevron-left"></i>
              </button>
              <div class="breadcrumb">
                {{ t("nav.home") }} › {{ t("nav.destinations") }} ›
                {{ getCategoryName(place.category_id) }}
              </div>
            </div>

            <div class="hero-main-info">
              <h1 class="serif-title">{{ place.name }}</h1>
              <p class="local-name">{{ place.name_local || place.name }}</p>
              <p class="hero-description">{{ place.description }}</p>
            </div>

            <button
              v-if="!user || user.role !== 'admin'"
              class="floating-heart-main"
              :class="{ active: isFavorite }"
              @click="toggleHeart()"
            >
              <i class="fas fa-heart"></i>
              <span>{{ isFavorite ? t("place.saved") : t("place.save") }}</span>
            </button>
          </div>
        </header>

        <div
          class="stats-bar"
          v-if="
            place.best_months ||
            place.ideal_stay ||
            place.daily_budget ||
            place.location_name
          "
        >
          <div
            class="stat-item"
            v-if="place.best_months && !place.best_months.includes('undefined')"
          >
            <label>{{ t("place.best_months") }}</label>
            <div class="stat-value">
              {{
                place.best_months === "Year-round"
                  ? t("place.year_round")
                  : place.best_months
              }}
            </div>
          </div>
          <div class="stat-item" v-if="place.ideal_stay">
            <label>{{ t("place.ideal_stay") }}</label>
            <div class="stat-value">{{ place.ideal_stay }}</div>
          </div>
          <div
            class="stat-item"
            v-if="
              place.daily_budget &&
              place.daily_budget !== '₭ 0 - 0' &&
              !place.daily_budget.includes('undefined')
            "
          >
            <label>{{ t("place.daily_budget") }}</label>
            <div class="stat-value">
              {{ place.daily_budget }}
            </div>
          </div>
          <div class="stat-item" v-if="place.location_name">
            <label>{{ t("place.airport_location") }}</label>
            <div class="stat-value">{{ place.location_name }}</div>
          </div>
        </div>

        <div
          class="tags-container"
          v-if="
            (place.best_for && place.best_for.length > 0) ||
            (place.avoid_if && place.avoid_if.length > 0)
          "
        >
          <div
            class="tag-column best-for"
            v-if="place.best_for && place.best_for.length > 0"
          >
            <label>{{ t("place.best_for") }}</label>
            <div class="tag-list">
              <span
                v-for="(tag, idx) in place.best_for"
                :key="'bf-' + idx"
                class="tag"
                >{{ tag }}</span
              >
            </div>
          </div>
          <div
            class="tag-column avoid-if"
            v-if="place.avoid_if && place.avoid_if.length > 0"
          >
            <label>{{ t("place.avoid_if") }}</label>
            <div class="tag-list">
              <span
                v-for="(tag, idx) in place.avoid_if"
                :key="'ai-' + idx"
                class="tag"
                >{{ tag }}</span
              >
            </div>
          </div>
        </div>
      </div>

      <div class="ta-container">
        <div
          class="gallery-preview-strip"
          @click="openLightbox"
          v-if="galleryImages && galleryImages.length > 0"
        >
          <div
            v-for="(img, idx) in galleryImages.slice(0, 4)"
            :key="'strip-' + idx"
            class="strip-item"
          >
            <img :src="img" alt="Gallery preview" />
          </div>
          <div v-if="galleryImages.length > 4" class="more-indicator">
            +{{ galleryImages.length - 4 }}
          </div>
        </div>

        <div
          class="deals-banner"
          v-if="isHotel && (place.booking_url || place.agoda_url)"
          id="deals"
        >
          <div class="deals-banner-title">
            <i class="fas fa-tags"></i>
            <span>{{ t("place.checkPrices") }}</span>
          </div>
          <div class="deals-rows">
            <a
              v-if="place.booking_url"
              :href="place.booking_url"
              target="_blank"
              class="deals-row-item"
            >
              <div class="deals-row-brand">
                <span class="booking-text"
                  >Booking<span class="booking-dot">.</span>com</span
                >
              </div>
              <div class="deals-row-price">
                <span class="deals-price-main">{{
                  t("hotels.seePrices")
                }}</span>
              </div>
              <div class="deals-row-btn deals-btn-booking">
                {{ t("hotels.viewPartnerDeal") }}
                <i class="fas fa-external-link-alt"></i>
              </div>
            </a>

            <div
              class="deals-row-divider"
              v-if="place.booking_url && place.agoda_url"
            ></div>

            <a
              v-if="place.agoda_url"
              :href="place.agoda_url"
              target="_blank"
              class="deals-row-item"
            >
              <div class="deals-row-brand">
                <span class="agoda-text">agoda</span>
                <div class="agoda-dots-row">
                  <span style="background: #e91e8c"></span>
                  <span style="background: #f8a316"></span>
                  <span style="background: #4caf50"></span>
                  <span style="background: #2196f3"></span>
                  <span style="background: #e91e8c"></span>
                </div>
              </div>
              <div class="deals-row-price">
                <span class="deals-price-main">{{
                  t("hotels.seePrices")
                }}</span>
              </div>
              <div class="deals-row-btn deals-btn-agoda">
                {{ t("hotels.viewPartnerDeal") }}
                <i class="fas fa-external-link-alt"></i>
              </div>
            </a>
          </div>
          <p class="deals-disclaimer">
            <i class="fas fa-info-circle"></i>
            {{
              t("hotels.price_disclaimer") ||
              "Prices are approximate. Actual prices on partner site."
            }}
          </p>
        </div>

        <div class="sticky-nav-wrapper" ref="stickyNavRef">
          <div class="sticky-nav" :class="{ 'is-sticky': isSticky }">
            <div class="nav-links">
              <a
                v-if="isHotel"
                href="#deals"
                :class="{ active: activeSection === 'deals' }"
                @click.prevent="scrollTo('deals')"
                >{{ t("place.deals") }}</a
              >
              <a
                href="#about"
                :class="{ active: activeSection === 'about' }"
                @click.prevent="scrollTo('about')"
                >{{ t("place.about") }}</a
              >
              <a
                href="#location"
                :class="{ active: activeSection === 'location' }"
                @click.prevent="scrollTo('location')"
                >{{ t("place.location") }}</a
              >
              <a
                href="#reviews"
                :class="{ active: activeSection === 'reviews' }"
                @click.prevent="scrollTo('reviews')"
                >{{ t("place.reviews") }}</a
              >
            </div>
          </div>
        </div>

        <div class="content-split">
          <div class="main-column">
            <section
              class="about-section"
              id="about"
              style="
                background: white;
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 4px 25px rgba(0, 0, 0, 0.04);
                border: 1px solid #f1f5f9;
                margin-bottom: 30px;
              "
            >
              <h2
                style="
                  font-size: 1.6rem;
                  font-weight: 800;
                  margin-top: 0;
                  margin-bottom: 15px;
                  color: #0f172a;
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                "
              >
                <div style="display: flex; align-items: center; gap: 12px">
                  <div
                    style="
                      background: #eff6ff;
                      padding: 8px;
                      border-radius: 10px;
                      color: #3b82f6;
                      display: flex;
                      align-items: center;
                      justify-content: center;
                    "
                  >
                    <i class="fas fa-info-circle" style="font-size: 1.2rem"></i>
                  </div>
                  {{ t("place.aboutThisPlace") }}
                </div>

                <div style="display: flex; gap: 10px">
                  <button
                    v-if="
                      !isTranslatingAbout &&
                      !translatedAboutText &&
                      place.description
                    "
                    @click="translateAbout()"
                    class="btn-premium-translate"
                  >
                    <i
                      class="fas fa-language"
                      style="font-size: 1.1rem; color: #4f46e5"
                    ></i>
                    <span>{{
                      t("place.seeTranslation") !== "place.seeTranslation"
                        ? t("place.seeTranslation")
                        : "See Translation"
                    }}</span>
                  </button>
                  <span
                    v-if="isTranslatingAbout"
                    class="btn-premium-translate"
                    style="cursor: default"
                  >
                    <i
                      class="fas fa-circle-notch fa-spin"
                      style="color: #4f46e5"
                    ></i>
                    Translating...
                  </span>
                  <button
                    v-if="translatedAboutText"
                    @click="translatedAboutText = null"
                    class="btn-premium-translate active"
                  >
                    <i class="fas fa-undo"></i>
                    {{
                      t("place.showOriginal") !== "place.showOriginal"
                        ? t("place.showOriginal")
                        : "Original"
                    }}
                  </button>
                </div>
              </h2>

              <p
                class="description-text"
                @contextmenu.prevent="openTranslateMenu($event, 'about')"
                style="
                  font-size: 1.05rem;
                  line-height: 1.8;
                  color: #334155;
                  white-space: pre-line;
                  margin: 0;
                  cursor: context-menu;
                "
              >
                {{
                  translatedAboutText ||
                  place.description ||
                  "No description available for this place yet."
                }}
              </p>
            </section>

            <!-- ✨ Travel Guide Sections — Rich content blocks -->
            <section
              v-if="placeSections && placeSections.length > 0"
              class="guide-sections-block"
            >
              <div
                style="
                  display: flex;
                  justify-content: flex-end;
                  margin-bottom: 15px;
                  gap: 10px;
                "
              >
                <button
                  v-if="!isTranslatingSections && !translatedSectionsActive"
                  @click="translateSections()"
                  class="btn-premium-translate"
                >
                  <i
                    class="fas fa-language"
                    style="font-size: 1.1rem; color: #4f46e5"
                  ></i>
                  <span>{{
                    t("place.seeTranslation") !== "place.seeTranslation"
                      ? t("place.seeTranslation")
                      : "See Translation"
                  }}</span>
                </button>
                <span
                  v-if="isTranslatingSections"
                  class="btn-premium-translate"
                  style="cursor: default"
                >
                  <i
                    class="fas fa-circle-notch fa-spin"
                    style="color: #4f46e5"
                  ></i>
                  Translating...
                </span>
                <button
                  v-if="translatedSectionsActive"
                  @click="translatedSectionsActive = false"
                  class="btn-premium-translate active"
                >
                  <i class="fas fa-undo"></i>
                  {{
                    t("place.showOriginal") !== "place.showOriginal"
                      ? t("place.showOriginal")
                      : "Original"
                  }}
                </button>
              </div>

              <div
                v-for="(sec, idx) in placeSections"
                :key="sec.id"
                class="guide-section-item"
              >
                <img
                  v-if="sec.image_url"
                  :src="getSectionImageUrl(sec.image_url)"
                  :alt="`Section ${idx + 1}`"
                  class="guide-section-img"
                />
                <p
                  v-if="sec.description"
                  @contextmenu.prevent="openTranslateMenu($event, 'guide')"
                  style="cursor: context-menu"
                  class="guide-section-desc"
                >
                  {{
                    translatedSectionsActive && sec.translatedDesc
                      ? sec.translatedDesc
                      : sec.description
                  }}
                </p>
              </div>
            </section>

            <hr class="section-divider" />

            <section class="reviews-section" id="reviews">
              <h2>
                {{ t("place.travelerReviews") }} ({{ comments?.length || 0 }})
              </h2>

              <div
                class="write-review-box"
                v-if="user && user.role !== 'admin'"
              >
                <div
                  class="u-avatar-large"
                  style="
                    padding: 0;
                    overflow: hidden;
                    border: none;
                    background: none;
                  "
                >
                  <img
                    :src="getUserAvatar(user.profile_image)"
                    alt="avatar"
                    style="width: 100%; height: 100%; object-fit: cover"
                  />
                </div>
                <div class="review-input-area">
                  <p class="prompt-text">{{ t("place.whatDoYouThink") }}</p>
                  <div class="star-picker">
                    <i
                      v-for="star in 5"
                      :key="'picker-' + star"
                      :class="[newRating >= star ? 'fas' : 'far', 'fa-circle']"
                      @click="newRating = star"
                    ></i>
                    <span class="rating-label">{{
                      t("place.ratingLabels")[newRating - 1]
                    }}</span>
                  </div>
                  <textarea
                    v-model="newComment"
                    :placeholder="t('place.writeReviewPlaceholder')"
                  ></textarea>

                  <div class="review-images-upload">
                    <label class="btn-upload-photos">
                      <i class="fas fa-camera"></i> {{ t("nav.postPhoto") }}
                      <input
                        type="file"
                        multiple
                        accept="image/*"
                        @change="handleReviewImages"
                        hidden
                      />
                    </label>
                    <div
                      v-if="reviewImagesPreviews.length > 0"
                      class="previews-row"
                    >
                      <div
                        v-for="(src, idx) in reviewImagesPreviews"
                        :key="idx"
                        class="preview-item"
                      >
                        <img :src="src" />
                        <button
                          @click="removeReviewImage(idx)"
                          class="btn-remove-img"
                        >
                          ×
                        </button>
                      </div>
                    </div>
                  </div>

                  <div class="action-row">
                    <button
                      class="btn-submit"
                      @click="submitComment"
                      :disabled="submitting || !newComment.trim()"
                    >
                      {{
                        submitting
                          ? t("place.submitting")
                          : t("place.submitReviewBtn")
                      }}
                    </button>
                  </div>
                  <p v-if="reviewSuccess" class="success-msg">
                    <i class="fas fa-check-circle"></i>
                    {{ t("place.submitReviewSuccess") }}
                  </p>
                </div>
              </div>
              <div v-else-if="!user" class="login-prompt">
                <p>{{ t("place.pleaseLoginToReview") }}</p>
                <button
                  @click="router.push('/login')"
                  class="btn-login-outline"
                >
                  {{ t("nav.signIn") }}
                </button>
              </div>

              <div class="review-list">
                <div
                  v-if="!comments || comments.length === 0"
                  class="no-reviews"
                >
                  <i class="far fa-comment-alt"></i>
                  <p>{{ t("place.noReviewsYet") }}</p>
                </div>

                <div
                  v-for="comment in comments"
                  :key="comment.id"
                  class="review-item"
                >
                  <div class="reviewer-info">
                    <div
                      class="r-avatar"
                      style="
                        padding: 0;
                        overflow: hidden;
                        border: none;
                        background: none;
                      "
                    >
                      <img
                        :src="getUserAvatar(comment.profile_image)"
                        alt="avatar"
                        style="
                          width: 100%;
                          height: 100%;
                          object-fit: cover;
                          border-radius: 50%;
                        "
                      />
                    </div>
                    <div
                      class="r-details"
                      style="
                        flex-grow: 1;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                      "
                    >
                      <div>
                        <strong>{{ comment.username }}</strong>
                        <span class="r-date">{{
                          t("place.recentReview")
                        }}</span>
                      </div>
                      <div
                        class="review-actions"
                        v-if="user && user.username === comment.username"
                        style="position: relative"
                      >
                        <button
                          @click="toggleDropdown(comment.id)"
                          style="
                            background: none;
                            border: none;
                            cursor: pointer;
                            color: #64748b;
                            padding: 5px;
                            border-radius: 50%;
                            width: 30px;
                            height: 30px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            transition: background 0.2s;
                          "
                        >
                          <i class="fas fa-ellipsis-h"></i>
                        </button>
                        <div
                          v-if="showDropdownFor === comment.id"
                          style="
                            position: absolute;
                            right: 0;
                            top: 100%;
                            background: white;
                            border: 1px solid #e2e8f0;
                            border-radius: 8px;
                            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                            z-index: 10;
                            min-width: 120px;
                            overflow: hidden;
                          "
                        >
                          <button
                            @click="startEdit(comment)"
                            style="
                              display: block;
                              width: 100%;
                              text-align: left;
                              padding: 10px 15px;
                              background: none;
                              border: none;
                              cursor: pointer;
                              font-size: 0.9rem;
                              color: #1e293b;
                              transition: background 0.2s;
                            "
                          >
                            <i
                              class="fas fa-pen"
                              style="margin-right: 8px; color: #64748b"
                            ></i>
                            {{ t("common.edit") }}
                          </button>
                          <button
                            @click="deleteReview(comment.id)"
                            style="
                              display: block;
                              width: 100%;
                              text-align: left;
                              padding: 10px 15px;
                              background: none;
                              border: none;
                              cursor: pointer;
                              font-size: 0.9rem;
                              color: #ef4444;
                              transition: background 0.2s;
                            "
                          >
                            <i
                              class="fas fa-trash"
                              style="margin-right: 8px"
                            ></i>
                            {{ t("common.delete") }}
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="review-content">
                    <div
                      v-if="editingCommentId === comment.id"
                      class="edit-comment-area"
                      style="
                        margin-top: 10px;
                        background: #f8fafc;
                        padding: 15px;
                        border-radius: 12px;
                        border: 1px solid #e2e8f0;
                      "
                    >
                      <div class="star-picker" style="margin-bottom: 10px">
                        <i
                          v-for="star in 5"
                          :key="'edit-picker-' + star"
                          :class="[
                            editRating >= star ? 'fas' : 'far',
                            'fa-circle',
                          ]"
                          @click="editRating = star"
                          style="
                            cursor: pointer;
                            color: #f59e0b;
                            margin-right: 5px;
                          "
                        ></i>
                      </div>
                      <textarea
                        v-model="editCommentText"
                        style="
                          width: 100%;
                          padding: 10px;
                          border: 1px solid #cbd5e1;
                          border-radius: 8px;
                          resize: vertical;
                          min-height: 80px;
                          font-family: inherit;
                          font-size: 0.95rem;
                          margin-bottom: 10px;
                        "
                      ></textarea>
                      <div
                        style="
                          display: flex;
                          gap: 10px;
                          justify-content: flex-end;
                        "
                      >
                        <button
                          @click="cancelEdit"
                          style="
                            padding: 8px 16px;
                            background: white;
                            border: 1px solid #cbd5e1;
                            border-radius: 6px;
                            cursor: pointer;
                            color: #475569;
                            font-weight: 600;
                          "
                        >
                          {{ t("common.cancel") }}
                        </button>
                        <button
                          @click="saveEdit(comment.id)"
                          style="
                            padding: 8px 16px;
                            background: #3b82f6;
                            border: none;
                            border-radius: 6px;
                            cursor: pointer;
                            color: white;
                            font-weight: 600;
                          "
                        >
                          {{ t("common.save") }}
                        </button>
                      </div>
                    </div>
                    <div v-else>
                      <div class="rating-bubbles small">
                        <i
                          v-for="s in 5"
                          :key="'rev-' + comment.id + '-' + s"
                          :class="[
                            comment.rating >= s ? 'fas' : 'far',
                            'fa-circle',
                          ]"
                        ></i>
                      </div>
                      <p class="r-text">{{ comment.comment_text }}</p>

                      <div
                        v-if="comment.images && comment.images.length > 0"
                        class="comment-images-grid"
                      >
                        <img
                          v-for="(img, idx) in comment.images"
                          :key="idx"
                          :src="getImageUrl(img)"
                          @click="openLightboxWith(comment.images, idx)"
                        />
                      </div>

                      <div class="comment-footer">
                        <button
                          class="btn-like-small"
                          :class="{ active: isLiked(comment) }"
                          @click="handleLike(comment)"
                        >
                          <i
                            :class="[
                              isLiked(comment) ? 'fas' : 'far',
                              'fa-heart',
                            ]"
                          ></i>
                          {{ comment.liked_by?.length || 0 }}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>

          <div class="sidebar-column">
            <div
              class="sidebar-card place-summary-card"
              style="
                background: white;
                padding: 25px;
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
                border: 1px solid #f1f5f9;
                margin-bottom: 20px;
              "
            >
              <h3
                style="
                  font-size: 1.1rem;
                  font-weight: 800;
                  margin: 0 0 16px;
                  color: #1e293b;
                  display: flex;
                  align-items: center;
                  gap: 8px;
                "
              >
                <i class="fas fa-list-ul" style="color: #6366f1"></i>
                {{ t("place.quick_details") }}
              </h3>
              <div
                class="place-summary-meta"
                style="
                  display: flex;
                  flex-direction: column;
                  gap: 12px;
                  font-size: 0.95rem;
                  color: #475569;
                "
              >
                <span
                  style="
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    border-bottom: 1px dashed #e2e8f0;
                    padding-bottom: 8px;
                  "
                >
                  <span style="display: flex; align-items: center; gap: 8px"
                    ><i
                      class="fas fa-tag"
                      style="color: #3b82f6; width: 16px; text-align: center"
                    ></i>
                    <strong>{{ t("place.category_label") }}</strong></span
                  >
                  <span
                    style="
                      font-weight: 600;
                      color: #0f172a;
                      background: #f1f5f9;
                      padding: 2px 8px;
                      border-radius: 6px;
                      font-size: 0.85rem;
                    "
                    >{{ getCategoryName(place.category_id) }}</span
                  >
                </span>
                <span
                  style="
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                  "
                >
                  <span style="display: flex; align-items: center; gap: 8px"
                    ><i
                      class="fas fa-star"
                      style="color: #eab308; width: 16px; text-align: center"
                    ></i>
                    <strong>{{ t("place.rating_label") }}</strong></span
                  >
                  <span
                    style="
                      font-weight: 700;
                      color: #00aa6c;
                      display: flex;
                      align-items: center;
                      gap: 4px;
                    "
                  >
                    {{
                      place.rating_avg
                        ? parseFloat(place.rating_avg).toFixed(1)
                        : "0.0"
                    }}
                  </span>
                </span>
              </div>
            </div>

            <div class="sidebar-card opening-hours-card">
              <h3
                style="
                  font-size: 1rem;
                  font-weight: 800;
                  margin: 0 0 16px;
                  color: #1e293b;
                "
              >
                {{ t("place.openingHours") || "Opening Hours" }}
              </h3>
              <div
                class="opening-hours-list"
                v-if="openingHoursList && openingHoursList.length"
              >
                <div
                  v-for="day in openingHoursList"
                  :key="day.key"
                  class="opening-hours-row"
                >
                  <span>{{ day.label }}</span>
                  <span
                    :class="['opening-hours-value', { closed: day.closed }]"
                  >
                    {{
                      day.closed
                        ? t("place.closed") || "Closed"
                        : `${day.open} - ${day.close}`
                    }}
                  </span>
                </div>
              </div>
              <p v-else class="no-opening-hours">
                {{ t("place.noOpeningHours") || "No opening hours available." }}
              </p>
            </div>

            <div class="sidebar-card rating-summary-card">
              <h3
                style="
                  font-size: 1rem;
                  font-weight: 800;
                  margin: 0 0 16px;
                  color: #1e293b;
                "
              >
                {{ t("place.travelerReviews") }}
              </h3>
              <div class="rating-overview">
                <div class="big-score">
                  <span class="score-number">{{
                    place.rating_avg
                      ? parseFloat(place.rating_avg).toFixed(1)
                      : "0.0"
                  }}</span>
                  <div class="score-bubbles">
                    <i
                      v-for="s in 5"
                      :key="'sb-' + s"
                      :class="[
                        (place.rating_avg || 0) >= s ? 'fas' : 'far',
                        'fa-circle',
                      ]"
                    ></i>
                  </div>
                  <span class="score-label">{{
                    t("place.ratingLabels")[
                      Math.round(place.rating_avg || 0) - 1
                    ] || "0.0"
                  }}</span>
                  <span class="score-count">({{ comments?.length || 0 }})</span>
                </div>
                <div class="score-bars">
                  <div
                    v-for="lvl in ratingBreakdown"
                    :key="lvl.value"
                    class="score-bar-row"
                  >
                    <span class="bar-label">{{
                      t("place.ratingLabels")[lvl.value - 1]
                    }}</span>
                    <div class="bar-track">
                      <div
                        class="bar-fill"
                        :style="{ width: lvl.percent + '%' }"
                      ></div>
                    </div>
                    <span class="bar-count">{{ lvl.count }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <SectionDivider icon="fas fa-map-marked-alt" />

        <div class="large-map-section" id="location">
          <div
            style="
              display: flex;
              justify-content: space-between;
              align-items: flex-end;
              margin-bottom: 20px;
            "
          >
            <div>
              <h2>{{ t("place.location") }}</h2>
              <p class="map-address" style="margin: 0">
                <i class="fas fa-map-marker-alt"></i> {{ addressText }}
              </p>
            </div>
            <button class="btn-action" @click="showMapModal = true">
              <i class="fas fa-external-link-alt"></i>
              {{ t("place.viewOnMap") }}
            </button>
          </div>
          <div
            class="large-map-container"
            v-if="place.location_lat && place.location_lng"
          >
            <div
              id="detail-map"
              style="
                width: 100%;
                height: 450px;
                border-radius: 12px;
                z-index: 1;
                border: 1px solid #e2e8f0;
                overflow: hidden;
              "
            ></div>
          </div>
        </div>

        <div
          class="nearby-section"
          v-if="
            (nearbyRestaurants && nearbyRestaurants.length > 0) ||
            (nearbyAttractions && nearbyAttractions.length > 0)
          "
        >
          <div class="nearby-grid">
            <div class="nearby-col getting-there-col">
              <h3>{{ t("place.gettingThere") }}</h3>
              <div class="walk-score-box">
                <div class="score-text">
                  <span class="score-title"
                    >{{ t("place.somewhatWalkable") }}
                    <i class="fas fa-info-circle"></i
                  ></span>
                  <span class="score-desc"
                    >{{ t("place.grade") }}: 64 {{ t("place.outOf") }} 100</span
                  >
                </div>
                <div class="score-number">64</div>
              </div>
              <div class="airport-info">
                <p>
                  <i class="fas fa-plane"></i>
                  <strong>Savannakhet Airport</strong>
                </p>
                <span class="distance-line"
                  ><i class="fas fa-car side-icon"></i> 1.2 miles</span
                >
              </div>
            </div>

            <div class="nearby-col">
              <div class="col-header">
                <div>
                  <h3>
                    {{ nearbyRestaurantsTotal }} {{ t("place.restaurants") }}
                  </h3>
                  <span>{{ t("place.within") }} 10 km</span>
                </div>
                <button class="btn-text-link" @click="openMapOverlay">
                  {{ t("common.viewOnMap") }}
                </button>
              </div>

              <div class="nearby-list">
                <div
                  v-for="n in nearbyRestaurants"
                  :key="n.id"
                  class="nearby-item"
                  @click="goToRecDetail(n.id)"
                >
                  <h4>{{ n.name }}</h4>
                  <div class="n-rating">
                    <span class="n-score">{{ n.rating_avg || "0.0" }}</span>
                    <div class="bubbles">
                      <i
                        v-for="s in 5"
                        :key="s"
                        :class="[
                          (n.rating_avg || 0) >= s ? 'fas' : 'far',
                          'fa-circle',
                        ]"
                      ></i>
                    </div>
                    <span class="n-reviews"
                      >({{ getCommentCountText(n) }}
                      {{ t("common.reviews") }})</span
                    >
                  </div>
                  <div class="n-meta">
                    <i class="fas fa-walking"></i>
                    {{ getDistanceText(n._distance) }}
                    <span class="dot-divider">•</span> $$ - $$$
                    <span class="dot-divider">•</span>
                    {{ getCategoryName(n.category_id) }}
                  </div>
                </div>
              </div>
            </div>

            <div class="nearby-col right-col">
              <div class="col-header">
                <div>
                  <h3>
                    {{ nearbyAttractionsTotal }} {{ t("place.attractions") }}
                  </h3>
                  <span>{{ t("place.within") }} 10 km</span>
                </div>
                <button class="btn-text-link" @click="openMapOverlay">
                  {{ t("common.viewOnMap") }}
                </button>
              </div>

              <div class="nearby-list">
                <div
                  v-for="n in nearbyAttractions"
                  :key="n.id"
                  class="nearby-item"
                  @click="goToRecDetail(n.id)"
                >
                  <h4>{{ n.name }}</h4>
                  <div class="n-rating">
                    <span class="n-score">{{ n.rating_avg || "0.0" }}</span>
                    <div class="bubbles">
                      <i
                        v-for="s in 5"
                        :key="s"
                        :class="[
                          (n.rating_avg || 0) >= s ? 'fas' : 'far',
                          'fa-circle',
                        ]"
                      ></i>
                    </div>
                    <span class="n-reviews"
                      >({{ getCommentCountText(n) }}
                      {{ t("common.reviews") }})</span
                    >
                  </div>
                  <div class="n-meta">
                    <i class="fas fa-walking"></i>
                    {{ getDistanceText(n._distance) }}
                    <span class="dot-divider">•</span>
                    {{ getCategoryName(n.category_id) }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- AI Recommendations (✨ AI Recommended) -->
        <div
          class="recommended-section"
          v-if="aiRecommendedPlaces && aiRecommendedPlaces.length > 0"
        >
          <div class="section-header-modern">
            <div class="sh-left">
              <span class="sh-badge">{{ t("recommend.hero_badge") }}</span>
              <h2 class="sh-title">{{ t("recommend.ai_recom") }}</h2>
              <p class="sh-subtitle">{{ t("recommend.ai_desc") }}</p>
            </div>
          </div>

          <div class="recommended-grid-modern">
            <div
              v-for="rec in aiRecommendedPlaces"
              :key="rec.place.id"
              class="modern-immersive-card"
              @click="goToRecDetail(rec.place.id)"
            >
              <img
                :src="getRecCoverImage(rec.place)"
                :alt="rec.place.name"
                class="mic-image"
              />

              <div
                class="mic-heart"
                :class="{ active: favoriteIds.includes(rec.place.id) }"
                @click.stop="toggleHeart(rec.place.id)"
              >
                <i
                  :class="
                    favoriteIds.includes(rec.place.id)
                      ? 'fas fa-heart'
                      : 'far fa-heart'
                  "
                ></i>
              </div>

              <div class="mic-overlay">
                <span class="mic-category">{{
                  rec.place.category?.name || t("place.category_label")
                }}</span>
                <h4 class="mic-title">{{ rec.place.name }}</h4>
                <div class="mic-rating">
                  <i class="fas fa-star"></i>
                  <span>{{ rec.place.rating_avg || "0.0" }}</span>
                  <span
                    style="opacity: 0.7; font-size: 0.75rem; margin-left: 4px"
                    >({{ rec.place.reviews_count || 0 }})</span
                  >
                </div>

                <div class="mic-footer">
                  <div class="mic-verified">
                    <i class="fas fa-certificate"></i>
                    <span>{{ t("landmarks.verified") }}</span>
                  </div>
                  <div class="mic-action">
                    {{ t("landmarks.openGuide") }}
                    <i class="fas fa-arrow-right"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Similar Places Section -->
        <div
          class="recommended-section"
          v-if="similarPlaces && similarPlaces.length > 0"
        >
          <div class="section-header-modern">
            <div class="sh-left">
              <h2 class="sh-title">{{ t("recommend.similar") }}</h2>
            </div>
          </div>

          <div class="recommended-grid-modern">
            <div
              v-for="rec in similarPlaces"
              :key="rec.place.id"
              class="modern-immersive-card"
              @click="goToRecDetail(rec.place.id)"
            >
              <img
                :src="getRecCoverImage(rec.place)"
                :alt="rec.place.name"
                class="mic-image"
              />

              <div
                class="mic-heart"
                :class="{ active: favoriteIds.includes(rec.place.id) }"
                @click.stop="toggleHeart(rec.place.id)"
              >
                <i
                  :class="
                    favoriteIds.includes(rec.place.id)
                      ? 'fas fa-heart'
                      : 'far fa-heart'
                  "
                ></i>
              </div>

              <div class="mic-overlay">
                <span class="mic-category">{{
                  rec.place.category?.name || t("place.category_label")
                }}</span>
                <h4 class="mic-title">{{ rec.place.name }}</h4>
                <div class="mic-rating">
                  <i class="fas fa-star"></i>
                  <span>{{ rec.place.rating_avg || "0.0" }}</span>
                </div>

                <div class="mic-footer">
                  <div class="mic-verified">
                    <i class="fas fa-certificate"></i>
                    <span>{{ t("landmarks.verified") }}</span>
                  </div>
                  <div class="mic-action">
                    {{ t("landmarks.openGuide") }}
                    <i class="fas fa-arrow-right"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Fallback Recommendations -->
        <div
          class="recommended-section"
          v-else-if="recommendedPlaces && recommendedPlaces.length > 0"
        >
          <div class="section-header-modern">
            <div class="sh-left">
              <h2 class="sh-title">{{ t("place.recommended") }}</h2>
            </div>
          </div>

          <div class="recommended-grid-modern">
            <div
              v-for="rec in recommendedPlaces"
              :key="rec.id"
              class="modern-immersive-card"
              @click="goToRecDetail(rec.id)"
            >
              <img
                :src="getRecCoverImage(rec)"
                :alt="rec.name"
                class="mic-image"
              />

              <div
                class="mic-heart"
                :class="{ active: favoriteIds.includes(rec.id) }"
                @click.stop="toggleHeart(rec.id)"
              >
                <i
                  :class="
                    favoriteIds.includes(rec.id)
                      ? 'fas fa-heart'
                      : 'far fa-heart'
                  "
                ></i>
              </div>

              <div class="mic-overlay">
                <span class="mic-category">{{
                  rec.category?.name || t("place.category_label")
                }}</span>
                <h4 class="mic-title">{{ rec.name }}</h4>
                <div class="mic-rating">
                  <i class="fas fa-star"></i>
                  <span>{{ rec.rating_avg || "0.0" }}</span>
                </div>

                <div class="mic-footer">
                  <div class="mic-verified">
                    <i class="fas fa-certificate"></i>
                    <span>{{ t("landmarks.verified") }}</span>
                  </div>
                  <div class="mic-action">
                    {{ t("landmarks.openGuide") }}
                    <i class="fas fa-arrow-right"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="loading-screen">
      <div class="spinner"></div>
      <p>{{ t("common.loading") }}</p>
    </div>

    <div
      v-if="isLightboxOpen"
      class="lightbox-overlay"
      @click="closeLightbox"
      @wheel.prevent="handleScrollZoom"
    >
      <button class="btn-close-lightbox" @click="closeLightbox">
        <i class="fas fa-times"></i>
      </button>
      <button
        v-if="!user || user.role !== 'admin'"
        class="lightbox-heart-btn"
        :class="{ active: isFavorite }"
        @click.stop="toggleHeart()"
      >
        <i class="fas fa-heart"></i>
      </button>
      <button
        v-if="activeLightboxImages.length > 1"
        class="btn-nav prev"
        @click.stop="prevImage"
      >
        <i class="fas fa-chevron-left"></i>
      </button>
      <img
        :src="activeLightboxImages[currentImageIndex]"
        class="lightbox-img"
        :style="{ transform: `scale(${zoomLevel})` }"
        @click.stop
      />
      <button
        v-if="activeLightboxImages.length > 1"
        class="btn-nav next"
        @click.stop="nextImage"
      >
        <i class="fas fa-chevron-right"></i>
      </button>
    </div>

    <div class="like-popup" :class="{ show: showLikePopup }">
      <div class="popup-header" v-if="place">
        <img :src="galleryImages[0]" class="popup-liked-img" />
        <div class="popup-title-area">
          <h4 class="popup-place-name">{{ place.name }}</h4>
          <p class="popup-status-text">
            <i class="fas fa-check-circle"></i> {{ t("place.save_success") }}
          </p>
        </div>
        <button @click="showLikePopup = false" class="close-popup">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="popup-recommend-label" v-if="similarPlaces.length > 0">
        {{ t("place.save_success_desc") }}
      </div>
      <div class="popup-body" v-if="similarPlaces.length > 0">
        <div
          v-for="rec in similarPlaces.slice(0, 2)"
          :key="'pop-' + rec.place.id"
          class="popup-rec-item"
          @click="goToRecDetail(rec.place.id)"
        >
          <img :src="getRecCoverImage(rec.place)" alt="" />
          <div class="popup-rec-info">
            <strong>{{ rec.place.name }}</strong>
            <span
              ><i class="fas fa-star" style="color: #eab308"></i>
              {{ rec.place.rating_avg || "0.0" }}</span
            >
          </div>
        </div>
      </div>
    </div>

    <MapOverlay
      v-if="place"
      :is-open="showMapModal"
      :places="allPlaces"
      :categories="categories"
      :initial-selected-id="place.id"
      title="Explore Places"
      @close="showMapModal = false"
    />

    <!-- Language Context Menu -->
    <div
      v-if="contextMenu.visible"
      class="custom-context-menu"
      :style="{ top: contextMenu.y + 'px', left: contextMenu.x + 'px' }"
    >
      <div class="context-menu-title">
        <i class="fas fa-language"></i> Translate to
      </div>
      <div class="context-menu-item" @click="translateSectionTo('th')">
        🇹🇭 Thai
      </div>
      <div class="context-menu-item" @click="translateSectionTo('vi')">
        🇻🇳 Vietnamese
      </div>
      <div class="context-menu-item" @click="translateSectionTo('lo')">
        🇱🇦 Lao
      </div>
      <div class="context-menu-item" @click="translateSectionTo('en')">
        🇬🇧 English
      </div>
    </div>
  </div>
  <!-- End ta-detail-page -->
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted, watch, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import { placeRepository } from "@/repositories/placeRepository";
import { categoryRepository } from "@/repositories/categoryRepository";
import { favoriteRepository } from "@/repositories/favoriteRepository";
import { gnnRepository } from "@/repositories/gnnRepository";
import { useI18n } from "@/composables/useI18n";
import Navbar from "@/components/Navbar.vue";
import MapOverlay from "@/components/MapOverlay.vue";
import SectionDivider from "@/components/SectionDivider.vue";
import axios from "axios";

const route = useRoute();
const router = useRouter();

const handleBack = () => {
  // If there's no history (e.g. opened in new tab), go to home
  if (window.history.state && window.history.state.back) {
    router.back();
  } else {
    router.push("/");
  }
};
const { t } = useI18n();
const place = ref(null);
const categories = ref([]);
const comments = ref([]);
const user = ref(JSON.parse(localStorage.getItem("user")));
const isFavorite = ref(false);
const favoriteIds = ref([]);
const reviewSuccess = ref(false);
const addressText = ref(t("common.loading"));
const showMapModal = ref(false);
const allPlaces = ref([]);
const aiRecommendedPlaces = ref([]);
const similarPlaces = ref([]);
const showLikePopup = ref(false);
const placeSections = ref([]);

const recommendedPlaces = computed(() => {
  if (!place.value || !allPlaces.value.length) return [];
  return allPlaces.value
    .filter(
      (p) =>
        p.category_id === place.value.category_id && p.id !== place.value.id,
    )
    .slice(0, 4);
});

// Translation State and Methods
const targetTranslateLang = ref("vi");
const isTranslatingAbout = ref(false);
const translatedAboutText = ref(null);

const contextMenu = ref({
  visible: false,
  x: 0,
  y: 0,
  targetSection: null, // 'about' or 'guide'
});

const openTranslateMenu = (e, section) => {
  e.preventDefault();
  if (contextMenu.value.visible) {
    contextMenu.value.visible = false;
    return;
  }
  contextMenu.value.visible = true;
  contextMenu.value.x = e.clientX;
  contextMenu.value.y = e.clientY;
  contextMenu.value.targetSection = section;
};

const closeContextMenu = () => {
  if (contextMenu.value.visible) {
    contextMenu.value.visible = false;
  }
};

const translateSectionTo = (lang) => {
  targetTranslateLang.value = lang;
  if (contextMenu.value.targetSection === "about") {
    translateAbout();
  } else if (contextMenu.value.targetSection === "guide") {
    translateSections();
  }
  contextMenu.value.visible = false;
};

watch(targetTranslateLang, () => {
  translatedAboutText.value = null;
  translatedSectionsActive.value = false;
});

const translateAbout = async () => {
  if (!place.value || !place.value.description) return;
  isTranslatingAbout.value = true;
  try {
    const lang = targetTranslateLang.value;
    const res = await fetch(
      `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${lang}&dt=t&q=${encodeURIComponent(place.value.description)}`,
    );
    const data = await res.json();
    translatedAboutText.value = data[0].map((item) => item[0]).join("");
  } catch (err) {
    console.error("Translation failed", err);
  } finally {
    isTranslatingAbout.value = false;
  }
};

const isTranslatingSections = ref(false);
const translatedSectionsActive = ref(false);

const translateSections = async () => {
  if (!placeSections.value || placeSections.value.length === 0) return;
  isTranslatingSections.value = true;
  try {
    const lang = targetTranslateLang.value;
    for (const sec of placeSections.value) {
      if (sec.description) {
        const res = await fetch(
          `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${lang}&dt=t&q=${encodeURIComponent(sec.description)}`,
        );
        const data = await res.json();
        sec.translatedDesc = data[0].map((item) => item[0]).join("");
      }
    }
    translatedSectionsActive.value = true;
  } catch (err) {
    console.error("Translation failed", err);
  } finally {
    isTranslatingSections.value = false;
  }
};

const newComment = ref("");
const newRating = ref(5);
const submitting = ref(false);

const reviewImages = ref([]);
const reviewImagesPreviews = ref([]);

const editingCommentId = ref(null);
const editCommentText = ref("");
const editRating = ref(5);
const showDropdownFor = ref(null);

// 🚨 ตัวแปร State ใหม่สำหรับเก็บรูปใน Lightbox
const activeLightboxImages = ref([]);

const toggleDropdown = (id) => {
  showDropdownFor.value = showDropdownFor.value === id ? null : id;
};

const startEdit = (comment) => {
  editingCommentId.value = comment.id;
  editCommentText.value = comment.comment_text || "";
  editRating.value = comment.rating || 5;
  showDropdownFor.value = null;
};

const cancelEdit = () => {
  editingCommentId.value = null;
  editCommentText.value = "";
  editRating.value = 5;
};

const saveEdit = async (commentId) => {
  if (!editCommentText.value.trim()) return;
  try {
    const formData = new FormData();
    formData.append("user_id", user.value.id);
    formData.append("rating", editRating.value);
    formData.append("comment_text", editCommentText.value);

    await placeRepository.updateUserReview(commentId, formData);

    const comment = comments.value.find((c) => c.id === commentId);
    if (comment) {
      comment.comment_text = editCommentText.value;
      comment.rating = editRating.value;
    }
    cancelEdit();
    fetchData();
  } catch (err) {
    console.error("Failed to update comment", err);
  }
};

const deleteReview = async (commentId) => {
  if (!confirm("Are you sure you want to delete this review?")) return;
  showDropdownFor.value = null;
  try {
    await placeRepository.deleteUserReview(commentId, user.value.id);
    comments.value = comments.value.filter((c) => c.id !== commentId);
    fetchData();
  } catch (err) {
    console.error("Failed to delete review", err);
  }
};

const handleReviewImages = (e) => {
  const files = Array.from(e.target.files);
  files.forEach((file) => {
    reviewImages.value.push(file);
    reviewImagesPreviews.value.push(URL.createObjectURL(file));
  });
};

const removeReviewImage = (idx) => {
  reviewImages.value.splice(idx, 1);
  reviewImagesPreviews.value.splice(idx, 1);
};

// Booking date pickers
const today = new Date();
const tomorrow = new Date(today);
tomorrow.setDate(tomorrow.getDate() + 1);
const dayAfter = new Date(today);
dayAfter.setDate(dayAfter.getDate() + 2);
const bookingCheckin = ref(tomorrow.toISOString().split("T")[0]);
const bookingCheckout = ref(dayAfter.toISOString().split("T")[0]);

const currentImageIndex = ref(0);
const isLightboxOpen = ref(false);
const zoomLevel = ref(1);

const getUserAvatar = (url) => {
  if (url) {
    if (url.startsWith("http") || url.startsWith("data:")) return url;
    return `http://127.0.0.1:8000/${url.startsWith("/") ? url.slice(1) : url}`;
  }
  return 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23ccc"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/></svg>';
};

const galleryImages = computed(() => {
  const getValidImageUrl = (rawUrl) => {
    if (!rawUrl || rawUrl === "null" || rawUrl === "undefined")
      return "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1920&q=80";
    let url = rawUrl;
    if (typeof url === "string" && url.trim().startsWith("[")) {
      try {
        const parsed = JSON.parse(url);
        if (Array.isArray(parsed) && parsed.length > 0) url = parsed[0];
      } catch (e) {
        url = url.replace(/^\["?|"?\]$/g, "").replace(/\\"/g, "");
      }
    }
    if (typeof url !== "string")
      return "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1920&q=80";
    if (
      url.startsWith("http://") ||
      url.startsWith("https://") ||
      url.startsWith("data:")
    )
      return url;
    // ถ้าเป็น base64 raw string (ไม่มี data: prefix)
    if (url.length > 200 && !url.includes("/") && !url.includes("\\")) {
      return `data:image/jpeg;base64,${url}`;
    }
    return `http://127.0.0.1:8000${url.startsWith("/") ? "" : "/"}${url}`;
  };

  const imgs = [];
  if (
    place.value?.images &&
    Array.isArray(place.value.images) &&
    place.value.images.length > 0
  ) {
    place.value.images.forEach((img) =>
      imgs.push(getValidImageUrl(img.image_url || img.url || img)),
    );
  } else if (place.value?.image_url) {
    let parsedArray = [];
    if (
      typeof place.value.image_url === "string" &&
      place.value.image_url.trim().startsWith("[")
    ) {
      try {
        parsedArray = JSON.parse(place.value.image_url);
      } catch (e) {}
    }

    if (parsedArray.length > 0) {
      parsedArray.forEach((url) => imgs.push(getValidImageUrl(url)));
    } else {
      imgs.push(getValidImageUrl(place.value.image_url));
    }
  }

  if (imgs.length === 0) {
    imgs.push(
      "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1920&q=80",
    );
  }
  return imgs;
});

const isHotel = computed(() => {
  if (!place.value || !categories.value.length) return false;
  const cat = categories.value.find((c) => c.id === place.value.category_id);
  return (
    cat &&
    (cat.name.toLowerCase().includes("hotel") || cat.parent_type === "hotel")
  );
});

const weekDays = computed(() => [
  { key: "mon", label: t("common.monday") },
  { key: "tue", label: t("common.tuesday") },
  { key: "wed", label: t("common.wednesday") },
  { key: "thu", label: t("common.thursday") },
  { key: "fri", label: t("common.friday") },
  { key: "sat", label: t("common.saturday") },
  { key: "sun", label: t("common.sunday") },
]);

const openingHoursList = computed(() => {
  if (!place.value) return [];
  let hours = place.value.opening_hours;
  if (typeof hours === "string") {
    try {
      hours = JSON.parse(hours);
    } catch (e) {
      hours = null;
    }
  }
  if (!hours || typeof hours !== "object") return [];

  return weekDays.value.map((day) => {
    const values = hours[day.key] || {};
    const closed =
      values.closed === true ||
      values.closed === "true" ||
      values.closed === 1 ||
      values.closed === "1";
    return {
      key: day.key,
      label: day.label,
      open: values.open || "08:00",
      close: values.close || "17:00",
      closed,
    };
  });
});

// คำนวณกราฟดาว
const ratingBreakdown = computed(() => {
  const levels = [
    { value: 5 },
    { value: 4 },
    { value: 3 },
    { value: 2 },
    { value: 1 },
  ];
  if (!comments.value || comments.value.length === 0) {
    return levels.map((lvl) => ({ value: lvl.value, count: 0, percent: 0 }));
  }

  const total = comments.value.length;
  return levels.map((lvl) => {
    const count = comments.value.filter(
      (c) => Math.round(c.rating) === lvl.value,
    ).length;
    return {
      value: lvl.value,
      count,
      percent: Math.round((count / total) * 100),
    };
  });
});

// Haversine Distance Calculator
const getDistance = (lat1, lon1, lat2, lon2) => {
  if (!lat1 || !lon1 || !lat2 || !lon2) return null;
  const R = 6371; // km
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    0.5 -
    Math.cos(dLat) / 2 +
    (Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      (1 - Math.cos(dLon))) /
      2;
  return R * 2 * Math.asin(Math.sqrt(a));
};

const nearbyRestaurantsTotal = ref(0);
const nearbyAttractionsTotal = ref(0);

const nearbyRestaurants = computed(() => {
  if (!place.value || !allPlaces.value.length) return [];
  const lat1 = parseFloat(place.value.location_lat);
  const lng1 = parseFloat(place.value.location_lng);

  let filtered = allPlaces.value
    .filter((p) => {
      if (p.id === place.value.id) return false;
      const cat = categories.value.find((c) => c.id === p.category_id);
      if (!cat || cat.parent_type !== "restaurant") return false;

      p._distance = getDistance(
        lat1,
        lng1,
        parseFloat(p.location_lat),
        parseFloat(p.location_lng),
      );
      return p._distance !== null && p._distance < 10.0;
    })
    .sort(
      (a, b) =>
        (a._distance === null ? 9999 : a._distance) -
        (b._distance === null ? 9999 : b._distance),
    );

  nearbyRestaurantsTotal.value = filtered.length;
  return filtered.slice(0, 4);
});

const nearbyAttractions = computed(() => {
  if (!place.value || !allPlaces.value.length) return [];
  const lat1 = parseFloat(place.value.location_lat);
  const lng1 = parseFloat(place.value.location_lng);

  let filtered = allPlaces.value
    .filter((p) => {
      if (p.id === place.value.id) return false;
      const cat = categories.value.find((c) => c.id === p.category_id);
      if (
        !cat ||
        cat.parent_type === "restaurant" ||
        cat.parent_type === "hotel"
      )
        return false;

      p._distance = getDistance(
        lat1,
        lng1,
        parseFloat(p.location_lat),
        parseFloat(p.location_lng),
      );
      return p._distance !== null && p._distance < 10.0;
    })
    .sort(
      (a, b) =>
        (a._distance === null ? 9999 : a._distance) -
        (b._distance === null ? 9999 : b._distance),
    );

  nearbyAttractionsTotal.value = filtered.length;
  return filtered.slice(0, 4);
});

const getDistanceText = (km) => {
  if (km === null || km === undefined) return "N/A";
  if (km < 1) {
    const min = Math.round(km * 12);
    return min < 1 ? "1 min walk" : min + " min walk";
  }
  return km.toFixed(1) + " km";
};

const getCommentCountText = (pl) => {
  if (pl && pl.review_count !== undefined) {
    return pl.review_count;
  }
  return 0;
};

const getImageUrl = (url) => {
  if (!url) return "";
  if (url.startsWith("http") || url.startsWith("data:")) return url;
  return `http://127.0.0.1:8000/${url.startsWith("/") ? url.slice(1) : url}`;
};

const getSectionImageUrl = (url) => {
  if (!url) return "";
  if (url.startsWith("http") || url.startsWith("data:")) return url;
  return `http://127.0.0.1:8000${url.startsWith("/") ? "" : "/"}${url}`;
};

const stickyNavRef = ref(null);
const isSticky = ref(false);
const activeSection = ref("about");

const handleScroll = () => {
  if (stickyNavRef.value) {
    const rect = stickyNavRef.value.getBoundingClientRect();
    isSticky.value = rect.top <= 0;
  }

  const sections = ["deals", "about", "location", "reviews"];
  for (const sec of sections) {
    const el = document.getElementById(sec);
    if (el) {
      const rect = el.getBoundingClientRect();
      if (rect.top >= -50 && rect.top < 300) {
        activeSection.value = sec;
        break;
      }
    }
  }
};

const scrollTo = (id) => {
  activeSection.value = id;
  const el = document.getElementById(id);
  if (el) {
    const y = el.getBoundingClientRect().top + window.scrollY - 70;
    window.scrollTo({ top: y, behavior: "smooth" });
  }
};

const getRecCoverImage = (p) => {
  let url = "";
  if (p.images && p.images.length > 0) {
    url = p.images[0].image_url || p.images[0].url || p.images[0];
  } else if (p.image_url) {
    try {
      if (p.image_url.startsWith("[")) {
        const parsed = JSON.parse(p.image_url);
        url = Array.isArray(parsed) && parsed.length > 0 ? parsed[0] : "";
      } else {
        url = p.image_url;
      }
    } catch (e) {
      url = p.image_url;
    }
  }
  if (!url)
    return "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=800&q=80";
  // รองรับ data: URI
  if (url.startsWith("data:")) return url;
  // รองรับ base64 raw string (ไม่มี slash, ยาวมาก)
  if (url.length > 200 && !url.includes("/") && !url.includes("\\")) {
    return `data:image/jpeg;base64,${url}`;
  }
  // รองรับ http absolute URL
  if (url.startsWith("http://") || url.startsWith("https://")) return url;
  // Relative path → prepend backend URL
  return `http://127.0.0.1:8000/${url.replace(/^\//, "")}`;
};

const goToRecDetail = (id) => {
  router.push(`/places/${id}`);
};

watch(
  () => route.params.id,
  (newId, oldId) => {
    if (newId && newId !== oldId) {
      fetchData();
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  },
);

let detailMap = null;
let mapMarkers = [];

const initDetailMap = () => {
  if (!window.L) return;
  if (!place.value || !place.value.location_lat || !place.value.location_lng)
    return;

  if (detailMap) {
    detailMap.remove();
    detailMap = null;
  }

  const lat = parseFloat(place.value.location_lat);
  const lng = parseFloat(place.value.location_lng);

  detailMap = window.L.map("detail-map", {
    zoomControl: false,
    scrollWheelZoom: false,
  }).setView([lat, lng], 14);

  window.L.control.zoom({ position: "bottomright" }).addTo(detailMap);

  window.L.tileLayer(
    "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
    {
      attribution: "© OpenStreetMap contributors © CARTO",
    },
  ).addTo(detailMap);

  mapMarkers = [];

  const createMarker = (p, isTarget = false) => {
    const pLat = parseFloat(p.location_lat);
    const pLng = parseFloat(p.location_lng);
    if (isNaN(pLat) || isNaN(pLng)) return;

    let ratingText = p.rating_avg
      ? parseFloat(p.rating_avg).toFixed(1)
      : '<i class="fas fa-map-marker-alt"></i>';
    const markerHtml = `
            <div class="custom-marker pill-style ${isTarget ? "selected" : ""}">
                <span class="m-text">${ratingText}</span>
            </div>
        `;
    const customIcon = window.L.divIcon({
      html: markerHtml,
      className: "empty-leaflet-icon",
      iconSize: [40, 26],
      iconAnchor: [20, 26],
      popupAnchor: [0, -28],
    });

    let marker = window.L.marker([pLat, pLng], { icon: customIcon }).addTo(
      detailMap,
    );
    mapMarkers.push(marker);

    const goToDetail = (id) => {
      const baseUrl = import.meta.env.BASE_URL || "/";
      // Use hash for hash mode
      window.open(`${baseUrl}#/places/${id}`, "_blank");
    };

    const bubblesHtml = [1, 2, 3, 4, 5]
      .map(
        (s) =>
          `<i class="${(p.rating_avg || 0) >= s ? "fas" : "far"} fa-circle"></i>`,
      )
      .join("");
    const baseUrl = import.meta.env.BASE_URL || "/";
    const popupContentHtml = `
            <div class="leaflet-custom-card" onclick="window.open('${baseUrl}#/places/${p.id}', '_blank')" style="cursor:pointer; display:flex; flex-direction:column; background:white; font-family:'Inter', sans-serif;">
                <div style="height: 120px; width: 100%;">
                    <img src="${getRecCoverImage(p)}" style="width:100%; height:100%; object-fit:cover;" />
                </div>
                <div style="padding: 12px; color:#0f172a;">
                    <h3 style="margin: 0 0 4px; font-size: 1rem; font-weight: 800; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${p.name}</h3>
                    <div style="display:flex; align-items:center;">
                        <span style="color:#00aa6c; font-size:0.75rem;">${bubblesHtml}</span>
                        <span style="color:#64748b; font-size:0.75rem; margin-left:6px; font-weight:600;">(${p.rating_avg || "0.0"})</span>
                    </div>
                </div>
            </div>
        `;
    marker.bindPopup(popupContentHtml, {
      closeButton: false,
      className: "custom-tripadvisor-popup",
    });
    if (isTarget) {
      setTimeout(() => marker.openPopup(), 500);
    }
  };

  createMarker(place.value, true);

  const allNearby = [...nearbyRestaurants.value, ...nearbyAttractions.value];
  allNearby.forEach((p) => createMarker(p, false));

  if (mapMarkers.length > 1) {
    const group = window.L.featureGroup(mapMarkers);
    // add slight delay to fit bounds correctly
    setTimeout(() => {
      if (detailMap)
        detailMap.fitBounds(group.getBounds(), {
          padding: [50, 50],
          maxZoom: 16,
        });
    }, 100);
  }
};

const handleScrollZoom = (e) => {
  const zoomStep = 0.15;
  if (e.deltaY < 0) zoomLevel.value = Math.min(zoomLevel.value + zoomStep, 5);
  else zoomLevel.value = Math.max(zoomLevel.value - zoomStep, 0.5);
};

// 🚨 อัปเดตฟังก์ชัน Lightbox 🚨
const openLightbox = () => {
  // 1. นำรูปจากอัลบั้มหลัก ไปแสดงใน Lightbox
  activeLightboxImages.value = galleryImages.value;
  isLightboxOpen.value = true;
  currentImageIndex.value = 0;
  zoomLevel.value = 1;
  document.body.style.overflow = "hidden";
};

// 🚨 อัปเดตฟังก์ชัน Lightbox 🚨
const openLightboxWith = (images, idx) => {
  // 2. นำรูปรวมถึงแปลง URL จากคอมเมนต์ผู้ใช้ ไปแสดงใน Lightbox
  activeLightboxImages.value = images.map((img) => getImageUrl(img));
  isLightboxOpen.value = true;
  currentImageIndex.value = idx;
  zoomLevel.value = 1;
  document.body.style.overflow = "hidden";
};

const closeLightbox = () => {
  isLightboxOpen.value = false;
  zoomLevel.value = 1;
  document.body.style.overflow = "auto";
};

const nextImage = () => {
  zoomLevel.value = 1;
  if (currentImageIndex.value < activeLightboxImages.value.length - 1) {
    currentImageIndex.value++;
  } else {
    currentImageIndex.value = 0;
  }
};

const prevImage = () => {
  zoomLevel.value = 1;
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--;
  } else {
    currentImageIndex.value = activeLightboxImages.value.length - 1;
  }
};

const handleKeydown = (e) => {
  if (!isLightboxOpen.value) return;
  if (e.key === "Escape") closeLightbox();
  if (e.key === "ArrowRight") nextImage();
  if (e.key === "ArrowLeft") prevImage();
};

onMounted(() => {
  fetchData();
  window.addEventListener("keydown", handleKeydown);
  window.addEventListener("scroll", handleScroll);
});

onUnmounted(() => {
  window.removeEventListener("keydown", handleKeydown);
  window.removeEventListener("scroll", handleScroll);
  document.body.style.overflow = "auto";
  if (detailMap) {
    detailMap.remove();
    detailMap = null;
  }
});

const fetchData = async () => {
  const id = route.params.id;
  try {
    // Fetch the main place first to show content immediately
    const resPlace = await placeRepository.getById(id);
    place.value = resPlace.data;

    // Then fetch secondary data in the background
    const [resCats, resAll] = await Promise.all([
      categoryRepository.getAll(),
      placeRepository.getAll(),
    ]);
    categories.value = resCats.data;
    allPlaces.value = resAll.data;

    // แปลงพิกัดเป็นชื่อสถานที่ (Reverse Geocoding) - Non-blocking
    if (place.value.location_lat && place.value.location_lng) {
      const lat = parseFloat(place.value.location_lat);
      const lng = parseFloat(place.value.location_lng);

      axios
        .get(
          `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&accept-language=th,en`,
        )
        .then((mapRes) => {
          if (mapRes.data && mapRes.data.display_name) {
            const parts = mapRes.data.display_name.split(", ");
            addressText.value =
              parts.length > 3
                ? parts.slice(0, 3).join(", ")
                : mapRes.data.display_name;
          } else {
            addressText.value = `📍 พิกัด (Lat: ${lat.toFixed(4)}, Lng: ${lng.toFixed(4)})`;
          }
        })
        .catch(() => {
          addressText.value = `📍 พิกัด (Lat: ${lat.toFixed(4)}, Lng: ${lng.toFixed(4)})`;
        });
    } else {
      addressText.value = "ไม่พบข้อมูลตำแหน่ง";
    }

    // --- Save to recently_viewed in localStorage ---
    let rv = JSON.parse(localStorage.getItem("recently_viewed") || "[]");
    rv = rv.filter((item) => item !== parseInt(id));
    rv.unshift(parseInt(id));
    if (rv.length > 8) rv.pop();
    localStorage.setItem("recently_viewed", JSON.stringify(rv));

    if (user.value && user.value.role !== "admin") {
      favoriteRepository
        .getUserFavorites(user.value.id)
        .then((favRes) => {
          favoriteIds.value = favRes.data.map((f) => f.place_id);
          isFavorite.value = favoriteIds.value.includes(parseInt(id));
        })
        .catch((err) => console.warn("Failed to fetch favorites", err));

      // Log 'view' action for GNN
      gnnRepository
        .logInteraction({
          user_id: user.value.id,
          place_id: parseInt(id),
          action_type: "view",
        })
        .catch((gnnErr) => console.warn("Failed to log view", gnnErr));

      // Fetch AI recommendations
      gnnRepository
        .getRecommendations(user.value.id)
        .then((recRes) => {
          if (recRes.data && recRes.data.recommended_places) {
            aiRecommendedPlaces.value = recRes.data.recommended_places
              .filter((r) => r.place && r.place.id !== parseInt(id))
              .slice(0, 4);
          }
        })
        .catch((recErr) => console.warn("No AI recommendations", recErr));

      // Fetch Similar Places
      gnnRepository
        .getSimilarPlaces(id)
        .then((simRes) => {
          if (simRes.data && simRes.data.similar_places) {
            similarPlaces.value = simRes.data.similar_places
              .filter((r) => r.place && r.place.id !== parseInt(id))
              .slice(0, 3);
          }
        })
        .catch((simErr) =>
          console.warn("Failed to fetch similar places", simErr),
        );
    }

    try {
      const resComm = await placeRepository.getComments(id);
      comments.value = resComm.data;
    } catch (e) {
      comments.value = [];
    }

    // Fetch Travel Guide Sections
    try {
      const resSec = await placeRepository.getSections(id);
      placeSections.value = resSec.data;
    } catch (e) {
      placeSections.value = [];
    }

    nextTick(() => {
      initDetailMap();
    });
  } catch (err) {
    console.error(err);
  }
};

const submitComment = async () => {
  if (!user.value) return router.push("/login");
  if (!newComment.value.trim()) return;

  submitting.value = true;
  reviewSuccess.value = false;
  try {
    const formData = new FormData();
    formData.append("place_id", route.params.id);
    formData.append("user_id", user.value.id);
    formData.append("rating", newRating.value);
    formData.append("comment_text", newComment.value);

    reviewImages.value.forEach((file) => {
      formData.append("images", file);
    });

    await placeRepository.addComment(formData);

    try {
      await gnnRepository.logInteraction({
        user_id: user.value.id,
        place_id: parseInt(route.params.id),
        action_type: "review",
        score: newRating.value,
      });
    } catch (aiErr) {
      console.warn("AI Log failed", aiErr);
    }

    newComment.value = "";
    newRating.value = 5;
    reviewImages.value = [];
    reviewImagesPreviews.value = [];
    reviewSuccess.value = true;
    setTimeout(() => (reviewSuccess.value = false), 3000);
    fetchData();
  } catch (err) {
    console.error(err);
  } finally {
    submitting.value = false;
  }
};

const handleLike = async (comment) => {
  if (!user.value) return alert("Please login to like");
  try {
    const res = await placeRepository.toggleLike(comment.id, user.value.id);
    if (res.data.status === "liked") {
      if (!comment.liked_by) comment.liked_by = [];
      comment.liked_by.push(user.value.id);
    } else {
      comment.liked_by = comment.liked_by.filter((id) => id !== user.value.id);
    }
  } catch (err) {
    console.error("Like failed", err);
  }
};

const isLiked = (comment) => {
  return (
    user.value && comment.liked_by && comment.liked_by.includes(user.value.id)
  );
};

const toggleHeart = async (id = null) => {
  const targetId = id || route.params.id;
  if (!user.value) return router.push("/login");
  try {
    const res = await favoriteRepository.toggleFavorite(
      user.value.id,
      targetId,
    );
    const added = res.data.status === "added";

    if (!id || parseInt(id) === parseInt(route.params.id)) {
      isFavorite.value = added;
    }

    if (added) {
      if (!favoriteIds.value.includes(parseInt(targetId))) {
        favoriteIds.value.push(parseInt(targetId));
      }
      try {
        await gnnRepository.logInteraction({
          user_id: user.value.id,
          place_id: parseInt(targetId),
          action_type: "like",
        });

        // Show Popup after liking
        showLikePopup.value = true;
        setTimeout(() => {
          showLikePopup.value = false;
        }, 6000);
      } catch (err) {
        console.warn("AI Log failed", err);
      }
    } else {
      favoriteIds.value = favoriteIds.value.filter(
        (fid) => fid !== parseInt(targetId),
      );
    }
  } catch (err) {
    console.error(err);
  }
};

const getCategoryName = (id) =>
  categories.value.find((c) => c.id === id)?.name || "General";
const openMapOverlay = () => {
  showMapModal.value = true;
};

// 🚨 อัปเดตฟังก์ชันกดดู Google Maps ของจริง 🚨
const openGoogleMaps = () => {
  if (place.value?.location_lat && place.value?.location_lng) {
    window.open(
      `https://maps.google.com/?q=${place.value.location_lat},${place.value.location_lng}`,
      "_blank",
    );
  }
};

const placeSummary = computed(() => {
  if (!place.value || !place.value.description)
    return "No description available.";
  const text = place.value.description.trim();
  return text.length > 220 ? text.slice(0, 220).trim() + "..." : text;
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@700;800;900&display=swap");

.ta-detail-page {
  background-color: #ffffff;
  min-height: 100vh;
  font-family: "Inter", sans-serif;
  color: #1e293b;
  width: 100%;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

.floating-heart-main {
  position: absolute;
  bottom: 40px;
  right: 40px;
  z-index: 50;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 12px 28px;
  border-radius: 50px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  font-weight: 700;
  font-size: 1.1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

@media (max-width: 768px) {
  .floating-heart-main {
    bottom: 20px;
    right: 20px; /* Ensure it stays visible */
    padding: 10px 18px;
    font-size: 0.9rem;
  }
  .floating-heart-main span {
    display: none; /* Hide text on small screens if still tight */
  }
}

@media (max-width: 400px) {
  .floating-heart-main {
    right: 15px;
    bottom: 15px;
  }
}

.floating-heart-main i {
  font-size: 1.4rem;
}

.floating-heart-main:hover {
  background: white;
  color: #ef4444;
  transform: translateY(-5px);
}

.floating-heart-main.active {
  background: #ef4444;
  color: white;
  border-color: #ef4444;
}

.lightbox-heart-btn {
  position: fixed;
  top: 30px;
  right: 100px;
  z-index: 2001;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1.5rem;
}

.lightbox-heart-btn:hover {
  background: #ef4444;
  transform: scale(1.1);
}

.lightbox-heart-btn.active {
  background: #ef4444;
  color: white;
}

.mic-heart {
  cursor: pointer !important;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.9) !important;
}

.mic-heart:hover {
  transform: scale(1.2);
  background: white !important;
}

.mic-heart.active {
  color: #ef4444 !important;
  background: white !important;
}

/* Premium Hero Section */
.premium-hero-wrapper {
  margin-bottom: 40px;
  width: 100%;
  margin-left: 0;
  margin-right: 0;
}

.premium-hero {
  position: relative;
  height: 85vh;
  width: 100%;
  background-size: cover;
  background-position: center;
  color: white;
  display: flex;
  flex-direction: column;
}

.hero-nav {
  position: relative;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 40px;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.6) 0%,
    rgba(0, 0, 0, 0) 100%
  );
  width: 100%;
  box-sizing: border-box;
}

@media (max-width: 1100px) {
  .nav-items {
    display: none !important;
  }
}

@media (max-width: 768px) {
  .hero-nav {
    padding: 15px 20px;
  }
  .btn-plan {
    display: none;
  }
}

.logo {
  cursor: pointer;
  font-size: 1.5rem;
  font-weight: 900;
}

.logo-main {
  color: white;
}

.logo-sub {
  color: #4ade80;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 30px;
}

.nav-items {
  display: flex;
  gap: 25px;
}

.nav-items a {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 1px;
  cursor: pointer;
  transition: 0.3s;
}

.nav-items a:hover {
  color: white;
}

.btn-plan {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.4);
  color: white;
  padding: 8px 20px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 1px;
  cursor: pointer;
  transition: 0.3s;
}

.btn-plan:hover {
  background: white;
  color: black;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.3) 0%,
    rgba(0, 0, 0, 0.1) 40%,
    rgba(0, 0, 0, 0.8) 100%
  );
}

.hero-content {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 0 40px 60px;
  box-sizing: border-box;
  overflow: hidden; /* Prevent children from expanding width */
}

@media (max-width: 768px) {
  .hero-content {
    padding: 0 20px 40px;
  }
}

.top-row {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: auto;
}

.btn-back-minimal {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: 0.3s;
}

.btn-back-minimal:hover {
  background: white;
  color: black;
}

.breadcrumb {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: rgba(255, 255, 255, 0.8);
}

.hero-main-info {
  margin-top: auto;
  max-width: 800px;
}

.verified-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(34, 197, 94, 0.2);
  border: 1px solid rgba(34, 197, 94, 0.4);
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 1px;
  color: #4ade80;
  margin-bottom: 20px;
}

.status-dot {
  width: 6px;
  height: 6px;
  background: #4ade80;
  border-radius: 50%;
  box-shadow: 0 0 8px #4ade80;
}

.date-sep {
  opacity: 0.3;
}

.serif-title {
  font-family: "Playfair Display", serif;
  font-size: clamp(3.5rem, 8vw, 6rem);
  font-weight: 900;
  line-height: 0.95;
  margin: 0;
  letter-spacing: -2px;
  text-transform: capitalize;
  padding-left: 5px;
  overflow-wrap: break-word;
  word-break: break-word;
}

.local-name {
  font-size: 2rem;
  color: rgba(255, 255, 255, 0.5);
  margin: 10px 0 30px;
  font-weight: 500;
  font-family: "Inter", sans-serif;
}

.hero-description {
  font-size: 1.3rem;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 400;
  max-width: 800px;
}

.btn-premium-translate {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 700;
  color: #1e293b;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}
.btn-premium-translate:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
.btn-premium-translate.active {
  background: #eef2ff;
  border-color: #c7d2fe;
  color: #4338ca;
}

.custom-context-menu {
  position: fixed;
  z-index: 9999;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  border: 1px solid #e2e8f0;
  min-width: 180px;
  padding: 8px;
  font-family: "Inter", sans-serif;
  animation: fadeIn 0.2s ease-out;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
.context-menu-title {
  font-size: 0.8rem;
  font-weight: 700;
  color: #64748b;
  padding: 6px 12px;
  border-bottom: 1px solid #f1f5f9;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.context-menu-item {
  padding: 8px 12px;
  font-size: 0.95rem;
  color: #334155;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s;
  display: flex;
  align-items: center;
  gap: 10px;
}
.context-menu-item:hover {
  background: #f1f5f9;
  color: #0f172a;
}

/* Stats Bar */
.stats-bar {
  max-width: 1280px;
  margin: 0 auto;
  background: white;
  position: relative;
  z-index: 5;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  border: 1px solid #f1f5f9;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  width: 100%;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .stats-bar {
    grid-template-columns: 1fr;
    margin: 0;
    border-left: none;
    border-right: none;
  }

  .stat-item {
    border-right: none;
    border-bottom: 1px solid #f1f5f9;
    padding: 20px;
  }
}

.booking-options-bar {
  max-width: 1280px;
  margin: 15px auto 0;
  background: #f8fafc;
  padding: 15px 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #f1f5f9;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
}

.booking-label {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 700;
  color: #475569;
  font-size: 0.95rem;
}

.booking-label i {
  color: #3b82f6;
  font-size: 1.2rem;
}

.booking-links {
  display: flex;
  gap: 20px;
}

.btn-booking-link {
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  padding: 8px 20px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  height: 44px;
}

.btn-booking-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.08);
  border-color: #3b82f6;
}

.btn-booking-link img {
  height: 22px;
  width: auto;
}

.stat-item {
  padding: 30px 40px;
  border-right: 1px solid #f1f5f9;
}

.stat-item:last-child {
  border-right: none;
}

.stat-item label {
  display: block;
  font-size: 0.6rem;
  font-weight: 900;
  color: #8c8c8c;
  letter-spacing: 3px;
  margin-bottom: 12px;
  text-transform: uppercase;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 800;
  color: #111111;
  font-family: "Playfair Display", serif;
}

/* Tags Section */
.tags-container {
  max-width: 1280px;
  margin: 40px auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

@media (max-width: 768px) {
  .tags-container {
    grid-template-columns: 1fr;
    margin: 20px;
  }
}

.tag-column {
  padding: 30px 35px;
  background: white;
  border: 1px solid #f1f5f9;
}

.tag-column label {
  display: block;
  font-size: 0.65rem;
  font-weight: 900;
  letter-spacing: 2.5px;
  margin-bottom: 20px;
  color: #8c8c8c;
}

.best-for {
  border-left: 3px solid #1a735c;
}

.avoid-if {
  border-left: 3px solid #b04c36;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 6px 12px;
  border-radius: 2px;
  font-size: 0.8rem;
  font-weight: 600;
}

.best-for .tag {
  background: #eaf4f1;
  color: #1a735c;
  border: 1px solid #d3e8e1;
}

.avoid-if .tag {
  background: #faebe7;
  color: #b04c36;
  border: 1px solid #f5d5cc;
}

/* Gallery Strip */
.gallery-preview-strip {
  max-width: 1280px;
  margin: 40px auto;
  display: flex;
  gap: 15px;
  height: 450px;
  cursor: pointer;
}

.strip-item {
  flex: 1;
  border-radius: 8px;
  overflow: hidden;
}

.strip-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: 0.3s;
}

.strip-item:hover img {
  transform: scale(1.05);
}

.more-indicator {
  width: 120px;
  background: #f1f5f9;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  color: #64748b;
}

/* 🚨 ใส่กลับคืนมาเพื่อแก้ปัญหาเมนูแตกตามที่ตรวจสอบไปในครั้งที่แล้ว 🚨 */
.sticky-nav-wrapper {
  position: sticky;
  top: 0;
  z-index: 100;
  background: white;
  border-bottom: 1px solid #e0e0e0;
  height: 60px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.sticky-nav {
  display: flex;
  align-items: center;
  max-width: 1140px;
  margin: 0 auto;
  height: 100%;
}

.nav-links {
  display: flex;
  gap: 30px;
  height: 100%;
}

.nav-links a {
  text-decoration: none;
  color: #475569;
  font-weight: 700;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  border-bottom: 3px solid transparent;
  transition: 0.2s;
  height: 100%;
  position: relative;
  top: 1px;
}

.nav-links a:hover {
  color: #000;
}

.nav-links a.active {
  color: #00aa6c;
  border-bottom-color: #00aa6c;
}

.opening-hours-list {
  display: grid;
  gap: 12px;
}

/* ══════════════════════════════════════
   TRAVEL GUIDE SECTIONS (Public Display)
══════════════════════════════════════ */
.guide-sections-block {
  margin-bottom: 30px;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.guide-section-item {
  margin-bottom: 36px;
  animation: fadeInUp 0.5s ease both;
}

.guide-section-item:last-child {
  margin-bottom: 10px;
}

.guide-section-img {
  width: 100%;
  border-radius: 16px;
  display: block;
  object-fit: cover;
  max-height: 480px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  transition:
    transform 0.4s ease,
    box-shadow 0.4s ease;
}
.guide-section-img:hover {
  transform: scale(1.008);
  box-shadow: 0 16px 45px rgba(0, 0, 0, 0.15);
}

.guide-section-desc {
  font-size: 1.05rem;
  line-height: 1.85;
  color: #334155;
  margin: 16px 0 0 0;
  white-space: pre-line;
  font-weight: 400;
  letter-spacing: 0.01em;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.opening-hours-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 14px;
  border-radius: 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  font-size: 0.95rem;
  color: #1f2937;
}

.opening-hours-value.closed {
  color: #dc2626;
  font-weight: 700;
}

.no-opening-hours {
  margin: 0;
  color: #64748b;
  font-size: 0.95rem;
}

/* --- Map Markers --- */
:deep(.empty-leaflet-icon) {
  background: transparent;
  border: none;
}

:deep(.custom-marker.pill-style) {
  background: #004d40;
  color: white;
  font-weight: 700;
  font-size: 0.85rem;
  padding: 4px 10px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
  transition: 0.2s;
  border: 2px solid white;
  white-space: nowrap;
  position: relative;
  font-family: "Inter", sans-serif;
}

:deep(.custom-marker.pill-style::after) {
  content: "";
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  border-width: 6px 6px 0;
  border-style: solid;
  border-color: white transparent transparent transparent;
}

:deep(.custom-marker.pill-style::before) {
  content: "";
  position: absolute;
  bottom: -4px;
  left: 50%;
  transform: translateX(-50%);
  border-width: 4px 4px 0;
  border-style: solid;
  border-color: #004d40 transparent transparent transparent;
  z-index: 1;
}

:deep(.custom-marker.pill-style:hover),
:deep(.custom-marker.pill-style.selected) {
  transform: scale(1.15);
  background: #00aa6c;
  z-index: 9999 !important;
}

:deep(.custom-marker.pill-style:hover::before),
:deep(.custom-marker.pill-style.selected::before) {
  border-color: #00aa6c transparent transparent transparent;
}

/* leafelt popup style */
:deep(.custom-tripadvisor-popup .leaflet-popup-content-wrapper) {
  padding: 0;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

:deep(.custom-tripadvisor-popup .leaflet-popup-content) {
  margin: 0;
  width: 260px !important;
}

:deep(.custom-tripadvisor-popup .leaflet-popup-tip) {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

/* ===== DEALS BANNER (Full-Width, Vertical Rows) ===== */
.deals-banner {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  margin-bottom: 24px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
}

.deals-banner-title {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 24px;
  background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
  color: white;
  font-size: 0.95rem;
  font-weight: 700;
}

.deals-banner-title i {
  font-size: 0.9rem;
}

/* Vertical rows container */
.deals-rows {
  padding: 8px 0;
}

/* Each partner row */
.deals-row-item {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 16px 24px;
  text-decoration: none;
  color: inherit;
  transition: background 0.2s;
  cursor: pointer;
}

.deals-row-item:hover {
  background: #f8fafc;
}

.deals-row-divider {
  height: 1px;
  background: #f1f5f9;
  margin: 0 24px;
}

/* Brand logo column */
.deals-row-brand {
  min-width: 120px;
  flex-shrink: 0;
}

/* Price column */
.deals-row-price {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  padding-right: 16px;
}

.deals-price-original {
  font-size: 0.82rem;
  color: #ef4444;
  text-decoration: line-through;
  font-weight: 500;
}

.deals-price-main {
  font-size: 0.88rem;
  font-weight: 600;
  color: #64748b;
}

.deals-price-sale {
  font-size: 1.2rem;
  font-weight: 800;
  color: #0f172a;
}

/* CTA button column */
.deals-row-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 10px 22px;
  border-radius: 50px;
  font-size: 0.88rem;
  font-weight: 700;
  text-decoration: none;
  transition: 0.2s;
  white-space: nowrap;
  flex-shrink: 0;
  cursor: pointer;
}

.deals-row-btn i {
  font-size: 0.7rem;
}

.deals-btn-booking {
  background: #00aa6c;
  color: white;
  box-shadow: 0 3px 10px rgba(0, 170, 108, 0.3);
}

.deals-row-item:hover .deals-btn-booking {
  background: #009960;
  box-shadow: 0 5px 14px rgba(0, 170, 108, 0.4);
  transform: translateY(-1px);
}

.deals-btn-agoda {
  background: white;
  color: #1e293b;
  border: 1.5px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
}

.deals-row-item:hover .deals-btn-agoda {
  background: #fce4f3;
  border-color: #e91e8c;
  color: #e91e8c;
  transform: translateY(-1px);
}

/* Brand text styles */
.booking-text {
  color: #003580;
  font-weight: 900;
  font-size: 1.05rem;
  letter-spacing: -0.5px;
}

.booking-dot {
  color: #003580;
}

.agoda-text {
  display: block;
  color: #e91e8c;
  font-weight: 900;
  font-size: 1.15rem;
  letter-spacing: -0.5px;
  line-height: 1;
  margin-bottom: 4px;
}

.agoda-dots-row {
  display: flex;
  gap: 3px;
}

.agoda-dots-row span {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  display: inline-block;
}

/* Disclaimer */
.deals-disclaimer {
  font-size: 0.73rem;
  color: #94a3b8;
  padding: 10px 24px 14px;
  background: #f8fafc;
  border-top: 1px solid #f1f5f9;
  margin: 0;
  display: flex;
  align-items: flex-start;
  gap: 6px;
  line-height: 1.5;
}

.deals-disclaimer i {
  color: #94a3b8;
  margin-top: 1px;
  flex-shrink: 0;
}

/* --- พื้นหลังคลีนแบบ TripAdvisor --- */
/* (Updated by Premium Theme) */

.ta-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 40px 60px;
}

/* --- Top Actions (Back Button) --- */
.top-actions {
  margin-bottom: 15px;
}

/* --- Interactive Like Popup --- */
.like-popup {
  position: fixed;
  bottom: -150%;
  right: 30px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid #e2e8f0;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  border-radius: 16px;
  width: 320px;
  padding: 20px;
  z-index: 9999;
  transition: all 0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55);
  opacity: 0;
}

.like-popup.show {
  bottom: 30px;
  opacity: 1;
}

.popup-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 15px;
  position: relative;
}

.popup-liked-img {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  object-fit: cover;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.popup-title-area {
  flex: 1;
  overflow: hidden;
}

.popup-place-name {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 800;
  color: #1e293b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.popup-status-text {
  margin: 2px 0 0;
  font-size: 0.8rem;
  color: #10b981;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 4px;
}

.popup-recommend-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 600;
  margin: 15px 0 10px;
  padding-top: 15px;
  border-top: 1px solid #f1f5f9;
}

.close-popup {
  position: absolute;
  top: -5px;
  right: -5px;
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  font-size: 1rem;
}

.close-popup:hover {
  color: #1e293b;
}

.popup-rec-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  border-radius: 10px;
  transition: 0.2s;
  cursor: pointer;
  text-align: left;
}

.popup-rec-item:hover {
  background: #f8fafc;
}

.popup-rec-item img {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  object-fit: cover;
}

.popup-rec-info {
  display: flex;
  flex-direction: column;
}

.popup-rec-info strong {
  font-size: 0.9rem;
  color: #1e293b;
  margin-bottom: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
}

.popup-rec-info span {
  font-size: 0.8rem;
  color: #64748b;
}

.btn-back {
  background: none;
  border: none;
  color: #475569;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0;
  font-family: "Inter", sans-serif;
}

.btn-back:hover {
  color: #000;
  text-decoration: underline;
}

/* --- Header Section --- */
.place-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.header-main h1 {
  font-size: 2.2rem;
  font-weight: 800;
  margin: 0 0 10px;
  color: #000;
}

.meta-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 0.95rem;
  color: #475569;
}

/* วงกลมแบบ TripAdvisor */
.rating-bubbles i {
  color: #00aa6c;
  font-size: 0.9rem;
  margin-right: 2px;
}

.review-count {
  font-weight: 600;
  color: #475569;
  text-decoration: underline;
  cursor: pointer;
}

.divider {
  color: #cbd5e1;
}

.category-link {
  font-weight: 600;
  color: #475569;
}

.top-location-link {
  cursor: pointer;
  transition: color 0.2s;
}

.top-location-link:hover {
  color: #000;
  text-decoration: underline;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.btn-action {
  background: white;
  border: 1px solid #cbd5e1;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: 0.2s;
  color: #0f172a;
  font-family: "Inter", sans-serif;
}

.btn-action:hover {
  border-color: #000;
  background: #f8fafc;
}

.btn-save.active {
  color: #ef4444;
  border-color: #ef4444;
  background: #fef2f2;
}

/* --- Gallery Grid --- */
.gallery-grid {
  display: flex;
  gap: 4px;
  height: 400px;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 30px;
  position: relative;
  cursor: pointer;
}

.gallery-grid:hover::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.05);
  pointer-events: none;
}

.main-photo {
  flex: 2;
  height: 100%;
}

.main-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.side-photos {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
  height: 100%;
}

.side-photos img {
  width: 100%;
  height: calc(50% - 2px);
  object-fit: cover;
}

.empty-photo-slot {
  width: 100%;
  height: calc(50% - 2px);
  background: #e2e8f0;
}

.btn-view-photos {
  position: absolute;
  bottom: 20px;
  right: 20px;
  background: white;
  border: 1px solid #000;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* --- Content Split Layout --- */
.content-split {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 40px;
}

@media (max-width: 992px) {
  .content-split {
    grid-template-columns: 1fr;
  }

  .sidebar-column {
    position: static;
    top: auto;
  }
}

/* Main Column */
.main-column h2 {
  font-size: 1.5rem;
  font-weight: 800;
  margin: 0 0 15px;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 10px;
}

.description-text {
  line-height: 1.7;
  color: #334155;
  font-size: 1.05rem;
}

.section-divider {
  border: none;
  height: 1px;
  background: #e2e8f0;
  margin: 30px 0;
}

/* Reviews Section */
.write-review-box {
  display: flex;
  gap: 15px;
  background: white;
  padding: 24px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  margin-bottom: 30px;
}

.u-avatar-large {
  width: 48px;
  height: 48px;
  background: #000;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: 700;
  flex-shrink: 0;
}

.review-input-area {
  flex: 1;
}

.prompt-text {
  font-weight: 700;
  margin: 0 0 10px;
  color: #0f172a;
}

.star-picker {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 15px;
}

.star-picker i {
  color: #00aa6c;
  font-size: 1.5rem;
  cursor: pointer;
  transition: 0.1s;
}

/* Social: Review Upload Styles */
.review-images-upload {
  margin-bottom: 15px;
}

.btn-upload-photos {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: 1px dashed #cbd5e1;
  border-radius: 8px;
  color: #64748b;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: 0.2s;
}

.btn-upload-photos:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  background: #f0f9ff;
}

.previews-row {
  display: flex;
  gap: 10px;
  margin-top: 10px;
  flex-wrap: wrap;
}

.preview-item {
  position: relative;
  width: 60px;
  height: 60px;
}

.preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 6px;
}

.btn-remove-img {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Social: Review List Images */
.comment-images-grid {
  display: flex;
  gap: 8px;
  margin-top: 12px;
  overflow-x: auto;
  padding-bottom: 5px;
}

.comment-images-grid img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s;
}

.comment-images-grid img:hover {
  transform: scale(1.05);
}

.comment-footer {
  margin-top: 12px;
  display: flex;
  gap: 15px;
}

.btn-like-small {
  background: none;
  border: none;
  color: #64748b;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: 0.2s;
}

.btn-like-small:hover {
  color: #000;
}

.btn-like-small.active {
  color: #e0245e;
}

.star-picker i:hover {
  transform: scale(1.1);
}

.rating-label {
  margin-left: 10px;
  font-weight: 600;
  color: #475569;
}

textarea {
  width: 100%;
  height: 100px;
  padding: 15px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  resize: none;
  font-family: inherit;
  margin-bottom: 15px;
  box-sizing: border-box;
}

textarea:focus {
  outline: none;
  border-color: #000;
}

.action-row {
  display: flex;
  justify-content: flex-end;
}

.btn-submit {
  background: #000;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
}

.btn-submit:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
}

.success-msg {
  color: #00aa6c;
  font-weight: 600;
  text-align: right;
  margin-top: 10px;
}

.login-prompt {
  background: white;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  text-align: center;
  margin-bottom: 30px;
}

.btn-login-outline {
  margin-top: 10px;
  background: white;
  border: 1px solid #000;
  padding: 8px 24px;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
}

/* Review List */
.review-item {
  border-bottom: 1px solid #e2e8f0;
  padding: 20px 0;
}

.review-item:last-child {
  border-bottom: none;
}

.reviewer-info {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
}

.r-avatar {
  width: 40px;
  height: 40px;
  background: #e2e8f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #475569;
}

.r-details {
  display: flex;
  flex-direction: column;
}

.r-date {
  font-size: 0.8rem;
  color: #64748b;
}

.rating-bubbles.small i {
  font-size: 0.8rem;
}

.r-text {
  margin: 10px 0 0;
  line-height: 1.6;
  color: #334155;
}

.no-reviews {
  text-align: center;
  color: #64748b;
  padding: 40px 0;
}

.no-reviews i {
  font-size: 2rem;
  margin-bottom: 10px;
}

/* Sidebar Column */
.sidebar-column {
  position: sticky;
  top: 90px;
  align-self: start;
}

.sidebar-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
}

.sidebar-card h3 {
  margin: 0 0 15px;
  font-size: 1.1rem;
  font-weight: 800;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 10px;
}

.place-summary-text {
  margin: 0 0 16px;
  color: #475569;
  line-height: 1.7;
  font-size: 0.95rem;
}

.place-summary-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  color: #64748b;
  font-size: 0.9rem;
}

.place-summary-meta span {
  display: inline-flex;
  gap: 4px;
  align-items: center;
}

/* --- Rating Summary Card --- */
.rating-summary-card {
  position: relative;
  /* override sticky for this card */
}

.rating-overview {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.big-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  min-width: 72px;
}

.score-number {
  font-size: 3rem;
  font-weight: 900;
  color: #1e293b;
  line-height: 1;
  margin-bottom: 6px;
}

.score-bubbles {
  display: flex;
  gap: 2px;
  margin-bottom: 4px;
}

.score-bubbles i {
  color: #00aa6c;
  font-size: 0.85rem;
}

.score-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: #00aa6c;
}

.score-count {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-top: 4px;
}

.score-bars {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.score-bar-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.bar-label {
  font-size: 0.8rem;
  color: #475569;
  font-weight: 500;
  width: 80px;
  flex-shrink: 0;
  text-align: left;
  white-space: nowrap;
}

.bar-track {
  flex: 1;
  height: 8px;
  background: #e2e8f0;
  border-radius: 99px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: #00aa6c;
  border-radius: 99px;
  transition: width 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.bar-count {
  font-size: 0.78rem;
  color: #64748b;
  font-weight: 600;
  width: 24px;
  text-align: right;
  flex-shrink: 0;
}

/* ===== BOOKING COMPARE CARD ===== */
.booking-compare-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
}

.bcc-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 20px;
  background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
  color: white;
  font-size: 1rem;
  font-weight: 700;
}

.bcc-header i {
  font-size: 1rem;
}

/* Date Row */
.bcc-date-row {
  display: flex;
  align-items: stretch;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  margin: 16px 16px 10px;
  overflow: hidden;
  background: #f8fafc;
}

.bcc-date-field {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
}

.bcc-date-field > i {
  color: #0ea5e9;
  font-size: 1rem;
  flex-shrink: 0;
}

.bcc-date-field > div {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.bcc-date-sep {
  width: 1px;
  background: #e2e8f0;
  margin: 8px 0;
}

.bcc-date-label {
  font-size: 0.7rem;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 2px;
}

.bcc-date-input {
  border: none;
  background: transparent;
  font-family: "Inter", sans-serif;
  font-size: 0.85rem;
  font-weight: 600;
  color: #1e293b;
  outline: none;
  width: 100%;
  cursor: pointer;
  padding: 0;
}

.bcc-date-input::-webkit-calendar-picker-indicator {
  opacity: 0;
  position: absolute;
  width: 100%;
  cursor: pointer;
}

.bcc-guest-field {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 16px 16px;
  padding: 10px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  font-size: 0.88rem;
  font-weight: 600;
  color: #475569;
  background: #f8fafc;
  cursor: pointer;
}

.bcc-guest-field i {
  color: #0ea5e9;
}

/* Partner rows */
.bcc-partners {
  border-top: 1px solid #f1f5f9;
  padding: 0 16px;
}

.bcc-partner-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 0;
  border-bottom: 1px solid #f1f5f9;
}

.bcc-partner-row:last-child {
  border-bottom: none;
}

.bcc-brand {
  width: 100px;
  flex-shrink: 0;
}

.bcc-booking-logo {
  display: flex;
  align-items: center;
  line-height: 1;
}

.bcc-agoda-logo {
  display: flex;
  flex-direction: column;
  gap: 3px;
  line-height: 1;
}

.agoda-dots {
  display: flex;
  gap: 3px;
}

.agoda-dots span {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  display: inline-block;
}

.bcc-brand-logo {
  max-height: 22px;
  max-width: 100px;
  object-fit: contain;
  display: block;
}
.bcc-btn-booking {
  background: #003580;
  color: white;
  box-shadow: 0 3px 10px rgba(0, 53, 128, 0.25);
}

.bcc-btn-booking:hover {
  background: #00224f;
  box-shadow: 0 5px 14px rgba(0, 53, 128, 0.35);
  transform: translateY(-1px);
}

.bcc-btn-agoda {
  background: white;
  color: #1e293b;
  border: 1.5px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
}

.bcc-btn-agoda:hover {
  background: #f8fafc;
  border-color: #94a3b8;
  transform: translateY(-1px);
}

.bcc-disclaimer {
  font-size: 0.73rem;
  color: #94a3b8;
  padding: 12px 16px;
  background: #f8fafc;
  border-top: 1px solid #f1f5f9;
  margin: 0;
  display: flex;
  align-items: flex-start;
  gap: 6px;
  line-height: 1.5;
}

.bcc-disclaimer i {
  color: #94a3b8;
  margin-top: 1px;
  flex-shrink: 0;
}

/* Recommended Places Section Refined */
.recommended-section {
  margin-top: 60px;
  padding-top: 40px;
  border-top: 1px solid #f1f5f9;
}

.section-header-modern {
  margin-bottom: 30px;
}

.sh-badge {
  background: #e0e7ff;
  color: #4338ca;
  padding: 6px 12px;
  border-radius: 100px;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 12px;
  display: inline-block;
}

.sh-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0 0 8px;
}

.sh-subtitle {
  font-size: 1rem;
  color: #64748b;
  margin: 0;
}

.recommended-grid-modern {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 25px;
}

/* Premium Immersive Card Style */
.modern-immersive-card {
  position: relative;
  height: 420px;
  border-radius: 0;
  overflow: hidden;
  cursor: pointer;
  background-color: #1e293b;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.modern-immersive-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.mic-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.8s ease;
}

.modern-immersive-card:hover .mic-image {
  transform: scale(1.1);
}

.mic-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 40px 16px 16px;
  background: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.9) 0%,
    rgba(0, 0, 0, 0.6) 50%,
    transparent 100%
  );
  color: white;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 2;
}

.mic-category {
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: #38bdf8;
}

.mic-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.2;
  color: white;
}

.mic-rating {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.95rem;
  font-weight: 700;
}

.mic-rating i {
  color: #fbbf24;
}

.mic-desc {
  font-size: 0.88rem;
  opacity: 0.9;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.6;
  margin: 5px 0;
}

.mic-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 5px;
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.mic-verified {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  font-weight: 700;
  color: #10b981;
}

.mic-action {
  font-size: 0.8rem;
  font-weight: 800;
  color: white;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: 0.2s;
}

.modern-immersive-card:hover .mic-action {
  gap: 10px;
}

.mic-heart {
  position: absolute;
  top: 15px;
  right: 15px;
  width: 38px;
  height: 38px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ef4444;
  font-size: 1.2rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  z-index: 50;
}

.mic-heart:hover {
  transform: scale(1.1);
  background: #ef4444;
  color: white;
}

/* Nearby Section */
.nearby-section {
  margin-top: 40px;
  padding-top: 30px;
  border-top: 1px solid #e2e8f0;
}

.nearby-grid {
  display: grid;
  grid-template-columns: 1.2fr 1.5fr 1.5fr;
  gap: 30px;
}

.nearby-col h3 {
  font-size: 1.15rem;
  font-weight: 800;
  margin: 0 0 5px;
  color: #0f172a;
}

.col-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 2px solid #000;
  padding-bottom: 15px;
  margin-bottom: 15px;
}

.col-header span {
  font-size: 0.85rem;
  color: #475569;
}

.btn-text-link {
  background: none;
  border: none;
  color: #000;
  font-weight: 700;
  text-decoration: underline;
  cursor: pointer;
  font-size: 0.85rem;
  padding: 0;
}

.btn-text-link:hover {
  color: #00aa6c;
}

.walk-score-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.score-title {
  display: block;
  font-weight: 700;
  color: #00aa6c;
  font-size: 0.95rem;
  margin-bottom: 4px;
}

.score-number {
  font-size: 1.8rem;
  font-weight: 800;
  color: #00aa6c;
}

/* List Items */
.nearby-list {
  display: flex;
  flex-direction: column;
}

.nearby-item {
  padding: 15px 0;
  border-bottom: 1px solid #e2e8f0;
  cursor: pointer;
}

.nearby-item h4 {
  margin: 0 0 6px;
  font-size: 0.95rem;
  font-weight: 700;
}

.n-rating {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
  font-size: 0.85rem;
}

.n-rating .bubbles i {
  color: #00aa6c;
  font-size: 0.75rem;
}

.n-meta {
  font-size: 0.85rem;
  color: #475569;
}

@media (max-width: 992px) {
  .nearby-grid {
    grid-template-columns: 1fr;
    gap: 40px;
  }
}

@media (max-width: 768px) {
  .sh-title {
    font-size: 1.5rem;
  }
  .modern-immersive-card {
    height: 380px;
  }
  .recommended-grid-modern {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 15px;
  }
}

/* Lightbox Styling */
.lightbox-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.95);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 99999;
}

.lightbox-img {
  max-width: 95vw;
  max-height: 90vh;
  object-fit: contain;
  transition: transform 0.2s ease-out;
  user-select: none;
  border-radius: 4px;
}

.btn-close-lightbox {
  position: absolute;
  top: 25px;
  right: 25px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  font-size: 1.5rem;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  cursor: pointer;
  z-index: 100000;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.2s;
}

.btn-close-lightbox:hover {
  background: #ef4444;
}

.btn-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  font-size: 1.5rem;
  width: 54px;
  height: 54px;
  border-radius: 50%;
  cursor: pointer;
  z-index: 100000;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(4px);
  transition: 0.2s;
}

.btn-nav:hover {
  background: rgba(255, 255, 255, 0.2);
}

.btn-nav.prev {
  left: 20px;
}
.btn-nav.next {
  right: 20px;
}

.loading-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: white;
  z-index: 9999;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f1f5f9;
  border-top: 4px solid #6366f1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
