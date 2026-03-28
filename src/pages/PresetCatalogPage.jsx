import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LoadingState } from '../components/LoadingState';
import { ErrorState } from '../components/ErrorState';
import { useAsyncData } from '../components/useAsyncData';
import { fetchPresetCatalogMetadata } from '../services/api';

function summarizePreset(preset, indicatorById, sourceById) {
  const indicators = preset.sections.flatMap((section) =>
    section.indicator_ids.map((indicatorId) => indicatorById.get(indicatorId)).filter(Boolean)
  );

  const categorySet = new Set(indicators.map((indicator) => indicator.category));
  const sourceSet = new Set(indicators.flatMap((indicator) => indicator.source_ids));
  const sourceNames = [...sourceSet].map((sourceId) => sourceById.get(sourceId)?.name || sourceId);

  return {
    ...preset,
    categories: [...categorySet],
    sourceIds: [...sourceSet],
    sourceNames,
    comparisonGroupIds: preset.sections.map((section) => section.comparison_group_id).filter(Boolean),
    programGroupIds: preset.sections.flatMap((section) => section.program_group_ids)
  };
}

export function PresetCatalogPage() {
  const navigate = useNavigate();
  const { data, loading, error, retry } = useAsyncData(fetchPresetCatalogMetadata);
  const [filters, setFilters] = useState({ funder: 'all', category: 'all', source: 'all' });
  const [selectedPresetId, setSelectedPresetId] = useState(null);

  const catalog = useMemo(() => {
    if (!data) {
      return null;
    }

    const indicatorById = new Map(data.indicators.map((indicator) => [indicator.id, indicator]));
    const sourceById = new Map(data.sources.map((source) => [source.id, source]));
    const presets = data.presets.map((preset) => summarizePreset(preset, indicatorById, sourceById));

    return { presets, sourceById };
  }, [data]);

  const filterOptions = useMemo(() => {
    if (!catalog) {
      return { funders: [], categories: [], sources: [] };
    }

    return {
      funders: [...new Set(catalog.presets.flatMap((preset) => preset.sponsor_context))].sort(),
      categories: [...new Set(catalog.presets.flatMap((preset) => preset.categories))].sort(),
      sources: [...new Set(catalog.presets.flatMap((preset) => preset.sourceIds))]
        .map((sourceId) => ({ id: sourceId, name: catalog.sourceById.get(sourceId)?.name || sourceId }))
        .sort((a, b) => a.name.localeCompare(b.name))
    };
  }, [catalog]);

  const filteredPresets = useMemo(() => {
    if (!catalog) {
      return [];
    }

    return catalog.presets.filter((preset) => {
      const matchesFunder = filters.funder === 'all' || preset.sponsor_context.includes(filters.funder);
      const matchesCategory = filters.category === 'all' || preset.categories.includes(filters.category);
      const matchesSource = filters.source === 'all' || preset.sourceIds.includes(filters.source);
      return matchesFunder && matchesCategory && matchesSource;
    });
  }, [catalog, filters]);

  const selectedPreset = filteredPresets.find((preset) => preset.id === selectedPresetId) || filteredPresets[0] || null;

  if (loading) {
    return <LoadingState label="Loading proposal-ready preset catalog…" />;
  }

  if (error) {
    return <ErrorState message={error.message} onRetry={retry} />;
  }

  return (
    <section>
      <h2>Proposal Preset Catalog</h2>
      <p>
        Start from sponsor-aware reporting presets that frame TTU&apos;s story for proposal development, then launch into
        a workspace to refine assumptions and run query steps.
      </p>

      <div className="panel catalog-filters">
        <h3>Filter Presets</h3>
        <div className="grid-three">
          <label>
            Funder
            <select
              aria-label="Filter by funder"
              value={filters.funder}
              onChange={(event) => setFilters((current) => ({ ...current, funder: event.target.value }))}
            >
              <option value="all">All funders</option>
              {filterOptions.funders.map((funder) => (
                <option key={funder} value={funder}>
                  {funder}
                </option>
              ))}
            </select>
          </label>

          <label>
            Domain / Category
            <select
              aria-label="Filter by domain or category"
              value={filters.category}
              onChange={(event) => setFilters((current) => ({ ...current, category: event.target.value }))}
            >
              <option value="all">All domains</option>
              {filterOptions.categories.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </label>

          <label>
            Source
            <select
              aria-label="Filter by source"
              value={filters.source}
              onChange={(event) => setFilters((current) => ({ ...current, source: event.target.value }))}
            >
              <option value="all">All sources</option>
              {filterOptions.sources.map((source) => (
                <option key={source.id} value={source.id}>
                  {source.name}
                </option>
              ))}
            </select>
          </label>
        </div>
      </div>

      <div className="catalog-layout">
        <div>
          <h3>Available Presets ({filteredPresets.length})</h3>
          {filteredPresets.length === 0 ? (
            <div className="panel">No presets match the selected filters.</div>
          ) : (
            filteredPresets.map((preset) => (
              <article className="panel preset-card" key={preset.id}>
                <div className="preset-card-header">
                  <div>
                    <h4>{preset.label}</h4>
                    <p className="muted">{preset.description}</p>
                  </div>
                  <button type="button" onClick={() => setSelectedPresetId(preset.id)}>
                    View Details
                  </button>
                </div>
                <p>
                  <strong>Funders:</strong> {preset.sponsor_context.join(', ')}
                </p>
                <p>
                  <strong>Domains:</strong> {preset.categories.join(', ') || 'Not categorized'}
                </p>
                <p>
                  <strong>Required Sources:</strong> {preset.sourceNames.join(', ') || 'No source requirements'}
                </p>
                <button type="button" onClick={() => navigate(`/report-workspace?presetId=${preset.id}`)}>
                  Launch in Report Workspace
                </button>
              </article>
            ))
          )}
        </div>

        <aside className="panel">
          <h3>Preset Details</h3>
          {selectedPreset ? (
            <>
              <h4>{selectedPreset.label}</h4>
              <p>{selectedPreset.description}</p>
              <ul>
                <li>
                  <strong>Sections:</strong> {selectedPreset.sections.length}
                </li>
                <li>
                  <strong>Comparison support:</strong>{' '}
                  {selectedPreset.comparisonGroupIds.length > 0 ? 'Includes comparison group configuration' : 'None'}
                </li>
                <li>
                  <strong>Program-group support:</strong>{' '}
                  {selectedPreset.programGroupIds.length > 0 ? 'Includes mapped program groups' : 'Institution-level only'}
                </li>
              </ul>
            </>
          ) : (
            <p className="muted">Select a preset to review proposal setup details.</p>
          )}
        </aside>
      </div>
    </section>
  );
}
