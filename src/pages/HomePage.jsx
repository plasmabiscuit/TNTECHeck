import { LoadingState } from '../components/LoadingState';
import { ErrorState } from '../components/ErrorState';
import { useAsyncData } from '../components/useAsyncData';
import { fetchWorkbenchMetadata } from '../services/api';

export function HomePage() {
  const { data, loading, error, retry } = useAsyncData(fetchWorkbenchMetadata);

  if (loading) {
    return <LoadingState label="Loading workbench metadata…" />;
  }

  if (error) {
    return <ErrorState message={error.message} onRetry={retry} />;
  }

  return (
    <section>
      <h2>Home</h2>
      <p>Launch common TTU-first grant development workflows and review data-source readiness.</p>

      <div className="grid-two">
        <article className="panel">
          <h3>Quick Launch</h3>
          <ul>
            {data.quickLinks.map((link) => (
              <li key={link.route}>{link.label}</li>
            ))}
          </ul>
        </article>

        <article className="panel">
          <h3>Source Health</h3>
          <ul>
            {data.sourceHealth.map((source) => (
              <li key={source.source}>
                <strong>{source.source}:</strong> {source.status}
              </li>
            ))}
          </ul>
        </article>
      </div>

      <article className="panel">
        <h3>Latest Data Year by Source</h3>
        <table>
          <thead>
            <tr>
              <th>Source</th>
              <th>Latest Year</th>
              <th>Updated</th>
            </tr>
          </thead>
          <tbody>
            {data.latestYearBySource.map((entry) => (
              <tr key={entry.source}>
                <td>{entry.source}</td>
                <td>{entry.latestYear}</td>
                <td>{entry.lastUpdatedUtc}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </article>
    </section>
  );
}
