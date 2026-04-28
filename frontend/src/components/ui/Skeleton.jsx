export function SkeletonCard({ className = '' }) {
  return (
    <div className={`card p-6 ${className}`}>
      <div className="shimmer-bg h-4 w-24 rounded-lg mb-4" />
      <div className="shimmer-bg h-8 w-40 rounded-lg mb-2" />
      <div className="shimmer-bg h-3 w-32 rounded-lg" />
    </div>
  )
}

export function SkeletonRow() {
  return (
    <div className="flex items-center gap-4 py-4 px-5">
      <div className="shimmer-bg w-10 h-10 rounded-xl shrink-0" />
      <div className="flex-1 space-y-2">
        <div className="shimmer-bg h-4 w-48 rounded-lg" />
        <div className="shimmer-bg h-3 w-24 rounded-lg" />
      </div>
      <div className="shimmer-bg h-5 w-20 rounded-lg" />
    </div>
  )
}

export function SkeletonText({ className = '' }) {
  return <div className={`shimmer-bg rounded-lg ${className}`} />
}
