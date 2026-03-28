export function ErrorState({ title = 'Unable to load data', message, onRetry }) {
  return (
    <section className="state-card error" role="alert">
      <h2>{title}</h2>
      <p>{message ?? 'Please retry. If this continues, check backend connectivity.'}</p>
      {onRetry ? (
        <button type="button" onClick={onRetry}>
          Retry
        </button>
      ) : null}
    </section>
  );
}
