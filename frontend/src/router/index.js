// 💡 แก้ไข: นำเข้า createWebHashHistory แทนของเดิมเพื่อรองรับ GitHub Pages
import { createRouter, createWebHashHistory /* , createWebHistory */ } from 'vue-router'

// --- Public Components ---
import HomeView from '../pages/HomeView.vue'
import RecommendList from '../pages/RecommendList.vue'
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import PlaceDetail from '../pages/PlaceDetail.vue'
import EditPlace from '../pages/admin/location/update/EditPlace.vue'
import Favorites from '../pages/Favorites.vue'
import Profile from '../pages/Profile.vue'
import AddPlace from '../pages/admin/location/AddPlace.vue'
import Hotels from '../pages/Hotels.vue'
import HotelDetail from '../pages/HotelDetail.vue'
import Restaurants from '../pages/Restaurants.vue'
import nature from '../pages/Nature.vue'

// --- Admin Components ---
import AdminLayout from '../pages/admin/AdminLayout.vue'
import AdminPlaces from '../pages/admin/AdminPlaces.vue'
import AdminCategories from '../pages/admin/AdminCategories.vue'
import AdminComments from '../pages/admin/AdminComments.vue'
import AdminUsers from '../pages/admin/AdminUsers.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomeView
    },
    {
        path: '/explore',
        name: 'Explore',
        component: RecommendList
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/register',
        name: 'Register',
        component: Register
    },
    {
        path: '/places/:id',
        name: 'PlaceDetail',
        component: PlaceDetail,
        props: true
    },
    {
        path: '/admin/location/update/:id',
        name: 'EditPlace',
        component: EditPlace,
    },
    {
        path: '/admin/location/create',
        name: 'AddPlace',
        component: AddPlace,
    },
    {
        path: '/favorites',
        name: 'Favorites',
        component: Favorites
    },
    {
        path: '/profile',
        name: 'Profile',
        component: Profile
    },
    {
        path: '/hotels',
        name: 'Hotels',
        component: Hotels
    },
    {
        path: '/hotels/:id',
        name: 'HotelDetail',
        component: HotelDetail
    },
    {
        path: '/restaurants',
        name: 'Restaurants',
        component: Restaurants
    },
    {
        path: '/nature',
        name: 'Nature',
        component: nature
    },

    // --- Admin Routes with Sidebar System ---
    {
        path: '/admin',
        component: AdminLayout,
        children: [
            {
                path: 'places',
                name: 'AdminPlaces',
                component: AdminPlaces
            },
            {
                path: 'categories',
                name: 'AdminCategories',
                component: AdminCategories
            },
            {
                path: 'comments',
                name: 'AdminComments',
                component: AdminComments
            },
            {
                path: 'manage-users',
                name: 'AdminManageUsers',
                component: AdminUsers
            },
            {
                path: '',
                redirect: '/admin/places'
            }
        ]
    }
]

const router = createRouter({
    /** * 💡 โค้ดเก่า: history: createWebHistory() 
     * สาเหตุที่คอมเมนต์: GitHub Pages ไม่รองรับการจัดการ URL แบบปกติเมื่อกด Refresh หน้าเว็บ (จะเจอ 404)
     */
    // history: createWebHistory(), 

    /**
     * ✅ โค้ดใหม่: ใช้ createWebHashHistory
     * วิธีนี้จะเติม /#/ ใน URL เพื่อให้ GitHub Pages ทำงานร่วมกับ Vue Router ได้โดยไม่จอขาว
     */
    history: createWebHashHistory(import.meta.env.BASE_URL),
    routes
})

// 🔐 Navigation Guard: ตรวจสอบสิทธิ์การเข้าถึง
router.beforeEach((to, from, next) => {
    const user = JSON.parse(localStorage.getItem('user'))

    if (to.path.startsWith('/admin')) {
        if (!user || user.role !== 'admin') {
            alert('สิทธิ์การเข้าถึงเฉพาะผู้ดูแลระบบเท่านั้น')
            next('/login')
        } else {
            next()
        }
    }
    else if (to.path === '/') {
        if (user && user.role !== 'admin') {
            next('/explore')
        } else {
            next()
        }
    }
    else {
        next()
    }
})

export default router