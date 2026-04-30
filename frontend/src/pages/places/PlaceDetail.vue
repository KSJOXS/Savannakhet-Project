<template>
    <div class="ta-detail-page">
        <Navbar />

        <div class="ta-container" v-if="place">
            <div class="top-actions">
                <button @click="router.back()" class="btn-back">
                    <i class="fas fa-arrow-left"></i> {{ t('place.backToSearch') }}
                </button>
            </div>

            <div class="place-header">
                <div class="header-main">
                    <h1>{{ place.name }}</h1>
                    <div class="meta-row">
                        <div class="rating-bubbles">
                            <i v-for="s in 5" :key="'h-' + s"
                                :class="[(place.rating_avg || 0) >= s ? 'fas' : 'far', 'fa-circle']"></i>
                        </div>
                        <span class="review-count" @click="scrollTo('reviews')">{{ comments.length }} {{
                            t('place.reviews_count') }}</span>
                        <span class="divider">•</span>
                        <span class="category-link">{{ getCategoryName(place.category_id) }}</span>
                        <span class="divider">•</span>
                        <span class="location-text top-location-link" @click="openMapOverlay"
                            :title="t('place.viewOnMap')">
                            <i class="fas fa-map-marker-alt"></i> {{ addressText }}
                        </span>
                    </div>
                </div>
                <div class="header-actions">
                    <button v-if="!user || user.role !== 'admin'"
                        :class="['btn-action btn-save', { active: isFavorite }]" @click="toggleHeart">
                        <i class="fas fa-heart"></i> {{ isFavorite ? 'Saved' : 'Save' }}
                    </button>
                </div>
            </div>

            <div class="gallery-grid" @click="openLightbox">
                <div class="main-photo">
                    <img :src="galleryImages[0]" alt="Main Place Image" />
                </div>
                <div class="side-photos" v-if="galleryImages.length > 1">
                    <img :src="galleryImages[1]" alt="Place Image 2" />
                    <img v-if="galleryImages.length > 2" :src="galleryImages[2]" alt="Place Image 3"
                        class="third-img" />
                    <div v-else class="empty-photo-slot"></div>
                </div>
                <button class="btn-view-photos"><i class="fas fa-th"></i> {{ t('place.viewAllPhotos') }} ({{
                    galleryImages.length }})</button>
            </div>

            <div class="deals-banner" v-if="isHotel" id="deals">
                <div class="deals-banner-title">
                    <i class="fas fa-tags"></i>
                    <span>{{ t('place.checkPrices') }}</span>
                </div>
                <div class="deals-rows">
                    <a :href="`https://www.booking.com/searchresults.html?ss=${encodeURIComponent(place.name)}`"
                        target="_blank" class="deals-row-item">
                        <div class="deals-row-brand">
                            <span class="booking-text">Booking<span class="booking-dot">.</span>com</span>
                        </div>
                        <div class="deals-row-price">
                            <span class="deals-price-main">See prices on site</span>
                        </div>
                        <div class="deals-row-btn deals-btn-booking">ดูข้อเสนอ <i class="fas fa-external-link-alt"></i>
                        </div>
                    </a>

                    <div class="deals-row-divider"></div>

                    <a :href="`https://www.agoda.com/search?query=${encodeURIComponent(place.name)}`" target="_blank"
                        class="deals-row-item">
                        <div class="deals-row-brand">
                            <span class="agoda-text">agoda</span>
                            <div class="agoda-dots-row">
                                <span style="background:#e91e8c;"></span>
                                <span style="background:#f8a316;"></span>
                                <span style="background:#4caf50;"></span>
                                <span style="background:#2196f3;"></span>
                                <span style="background:#e91e8c;"></span>
                            </div>
                        </div>
                        <div class="deals-row-price">
                            <span class="deals-price-main">See prices on site</span>
                        </div>
                        <div class="deals-row-btn deals-btn-agoda">ดูข้อเสนอ <i class="fas fa-external-link-alt"></i>
                        </div>
                    </a>
                </div>
                <p class="deals-disclaimer">
                    <i class="fas fa-info-circle"></i>
                    ราคาเป็นราคาเฉลี่ยอ้างอิงเท่านั้น ราคาจริงจะแสดงบนเว็บไซต์พาร์ทเนอร์
                </p>
            </div>

            <div class="sticky-nav-wrapper" ref="stickyNavRef">
                <div class="sticky-nav" :class="{ 'is-sticky': isSticky }">
                    <div class="nav-links">
                        <a v-if="isHotel" href="#deals" :class="{ active: activeSection === 'deals' }"
                            @click.prevent="scrollTo('deals')">{{ t('place.deals') }}</a>
                        <a href="#about" :class="{ active: activeSection === 'about' }"
                            @click.prevent="scrollTo('about')">{{ t('place.about') }}</a>
                        <a href="#location" :class="{ active: activeSection === 'location' }"
                            @click.prevent="scrollTo('location')">{{ t('place.location') }}</a>
                        <a href="#reviews" :class="{ active: activeSection === 'reviews' }"
                            @click.prevent="scrollTo('reviews')">{{ t('place.reviews') }}</a>
                    </div>
                </div>
            </div>

            <div class="content-split">
                <div class="main-column">
                    <section class="about-section" id="about">
                        <h2>{{ t('place.aboutThisPlace') }}</h2>
                        <p class="description-text">{{ place.description }}</p>
                    </section>

                    <hr class="section-divider" />

                    <section class="reviews-section" id="reviews">
                        <h2>{{ t('place.travelerReviews') }} ({{ comments.length }})</h2>

                        <div class="write-review-box" v-if="user && user.role !== 'admin'">
                            <div class="u-avatar-large"
                                style="padding: 0; overflow: hidden; border: none; background: none;">
                                <img v-if="user.profile_image" :src="getImageUrl(user.profile_image)" alt="avatar"
                                    style="width:100%; height:100%; object-fit:cover;" />
                                <div v-else
                                    style="width:100%; height:100%; display:flex; align-items:center; justify-content:center; background:#ff6b6b; color:white; border-radius:50%; font-size:1.2rem; font-weight:bold;">
                                    {{ user.username ? user.username.charAt(0).toUpperCase() : 'U' }}
                                </div>
                            </div>
                            <div class="review-input-area">
                                <p class="prompt-text">{{ t('place.whatDoYouThink') }}</p>
                                <div class="star-picker">
                                    <i v-for="star in 5" :key="'picker-' + star"
                                        :class="[newRating >= star ? 'fas' : 'far', 'fa-circle']"
                                        @click="newRating = star"></i>
                                    <span class="rating-label">{{ t('place.ratingLabels')[newRating - 1] }}</span>
                                </div>
                                <textarea v-model="newComment"
                                    :placeholder="t('place.writeReviewPlaceholder')"></textarea>

                                <div class="review-images-upload">
                                    <label class="btn-upload-photos">
                                        <i class="fas fa-camera"></i> {{ t('nav.postPhoto') }}
                                        <input type="file" multiple accept="image/*" @change="handleReviewImages"
                                            hidden />
                                    </label>
                                    <div v-if="reviewImagesPreviews.length > 0" class="previews-row">
                                        <div v-for="(src, idx) in reviewImagesPreviews" :key="idx" class="preview-item">
                                            <img :src="src" />
                                            <button @click="removeReviewImage(idx)" class="btn-remove-img">×</button>
                                        </div>
                                    </div>
                                </div>

                                <div class="action-row">
                                    <button class="btn-submit" @click="submitComment"
                                        :disabled="submitting || !newComment.trim()">
                                        {{ submitting ? t('place.submitting') : t('place.submitReviewBtn') }}
                                    </button>
                                </div>
                                <p v-if="reviewSuccess" class="success-msg"><i class="fas fa-check-circle"></i>
                                    {{ t('place.submitReviewSuccess') }}</p>
                            </div>
                        </div>
                        <div v-else-if="!user" class="login-prompt">
                            <p>{{ t('place.pleaseLoginToReview') }}</p>
                            <button @click="router.push('/login')" class="btn-login-outline">{{ t('nav.signIn')
                                }}</button>
                        </div>

                        <div class="review-list">
                            <div v-if="comments.length === 0" class="no-reviews">
                                <i class="far fa-comment-alt"></i>
                                <p>{{ t('place.noReviewsYet') }}</p>
                            </div>

                            <div v-for="comment in comments" :key="comment.id" class="review-item">
                                <div class="reviewer-info">
                                    <div class="r-avatar"
                                        style="padding: 0; overflow: hidden; border: none; background: none;">
                                        <img v-if="comment.profile_image" :src="getImageUrl(comment.profile_image)"
                                            alt="avatar"
                                            style="width:100%; height:100%; object-fit:cover; border-radius:50%;" />
                                        <div v-else
                                            style="width:100%; height:100%; display:flex; align-items:center; justify-content:center; background:#e2e8f0; color:#475569; font-weight:700; border-radius:50%;">
                                            {{ comment.username?.charAt(0).toUpperCase() }}
                                        </div>
                                    </div>
                                    <div class="r-details"
                                        style="flex-grow: 1; display: flex; justify-content: space-between; align-items: center;">
                                        <div>
                                            <strong>{{ comment.username }}</strong>
                                            <span class="r-date">{{ t('place.recentReview') }}</span>
                                        </div>
                                        <div class="review-actions" v-if="user && user.username === comment.username"
                                            style="position: relative;">
                                            <button @click="toggleDropdown(comment.id)"
                                                style="background: none; border: none; cursor: pointer; color: #64748b; padding: 5px; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; transition: background 0.2s;">
                                                <i class="fas fa-ellipsis-h"></i>
                                            </button>
                                            <div v-if="showDropdownFor === comment.id"
                                                style="position: absolute; right: 0; top: 100%; background: white; border: 1px solid #e2e8f0; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); z-index: 10; min-width: 120px; overflow: hidden;">
                                                <button @click="startEdit(comment)"
                                                    style="display: block; width: 100%; text-align: left; padding: 10px 15px; background: none; border: none; cursor: pointer; font-size: 0.9rem; color: #1e293b; transition: background 0.2s;">
                                                    <i class="fas fa-pen"
                                                        style="margin-right: 8px; color: #64748b;"></i> Edit
                                                </button>
                                                <button @click="deleteReview(comment.id)"
                                                    style="display: block; width: 100%; text-align: left; padding: 10px 15px; background: none; border: none; cursor: pointer; font-size: 0.9rem; color: #ef4444; transition: background 0.2s;">
                                                    <i class="fas fa-trash" style="margin-right: 8px;"></i> Delete
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="review-content">
                                    <div v-if="editingCommentId === comment.id" class="edit-comment-area"
                                        style="margin-top: 10px; background: #f8fafc; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0;">
                                        <div class="star-picker" style="margin-bottom: 10px;">
                                            <i v-for="star in 5" :key="'edit-picker-' + star"
                                                :class="[editRating >= star ? 'fas' : 'far', 'fa-circle']"
                                                @click="editRating = star"
                                                style="cursor: pointer; color: #f59e0b; margin-right: 5px;"></i>
                                        </div>
                                        <textarea v-model="editCommentText"
                                            style="width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; resize: vertical; min-height: 80px; font-family: inherit; font-size: 0.95rem; margin-bottom: 10px;"></textarea>
                                        <div style="display: flex; gap: 10px; justify-content: flex-end;">
                                            <button @click="cancelEdit"
                                                style="padding: 8px 16px; background: white; border: 1px solid #cbd5e1; border-radius: 6px; cursor: pointer; color: #475569; font-weight: 600;">Cancel</button>
                                            <button @click="saveEdit(comment.id)"
                                                style="padding: 8px 16px; background: #3b82f6; border: none; border-radius: 6px; cursor: pointer; color: white; font-weight: 600;">Save</button>
                                        </div>
                                    </div>
                                    <div v-else>
                                        <div class="rating-bubbles small">
                                            <i v-for="s in 5" :key="'rev-' + comment.id + '-' + s"
                                                :class="[comment.rating >= s ? 'fas' : 'far', 'fa-circle']"></i>
                                        </div>
                                        <p class="r-text">{{ comment.comment_text }}</p>

                                        <div v-if="comment.images && comment.images.length > 0"
                                            class="comment-images-grid">
                                            <img v-for="(img, idx) in comment.images" :key="idx" :src="getImageUrl(img)"
                                                @click="openLightboxWith(comment.images, idx)" />
                                        </div>

                                        <div class="comment-footer">
                                            <button class="btn-like-small" :class="{ active: isLiked(comment) }"
                                                @click="handleLike(comment)">
                                                <i :class="[isLiked(comment) ? 'fas' : 'far', 'fa-heart']"></i>
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
                    <div class="sidebar-card rating-summary-card">
                        <h3 style="font-size: 1rem; font-weight: 800; margin: 0 0 16px; color: #1e293b;">{{
                            t('place.travelerReviews') }}</h3>
                        <div class="rating-overview">
                            <div class="big-score">
                                <span class="score-number">{{ place.rating_avg ? parseFloat(place.rating_avg).toFixed(1)
                                    : '0.0' }}</span>
                                <div class="score-bubbles">
                                    <i v-for="s in 5" :key="'sb-' + s"
                                        :class="[(place.rating_avg || 0) >= s ? 'fas' : 'far', 'fa-circle']"></i>
                                </div>
                                <span class="score-label">{{ t('place.ratingLabels')[Math.round(place.rating_avg || 0) -
                                    1] || 'N/A' }}</span>
                                <span class="score-count">({{ comments.length }})</span>
                            </div>
                            <div class="score-bars">
                                <div v-for="lvl in ratingBreakdown" :key="lvl.value" class="score-bar-row">
                                    <span class="bar-label">{{ t('place.ratingLabels')[lvl.value - 1] }}</span>
                                    <div class="bar-track">
                                        <div class="bar-fill" :style="{ width: lvl.percent + '%' }"></div>
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
                <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px;">
                    <div>
                        <h2>Location</h2>
                        <p class="map-address" style="margin: 0;"><i class="fas fa-map-marker-alt"></i> {{ addressText
                            }}</p>
                    </div>
                    <button class="btn-action" @click="openGoogleMaps">
                        <i class="fas fa-external-link-alt"></i> Open in Maps
                    </button>
                </div>
                <div class="large-map-container" v-if="place.location_lat && place.location_lng">
                    <div id="detail-map"
                        style="width: 100%; height: 450px; border-radius: 12px; z-index: 1; border: 1px solid #e2e8f0; overflow:hidden;">
                    </div>
                </div>
            </div>

            <div class="nearby-section" v-if="nearbyRestaurants.length > 0 || nearbyAttractions.length > 0">
                <div class="nearby-grid">
                    <div class="nearby-col getting-there-col">
                        <h3>Getting there</h3>
                        <div class="walk-score-box">
                            <div class="score-text">
                                <span class="score-title">Somewhat walkable <i class="fas fa-info-circle"></i></span>
                                <span class="score-desc">Grade: 64 out of 100</span>
                            </div>
                            <div class="score-number">64</div>
                        </div>
                        <div class="airport-info">
                            <p><i class="fas fa-plane"></i> <strong>Savannakhet Airport</strong></p>
                            <span class="distance-line"><i class="fas fa-car side-icon"></i> 1.2 miles</span>
                        </div>
                    </div>

                    <div class="nearby-col">
                        <div class="col-header">
                            <div>
                                <h3>{{ nearbyRestaurantsTotal }} Restaurants</h3>
                                <span>within 0.75 miles</span>
                            </div>
                            <button class="btn-text-link" @click="openMapOverlay">View on map</button>
                        </div>

                        <div class="nearby-list">
                            <div v-for="n in nearbyRestaurants" :key="n.id" class="nearby-item"
                                @click="goToRecDetail(n.id)">
                                <h4>{{ n.name }}</h4>
                                <div class="n-rating">
                                    <span class="n-score">{{ n.rating_avg || '0.0' }}</span>
                                    <div class="bubbles">
                                        <i v-for="s in 5" :key="s"
                                            :class="[(n.rating_avg || 0) >= s ? 'fas' : 'far', 'fa-circle']"></i>
                                    </div>
                                    <span class="n-reviews">({{ getCommentCountText(n) }} reviews)</span>
                                </div>
                                <div class="n-meta">
                                    <i class="fas fa-walking"></i> {{ getDistanceText(n._distance) }} <span
                                        class="dot-divider">•</span> $$ - $$$ <span class="dot-divider">•</span> {{
                                    getCategoryName(n.category_id) }}
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="nearby-col right-col">
                        <div class="col-header">
                            <div>
                                <h3>{{ nearbyAttractionsTotal }} Attractions</h3>
                                <span>within 0.75 miles</span>
                            </div>
                            <button class="btn-text-link" @click="openMapOverlay">View on map</button>
                        </div>

                        <div class="nearby-list">
                            <div v-for="n in nearbyAttractions" :key="n.id" class="nearby-item"
                                @click="goToRecDetail(n.id)">
                                <h4>{{ n.name }}</h4>
                                <div class="n-rating">
                                    <span class="n-score">{{ n.rating_avg || '0.0' }}</span>
                                    <div class="bubbles">
                                        <i v-for="s in 5" :key="s"
                                            :class="[(n.rating_avg || 0) >= s ? 'fas' : 'far', 'fa-circle']"></i>
                                    </div>
                                    <span class="n-reviews">({{ getCommentCountText(n) }} reviews)</span>
                                </div>
                                <div class="n-meta">
                                    <i class="fas fa-walking"></i> {{ getDistanceText(n._distance) }} <span
                                        class="dot-divider">•</span> {{ getCategoryName(n.category_id) }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="recommended-section" v-if="aiRecommendedPlaces.length > 0">
                <h2 style="color: #6366f1; font-weight: 800; display: flex; align-items: center; gap: 10px;">
                    <i class="fas fa-magic"></i> {{ t('recommend.ai_recom') }}
                </h2>
                <p style="color: #64748b; margin-top: -10px; margin-bottom: 20px;">{{ t('recommend.ai_desc') }}</p>
                <div class="recommended-grid">
                    <div v-for="rec in aiRecommendedPlaces" :key="rec.place.id" class="rec-card"
                        @click="goToRecDetail(rec.place.id)"
                        style="border: 2px solid #e0e7ff; box-shadow: 0 10px 25px rgba(99,102,241,0.15); transform: translateY(-5px); transition: 0.3s; cursor: pointer;">
                        <div class="rec-img-wrapper" style="position: relative;">
                            <img :src="getRecCoverImage(rec.place)" :alt="rec.place.name" />
                            <span
                                style="position: absolute; top: 12px; left: 12px; background: #6366f1; color: white; padding: 5px 10px; border-radius: 8px; font-size: 0.8rem; font-weight: 700; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
                                <i class="fas fa-sparkles"></i> AI Pick
                            </span>
                        </div>
                        <div class="rec-info" style="padding: 18px;">
                            <h4 style="font-size: 1.15rem; color: #1e293b; font-weight: 800; margin-bottom: 12px;">{{
                                rec.place.name }}</h4>
                            <div
                                style="background: #fefce8; color: #b45309; font-size: 0.85rem; padding: 10px 12px; border-radius: 8px; margin-bottom: 15px; font-weight: 600; border: 1px solid #fef08a;">
                                <i class="fas fa-lightbulb" style="color: #f59e0b; margin-right: 5px;"></i> {{
                                rec.reason }}
                            </div>
                            <div class="rec-rating"
                                style="display: flex; justify-content: space-between; align-items: center; color: #00aa6c; font-weight: 700;">
                                <span class="bubbles">
                                    <i v-for="s in 5" :key="s"
                                        :class="[(rec.place.rating_avg || 0) >= s ? 'fas' : 'far', 'fa-circle']"
                                        style="margin-right:2px;"></i>
                                </span>
                                <span>{{ t('place.scoreString') }} {{ rec.place.rating_avg || '0.0' }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="recommended-section" v-if="similarPlaces.length > 0">
                <h2 style="color: #0ea5e9; font-weight: 800; display: flex; align-items: center; gap: 10px;">
                    <i class="fas fa-project-diagram"></i> ผู้ที่สนใจสถานที่นี้ มักจะชอบ...
                </h2>
                <div class="recommended-grid">
                    <div v-for="rec in similarPlaces" :key="rec.place.id" class="rec-card"
                        @click="goToRecDetail(rec.place.id)"
                        style="border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; cursor: pointer; transition: 0.3s;">
                        <div class="rec-img-wrapper">
                            <img :src="getRecCoverImage(rec.place)" :alt="rec.place.name"
                                style="width: 100%; height: 180px; object-fit: cover;" />
                        </div>
                        <div class="rec-info" style="padding: 15px;">
                            <h4 style="font-size: 1.1rem; color: #1e293b; font-weight: 700; margin-bottom: 8px;">{{
                                rec.place.name }}</h4>
                            <div style="color: #64748b; font-size: 0.85rem; margin-bottom: 12px;">
                                <i class="fas fa-info-circle"></i> {{ rec.reason }}
                            </div>
                            <div class="rec-rating"
                                style="display: flex; justify-content: space-between; align-items: center; color: #00aa6c; font-weight: 700;">
                                <span class="bubbles">
                                    <i v-for="s in 5" :key="s"
                                        :class="[(rec.place.rating_avg || 0) >= s ? 'fas' : 'far', 'fa-circle']"
                                        style="margin-right:2px;"></i>
                                </span>
                                <span>{{ rec.place.rating_avg || '0.0' }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="recommended-section" v-else-if="recommendedPlaces.length > 0">
                <h2>{{ t('place.recommended') }}</h2>
                <div class="recommended-grid">
                    <div v-for="rec in recommendedPlaces" :key="rec.id" class="rec-card" @click="goToRecDetail(rec.id)">
                        <div class="rec-img-wrapper">
                            <img :src="getRecCoverImage(rec)" :alt="rec.name" />
                        </div>
                        <div class="rec-info">
                            <h4>{{ rec.name }}</h4>
                            <div class="rec-rating">
                                <span class="bubbles">
                                    <i v-for="s in 5" :key="s"
                                        :class="[(rec.rating_avg || 0) >= s ? 'fas' : 'far', 'fa-circle']"></i>
                                </span>
                                <span>{{ rec.rating_avg || '0.0' }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div v-else class="loading-screen">
            <div class="spinner"></div>
            <p>{{ t('common.loading') }}</p>
        </div>

        <div v-if="isLightboxOpen" class="lightbox-overlay" @click="closeLightbox" @wheel.prevent="handleScrollZoom">
            <button class="btn-close-lightbox" @click="closeLightbox"><i class="fas fa-times"></i></button>
            <button v-if="activeLightboxImages.length > 1" class="btn-nav prev" @click.stop="prevImage"><i
                    class="fas fa-chevron-left"></i></button>
            <img :src="activeLightboxImages[currentImageIndex]" class="lightbox-img"
                :style="{ transform: `scale(${zoomLevel})` }" @click.stop />
            <button v-if="activeLightboxImages.length > 1" class="btn-nav next" @click.stop="nextImage"><i
                    class="fas fa-chevron-right"></i></button>
        </div>

        <div class="like-popup" :class="{ 'show': showLikePopup }">
            <div class="popup-header">
                <div class="icon-circle"><i class="fas fa-heart" style="color: #ef4444;"></i></div>
                <div>
                    <h4 style="margin: 0; font-size: 1rem; font-weight: 700; color: #1e293b;">บันทึกสถานที่สำเร็จ!</h4>
                    <p style="margin: 0; font-size: 0.85rem; color: #64748b;">คุณอาจจะติดใจสถานที่ระดับแนะนำเหล่านี้ด้วย
                    </p>
                </div>
                <button @click="showLikePopup = false" class="close-popup"><i class="fas fa-times"></i></button>
            </div>
            <div class="popup-body" v-if="similarPlaces.length > 0">
                <div v-for="rec in similarPlaces.slice(0, 2)" :key="'pop-' + rec.place.id" class="popup-rec-item"
                    @click="goToRecDetail(rec.place.id)">
                    <img :src="getRecCoverImage(rec.place)" alt="" />
                    <div class="popup-rec-info">
                        <strong>{{ rec.place.name }}</strong>
                        <span><i class="fas fa-star" style="color: #eab308;"></i> {{ rec.place.rating_avg || '0.0'
                            }}</span>
                    </div>
                </div>
            </div>
        </div>

        <MapOverlay v-if="place" :is-open="showMapModal" :places="allPlaces" :categories="categories"
            :initial-selected-id="place.id" title="Explore Places" @close="showMapModal = false" />
    </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { placeRepository } from '@/repositories/placeRepository'
import { categoryRepository } from '@/repositories/categoryRepository'
import { favoriteRepository } from '@/repositories/favoriteRepository'
import { gnnRepository } from '@/repositories/gnnRepository'
import { useI18n } from '@/composables/useI18n'
import Navbar from '@/components/Navbar.vue'
import MapOverlay from '@/components/MapOverlay.vue'
import SectionDivider from '@/components/SectionDivider.vue'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const place = ref(null)
const categories = ref([])
const comments = ref([])
const user = ref(JSON.parse(localStorage.getItem('user')))
const isFavorite = ref(false)
const reviewSuccess = ref(false)
const addressText = ref(t('common.loading'))
const showMapModal = ref(false)
const allPlaces = ref([])
const aiRecommendedPlaces = ref([])
const similarPlaces = ref([])
const showLikePopup = ref(false)

const newComment = ref('')
const newRating = ref(5)
const submitting = ref(false)

const reviewImages = ref([])
const reviewImagesPreviews = ref([])

const editingCommentId = ref(null)
const editCommentText = ref('')
const editRating = ref(5)
const showDropdownFor = ref(null)

// 🚨 ตัวแปร State ใหม่สำหรับเก็บรูปใน Lightbox
const activeLightboxImages = ref([]);

const toggleDropdown = (id) => {
    showDropdownFor.value = showDropdownFor.value === id ? null : id
}

const startEdit = (comment) => {
    editingCommentId.value = comment.id
    editCommentText.value = comment.comment_text || ''
    editRating.value = comment.rating || 5
    showDropdownFor.value = null
}

const cancelEdit = () => {
    editingCommentId.value = null
    editCommentText.value = ''
    editRating.value = 5
}

const saveEdit = async (commentId) => {
    if (!editCommentText.value.trim()) return
    try {
        const formData = new FormData()
        formData.append('user_id', user.value.id)
        formData.append('rating', editRating.value)
        formData.append('comment_text', editCommentText.value)

        await placeRepository.updateUserReview(commentId, formData)

        const comment = comments.value.find(c => c.id === commentId)
        if (comment) {
            comment.comment_text = editCommentText.value
            comment.rating = editRating.value
        }
        cancelEdit()
        fetchData()
    } catch (err) {
        console.error("Failed to update comment", err)
    }
}

const deleteReview = async (commentId) => {
    if (!confirm('Are you sure you want to delete this review?')) return
    showDropdownFor.value = null
    try {
        await placeRepository.deleteUserReview(commentId, user.value.id)
        comments.value = comments.value.filter(c => c.id !== commentId)
        fetchData()
    } catch (err) {
        console.error("Failed to delete review", err)
    }
}

const handleReviewImages = (e) => {
    const files = Array.from(e.target.files)
    files.forEach(file => {
        reviewImages.value.push(file)
        reviewImagesPreviews.value.push(URL.createObjectURL(file))
    })
}

const removeReviewImage = (idx) => {
    reviewImages.value.splice(idx, 1)
    reviewImagesPreviews.value.splice(idx, 1)
}

// Booking date pickers
const today = new Date()
const tomorrow = new Date(today); tomorrow.setDate(tomorrow.getDate() + 1)
const dayAfter = new Date(today); dayAfter.setDate(dayAfter.getDate() + 2)
const bookingCheckin = ref(tomorrow.toISOString().split('T')[0])
const bookingCheckout = ref(dayAfter.toISOString().split('T')[0])

const currentImageIndex = ref(0)
const isLightboxOpen = ref(false)
const zoomLevel = ref(1)

const galleryImages = computed(() => {
    const getValidImageUrl = (rawUrl) => {
        if (!rawUrl) return null;
        let url = rawUrl;
        if (typeof url === 'string' && url.trim().startsWith('[')) {
            try {
                const parsed = JSON.parse(url);
                if (Array.isArray(parsed) && parsed.length > 0) url = parsed[0];
            } catch (e) {
                url = url.replace(/^\["?|"?\]$/g, '').replace(/\\"/g, '');
            }
        }
        if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) return url;
        return `http://localhost:8000${url.startsWith('/') ? '' : '/'}${url}`;
    }

    if (place.value?.images && Array.isArray(place.value.images) && place.value.images.length > 0) {
        return place.value.images.map(img => getValidImageUrl(img.image_url || img.url || img));
    }
    else if (place.value?.image_url) {
        let parsedArray = [];
        if (typeof place.value.image_url === 'string' && place.value.image_url.trim().startsWith('[')) {
            try { parsedArray = JSON.parse(place.value.image_url); } catch (e) { }
        }
        if (parsedArray.length > 0) return parsedArray.map(img => getValidImageUrl(img));
        else return [getValidImageUrl(place.value.image_url)];
    }

    return ['data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22800%22%20height%3D%22450%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20fill%3D%22%23e2e8f0%22%2F%3E%3Ctext%20x%3D%2250%25%22%20y%3D%2250%25%22%20fill%3D%22%2364748b%22%20font-family%3D%22sans-serif%22%20font-size%3D%2224%22%20text-anchor%3D%22middle%22%20dy%3D%22.3em%22%3ENo%20Image%20Available%3C%2Ftext%3E%3C%2Fsvg%3E']
})

const isHotel = computed(() => {
    if (!place.value || !categories.value.length) return false;
    const cat = categories.value.find(c => c.id === place.value.category_id);
    return cat && (cat.name.toLowerCase().includes('hotel') || cat.parent_type === 'hotel');
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
        return levels.map(lvl => ({ value: lvl.value, count: 0, percent: 0 }));
    }

    const total = comments.value.length;
    return levels.map(lvl => {
        const count = comments.value.filter(c => Math.round(c.rating) === lvl.value).length;
        return { value: lvl.value, count, percent: Math.round((count / total) * 100) };
    });
});

const recommendedPlaces = computed(() => {
    if (!place.value || !allPlaces.value.length) return [];
    return allPlaces.value
        .filter(p => p.category_id === place.value.category_id && p.id !== place.value.id)
        .slice(0, 4);
});

// Haversine Distance Calculator
const getDistance = (lat1, lon1, lat2, lon2) => {
    if (!lat1 || !lon1 || !lat2 || !lon2) return null;
    const R = 6371; // km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = 0.5 - Math.cos(dLat) / 2 + Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * (1 - Math.cos(dLon)) / 2;
    return R * 2 * Math.asin(Math.sqrt(a));
}

const nearbyRestaurantsTotal = ref(0);
const nearbyAttractionsTotal = ref(0);

const nearbyRestaurants = computed(() => {
    if (!place.value || !allPlaces.value.length) return [];
    const lat1 = parseFloat(place.value.location_lat);
    const lng1 = parseFloat(place.value.location_lng);

    let filtered = allPlaces.value.filter(p => {
        if (p.id === place.value.id) return false;
        const cat = categories.value.find(c => c.id === p.category_id);
        if (!cat || cat.parent_type !== 'restaurant') return false;

        p._distance = getDistance(lat1, lng1, parseFloat(p.location_lat), parseFloat(p.location_lng));
        return p._distance === null || p._distance < 1.2; // roughly 0.75 miles
    }).sort((a, b) => (a._distance || 0) - (b._distance || 0));

    nearbyRestaurantsTotal.value = filtered.length;
    return filtered.slice(0, 4);
});

const nearbyAttractions = computed(() => {
    if (!place.value || !allPlaces.value.length) return [];
    const lat1 = parseFloat(place.value.location_lat);
    const lng1 = parseFloat(place.value.location_lng);

    let filtered = allPlaces.value.filter(p => {
        if (p.id === place.value.id) return false;
        const cat = categories.value.find(c => c.id === p.category_id);
        if (!cat || cat.parent_type === 'restaurant' || cat.parent_type === 'hotel') return false;

        p._distance = getDistance(lat1, lng1, parseFloat(p.location_lat), parseFloat(p.location_lng));
        return p._distance === null || p._distance < 1.2;
    }).sort((a, b) => (a._distance || 0) - (b._distance || 0));

    nearbyAttractionsTotal.value = filtered.length;
    return filtered.slice(0, 4);
});

const getDistanceText = (km) => {
    if (km === null || km === undefined) return "5 min";
    const min = Math.round(km * 12);
    return min < 1 ? "1 min" : min + " min";
}

const getCommentCountText = (pl) => {
    if (pl && pl.review_count !== undefined) {
        return pl.review_count;
    }
    return 0;
}

const getImageUrl = (url) => {
    if (!url) return '';
    if (url.startsWith('http') || url.startsWith('data:')) return url;
    return `http://localhost:8000/${url.startsWith('/') ? url.slice(1) : url}`;
}

const stickyNavRef = ref(null);
const isSticky = ref(false);
const activeSection = ref('about');

const handleScroll = () => {
    if (stickyNavRef.value) {
        const rect = stickyNavRef.value.getBoundingClientRect();
        isSticky.value = rect.top <= 0;
    }

    const sections = ['deals', 'about', 'location', 'reviews'];
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
        window.scrollTo({ top: y, behavior: 'smooth' });
    }
};

const getRecCoverImage = (p) => {
    let url = '';
    if (p.images && p.images.length > 0) {
        url = p.images[0].image_url || p.images[0].url || p.images[0];
    } else if (p.image_url) {
        try {
            if (p.image_url.startsWith('[')) url = JSON.parse(p.image_url)[0];
            else url = p.image_url;
        } catch (e) { url = p.image_url; }
    }
    if (!url) return 'https://via.placeholder.com/300x200?text=No+Image';
    return url.startsWith('http') ? url : `http://localhost:8000/${url.replace(/^\//, '')}`;
};

const goToRecDetail = (id) => {
    router.push(`/places/${id}`);
};

watch(() => route.params.id, (newId, oldId) => {
    if (newId && newId !== oldId) {
        fetchData()
        window.scrollTo({ top: 0, behavior: 'smooth' })
    }
})

let detailMap = null;
let mapMarkers = [];

const initDetailMap = () => {
    if (!window.L) return;
    if (!place.value || !place.value.location_lat || !place.value.location_lng) return;

    if (detailMap) {
        detailMap.remove();
        detailMap = null;
    }

    const lat = parseFloat(place.value.location_lat);
    const lng = parseFloat(place.value.location_lng);

    detailMap = window.L.map('detail-map', {
        zoomControl: false,
        scrollWheelZoom: false
    }).setView([lat, lng], 14);

    window.L.control.zoom({ position: 'bottomright' }).addTo(detailMap);

    window.L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '© OpenStreetMap contributors © CARTO'
    }).addTo(detailMap);

    mapMarkers = [];

    const createMarker = (p, isTarget = false) => {
        const pLat = parseFloat(p.location_lat);
        const pLng = parseFloat(p.location_lng);
        if (isNaN(pLat) || isNaN(pLng)) return;

        let ratingText = p.rating_avg ? parseFloat(p.rating_avg).toFixed(1) : '<i class="fas fa-map-marker-alt"></i>';
        const markerHtml = `
            <div class="custom-marker pill-style ${isTarget ? 'selected' : ''}">
                <span class="m-text">${ratingText}</span>
            </div>
        `;
        const customIcon = window.L.divIcon({
            html: markerHtml,
            className: 'empty-leaflet-icon',
            iconSize: [40, 26],
            iconAnchor: [20, 26],
            popupAnchor: [0, -28]
        });

        let marker = window.L.marker([pLat, pLng], { icon: customIcon }).addTo(detailMap);
        mapMarkers.push(marker);

        const bubblesHtml = [1, 2, 3, 4, 5].map(s => `<i class="${(p.rating_avg || 0) >= s ? 'fas' : 'far'} fa-circle"></i>`).join('');
        const popupContentHtml = `
            <div class="leaflet-custom-card" onclick="window.open('/places/${p.id}', '_blank')" style="cursor:pointer; display:flex; flex-direction:column; background:white; font-family:'Inter', sans-serif;">
                <div style="height: 120px; width: 100%;">
                    <img src="${getRecCoverImage(p)}" style="width:100%; height:100%; object-fit:cover;" />
                </div>
                <div style="padding: 12px; color:#0f172a;">
                    <h3 style="margin: 0 0 4px; font-size: 1rem; font-weight: 800; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${p.name}</h3>
                    <div style="display:flex; align-items:center;">
                        <span style="color:#00aa6c; font-size:0.75rem;">${bubblesHtml}</span>
                        <span style="color:#64748b; font-size:0.75rem; margin-left:6px; font-weight:600;">(${p.rating_avg || '0.0'})</span>
                    </div>
                </div>
            </div>
        `;
        marker.bindPopup(popupContentHtml, { closeButton: false, className: 'custom-tripadvisor-popup' });
        if (isTarget) {
            setTimeout(() => marker.openPopup(), 500);
        }
    }

    createMarker(place.value, true);

    const allNearby = [...nearbyRestaurants.value, ...nearbyAttractions.value];
    allNearby.forEach(p => createMarker(p, false));

    if (mapMarkers.length > 1) {
        const group = window.L.featureGroup(mapMarkers);
        // add slight delay to fit bounds correctly
        setTimeout(() => {
            if (detailMap) detailMap.fitBounds(group.getBounds(), { padding: [50, 50], maxZoom: 16 });
        }, 100);
    }
}

