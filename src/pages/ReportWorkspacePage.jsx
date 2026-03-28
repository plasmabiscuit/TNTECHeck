import { useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { LoadingState } from '../components/LoadingState';
import { ErrorState } from '../components/ErrorState';
import { useAsyncData } from '../components/useAsyncData';
import { fetchWorkspacePresetMetadata } from '../services/api';

export function ReportWorkspacePage() {
  const [searchParams] = useSearchParams();
  const presetId = searchParams.get('presetId');
  const { data, loading, error, retry } = useAsyncData(fetchWorkspacePresetMetadata);

  const workspace = useMemo(() => {
    if (!data || !presetId) {
      return null;
    }

    const preset = data.presets.find((item) => item.id === presetId);
    if (!preset) {
      return { missing: true };
    }

    const indicatorById = new Map(data.indicators.map((indicator) => [indicator.id, indicator]));
    const sourceById = new Map(data.sources.map((source) => [source.id, source]));
    const comparisonById = new Map(data.comparisonGroups.map((group) => [group.id, group]));
    const programById = new Map(data.programGroups.map((group) => [group.id, group]));

    const indicatorIds = new Set(preset.sections.flatMap((section) => section.indicator_ids));
    const indicators = [...indicatorIds].map((indicatorId) => indicatorById.get(indicatorId)).filter(Boolean);
    const sourceIds = new Set(indicators.flatMap((indicator) => indicator.source_ids));

    const comparisonGroups = preset.sections
      .map((section) => section.comparison_group_id)
      .filter(Boolean)
      .map((groupId) => comparisonById.get(groupId))
      .filter(Boolean);

    const programGroups = preset.sections
      .flatMap((section) => section.program_group_ids)
      .map((groupId) => programById.get(groupId))
      .filter(Boolean);

    return {
      preset,
      requiredSources: [...sourceIds].map((sourceId) => sourceById.get(sourceId)).filter(Boolean),
      indicators,
      comparisonGroups,
      programGroups
    };
  }, [data, presetId]);

  if (loading) {
    return <LoadingState label="Loading report workspace…" />;
  }

  if (error) {
    return <ErrorState message={error.message} onRetry={retry} />;
  }

  if (!presetId) {
    return (
      <section>
        <h2>Report Workspace</h2>
        <p className="muted">Launch from the Preset Catalog to initialize a proposal-oriented workspace state.</p>
      </section>
    );
  }

  if (workspace?.missing) {
    return (
      <section>
        <h2>Report Workspace</h2>
        <p className="muted">Preset &quot;{presetId}&quot; was not found in the backend preset registry.</p>
      </section>
    );
  }

  if (!workspace) {
    return null;
  }

  return (
    <section>
      <h2>Report Workspace</h2>
      <p>
        Structured launch state for proposal development. Confirm metadata, required sources, and comparison/program
        context before running query steps.
      </p>

      <article className="panel">
        <h3>Preset Metadata</h3>
        <p>
          <strong>{workspace.preset.label}</strong>
        </p>
        <p>{workspace.preset.description}</p>
        <p>
          <strong>Funder context:</strong> {workspace.preset.sponsor_context.join(', ')}
        </p>
      </article>

      <div className="grid-two">
        <article className="panel">
          <h3>Required Sources</h3>
          <ul>
            {workspace.requiredSources.map((source) => (
              <li key={source.id}>
                {source.name} <span className="muted">({source.id})</span>
              </li>
            ))}
          </ul>
        </article>

        <article className="panel">
          <h3>Supported Comparison / Program-Group Behavior</h3>
          <p>
            <strong>Comparison groups:</strong>{' '}
            {workspace.comparisonGroups.length > 0
              ? workspace.comparisonGroups.map((group) => group.label).join(', ')
              : 'No preset comparison groups'}
          </p>
          <p>
            <strong>Program groups:</strong>{' '}
            {workspace.programGroups.length > 0
              ? workspace.programGroups.map((group) => group.label).join(', ')
              : 'No preset program-group mappings'}
          </p>
        </article>
      </div>

      <article className="panel">
        <h3>Next Query Controls (Placeholder)</h3>
        <p className="muted">
          Full report execution is not implemented yet. Use these controls as the coherent launch scaffolding for
          upcoming query orchestration.
        </p>
        <div className="button-row">
          <button type="button">Select section</button>
          <button type="button">Review source readiness</button>
          <button type="button">Run preview query</button>
        </div>
      </article>

      <article className="panel">
        <h3>Indicator Snapshot</h3>
        <ul>
          {workspace.indicators.map((indicator) => (
            <li key={indicator.id}>
              <strong>{indicator.label}</strong> <span className="muted">({indicator.category})</span>
            </li>
          ))}
        </ul>
      </article>
    </section>
  );
}
