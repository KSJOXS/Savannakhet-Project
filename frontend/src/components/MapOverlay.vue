<template>
  <div class="map-overlay-backdrop" v-if="isOpen">
    <div class="map-overlay-modal">
      <!-- Map Container must be the background -->
      <div id="overlay-map" class="overlay-map-container"></div>
      
      <!-- Floating Header on top of the Map -->
      <div class="floating-header">
        <div class="header-left">
          <div class="search-box">
              <i class="fas fa-search"></i>
              <input type="text" v-model="searchQuery" placeholder="Search places...">
          </div>
          <div class="header-filters">
              <button v-for="filter in filterOptions" :key="filter.id" 
                      :class="['filter-btn', { active: activeFilters.has(filter.id) }]"
                      @click="toggleFilter(filter.id)">
                  <i :class="filter.icon"></i> {{ filter.label }}
              </button>
          </div>
        </div>
        <button class="btn-close" @click="closeMap"><i class="fas fa-times"></i></button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  places: { type: Array, default: () => [] },
  categories: { type: Array, default: () => [] },
  initialFilter: { type: String, default: null },
  initialSelectedId: { type: [String, Number], default: null },
  title: { type: String, default: 'Places' }
});

const emit = defineEmits(['close']);
const router = useRouter();

const selectedPlace = ref(null);
let map = null;
let markers = [];
let hasViewBeenSet = false;

const filterOptions = [
    { id: 'hotel', label: 'Hotels', icon: 'fas fa-bed' },
    { id: 'restaurant', label: 'Restaurants', icon: 'fas fa-utensils' },
    { id: 'nature', label: 'Nature & Parks', icon: 'fas fa-tree' },
    { id: 'landmark', label: 'Landmarks', icon: 'fas fa-monument' },
    { id: 'culture', label: 'Culture', icon: 'fas fa-vihara' }
];

const activeFilters = ref(new Set());
const searchQuery = ref('');

const toggleFilter = (id) => {
    const newFilters = new Set(activeFilters.value);
    if (newFilters.has(id)) {
        newFilters.delete(id);
    } else {
        newFilters.add(id);
    }
    activeFilters.value = newFilters;
};

const displayedPlaces = computed(() => {
    let places = props.places;

    if (searchQuery.value.trim() !== '') {
        const query = searchQuery.value.toLowerCase();
        places = places.filter(p => p.name && p.name.toLowerCase().includes(query));
    }

    if (!props.categories || props.categories.length === 0) return places;
    if (activeFilters.value.size === 0) return []; 
    
    return places.filter(p => {
        const cat = props.categories.find(c => c.id === p.category_id);
        if (!cat) return false;
        return activeFilters.value.has(cat.parent_type) || (cat.parent_type === null && activeFilters.value.has('landmark')); // fallback to landmark
    });
});

const closeMap = () => {
    emit('close');
};

const goToDetail = (id) => {
    window.open(`/places/${id}`, '_blank');
};

const getCoverImage = (place) => {
    let url = place.image_url;
    if (!url || String(url).trim() === '[]' || String(url).trim() === '') return 'https://via.placeholder.com/400x300?text=No+Image';
    
    if (typeof url === 'string' && url.startsWith('[')) {
        try { 
            const arr = JSON.parse(url);
            if (Array.isArray(arr) && arr.length > 0) {
                url = arr[0];
            } else {
                return 'https://via.placeholder.com/400x300?text=No+Image';
            }
        } catch (e) {
            url = url.replace(/[\[\]"]/g, '');
        }
    }
    
    if (!url) return 'https://via.placeholder.com/400x300?text=No+Image';
    if (url.startsWith('data:')) return url;
    return url.startsWith('http') ? url : `http://localhost:8000/${url.replace(/^\//, '')}`;
}

const initMap = () => {
    if (!window.L) return;

    if (map) {
        map.remove();
        map = null;
    }

    map = window.L.map('overlay-map', {
        zoomControl: false // Custom controls position if needed
    }).setView([16.5501, 104.7570], 12); // Default to Savannakhet

    window.L.control.zoom({
        position: 'bottomright'
    }).addTo(map);

    window.L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
    }).addTo(map);

    renderMarkers();
};

