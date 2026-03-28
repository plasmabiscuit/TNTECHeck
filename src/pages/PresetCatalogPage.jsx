import { LoadingState } from '../components/LoadingState';
import { ErrorState } from '../components/ErrorState';
import { useAsyncData } from '../components/useAsyncData';
import { fetchPresetCatalog } from '../services/api';

export function PresetCatalogPage() {
  const { data, loading, error, retry } = useAsyncData(fetchPresetCatalog);

  if (loading) {
    return <LoadingState label="Loading preset catalog…" />;
  }

  if (error) {
    return <ErrorState message={error.message} onRetry={retry} />;
  }

  return (
    <section>
      <h2>Preset Catalog</h2>
      <p>Curated, proposal-oriented report presets with source and indicator provenance.</p>

      <div className="panel">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Category</th>
              <th>Funder Tags</th>
              <th>Required Sources</th>
            </tr>
          </thead>
          <tbody>
            {data.presets.map((preset) => (
              <tr key={preset.id}>
                <td>
                  <strong>{preset.name}</strong>
                  <div className="muted">{preset.description}</div>
                </td>
                <td>{preset.category}</td>
                <td>{preset.funderTags.join(', ') || 'None'}</td>
                <td>{preset.requiredSources.join(', ')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
