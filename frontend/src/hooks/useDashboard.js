import { useEffect } from 'react'
import { useTransactionStore } from '../store/transactionStore'

export function useDashboard() {
  const { fetchDashboard, transactions, balance, summary, loading, error, filter, setFilter, filteredTransactions } =
    useTransactionStore()

  useEffect(() => {
    fetchDashboard()
  }, [])

  return {
    transactions,
    filtered: filteredTransactions(),
    balance,
    summary,
    loading,
    error,
    filter,
    setFilter,
    refresh: fetchDashboard,
  }
}