const renderMarkers = () => {
    if (!map || !window.L) return;

    // Clear old markers
    markers.forEach(m => map.removeLayer(m));
    markers = [];
    selectedPlace.value = null;

    let group = window.L.featureGroup();
    let hasInitial = false;
    let initialLatLng = null;

    displayedPlaces.value.forEach(place => {
        if (!place.location_lat || !place.location_lng) return;
        
        let lat = parseFloat(place.location_lat);
        let lng = parseFloat(place.location_lng);
        if (isNaN(lat) || isNaN(lng)) return;

        let ratingText = place.rating_avg ? parseFloat(place.rating_avg).toFixed(1) : '<i class="fas fa-map-marker-alt"></i>';
        
        // Custom Marker
        const markerHtml = `
            <div class="custom-marker pill-style">
                <span class="m-text">${ratingText}</span>
            </div>
        `;
        const customIcon = window.L.divIcon({
            html: markerHtml,
            className: 'empty-leaflet-icon',
            iconSize: [window.L.Point ? null : 40, 26],
            iconAnchor: [20, 26],
            popupAnchor: [0, -28]
        });

        let marker = window.L.marker([lat, lng], { icon: customIcon }).addTo(map);

        const bubblesHtml = [1,2,3,4,5].map(s => `<i class="${(place.rating_avg || 0) >= s ? 'fas' : 'far'} fa-circle"></i>`).join('');
        const descText = place.description ? place.description.substring(0, 80) + '...' : 'View details for more information.';
        
        const popupContentHtml = `
            <div class="leaflet-custom-card" onclick="window.open('#/places/${place.id}', '_blank')">
                <div class="card-img-wrapper">
                    <img src="${getCoverImage(place)}" alt="${place.name}" />
                    <button class="btn-heart-popup" onclick="event.stopPropagation()"><i class="far fa-heart"></i></button>
                </div>
                <div class="card-info">
                    <h3 class="place-name">${place.name}</h3>
                    <div class="rating-row">
                        <span class="bubbles">${bubblesHtml}</span>
                        <span class="review-count">(${place.rating_avg || '0.0'})</span>
                    </div>
                    <p class="desc-text">${descText}</p>
                </div>
            </div>
        `;
        
        marker.bindPopup(popupContentHtml, {
            closeButton: false,
            className: 'custom-tripadvisor-popup'
        });

        marker.on('popupopen', () => {
            selectedPlace.value = place;
            const el = marker.getElement();
            if (el) {
                const markerEl = el.querySelector('.custom-marker');
                if (markerEl) markerEl.classList.add('selected');
            }
        });

        marker.on('popupclose', () => {
            const el = marker.getElement();
            if (el) {
                const markerEl = el.querySelector('.custom-marker');
                if (markerEl) markerEl.classList.remove('selected');
            }
            if (selectedPlace.value && selectedPlace.value.id === place.id) {
                selectedPlace.value = null;
            }
        });

        markers.push(marker);
        group.addLayer(marker);

        if (props.initialSelectedId && place.id == props.initialSelectedId) {
            hasInitial = true;
            initialLatLng = [lat, lng];
            // Open popup slightly after it's added
            setTimeout(() => marker.openPopup(), 100);
        }
    });

    if (!hasViewBeenSet) {
        if (hasInitial && initialLatLng) {
            map.setView(initialLatLng, 15);
            hasViewBeenSet = true;
        } else if (markers.length > 0) {
            map.fitBounds(group.getBounds(), { padding: [50, 50], maxZoom: 16 });
            hasViewBeenSet = true;
        }
    }

    // Auto-open the popup if the search narrows down to a single place
    if (markers.length === 1 && !hasInitial && searchQuery.value.trim() !== '') {
        setTimeout(() => {
            if (markers[0]) markers[0].openPopup();
        }, 200);
    }
};

watch(() => props.isOpen, async (newVal) => {
    if (newVal) {
        // Setup initial filters based on prop or default to all
        if (props.initialFilter) {
            activeFilters.value = new Set([props.initialFilter]);
        } else {
            activeFilters.value = new Set(['hotel', 'restaurant', 'nature', 'landmark', 'culture']);
        }
        
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
        await nextTick(); // Wait for DOM to render map container
        setTimeout(() => {
            initMap();
        }, 100);
    } else {
        document.body.style.overflow = '';
        if (map) {
            map.remove();
            map = null;
        }
        selectedPlace.value = null;
        hasViewBeenSet = false;
        searchQuery.value = '';
    }
});

watch(searchQuery, () => {
    hasViewBeenSet = false;
});

watch(displayedPlaces, () => {
    if (props.isOpen && map) {
        renderMarkers();
    }
}, { deep: true });

onUnmounted(() => {
    if (map) map.remove();
    document.body.style.overflow = '';
});

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.map-overlay-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.4);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    box-sizing: border-box;
}

