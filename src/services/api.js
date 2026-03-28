const API_BASE = '/api';

async function handleJsonResponse(response) {
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with status ${response.status}`);
  }

  return response.json();
}

export async function fetchMetaRegistry(name) {
  const response = await fetch(`${API_BASE}/meta/${name}`);
  return handleJsonResponse(response);
}

export async function fetchWorkbenchMetadata() {
  const response = await fetch(`${API_BASE}/metadata/workbench`);
  return handleJsonResponse(response);
}

export async function fetchPresetCatalogMetadata() {
  const [presets, indicators, sources] = await Promise.all([
    fetchMetaRegistry('presets'),
    fetchMetaRegistry('indicators'),
    fetchMetaRegistry('sources')
  ]);

  return {
    presets: presets.data,
    indicators: indicators.data,
    sources: sources.data
  };
}

export async function fetchWorkspacePresetMetadata() {
  const [presets, indicators, sources, comparisonGroups, programGroups] = await Promise.all([
    fetchMetaRegistry('presets'),
    fetchMetaRegistry('indicators'),
    fetchMetaRegistry('sources'),
    fetchMetaRegistry('comparison-groups'),
    fetchMetaRegistry('program-groups')
  ]);

  return {
    presets: presets.data,
    indicators: indicators.data,
    sources: sources.data,
    comparisonGroups: comparisonGroups.data,
    programGroups: programGroups.data
  };
}

export async function runPresetReport({ presetId, filters = [] }) {
  const response = await fetch(`${API_BASE}/report/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      preset_id: presetId,
      filters: { items: filters }
    })
  });

  return handleJsonResponse(response);
}
