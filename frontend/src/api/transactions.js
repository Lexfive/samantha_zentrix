import api from './client'

export const transactionsApi = {
  getAll: async (params = {}) => {
    const { data } = await api.get('/transactions', { params })
    return data
  },

  create: async (payload) => {
    const { data } = await api.post('/transactions', payload)
    return data
  },

  getBalance: async () => {
    const { data } = await api.get('/transactions/balance')
    return data
  },

  getSummary: async () => {
    const { data } = await api.get('/transactions/summary')
    return data
  },
}
