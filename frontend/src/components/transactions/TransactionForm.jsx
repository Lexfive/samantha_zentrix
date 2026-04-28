import { useState } from 'react'
import { useTransactionStore } from '../../store/transactionStore'
import { useToast } from '../ui/Toast'

const initialForm = { amount: '', type: 'income', description: '' }

export function TransactionForm({ onSuccess }) {
  const [form, setForm] = useState(initialForm)
  const { createTransaction, creating } = useTransactionStore()
  const toast = useToast()

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.amount || isNaN(parseFloat(form.amount)) || parseFloat(form.amount) <= 0) {
      toast.add('Informe um valor válido.', 'error')
      return
    }

    const result = await createTransaction({
      amount: parseFloat(form.amount),
      type: form.type,
      description: form.description || undefined,
    })

    if (result.success) {
      toast.add('Transação criada com sucesso!', 'success')
      setForm(initialForm)
      onSuccess?.()
    } else {
      toast.add(result.error || 'Erro ao criar transação.', 'error')
    }
  }

  const set = (field) => (e) => setForm((prev) => ({ ...prev, [field]: e.target.value }))

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Type toggle */}
      <div className="flex bg-surface rounded-xl p-1 gap-1">
        {[
          { value: 'income', label: 'Entrada', color: 'income' },
          { value: 'expense', label: 'Saída', color: 'expense' },
        ].map((opt) => (
          <button
            key={opt.value}
            type="button"
            onClick={() => setForm((prev) => ({ ...prev, type: opt.value }))}
            className={`flex-1 py-2.5 px-4 rounded-lg text-sm font-medium transition-all duration-200 ${
              form.type === opt.value
                ? opt.value === 'income'
                  ? 'bg-income/15 text-income border border-income/25'
                  : 'bg-expense/15 text-expense border border-expense/25'
                : 'text-muted hover:text-white'
            }`}
          >
            {opt.label}
          </button>
        ))}
      </div>

      {/* Amount */}
      <div className="relative">
        <span className="absolute left-4 top-1/2 -translate-y-1/2 text-muted text-sm font-mono">R$</span>
        <input
          type="number"
          step="0.01"
          min="0.01"
          placeholder="0,00"
          value={form.amount}
          onChange={set('amount')}
          className="input-field pl-10 font-mono text-lg"
          required
        />
      </div>

      {/* Description */}
      <input
        type="text"
        placeholder="Descrição (opcional)"
        value={form.description}
        onChange={set('description')}
        className="input-field"
        maxLength={200}
      />

      <button
        type="submit"
        disabled={creating}
        className="btn-primary w-full flex items-center justify-center gap-2"
      >
        {creating ? (
          <>
            <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            Criando...
          </>
        ) : (
          <>
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            Adicionar transação
          </>
        )}
      </button>
    </form>
  )
}
