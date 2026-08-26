

export type StatusVariant = 'ready' | 'idle' | 'success' | 'warning' | 'error' | 'offline';

interface StatusIndicatorProps {
  variant: StatusVariant;
  label: string;
}

export function StatusIndicator({ variant, label }: StatusIndicatorProps) {
  const getColors = () => {
    switch (variant) {
      case 'ready':
      case 'success':
        return 'bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.5)]';
      case 'warning':
        return 'bg-amber-400 shadow-[0_0_8px_rgba(251,191,36,0.5)]';
      case 'error':
        return 'bg-rose-500 shadow-[0_0_8px_rgba(244,63,94,0.5)]';
      case 'offline':
      case 'idle':
      default:
        return 'bg-slate-500';
    }
  };

  return (
    <div className="flex items-center gap-2">
      <div className={`w-2 h-2 rounded-full ${getColors()}`} />
      <span className="text-xs text-slate-300 font-medium">{label}</span>
    </div>
  );
}
