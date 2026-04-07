<template>
    <div class="hotels-page">
        <Navbar />

        <div class="hotel-search-header">
            <div class="search-container">
                <h1>Hotels in Savannakhet</h1>
                
                <div class="booking-bar">
                    <div class="booking-input destination">
                        <i class="fas fa-map-marker-alt"></i>
                        <div class="input-content">
                            <label>Where to?</label>
                            <input type="text" value="Savannakhet, Laos" readonly />
                        </div>
                    </div>
                    
                    <div class="booking-divider"></div>
                    
                    <div class="booking-input dates">
                        <i class="far fa-calendar-alt"></i>
                        <div class="input-content">
                            <label>Check In - Check Out</label>
                            <input type="text" placeholder="Add dates" />
                        </div>
                    </div>
                    
                    <div class="booking-divider"></div>
                    
                    <div class="booking-input guests">
                        <i class="far fa-user"></i>
                        <div class="input-content">
                            <label>Guests</label>
                            <input type="text" value="2 adults, 1 room" readonly />
                        </div>
                    </div>
                    
                    <button class="btn-update-search">Update</button>
                </div>
            </div>
        </div>

        <div class="main-layout">
            <aside class="filter-sidebar">
                <div class="map-preview">
                    <img src="https://images.unsplash.com/photo-1524661135-423995f22d0b?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80" alt="Map View" />
                    <button class="btn-view-map"><i class="fas fa-map"></i> View on map</button>
                </div>

                <div class="filter-group">
                    <h3>Popular Filters</h3>
                    <label class="filter-checkbox"><input type="checkbox" checked /> <span>Pool</span></label>
                    <label class="filter-checkbox"><input type="checkbox" checked /> <span>Free Breakfast</span></label>
                    <label class="filter-checkbox"><input type="checkbox" /> <span>Free Wifi</span></label>
                    <label class="filter-checkbox"><input type="checkbox" /> <span>Spa</span></label>
                </div>

                <div class="filter-divider"></div>

                <div class="filter-group">
                    <h3>Property Class (Stars)</h3>
                    <label class="filter-checkbox"><input type="checkbox" /> <span class="stars"><i class="fas fa-star" v-for="i in 5" :key="'5s'+i"></i></span></label>
                    <label class="filter-checkbox"><input type="checkbox" /> <span class="stars"><i class="fas fa-star" v-for="i in 4" :key="'4s'+i"></i></span></label>
                    <label class="filter-checkbox"><input type="checkbox" /> <span class="stars"><i class="fas fa-star" v-for="i in 3" :key="'3s'+i"></i></span></label>
                </div>
            </aside>

            <main class="hotel-list-area">
                <div class="list-header">
                    <h2>{{ hotels.length }} properties in Savannakhet</h2>
                    <div class="sort-by">
                        <span>Sort by:</span>
                        <select>
                            <option>Traveler Ranked</option>
                            <option>Price (Low to High)</option>
                            <option>Distance</option>
                        </select>
                    </div>
                </div>

                <div class="hotel-card" v-for="(hotel, index) in hotels" :key="hotel.id">
                    
                    <div class="hotel-img-wrapper">
                        <img :src="hotel.image" :alt="hotel.name" />
                        <button class="btn-heart" :class="{ active: hotel.isSaved }" @click="hotel.isSaved = !hotel.isSaved">
                            <i class="fas fa-heart"></i>
                        </button>
                        <div class="img-counter"><i class="fas fa-camera"></i> 1/12</div>
                    </div>

                    <div class="hotel-info">
                        <div class="rank-text" v-if="index === 0"><strong>#1 Best Value</strong> in Savannakhet</div>
                        <h3 class="hotel-name">{{ index + 1 }}. {{ hotel.name }}</h3>
                        
                        <div class="rating-row">
                            <span class="bubbles">
                                <i class="fas fa-circle"></i><i class="fas fa-circle"></i><i class="fas fa-circle"></i><i class="fas fa-circle"></i><i class="fas fa-circle-half-stroke"></i>
                            </span>
                            <span class="review-count">{{ hotel.reviews }} reviews</span>
                        </div>
                        
                        <div class="hotel-amenities">
                            <span v-if="hotel.hasWifi"><i class="fas fa-wifi"></i> Free Wifi</span>
                            <span v-if="hotel.hasPool"><i class="fas fa-swimming-pool"></i> Pool</span>
                            <span v-if="hotel.hasBreakfast"><i class="fas fa-coffee"></i> Free Breakfast</span>
                            <span v-if="hotel.hasParking"><i class="fas fa-parking"></i> Free Parking</span>
                        </div>

                        <p class="hotel-desc">
                            "{{ hotel.snippet }}"
                        </p>
                    </div>

                    <div class="hotel-deals">
                        <div class="deal-provider">
                            <span>Agoda.com</span>
                            <i class="fas fa-external-link-alt"></i>
                        </div>
                        <div class="deal-price">
                            <span class="price-strike" v-if="hotel.oldPrice">${{ hotel.oldPrice }}</span>
                            <span class="price-current">${{ hotel.price }}</span>
                        </div>
                        <button class="btn-view-deal">View Deal</button>
                        
                        <div class="other-deals">
                            <div class="mini-deal">
                                <span>Booking.com</span>
                                <strong>${{ hotel.price + 2 }}</strong>
                            </div>
                            <div class="mini-deal">
                                <span>Expedia</span>
                                <strong>${{ hotel.price + 5 }}</strong>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import Navbar from '../components/Navbar.vue' // นำเข้า Navbar ที่เราทำไว้

