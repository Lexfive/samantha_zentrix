import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useDashboard } from '../hooks/useDashboard'
import { BalanceCard } from '../components/dashboard/BalanceCard'
import { SummaryStats } from '../components/dashboard/SummaryStats'
import { TransactionList } from '../components/transactions/TransactionList'
import { TransactionForm } from '../components/transactions/TransactionForm'
import { useAuthStore } from '../store/authStore'

export default function DashboardPage() {
  const { transactions, filtered, balance, summary, loading, filter, setFilter, refresh } = useDashboard()
  const { user } = useAuthStore()
  const [showForm, setShowForm] = useState(false)

  const greeting = () => {
    const h = new Date().getHours()
    if (h < 12) return 'Bom dia'
    if (h < 18) return 'Boa tarde'
    return 'Boa noite'
  }

  return (
    <div className="p-6 lg:p-8 max-w-7xl mx-auto animate-fade-in">
      {/* Header */}
      <div className="flex items-start justify-between mb-8">
        <div>
          <p className="text-muted text-sm mb-1">{greeting()},</p>
          <h1 className="font-display font-bold text-2xl text-white">
            {user?.email?.split('@')[0] || 'Usuário'} 👋
          </h1>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={refresh}
            className="btn-ghost p-2.5"
            title="Atualizar dados"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
            </svg>
          </button>
          <button
            onClick={() => setShowForm((v) => !v)}
            className="btn-primary flex items-center gap-2"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            <span className="hidden sm:inline">Nova transação</span>
            <span className="sm:hidden">Nova</span>
          </button>
        </div>
      </div>

      {/* Quick add form */}
      {showForm && (
        <div className="card p-6 mb-6 animate-slide-up">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-display font-semibold text-white">Adicionar transação</h2>
            <button
              onClick={() => setShowForm(false)}
              className="text-muted hover:text-white transition-colors p-1"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <TransactionForm onSuccess={() => setShowForm(false)} />
        </div>
      )}

      {/* Main grid */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Left column */}
        <div className="xl:col-span-2 space-y-6">
          <BalanceCard balance={balance} summary={summary} loading={loading} />

          {/* Transactions card */}
          <div className="card overflow-hidden">
            <div className="flex items-center justify-between px-5 py-5 border-b border-border">
              <h2 className="font-display font-semibold text-white">Transações recentes</h2>
              <Link
                to="/transactions"
                className="text-xs text-violet-400 hover:text-violet-300 transition-colors font-medium"
              >
                Ver todas →
              </Link>
            </div>
            <TransactionList
              transactions={filtered}
              loading={loading}
              filter={filter}
              setFilter={setFilter}
              limit={8}
            />
          </div>
        </div>

        {/* Right column */}
        <div className="space-y-6">
          <SummaryStats summary={summary} loading={loading} />

          {/* Quick tip */}
          <div className="card p-5">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-violet-600/15 border border-violet-600/20 flex items-center justify-center shrink-0 mt-0.5">
                <svg className="w-4 h-4 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
                </svg>
              </div>
              <div>
                <p className="text-sm font-medium text-white mb-1">Dica rápida</p>
                <p className="text-xs text-muted leading-relaxed">
                  Registre todas as suas transações para ter uma visão clara do seu fluxo financeiro mensal.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
