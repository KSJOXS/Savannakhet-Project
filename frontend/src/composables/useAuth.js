import { ref } from 'vue'

const user = ref(JSON.parse(localStorage.getItem('user')) || null)

export function useAuth() {
    const login = (userData, token) => {
        user.value = userData
        localStorage.setItem('user', JSON.stringify(userData))
        localStorage.setItem('access_token', token)
    }

    const logout = () => {
        user.value = null
        localStorage.removeItem('user')
        localStorage.removeItem('access_token')
    }

    const isAuthenticated = () => {
        return !!user.value
    }

    const isAdmin = () => {
        return user.value?.role === 'admin'
    }

    return {
        user,
        login,
        logout,
        isAuthenticated,
        isAdmin
    }
}
