import { formatCurrency } from '../../utils/formatters'
import { SkeletonText } from '../ui/Skeleton'

function StatItem({ label, value, loading, color = 'white' }) {
  return (
    <div>
      <p className="text-xs text-muted uppercase tracking-wider mb-1.5">{label}</p>
      {loading ? (
        <SkeletonText className="h-6 w-32" />
      ) : (
        <p className={`font-display font-semibold text-xl ${color}`}>{value}</p>
      )}
    </div>
  )
}

export function SummaryStats({ summary, loading }) {
  const count = summary?.transaction_count ?? summary?.total_count ?? 0
  const avgIncome = summary?.average_income ?? 0
  const avgExpense = summary?.average_expense ?? 0
  const netFlow = (summary?.total_income ?? 0) - (summary?.total_expenses ?? 0)

  return (
    <div className="card p-6">
      <h3 className="text-sm font-display font-semibold text-white mb-5">Resumo do período</h3>
      <div className="grid grid-cols-2 gap-6">
        <StatItem label="Transações" value={count} loading={loading} />
        <StatItem
          label="Fluxo líquido"
          value={formatCurrency(netFlow)}
          loading={loading}
          color={netFlow >= 0 ? 'text-income' : 'text-expense'}
        />
        <StatItem label="Ticket médio entrada" value={formatCurrency(avgIncome)} loading={loading} color="text-income" />
        <StatItem label="Ticket médio saída" value={formatCurrency(avgExpense)} loading={loading} color="text-expense" />
      </div>
    </div>
  )
}
