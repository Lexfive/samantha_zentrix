import api from './client'

export const authApi = {
  login: async (credentials) => {
    const { data } = await api.post('/auth/login', {
      email: credentials.email,
      password: credentials.password,
    })
    return data
  },
}