const handleScrollZoom = (e) => {
    const zoomStep = 0.15;
    if (e.deltaY < 0) zoomLevel.value = Math.min(zoomLevel.value + zoomStep, 5);
    else zoomLevel.value = Math.max(zoomLevel.value - zoomStep, 0.5);
}

// 🚨 อัปเดตฟังก์ชัน Lightbox 🚨
const openLightbox = () => {
    // 1. นำรูปจากอัลบั้มหลัก ไปแสดงใน Lightbox
    activeLightboxImages.value = galleryImages.value;
    isLightboxOpen.value = true;
    currentImageIndex.value = 0;
    zoomLevel.value = 1;
    document.body.style.overflow = 'hidden';
}

// 🚨 อัปเดตฟังก์ชัน Lightbox 🚨
const openLightboxWith = (images, idx) => {
    // 2. นำรูปรวมถึงแปลง URL จากคอมเมนต์ผู้ใช้ ไปแสดงใน Lightbox
    activeLightboxImages.value = images.map(img => getImageUrl(img));
    isLightboxOpen.value = true;
    currentImageIndex.value = idx;
    zoomLevel.value = 1;
    document.body.style.overflow = 'hidden';
}

const closeLightbox = () => {
    isLightboxOpen.value = false;
    zoomLevel.value = 1;
    document.body.style.overflow = 'auto';
}

