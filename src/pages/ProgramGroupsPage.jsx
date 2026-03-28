import { useMemo, useState } from 'react';
import { ErrorState } from '../components/ErrorState';
import { LoadingState } from '../components/LoadingState';
import { useAsyncData } from '../components/useAsyncData';
import {
  createProgramGroup,
  deleteProgramGroup,
  fetchProgramGroups,
  previewProgramGroup,
  updateProgramGroup
} from '../services/api';

const scopeOptions = ['strict', 'broad', 'custom'];

function emptyForm() {
  return {
    id: '',
    label: '',
    scope: 'custom',
    description: '',
    cipCodesText: '',
    awardLevelsText: '',
    notes: ''
  };
}

function parseListInput(value) {
  return value
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
}

function toPayload(formState) {
  return {
    id: formState.id.trim(),
    label: formState.label.trim(),
    scope: formState.scope,
    description: formState.description.trim() || null,
    cip_codes: parseListInput(formState.cipCodesText),
    award_levels: parseListInput(formState.awardLevelsText),
    notes: formState.notes.trim() || null
  };
}

function applyGroupToForm(group) {
  return {
    id: group.id,
    label: group.label,
    scope: group.scope,
    description: group.description ?? '',
    cipCodesText: group.cip_codes.join(', '),
    awardLevelsText: group.award_levels.join(', '),
    notes: group.notes ?? ''
  };
}

