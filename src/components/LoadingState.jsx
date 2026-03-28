export function LoadingState({ label = 'Loading…' }) {
  return (
    <div role="status" className="state-card" aria-live="polite">
      <p>{label}</p>
    </div>
  );
}
