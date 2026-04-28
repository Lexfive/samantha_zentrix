import { formatCurrency } from '../../utils/formatters'
import { SkeletonText } from '../ui/Skeleton'

export function BalanceCard({ balance, summary, loading }) {
  const total = balance?.balance ?? balance?.total ?? 0
  const income = summary?.total_income ?? 0
  const expenses = summary?.total_expenses ?? 0

  return (
    <div className="relative card p-6 overflow-hidden">
      {/* Background glow */}
      <div className="absolute inset-0 bg-gradient-to-br from-violet-600/10 via-transparent to-transparent pointer-events-none" />
      <div className="absolute -top-12 -right-12 w-48 h-48 bg-violet-600/5 rounded-full blur-3xl pointer-events-none" />

      <div className="relative">
        <div className="flex items-start justify-between mb-6">
          <div>
            <p className="text-xs text-muted font-medium uppercase tracking-wider mb-1">Saldo Total</p>
            {loading ? (
              <SkeletonText className="h-10 w-48 mt-1" />
            ) : (
              <p className={`font-display font-bold text-4xl tracking-tight ${total >= 0 ? 'text-white' : 'text-expense'}`}>
                {formatCurrency(total)}
              </p>
            )}
          </div>
          <div className="w-11 h-11 rounded-xl bg-violet-600/20 border border-violet-600/30 flex items-center justify-center">
            <svg className="w-5 h-5 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M21 12a2.25 2.25 0 00-2.25-2.25H15a3 3 0 11-6 0H5.25A2.25 2.25 0 003 12m18 0v6a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 18v-6m18 0V9M3 12V9m18-3a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 9m18 0V6a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 6v3" />
            </svg>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          {/* Income */}
          <div className="bg-income/5 border border-income/10 rounded-xl p-4">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-5 h-5 rounded-full bg-income/20 flex items-center justify-center">
                <svg className="w-3 h-3 text-income" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 10.5L12 3m0 0l7.5 7.5M12 3v18" />
                </svg>
              </div>
              <span className="text-xs text-muted">Entradas</span>
            </div>
            {loading ? (
              <SkeletonText className="h-6 w-28" />
            ) : (
              <p className="font-display font-semibold text-income text-lg">{formatCurrency(income)}</p>
            )}
          </div>

          {/* Expenses */}
          <div className="bg-expense/5 border border-expense/10 rounded-xl p-4">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-5 h-5 rounded-full bg-expense/20 flex items-center justify-center">
                <svg className="w-3 h-3 text-expense" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 13.5L12 21m0 0l-7.5-7.5M12 21V3" />
                </svg>
              </div>
              <span className="text-xs text-muted">Saídas</span>
            </div>
            {loading ? (
              <SkeletonText className="h-6 w-28" />
            ) : (
              <p className="font-display font-semibold text-expense text-lg">{formatCurrency(expenses)}</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
