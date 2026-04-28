import { formatCurrency, formatDate } from '../../utils/formatters'
import { SkeletonRow } from '../ui/Skeleton'

const CATEGORY_ICONS = {
  income: (
    <svg className="w-4 h-4 text-income" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 10.5L12 3m0 0l7.5 7.5M12 3v18" />
    </svg>
  ),
  expense: (
    <svg className="w-4 h-4 text-expense" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 13.5L12 21m0 0l-7.5-7.5M12 21V3" />
    </svg>
  ),
}

function TransactionRow({ tx }) {
  const isIncome = tx.type === 'income'

  return (
    <div className="flex items-center gap-4 py-4 px-5 hover:bg-white/[0.02] transition-colors duration-150 border-b border-border last:border-0">
      {/* Icon */}
      <div
        className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${
          isIncome ? 'bg-income/10 border border-income/15' : 'bg-expense/10 border border-expense/15'
        }`}
      >
        {CATEGORY_ICONS[tx.type]}
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-white truncate">
          {tx.description || (isIncome ? 'Entrada' : 'Saída')}
        </p>
        <p className="text-xs text-muted mt-0.5">{formatDate(tx.created_at || tx.date)}</p>
      </div>

      {/* Amount */}
      <span
        className={`font-mono font-semibold text-sm shrink-0 ${isIncome ? 'text-income' : 'text-expense'}`}
      >
        {isIncome ? '+' : '-'}{formatCurrency(Math.abs(tx.amount))}
      </span>
    </div>
  )
}

function EmptyState({ filter }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
      <div className="w-14 h-14 rounded-2xl bg-white/5 border border-border flex items-center justify-center mb-4">
        <svg className="w-7 h-7 text-muted" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 12h16.5m-16.5 3.75h16.5M3.75 19.5h16.5M5.625 4.5h12.75a1.875 1.875 0 010 3.75H5.625a1.875 1.875 0 010-3.75z" />
        </svg>
      </div>
      <p className="text-sm font-medium text-white mb-1">Nenhuma transação</p>
      <p className="text-xs text-muted">
        {filter === 'all' ? 'Adicione sua primeira transação.' : `Nenhuma ${filter === 'income' ? 'entrada' : 'saída'} encontrada.`}
      </p>
    </div>
  )
}

export function TransactionList({ transactions, loading, filter, setFilter, showFilter = true, limit }) {
  const displayed = limit ? transactions.slice(0, limit) : transactions

  return (
    <div>
      {showFilter && (
        <div className="flex items-center gap-2 px-5 pt-5 pb-4 border-b border-border">
          {[
            { value: 'all', label: 'Todas' },
            { value: 'income', label: 'Entradas' },
            { value: 'expense', label: 'Saídas' },
          ].map((opt) => (
            <button
              key={opt.value}
              onClick={() => setFilter(opt.value)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
                filter === opt.value
                  ? 'bg-violet-600/15 text-violet-400 border border-violet-600/25'
                  : 'text-muted hover:text-white hover:bg-white/5'
              }`}
            >
              {opt.label}
            </button>
          ))}
        </div>
      )}

      {loading ? (
        <div>
          {Array.from({ length: 5 }).map((_, i) => (
            <SkeletonRow key={i} />
          ))}
        </div>
      ) : displayed.length === 0 ? (
        <EmptyState filter={filter} />
      ) : (
        <div>
          {displayed.map((tx) => (
            <TransactionRow key={tx.id} tx={tx} />
          ))}
        </div>
      )}
    </div>
  )
}
