import { create } from 'zustand'
import { authApi } from '../api/auth'

const TOKEN_KEY = 'zentrix_token'
const USER_KEY = 'zentrix_user'

export const useAuthStore = create((set, get) => ({
  token: localStorage.getItem(TOKEN_KEY) || null,
  user: JSON.parse(localStorage.getItem(USER_KEY) || 'null'),
  loading: false,
  error: null,

  isAuthenticated: () => !!get().token,

  login: async (credentials) => {
    set({ loading: true, error: null })
    try {
      const data = await authApi.login(credentials)
      const token = data.access_token

      localStorage.setItem(TOKEN_KEY, token)

      // Decode basic info from JWT payload (no sensitive data)
      let user = { email: credentials.email }
      try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        user = { ...user, id: payload.sub, ...payload }
      } catch { /* ignore decode errors */ }

      localStorage.setItem(USER_KEY, JSON.stringify(user))
      set({ token, user, loading: false, error: null })
      return { success: true }
    } catch (err) {
      const message = err.response?.data?.detail || 'Credenciais inválidas.'
      set({ loading: false, error: message })
      return { success: false, error: message }
    }
  },

  logout: () => {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    set({ token: null, user: null, error: null })
  },

  clearError: () => set({ error: null }),
}))