const nextImage = () => {
    zoomLevel.value = 1;
    if (currentImageIndex.value < activeLightboxImages.value.length - 1) {
        currentImageIndex.value++;
    } else {
        currentImageIndex.value = 0;
    }
}

const prevImage = () => {
    zoomLevel.value = 1;
    if (currentImageIndex.value > 0) {
        currentImageIndex.value--;
    } else {
        currentImageIndex.value = activeLightboxImages.value.length - 1;
    }
}

const handleKeydown = (e) => {
    if (!isLightboxOpen.value) return;
    if (e.key === 'Escape') closeLightbox()
    if (e.key === 'ArrowRight') nextImage()
    if (e.key === 'ArrowLeft') prevImage()
}

onMounted(() => {
    fetchData()
    window.addEventListener('keydown', handleKeydown)
    window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeydown)
    window.removeEventListener('scroll', handleScroll)
    document.body.style.overflow = 'auto'
    if (detailMap) {
        detailMap.remove();
        detailMap = null;
    }
})

const fetchData = async () => {
    const id = route.params.id
    try {
        const [resPlace, resCats, resAll] = await Promise.all([
            placeRepository.getById(id),
            categoryRepository.getAll(),
            placeRepository.getAll()
        ])
        place.value = resPlace.data
        categories.value = resCats.data
        allPlaces.value = resAll.data

        // แปลงพิกัดเป็นชื่อสถานที่ (Reverse Geocoding)
        if (place.value.location_lat && place.value.location_lng) {
            const lat = parseFloat(place.value.location_lat)
            const lng = parseFloat(place.value.location_lng)

            try {
                const mapRes = await axios.get(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&accept-language=th,en`)
                if (mapRes.data && mapRes.data.display_name) {
                    const parts = mapRes.data.display_name.split(', ')
                    addressText.value = parts.length > 3 ? parts.slice(0, 3).join(', ') : mapRes.data.display_name
                } else {
                    addressText.value = `📍 พิกัด (Lat: ${lat.toFixed(4)}, Lng: ${lng.toFixed(4)})`
                }
            } catch (e) {
                addressText.value = `📍 พิกัด (Lat: ${lat.toFixed(4)}, Lng: ${lng.toFixed(4)})`
            }
        } else {
            addressText.value = 'ไม่พบข้อมูลตำแหน่ง'
        }

        // --- Save to recently_viewed in localStorage ---
        let rv = JSON.parse(localStorage.getItem('recently_viewed') || '[]')
        rv = rv.filter(item => item !== parseInt(id))
        rv.unshift(parseInt(id))
        if (rv.length > 8) rv.pop()
        localStorage.setItem('recently_viewed', JSON.stringify(rv))

        if (user.value && user.value.role !== 'admin') {
            const favRes = await favoriteRepository.getUserFavorites(user.value.id)
            isFavorite.value = favRes.data.some(f => f.place_id === parseInt(id))

            // Log 'view' action for GNN
            try {
                await gnnRepository.logInteraction({
                    user_id: user.value.id,
                    place_id: parseInt(id),
                    action_type: 'view'
                })
            } catch (gnnErr) { console.warn("Failed to log view", gnnErr) }

            // Fetch AI recommendations
            try {
                const recRes = await gnnRepository.getRecommendations(user.value.id)
                if (recRes.data && recRes.data.recommended_places) {
                    aiRecommendedPlaces.value = recRes.data.recommended_places
                        .filter(r => r.place && r.place.id !== parseInt(id))
                        .slice(0, 4);
                }
            } catch (recErr) { console.warn("No AI recommendations", recErr) }

            // Fetch Similar Places
            try {
                const simRes = await gnnRepository.getSimilarPlaces(id)
                if (simRes.data && simRes.data.similar_places) {
                    similarPlaces.value = simRes.data.similar_places
                        .filter(r => r.place && r.place.id !== parseInt(id))
                        .slice(0, 3)
                }
            } catch (simErr) { console.warn("Failed to fetch similar places", simErr) }
        }

        try {
            const resComm = await placeRepository.getComments(id)
            comments.value = resComm.data
        } catch (e) { comments.value = [] }

        nextTick(() => {
            initDetailMap();
        });
    } catch (err) { console.error(err) }
}

const submitComment = async () => {
    if (!user.value) return router.push('/login')
    if (!newComment.value.trim()) return

    submitting.value = true
    reviewSuccess.value = false
    try {
        const formData = new FormData()
        formData.append('place_id', route.params.id)
        formData.append('user_id', user.value.id)
        formData.append('rating', newRating.value)
        formData.append('comment_text', newComment.value)

        reviewImages.value.forEach(file => {
            formData.append('images', file)
        })

        await placeRepository.addComment(formData)

        try {
            await gnnRepository.logInteraction({
                user_id: user.value.id,
                place_id: parseInt(route.params.id),
                action_type: 'review',
                score: newRating.value
            });
        } catch (aiErr) { console.warn("AI Log failed", aiErr); }

        newComment.value = ''
        newRating.value = 5
        reviewImages.value = []
        reviewImagesPreviews.value = []
        reviewSuccess.value = true
        setTimeout(() => reviewSuccess.value = false, 3000)
        fetchData()
    } catch (err) { console.error(err) } finally { submitting.value = false }
}

const handleLike = async (comment) => {
    if (!user.value) return alert('Please login to like')
    try {
        const res = await placeRepository.toggleLike(comment.id, user.value.id)
        if (res.data.status === 'liked') {
            if (!comment.liked_by) comment.liked_by = []
            comment.liked_by.push(user.value.id)
        } else {
            comment.liked_by = comment.liked_by.filter(id => id !== user.value.id)
        }
    } catch (err) { console.error("Like failed", err) }
}

const isLiked = (comment) => {
    return user.value && comment.liked_by && comment.liked_by.includes(user.value.id)
}

const toggleHeart = async () => {
    if (!user.value) return router.push('/login')
    try {
        const res = await favoriteRepository.toggleFavorite(user.value.id, route.params.id)
        isFavorite.value = res.data.status === 'added'

        if (isFavorite.value) {
            try {
                await gnnRepository.logInteraction({
                    user_id: user.value.id,
                    place_id: parseInt(route.params.id),
                    action_type: 'like'
                });

                // Show Popup after liking
                if (similarPlaces.value.length > 0) {
                    showLikePopup.value = true;
                    setTimeout(() => {
                        showLikePopup.value = false;
                    }, 6000);
                }
            } catch (err) { console.warn("AI Log failed", err); }
        }
    } catch (err) { console.error(err) }
}

const getCategoryName = (id) => categories.value.find(c => c.id === id)?.name || 'General'
const openMapOverlay = () => { showMapModal.value = true }

// 🚨 อัปเดตฟังก์ชันกดดู Google Maps ของจริง 🚨
const openGoogleMaps = () => {
    if (place.value?.location_lat && place.value?.location_lng) {
        window.open(`https://maps.google.com/?q=${place.value.location_lat},${place.value.location_lng}`, '_blank');
    }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

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
    font-family: 'Inter', sans-serif;
}

:deep(.custom-marker.pill-style::after) {
    content: '';
    position: absolute;
    bottom: -6px;
    left: 50%;
    transform: translateX(-50%);
    border-width: 6px 6px 0;
    border-style: solid;
    border-color: white transparent transparent transparent;
}

:deep(.custom-marker.pill-style::before) {
    content: '';
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
.ta-detail-page {
    background-color: #f7f9fa;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    color: #1e293b;
}

.ta-container {
    max-width: 1140px;
    margin: 0 auto;
    padding: 20px 20px 60px;
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

.icon-circle {
    width: 40px;
    height: 40px;
    background: #fee2e2;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
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
    font-family: 'Inter', sans-serif;
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
    font-family: 'Inter', sans-serif;
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
    content: '';
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
.sidebar-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    position: sticky;
    top: 90px;
    margin-bottom: 16px;
}

.sidebar-card h3 {
    margin: 0 0 15px;
    font-size: 1.1rem;
    font-weight: 800;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 10px;
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

.bcc-date-field>i {
    color: #0ea5e9;
    font-size: 1rem;
    flex-shrink: 0;
}

.bcc-date-field>div {
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
    font-family: 'Inter', sans-serif;
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

.bcc-price-col {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    padding-right: 8px;
}

.bcc-price-original {
    font-size: 0.78rem;
    color: #94a3b8;
    text-decoration: line-through;
    font-weight: 500;
}

.bcc-price {
    font-size: 0.88rem;
    font-weight: 700;
    color: #64748b;
}

.bcc-price-sale {
    font-size: 1.1rem;
    font-weight: 800;
    color: #0f172a;
}

.bcc-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 9px 14px;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 700;
    text-decoration: none;
    transition: 0.2s;
    white-space: nowrap;
    flex-shrink: 0;
}

.bcc-btn i {
    font-size: 0.7rem;
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

.popup-icon {
    font-size: 0.7rem;
    opacity: 0.8;
}

/* Recommended Places Section */
.recommended-section {
    margin-top: 40px;
    padding-top: 30px;
    border-top: 1px solid #e2e8f0;
}

.recommended-section h2 {
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: 20px;
    color: #0f172a;
}

.recommended-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
}

.rec-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
    cursor: pointer;
    transition: 0.2s;
}

.rec-card:hover {
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
}

.rec-img-wrapper {
    height: 140px;
    width: 100%;
}

.rec-img-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.rec-info {
    padding: 12px;
}

.rec-info h4 {
    margin: 0 0 8px;
    font-size: 0.95rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.3;
}

.rec-rating {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 0.8rem;
    color: #475569;
    font-weight: 600;
}

.rec-rating i {
    color: #00aa6c;
}

/* Large Map Section */
.large-map-section {
    margin-top: 40px;
    padding-top: 30px;
    border-top: 1px solid #e2e8f0;
}

.large-map-section h2 {
    font-size: 1.5rem;
    font-weight: 800;
    margin: 0 0 10px;
    color: #0f172a;
}

.map-address {
    font-size: 1rem;
    color: #475569;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.large-map-container {
    width: 100%;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
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

/* Getting there column */
.getting-there-col {
    padding-right: 20px;
}

.getting-there-col h3 {
    border-bottom: none;
    margin-bottom: 20px;
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

.score-title i {
    color: #64748b;
    font-size: 0.8rem;
}

.score-desc {
    font-size: 0.8rem;
    color: #475569;
}

.score-number {
    font-size: 1.8rem;
    font-weight: 800;
    color: #00aa6c;
}

.airport-info p {
    margin: 0 0 5px;
    font-size: 0.95rem;
}

.airport-info i {
    color: #64748b;
    margin-right: 8px;
}

.distance-line {
    font-size: 0.85rem;
    color: #475569;
    padding-left: 24px;
}

.side-icon {
    font-size: 0.8rem !important;
    margin-right: 4px !important;
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

.nearby-item:last-child {
    border-bottom: none;
}

.nearby-item:hover h4 {
    text-decoration: underline;
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

.n-score {
    font-weight: 700;
}

.n-rating .bubbles i {
    color: #00aa6c;
    font-size: 0.75rem;
}

.n-reviews {
    color: #475569;
    font-size: 0.8rem;
    text-decoration: underline;
}

.n-meta {
    font-size: 0.85rem;
    color: #475569;
}

.n-meta i {
    color: #94a3b8;
    margin-right: 4px;
}

@media (max-width: 992px) {
    .nearby-grid {
        grid-template-columns: 1fr;
        gap: 40px;
    }

    .getting-there-col {
        padding-right: 0;
        border-right: none;
    }
}

@media (max-width: 992px) {
    .recommended-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 480px) {
    .recommended-grid {
        grid-template-columns: 1fr;
    }
}

/* 🚨 CSS สำหรับ Lightbox (ดูรูปเต็มจอ) ที่ใส่เพิ่มให้แล้ว 🚨 */
.lightbox-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.92);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 99999;
}

.lightbox-img {
    max-width: 90vw;
    max-height: 90vh;
    object-fit: contain;
    transition: transform 0.2s ease-out;
    user-select: none;
    border-radius: 8px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.btn-close-lightbox {
    position: absolute;
    top: 25px;
    right: 35px;
    background: rgba(255, 255, 255, 0.1);
    border: none;
    color: white;
    font-size: 1.8rem;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    cursor: pointer;
    z-index: 100000;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn-close-lightbox:hover {
    background: #ef4444;
    transform: scale(1.1);
}

.btn-nav {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(255, 255, 255, 0.1);
    border: none;
    color: white;
    font-size: 2rem;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    cursor: pointer;
    z-index: 100000;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(4px);
}

.btn-nav:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-50%) scale(1.1);
}

.btn-nav.prev {
    left: 30px;
}

.btn-nav.next {
    right: 30px;
}
</style>