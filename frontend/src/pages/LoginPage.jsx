import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

export default function LoginPage() {
  const [form, setForm] = useState({ email: '', password: '' })
  const { login, loading, error, isAuthenticated, clearError } = useAuthStore()
  const navigate = useNavigate()

  useEffect(() => {
    if (isAuthenticated()) navigate('/dashboard')
  }, [])

  useEffect(() => {
    if (error) {
      const t = setTimeout(clearError, 4000)
      return () => clearTimeout(t)
    }
  }, [error])

  const set = (field) => (e) => setForm((p) => ({ ...p, [field]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    const result = await login(form)
    if (result.success) navigate('/dashboard')
  }

  return (
    <div className="min-h-screen flex">
      {/* Left — branding */}
      <div className="hidden lg:flex flex-col justify-between w-[480px] shrink-0 bg-panel border-r border-border p-12 relative overflow-hidden">
        {/* Decorative */}
        <div className="absolute inset-0 bg-gradient-to-b from-violet-600/10 via-transparent to-violet-600/5 pointer-events-none" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-violet-600/8 rounded-full blur-3xl pointer-events-none" />

        <div className="relative flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-violet-600 flex items-center justify-center shadow-glow">
            <span className="text-white font-display font-bold">Z</span>
          </div>
          <span className="font-display font-bold text-xl text-white tracking-tight">Zentrix</span>
        </div>

        <div className="relative">
          <h1 className="font-display font-bold text-5xl text-white leading-tight mb-6">
            Seu dinheiro,
            <br />
            <span className="text-violet-400">sob controle.</span>
          </h1>
          <p className="text-muted text-lg leading-relaxed">
            Gerencie entradas e saídas com clareza. Saldo em tempo real, sem complicação.
          </p>
        </div>

        <div className="relative flex items-center gap-4">
          {[
            { label: 'Saldo em tempo real' },
            { label: 'Histórico completo' },
            { label: 'Seguro e privado' },
          ].map((item) => (
            <div key={item.label} className="flex items-center gap-1.5 text-xs text-muted">
              <svg className="w-3.5 h-3.5 text-income" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
              </svg>
              {item.label}
            </div>
          ))}
        </div>
      </div>

      {/* Right — form */}
      <div className="flex-1 flex items-center justify-center p-6 lg:p-12">
        <div className="w-full max-w-md animate-slide-up">
          {/* Mobile logo */}
          <div className="flex items-center gap-3 mb-10 lg:hidden">
            <div className="w-9 h-9 rounded-xl bg-violet-600 flex items-center justify-center shadow-glow-sm">
              <span className="text-white font-display font-bold text-sm">Z</span>
            </div>
            <span className="font-display font-bold text-xl text-white">Zentrix</span>
          </div>

          <div className="mb-8">
            <h2 className="font-display font-bold text-3xl text-white mb-2">Bem-vindo de volta</h2>
            <p className="text-muted">Entre na sua conta para continuar.</p>
          </div>

          {error && (
            <div className="flex items-center gap-3 bg-expense/10 border border-expense/20 text-expense rounded-xl px-4 py-3 mb-6 text-sm animate-fade-in">
              <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
              </svg>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs text-muted font-medium mb-2 uppercase tracking-wider">Email</label>
              <input
                type="email"
                placeholder="seu@email.com"
                value={form.email}
                onChange={set('email')}
                className="input-field"
                required
                autoComplete="email"
              />
            </div>

            <div>
              <label className="block text-xs text-muted font-medium mb-2 uppercase tracking-wider">Senha</label>
              <input
                type="password"
                placeholder="••••••••"
                value={form.password}
                onChange={set('password')}
                className="input-field"
                required
                autoComplete="current-password"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full mt-2 flex items-center justify-center gap-2 py-3"
            >
              {loading ? (
                <>
                  <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Entrando...
                </>
              ) : (
                'Entrar'
              )}
            </button>
          </form>

          <p className="text-center text-xs text-muted mt-8">
            Zentrix · Gestão financeira pessoal
          </p>
        </div>
      </div>
    </div>
  )
}
