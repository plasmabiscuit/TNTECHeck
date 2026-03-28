import { useCallback, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { LoadingState } from '../components/LoadingState';
import { ErrorState } from '../components/ErrorState';
import { useAsyncData } from '../components/useAsyncData';
import { fetchWorkspacePresetMetadata, runPresetReport } from '../services/api';

function ChartPreview({ chart }) {
  if (!chart || chart.points.length === 0 || chart.chart_type === 'none') {
    return <p className="muted">No chart data is available for this report run.</p>;
  }

  const maxY = Math.max(...chart.points.map((point) => point.y), 1);

  return (
    <>
      <p className="muted">{chart.note}</p>
      <ul className="chart-preview-list">
        {chart.points.map((point) => (
          <li key={point.x}>
            <span>{point.x}</span>
            <div className="chart-preview-track" aria-hidden="true">
              <span className="chart-preview-bar" style={{ width: `${(point.y / maxY) * 100}%` }} />
            </div>
            <strong>{point.y}</strong>
          </li>
        ))}
      </ul>
    </>
  );
}

export function ReportWorkspacePage() {
  const [searchParams] = useSearchParams();
  const presetId = searchParams.get('presetId');
  const [selectedComparisonGroupId, setSelectedComparisonGroupId] = useState(null);

  const metadataState = useAsyncData(fetchWorkspacePresetMetadata);
  const loadReport = useCallback(async () => {
    if (!presetId) {
      return null;
    }

    const fallbackComparisonGroupId =
      selectedComparisonGroupId ??
      metadataState.data?.presets
        ?.find((item) => item.id === presetId)
        ?.sections?.find((section) => section.comparison_group_id)?.comparison_group_id ??
      'tn_public_peers';

    return runPresetReport({
      presetId,
      comparisonGroupId: fallbackComparisonGroupId,
      filters: [{ field: 'comparison_group_id', operator: 'eq', value: fallbackComparisonGroupId }]
    });
  }, [metadataState.data, presetId, selectedComparisonGroupId]);
  const reportState = useAsyncData(loadReport);

  const workspace = useMemo(() => {
    if (!metadataState.data || !presetId) {
      return null;
    }

    const preset = metadataState.data.presets.find((item) => item.id === presetId);
    if (!preset) {
      return { missing: true };
    }

    const indicatorById = new Map(metadataState.data.indicators.map((indicator) => [indicator.id, indicator]));
    const sourceById = new Map(metadataState.data.sources.map((source) => [source.id, source]));
    const comparisonById = new Map(metadataState.data.comparisonGroups.map((group) => [group.id, group]));
    const programById = new Map(metadataState.data.programGroups.map((group) => [group.id, group]));

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
      programGroups,
      selectedComparisonGroupId:
        selectedComparisonGroupId ?? comparisonGroups[0]?.id ?? preset.sections.find((section) => section.comparison_group_id)?.comparison_group_id
    };
  }, [metadataState.data, presetId, selectedComparisonGroupId]);

  if (metadataState.loading || (presetId && reportState.loading)) {
    return <LoadingState label="Loading report workspace…" />;
  }

  if (metadataState.error) {
    return <ErrorState message={metadataState.error.message} onRetry={metadataState.retry} />;
  }

  if (reportState.error) {
    return <ErrorState message={reportState.error.message} onRetry={reportState.retry} />;
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

  if (!workspace || !reportState.data) {
    return null;
  }

  const primaryTable = reportState.data.tables[0];
  const primaryChart = reportState.data.charts[0];

  return (
    <section>
      <h2>Report Workspace</h2>
      <p>One preset can now execute end-to-end and returns normalized KPI, table, chart preview, and provenance payloads.</p>

      <article className="panel">
        <h3>Preset Metadata</h3>
        <p>
          <strong>{workspace.preset.label}</strong>
        </p>
        <p>{workspace.preset.description}</p>
        <p>
          <strong>Funder context:</strong> {workspace.preset.sponsor_context.join(', ')}
        </p>
        <label>
          Comparison group
          <select
            value={workspace.selectedComparisonGroupId ?? ''}
            onChange={(event) => setSelectedComparisonGroupId(event.target.value || null)}
          >
            {workspace.comparisonGroups.map((group) => (
              <option key={group.id} value={group.id}>
                {group.label}
              </option>
            ))}
          </select>
        </label>
      </article>

      <article className="panel">
        <h3>KPI Snapshot</h3>
        <div className="grid-two">
          {reportState.data.kpis.map((kpi) => (
            <div key={kpi.id} className="state-card">
              <p className="muted">{kpi.label}</p>
              <p className="kpi-value">
                {kpi.value}
                {kpi.unit === 'percent' ? '%' : ''}
              </p>
              {kpi.context_note ? <p className="muted">{kpi.context_note}</p> : null}
            </div>
          ))}
        </div>
      </article>

      <article className="panel">
        <h3>{primaryTable?.label || 'Report Table'}</h3>
        {primaryTable ? (
          <table>
            <thead>
              <tr>
                {primaryTable.columns.map((column) => (
                  <th key={column.key}>{column.label}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {primaryTable.rows.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {primaryTable.columns.map((column) => (
                    <td key={column.key}>{row.cells[column.key]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="muted">No tabular result rows were returned for this preset run.</p>
        )}
      </article>

      <article className="panel">
        <h3>Chart Output</h3>
        <ChartPreview chart={primaryChart} />
      </article>

      <div className="grid-two">
        <article className="panel">
          <h3>Source Notes</h3>
          <ul>
            {reportState.data.source_notes.map((note) => (
              <li key={note.source_id}>
                <strong>{note.source_name}</strong>: {note.note}
              </li>
            ))}
          </ul>
          {reportState.data.warnings.length > 0 ? (
            <p className="muted">Warnings: {reportState.data.warnings.join(' | ')}</p>
          ) : null}
        </article>

        <article className="panel">
          <h3>Run Provenance</h3>
          <p>
            <strong>Run ID:</strong> {reportState.data.run_id}
          </p>
          <p>
            <strong>Generated:</strong> {new Date(reportState.data.generated_at_utc).toLocaleString()}
          </p>
          <pre>{JSON.stringify(reportState.data.provenance, null, 2)}</pre>
        </article>
      </div>

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
    </section>
  );
}