// ข้อมูลจำลองโรงแรมในสะหวันนะเขต (MOCK DATA)
const hotels = ref([
    {
        id: 1,
        name: "Daosavanh Resort & Spa",
        image: "https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        reviews: 142,
        price: 45,
        oldPrice: 55,
        hasWifi: true,
        hasPool: true,
        hasBreakfast: true,
        hasParking: true,
        snippet: "A beautiful resort right by the Mekong river. The pool is fantastic and the breakfast buffet has a great variety of Lao and Western food.",
        isSaved: true
    },
    {
        id: 2,
        name: "Avalon Residence",
        image: "https://images.unsplash.com/photo-1551882547-ff40c0d13c05?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        reviews: 98,
        price: 28,
        oldPrice: null,
        hasWifi: true,
        hasPool: false,
        hasBreakfast: true,
        hasParking: true,
        snippet: "Very clean and modern rooms right in the city center. Walking distance to the night market and famous cafes. Highly recommended for couples.",
        isSaved: false
    },
    {
        id: 3,
        name: "Pilgrim's Kitchen & Inn",
        image: "https://images.unsplash.com/photo-1505691938895-1758d7feb511?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        reviews: 215,
        price: 18,
        oldPrice: 22,
        hasWifi: true,
        hasPool: false,
        hasBreakfast: false,
        hasParking: false,
        snippet: "Best budget option in town! The food downstairs is amazing (try their burgers). The rooms are simple but have everything you need.",
        isSaved: false
    },
    {
        id: 4,
        name: "Macchiato Resort",
        image: "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        reviews: 76,
        price: 35,
        oldPrice: 40,
        hasWifi: true,
        hasPool: true,
        hasBreakfast: true,
        hasParking: true,
        snippet: "A hidden gem! The architecture is unique and the coffee served at the lobby is the best in Savannakhet.",
        isSaved: false
    }
])
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

.hotels-page {
    background-color: #f2f2f2; /* สีเทาอ่อนๆ แบบ TripAdvisor */
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    color: #1e293b;
}

/* --- 1. Booking Header Bar --- */
.hotel-search-header {
    background: white;
    padding: 30px 20px;
    border-bottom: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.02);
}

.search-container {
    max-width: 1200px;
    margin: 0 auto;
}

.search-container h1 {
    font-size: 2rem;
    font-weight: 800;
    margin: 0 0 20px;
    color: #000;
}

