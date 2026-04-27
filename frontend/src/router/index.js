// 💡 แก้ไข: นำเข้า createWebHashHistory แทนของเดิมเพื่อรองรับ GitHub Pages
import { createRouter, createWebHashHistory /* , createWebHistory */ } from 'vue-router'

// --- Public Components ---
import HomeView from '../pages/main/HomeView.vue'
import RecommendList from '../pages/places/RecommendList.vue'
import Login from '../pages/auth/Login.vue'
import Register from '../pages/auth/Register.vue'
import PlaceDetail from '../pages/places/PlaceDetail.vue'
import EditPlace from '../pages/admin/places/EditPlace.vue'
import Favorites from '../pages/user/Favorites.vue'
import Profile from '../pages/user/Profile.vue'
import SubmitPlace from '../pages/user/SubmitPlace.vue'
import AddPlace from '../pages/admin/places/AddPlace.vue'
import Hotels from '../pages/places/Hotels.vue'
import HotelDetail from '../pages/places/HotelDetail.vue'
import Restaurants from '../pages/places/Restaurants.vue'
import nature from '../pages/places/Nature.vue'
import Landmarks from '../pages/places/Landmarks.vue'
import About from '../pages/main/About.vue'
import Contact from '../pages/main/Contact.vue'
import Community from '../pages/community/Community.vue'

// --- Admin Components ---
import AdminLayout from '../pages/admin/common/AdminLayout.vue'
import AdminPlaces from '../pages/admin/places/Places.vue'
import AdminCategories from '../pages/admin/places/Categories.vue'
import AdminComments from '../pages/admin/common/Comments.vue'
import AdminUsers from '../pages/admin/users/Users.vue'
import AdminDashboard from '../pages/admin/common/Dashboard.vue'
import AdminSettings from '../pages/admin/settings/Settings.vue'
import PendingPlaces from '../pages/admin/places/PendingPlaces.vue'
import PendingPermissions from '../pages/admin/common/PendingPermissions.vue'
import UserDetail from '../pages/admin/users/UserDetail.vue'
import ContactMessages from '../pages/admin/common/ContactMessages.vue'

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
        path: '/submit-place',
        name: 'SubmitPlace',
        component: SubmitPlace
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
    {
        path: '/landmarks',
        name: 'Landmarks',
        component: Landmarks
    },
    {
        path: '/about',
        name: 'About',
        component: About
    },
    {
        path: '/contact',
        name: 'Contact',
        component: Contact
    },
    {
        path: '/community',
        name: 'Community',
        component: Community
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
                path: 'users/:id',
                name: 'AdminUserDetail',
                component: UserDetail
            },
            {
                path: 'pending-places',
                name: 'AdminPendingPlaces',
                component: PendingPlaces
            },
            {
                path: 'pending-permissions',
                name: 'AdminPendingPermissions',
                component: PendingPermissions
            },
            {
                path: 'messages',
                name: 'AdminMessages',
                component: ContactMessages
            },
            {
                path: '',
                redirect: '/admin/places'
            },
            {
                path: 'dashboard',
                name: 'AdminDashboard',
                component: AdminDashboard
            },
            {
                path: 'settings',
                name: 'AdminSettings',
                component: AdminSettings
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