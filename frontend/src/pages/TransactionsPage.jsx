import { useState } from 'react'
import { useDashboard } from '../hooks/useDashboard'
import { TransactionList } from '../components/transactions/TransactionList'
import { TransactionForm } from '../components/transactions/TransactionForm'
import { formatCurrency } from '../utils/formatters'

export default function TransactionsPage() {
  const { filtered, balance, loading, filter, setFilter, refresh } = useDashboard()
  const [showForm, setShowForm] = useState(false)

  return (
    <div className="p-6 lg:p-8 max-w-5xl mx-auto animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="font-display font-bold text-2xl text-white mb-1">Transações</h1>
          <p className="text-muted text-sm">{filtered.length} registro{filtered.length !== 1 ? 's' : ''}</p>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={refresh} className="btn-ghost p-2.5" title="Atualizar">
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
            Nova transação
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main list */}
        <div className="lg:col-span-2">
          {/* Form inline */}
          {showForm && (
            <div className="card p-6 mb-6 animate-slide-up">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-display font-semibold text-white text-sm">Adicionar transação</h2>
                <button onClick={() => setShowForm(false)} className="text-muted hover:text-white transition-colors">
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <TransactionForm onSuccess={() => { setShowForm(false); refresh() }} />
            </div>
          )}

          <div className="card overflow-hidden">
            <TransactionList
              transactions={filtered}
              loading={loading}
              filter={filter}
              setFilter={setFilter}
              showFilter
            />
          </div>
        </div>

        {/* Sidebar info */}
        <div className="space-y-4">
          {/* Balance mini card */}
          <div className="card p-5">
            <p className="text-xs text-muted uppercase tracking-wider mb-3">Saldo atual</p>
            <p className={`font-display font-bold text-3xl ${
              (balance?.balance ?? 0) >= 0 ? 'text-white' : 'text-expense'
            }`}>
              {formatCurrency(balance?.balance ?? 0)}
            </p>
          </div>

          {/* Filters explained */}
          <div className="card p-5">
            <p className="text-xs text-muted uppercase tracking-wider mb-3">Filtrar por tipo</p>
            <div className="space-y-2">
              {[
                { value: 'all', label: 'Todas as transações', desc: 'Entradas e saídas' },
                { value: 'income', label: 'Entradas', desc: 'Apenas créditos', color: 'text-income' },
                { value: 'expense', label: 'Saídas', desc: 'Apenas débitos', color: 'text-expense' },
              ].map((opt) => (
                <button
                  key={opt.value}
                  onClick={() => setFilter(opt.value)}
                  className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-sm transition-all duration-200 ${
                    filter === opt.value
                      ? 'bg-violet-600/15 border border-violet-600/25'
                      : 'hover:bg-white/5 border border-transparent'
                  }`}
                >
                  <div className="text-left">
                    <p className={`font-medium ${filter === opt.value ? 'text-violet-400' : 'text-white'}`}>
                      {opt.label}
                    </p>
                    <p className="text-xs text-muted">{opt.desc}</p>
                  </div>
                  {filter === opt.value && (
                    <svg className="w-4 h-4 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                    </svg>
                  )}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
