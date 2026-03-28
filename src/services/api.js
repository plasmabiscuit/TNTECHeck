const API_BASE = '/api';

async function handleJsonResponse(response) {
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with status ${response.status}`);
  }

  return response.json();
}

export async function fetchWorkbenchMetadata() {
  const response = await fetch(`${API_BASE}/metadata/workbench`);
  return handleJsonResponse(response);
}

export async function fetchPresetCatalog() {
  const response = await fetch(`${API_BASE}/metadata/presets`);
  return handleJsonResponse(response);
}