.booking-bar {
    display: flex;
    align-items: center;
    background: white;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    padding: 8px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.booking-input {
    display: flex;
    align-items: center;
    padding: 10px 20px;
    flex: 1;
    cursor: pointer;
    border-radius: 8px;
    transition: 0.2s;
}

.booking-input:hover { background: #f8fafc; }
.booking-input i { font-size: 1.4rem; color: #000; margin-right: 15px; }

.input-content { display: flex; flex-direction: column; }
.input-content label { font-size: 0.75rem; font-weight: 700; color: #475569; text-transform: uppercase; margin-bottom: 2px; cursor: pointer;}
.input-content input { border: none; background: transparent; font-size: 1rem; font-weight: 600; color: #000; outline: none; cursor: pointer; width: 100%;}
.input-content input::placeholder { color: #94a3b8; font-weight: 500; }

.booking-divider { width: 1px; height: 40px; background: #e2e8f0; margin: 0 10px; }

.btn-update-search {
    background: #000;
    color: white;
    border: none;
    padding: 15px 30px;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
    margin-left: 10px;
}
.btn-update-search:hover { background: #334155; }

/* --- Main Layout --- */
.main-layout {
    max-width: 1200px;
    margin: 30px auto;
    padding: 0 20px;
    display: grid;
    grid-template-columns: 260px 1fr;
    gap: 30px;
}

/* --- 2. Sidebar Filters --- */
.filter-sidebar { height: fit-content; }

.map-preview {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    height: 120px;
    margin-bottom: 25px;
    border: 1px solid #cbd5e1;
    cursor: pointer;
}
.map-preview img { width: 100%; height: 100%; object-fit: cover; }
.btn-view-map {
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    background: white; border: 1px solid #000; padding: 8px 16px; border-radius: 8px;
    font-weight: 700; font-size: 0.85rem; display: flex; align-items: center; gap: 8px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15); pointer-events: none;
}

.filter-group h3 { font-size: 1rem; font-weight: 800; margin: 0 0 15px; color: #000; }
.filter-checkbox { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; cursor: pointer; font-size: 0.95rem; color: #475569;}
.filter-checkbox input[type="checkbox"] { width: 18px; height: 18px; cursor: pointer; accent-color: #000;}
.stars { color: #f59e0b; font-size: 0.85rem; letter-spacing: 2px;}
.filter-divider { height: 1px; background: #cbd5e1; margin: 25px 0; }

/* --- 3. Hotel List Area --- */
.list-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.list-header h2 { font-size: 1.4rem; font-weight: 700; margin: 0; color: #000; }
.sort-by { display: flex; align-items: center; gap: 10px; font-size: 0.9rem; font-weight: 600;}
.sort-by select { padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-weight: 600; outline: none; cursor: pointer;}

/* 🏨 Hotel Card (Horizontal List View) */
.hotel-card {
    display: flex;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 20px;
    transition: 0.2s;
    height: 240px; /* Fix height for perfect alignment */
}
.hotel-card:hover { box-shadow: 0 10px 20px rgba(0,0,0,0.08); }

/* Left: Image */
.hotel-img-wrapper { width: 280px; position: relative; flex-shrink: 0;}
.hotel-img-wrapper img { width: 100%; height: 100%; object-fit: cover; }
.btn-heart { position: absolute; top: 15px; right: 15px; background: white; border: none; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 2px 6px rgba(0,0,0,0.2); font-size: 1.1rem; color: #94a3b8; transition: 0.2s;}
.btn-heart.active { color: #ef4444; }
.btn-heart:hover { transform: scale(1.1); }
.img-counter { position: absolute; bottom: 15px; left: 15px; background: rgba(0,0,0,0.6); color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; display: flex; align-items: center; gap: 6px;}

/* Middle: Details */
.hotel-info { flex: 1; padding: 20px; border-right: 1px solid #e2e8f0; display: flex; flex-direction: column;}
.rank-text { font-size: 0.8rem; color: #64748b; margin-bottom: 5px; }
.rank-text strong { color: #000; }
.hotel-name { font-size: 1.35rem; font-weight: 800; color: #000; margin: 0 0 10px; cursor: pointer; transition: 0.2s;}
.hotel-name:hover { text-decoration: underline; }

.rating-row { display: flex; align-items: center; margin-bottom: 12px; }
.bubbles i { color: #00aa6c; font-size: 0.9rem; margin-right: 2px; }
.review-count { font-size: 0.85rem; color: #475569; font-weight: 600; margin-left: 10px; text-decoration: underline; cursor: pointer;}

.hotel-amenities { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 12px;}
.hotel-amenities span { font-size: 0.8rem; color: #475569; display: flex; align-items: center; gap: 6px; font-weight: 500;}
.hotel-amenities i { color: #000; }

.hotel-desc { font-size: 0.85rem; color: #64748b; line-height: 1.5; margin: auto 0 0; font-style: italic;}

/* Right: Pricing Box */
.hotel-deals { width: 220px; padding: 20px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; background: #fdfdfd; flex-shrink: 0;}
.deal-provider { font-size: 0.85rem; font-weight: 700; color: #000; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;}
.deal-provider i { font-size: 0.7rem; color: #64748b; }
.deal-price { margin-bottom: 12px; display: flex; align-items: flex-end; justify-content: center; gap: 8px;}
.price-strike { font-size: 1rem; color: #ef4444; text-decoration: line-through; font-weight: 600; margin-bottom: 3px;}
.price-current { font-size: 2rem; font-weight: 900; color: #000; line-height: 1;}

.btn-view-deal { background: #fcd34d; /* สีเหลือง TripAdvisor */ color: #000; border: none; padding: 12px 24px; border-radius: 50px; font-size: 1rem; font-weight: 800; cursor: pointer; width: 100%; transition: 0.2s; margin-bottom: 15px;}
.btn-view-deal:hover { background: #f59e0b; }

.other-deals { width: 100%; border-top: 1px solid #e2e8f0; padding-top: 15px;}
.mini-deal { display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #475569; margin-bottom: 6px;}
.mini-deal strong { color: #000; font-size: 0.9rem;}

/* --- Responsive Design --- */
@media (max-width: 1024px) {
    .main-layout { grid-template-columns: 1fr; }
    .filter-sidebar { display: none; } /* ซ่อน Sidebar ในมือถือ (ในเว็บจริงจะทำเป็นปุ่ม Filter เด้งขึ้นมา) */
}

@media (max-width: 768px) {
    .booking-bar { flex-direction: column; }
    .booking-divider { width: 100%; height: 1px; margin: 10px 0; }
    .btn-update-search { width: 100%; margin: 10px 0 0; }
    
    .hotel-card { flex-direction: column; height: auto; }
    .hotel-img-wrapper { width: 100%; height: 200px; }
    .hotel-info { border-right: none; border-bottom: 1px solid #e2e8f0; }
    .hotel-deals { width: 100%; }
}
</style>