.map-overlay-modal {
    position: relative;
    width: 100%;
    max-width: 1400px;
    height: 100%;
    max-height: 85vh;
    background: #f1f5f9;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    font-family: 'Inter', sans-serif;
}

.overlay-map-container {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1;
}

.floating-header {
    position: absolute;
    top: 20px;
    left: 20px;
    right: 20px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    z-index: 1000;
    pointer-events: none; /* Let clicks pass through empty space */
}

/* Allow clicks on actual interactive elements */
.header-left, .btn-close, .search-box, .filter-btn {
    pointer-events: auto;
}

.header-left {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 12px;
}

.search-box {
    display: flex;
    align-items: center;
    background: white;
    border-radius: 30px;
    padding: 10px 18px;
    border: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    width: 250px;
    transition: 0.2s;
}

.search-box:focus-within {
    box-shadow: 0 6px 16px rgba(0,0,0,0.2);
}

.search-box i {
    color: #64748b;
    margin-right: 10px;
    font-size: 1rem;
}

.search-box input {
    background: transparent;
    border: none;
    outline: none;
    font-size: 0.95rem;
    color: #1e293b;
    width: 100%;
}

.header-filters {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.filter-btn {
    background: white;
    border: none;
    padding: 10px 18px;
    border-radius: 30px;
    font-size: 0.95rem;
    font-weight: 600;
    color: #1e293b;
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: 0.2s;
}

.filter-btn:hover {
    background: #f8fafc;
}

.filter-btn.active {
    background: #e2e8f0;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}

.btn-close {
    background: white;
    border: none;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    color: #475569;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: 0.2s;
}

.btn-close:hover {
    background: #cbd5e1;
    color: #0f172a;
}

/* --- Leaflet Popups --- */
:deep(.custom-tripadvisor-popup .leaflet-popup-content-wrapper) {
    padding: 0;
    overflow: hidden;
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}
:deep(.custom-tripadvisor-popup .leaflet-popup-content) {
    margin: 0;
    width: 260px !important;
}
:deep(.custom-tripadvisor-popup .leaflet-popup-tip) {
    box-shadow: 0 10px 30px rgba(0,0,0,0.2); /* match shadow */
}

:deep(.leaflet-custom-card) {
    display: flex;
    flex-direction: column;
    cursor: pointer;
    font-family: 'Inter', sans-serif;
    color: #0f172a;
    background: white;
}
:deep(.leaflet-custom-card:hover) {
    background: #f8fafc;
}
:deep(.leaflet-custom-card .card-img-wrapper) {
    height: 120px;
    position: relative;
    width: 100%;
}
:deep(.leaflet-custom-card .card-img-wrapper img) {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
:deep(.leaflet-custom-card .btn-heart-popup) {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: white;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #94a3b8;
    box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    cursor: pointer;
}
:deep(.leaflet-custom-card .card-info) {
    padding: 12px;
}
:deep(.leaflet-custom-card .place-name) {
    margin: 0 0 4px;
    font-size: 1rem;
    font-weight: 800;
    color: #0f172a;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
:deep(.leaflet-custom-card .rating-row) {
    display: flex;
    align-items: center;
    margin-bottom: 6px;
}
:deep(.leaflet-custom-card .bubbles i) {
    color: #00aa6c;
    font-size: 0.75rem;
    margin-right: 2px;
}
:deep(.leaflet-custom-card .review-count) {
    color: #64748b;
    font-size: 0.75rem;
    margin-left: 6px;
    font-weight: 600;
}
:deep(.leaflet-custom-card .desc-text) {
    font-size: 0.8rem;
    color: #475569;
    margin: 0;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* --- Map Markers (Applied globally to map panel) --- */
:deep(.empty-leaflet-icon) {
    background: transparent;
    border: none;
}

:deep(.custom-marker.pill-style) {
    background: #004d40; /* TripAdvisor dark green style */
    color: white;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 4px 10px;
    border-radius: 12px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 3px 8px rgba(0,0,0,0.3);
    transition: 0.2s;
    border: 2px solid white;
    white-space: nowrap;
    position: relative;
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

:deep(.custom-marker.pill-style:hover), :deep(.custom-marker.pill-style.selected) {
    transform: scale(1.15);
    background: #00aa6c; /* Bright TripAdvisor green */
    z-index: 9999 !important;
}

:deep(.custom-marker.pill-style:hover::before), :deep(.custom-marker.pill-style.selected::before) {
    border-color: #00aa6c transparent transparent transparent;
}
</style>