export function ProgramGroupsPage() {
  const { data, loading, error, retry } = useAsyncData(fetchProgramGroups);
  const [selectedId, setSelectedId] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [formState, setFormState] = useState(emptyForm);
  const [previewData, setPreviewData] = useState(null);
  const [actionError, setActionError] = useState('');
  const [statusMessage, setStatusMessage] = useState('');

  const groups = data?.data ?? [];

  const selectedGroup = useMemo(() => {
    if (!groups.length) return null;
    const found = groups.find((group) => group.id === selectedId);
    return found ?? groups[0];
  }, [groups, selectedId]);

  async function refreshAndReset(message) {
    await retry();
    setStatusMessage(message);
    setActionError('');
    setPreviewData(null);
  }

  function beginCreate() {
    setEditingId('__new__');
    setFormState(emptyForm());
    setPreviewData(null);
    setActionError('');
  }

  function beginEdit(group) {
    setEditingId(group.id);
    setSelectedId(group.id);
    setFormState(applyGroupToForm(group));
    setPreviewData(null);
    setActionError('');
  }

  function cancelEdit() {
    setEditingId(null);
    setFormState(emptyForm());
    setPreviewData(null);
    setActionError('');
  }

  async function handlePreview(event) {
    event.preventDefault();
    setActionError('');
    setStatusMessage('');

    try {
      const response = await previewProgramGroup(toPayload(formState));
      setPreviewData(response);
    } catch (previewError) {
      setPreviewData(null);
      setActionError(previewError.message);
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setActionError('');
    setStatusMessage('');

    const payload = toPayload(formState);

    try {
      if (editingId === '__new__') {
        const created = await createProgramGroup(payload);
        setSelectedId(created.id);
        setEditingId(null);
        await refreshAndReset(`Created program group '${created.label}'.`);
        return;
      }

      const updated = await updateProgramGroup(editingId, payload);
      setSelectedId(updated.id);
      setEditingId(null);
      await refreshAndReset(`Updated program group '${updated.label}'.`);
    } catch (submitError) {
      setActionError(submitError.message);
    }
  }

  async function handleDelete(id) {
    setActionError('');
    setStatusMessage('');

    try {
      await deleteProgramGroup(id);
      if (selectedId === id) {
        setSelectedId(null);
      }
      await refreshAndReset(`Deleted program group '${id}'.`);
    } catch (deleteError) {
      setActionError(deleteError.message);
    }
  }

  if (loading) {
    return <LoadingState label="Loading program groups…" />;
  }

  if (error) {
    return <ErrorState message={error.message} onRetry={retry} />;
  }

  return (
    <section>
      <h2>Program Group Manager</h2>
      <p>Manage CIP-based program groups so TTU can build department-like completions views without hardcoded mappings.</p>

      {statusMessage ? <p role="status">{statusMessage}</p> : null}
      {actionError ? <ErrorState message={actionError} /> : null}

      <div className="grid-two">
        <article className="panel">
          <div className="panel-header">
            <h3>Program Groups</h3>
            <button type="button" onClick={beginCreate}>
              New Group
            </button>
          </div>
          {groups.length ? (
            <ul className="list-reset">
              {groups.map((group) => (
                <li key={group.id}>
                  <button type="button" className="list-button" onClick={() => setSelectedId(group.id)}>
                    <strong>{group.label}</strong>
                    <span className="muted">{group.id}</span>
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <p className="muted">No groups defined yet.</p>
          )}
        </article>

        <article className="panel">
          <h3>Group Details</h3>
          {selectedGroup ? (
            <>
              <p>
                <strong>{selectedGroup.label}</strong> <span className="muted">({selectedGroup.id})</span>
              </p>
              <p>
                <strong>Scope:</strong> {selectedGroup.scope}
              </p>
              <p>
                <strong>Award levels:</strong> {selectedGroup.award_levels.join(', ')}
              </p>
              <p>
                <strong>CIPs:</strong> {selectedGroup.cip_codes.join(', ')}
              </p>
              <p>
                <strong>Version:</strong> {selectedGroup.version}
              </p>
              <p className="muted">{selectedGroup.description || 'No description provided.'}</p>
              <div className="button-row">
                <button type="button" onClick={() => beginEdit(selectedGroup)}>
                  Edit
                </button>
                <button type="button" onClick={() => handleDelete(selectedGroup.id)}>
                  Delete
                </button>
              </div>
            </>
          ) : (
            <p className="muted">Select a group to inspect details.</p>
          )}
        </article>
      </div>

      {editingId ? (
        <article className="panel">
          <h3>{editingId === '__new__' ? 'Create Program Group' : `Edit ${editingId}`}</h3>
          <form className="stack-form" onSubmit={handleSubmit}>
            <label>
              ID
              <input
                value={formState.id}
                onChange={(event) => setFormState((current) => ({ ...current, id: event.target.value }))}
                required
              />
            </label>

            <label>
              Label
              <input
                value={formState.label}
                onChange={(event) => setFormState((current) => ({ ...current, label: event.target.value }))}
                required
              />
            </label>

            <label>
              Scope
              <select
                value={formState.scope}
                onChange={(event) => setFormState((current) => ({ ...current, scope: event.target.value }))}
              >
                {scopeOptions.map((scope) => (
                  <option key={scope} value={scope}>
                    {scope}
                  </option>
                ))}
              </select>
            </label>

            <label>
              CIP codes (comma-separated)
              <input
                value={formState.cipCodesText}
                onChange={(event) => setFormState((current) => ({ ...current, cipCodesText: event.target.value }))}
                required
              />
            </label>

            <label>
              Award levels (comma-separated)
              <input
                value={formState.awardLevelsText}
                onChange={(event) => setFormState((current) => ({ ...current, awardLevelsText: event.target.value }))}
                required
              />
            </label>

            <label>
              Description
              <textarea
                value={formState.description}
                onChange={(event) => setFormState((current) => ({ ...current, description: event.target.value }))}
              />
            </label>

            <label>
              Notes
              <textarea
                value={formState.notes}
                onChange={(event) => setFormState((current) => ({ ...current, notes: event.target.value }))}
              />
            </label>

            <div className="button-row">
              <button type="button" onClick={handlePreview}>
                Preview
              </button>
              <button type="submit">Save</button>
              <button type="button" onClick={cancelEdit}>
                Cancel
              </button>
            </div>
          </form>

          {previewData ? (
            <div>
              <h4>Preview Summary</h4>
              <p>
                Scope <strong>{previewData.requested_scope}</strong> · {previewData.total_cip_codes} CIPs ·{' '}
                {previewData.total_award_levels} award levels · {previewData.total_combinations} combinations
              </p>
              <ul>
                {previewData.items.map((item) => (
                  <li key={item.cip_code}>
                    {item.cip_code}: {item.award_levels.join(', ')}
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
        </article>
      ) : null}
    </section>
  );
}
