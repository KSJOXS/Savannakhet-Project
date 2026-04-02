import { createRouter, createWebHistory } from 'vue-router'

// --- Public Components ---
import HomeView from '../pages/HomeView.vue'
import RecommendList from '../pages/RecommendList.vue'
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import PlaceDetail from '../pages/PlaceDetail.vue'
import EditPlace from '../pages/admin/location/update/EditPlace.vue'

// --- Admin Components (ต้องสร้างไฟล์เหล่านี้ในโฟลเดอร์ pages/admin/) ---
import AdminLayout from '../pages/admin/AdminLayout.vue'     // ไฟล์หลักที่มี Sidebar
import AdminPlaces from '../pages/admin/AdminPlaces.vue'     // หน้าจัดการสถานที่
import AdminCategories from '../pages/admin/AdminCategories.vue' // หน้าจัดการหมวดหมู่
import AdminComments from '../pages/admin/AdminComments.vue'   // หน้าจัดการรีวิว
import AdminUsers from '../pages/admin/AdminUsers.vue'       // หน้าจัดการผู้ใช้งาน (ต้องสร้างไฟล์นี้ด้วย)

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

    // --- Admin Routes with Sidebar System ---
    {
        path: '/admin',
        component: AdminLayout, // ใช้ Layout นี้เป็นตัวคุม Sidebar
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
                path: '', // Default path เมื่อเข้า /admin
                redirect: '/admin/places'
            },
            {
                path: 'manage-users',
                name: 'AdminManageUsers',
                component: AdminUsers // Lazy load หน้าจัดการผู้ใช้งาน
            }

        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// 🔐 Navigation Guard: ป้องกันคนทั่วไปแอบเข้าหน้า Admin
router.beforeEach((to, from, next) => {
    const user = JSON.parse(localStorage.getItem('user'))

    // ถ้าจะเข้าหน้า admin แต่ไม่มี user หรือไม่ใช่ admin ให้ไปหน้า login
    if (to.path.startsWith('/admin')) {
        if (!user || user.role !== 'admin') {
            alert('สิทธิ์การเข้าถึงเฉพาะผู้ดูแลระบบเท่านั้น')
            next('/login')
        } else {
            next()
        }
    } else {
        next()
    }
})

export default router