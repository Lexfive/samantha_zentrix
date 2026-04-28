import { create } from 'zustand'
import { transactionsApi } from '../api/transactions'

export const useTransactionStore = create((set, get) => ({
  transactions: [],
  balance: null,
  summary: null,
  loading: false,
  creating: false,
  error: null,
  filter: 'all', // 'all' | 'income' | 'expense'

  setFilter: (filter) => set({ filter }),

  fetchAll: async () => {
    set({ loading: true, error: null })
    try {
      const data = await transactionsApi.getAll()
      set({ transactions: data, loading: false })
    } catch (err) {
      set({ loading: false, error: err.response?.data?.detail || 'Erro ao carregar transações.' })
    }
  },

  fetchBalance: async () => {
    try {
      const data = await transactionsApi.getBalance()
      set({ balance: data })
    } catch { /* silent */ }
  },

  fetchSummary: async () => {
    try {
      const data = await transactionsApi.getSummary()
      set({ summary: data })
    } catch { /* silent */ }
  },

  fetchDashboard: async () => {
    set({ loading: true, error: null })
    try {
      const [transactions, balance, summary] = await Promise.all([
        transactionsApi.getAll(),
        transactionsApi.getBalance(),
        transactionsApi.getSummary(),
      ])
      set({ transactions, balance, summary, loading: false })
    } catch (err) {
      set({ loading: false, error: err.response?.data?.detail || 'Erro ao carregar dados.' })
    }
  },

  createTransaction: async (payload) => {
    set({ creating: true, error: null })
    try {
      const newTx = await transactionsApi.create(payload)
      // Optimistically add to list and refresh balance
      set((state) => ({
        transactions: [newTx, ...state.transactions],
        creating: false,
      }))
      // Refresh balance and summary in background
      get().fetchBalance()
      get().fetchSummary()
      return { success: true, data: newTx }
    } catch (err) {
      const message = err.response?.data?.detail || 'Erro ao criar transação.'
      set({ creating: false, error: message })
      return { success: false, error: message }
    }
  },

  filteredTransactions: () => {
    const { transactions, filter } = get()
    if (filter === 'all') return transactions
    return transactions.filter((tx) => tx.type === filter)
  },

  clearError: () => set({ error: null }),
}))
