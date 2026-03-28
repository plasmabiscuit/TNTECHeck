import { useMemo, useState } from 'react';
import { ErrorState } from '../components/ErrorState';
import { LoadingState } from '../components/LoadingState';
import { useAsyncData } from '../components/useAsyncData';
import {
  createComparisonGroup,
  deleteComparisonGroup,
  fetchComparisonGroups,
  updateComparisonGroup
} from '../services/api';

const definitionTypes = ['manual_list', 'rule_based_placeholder'];

function emptyForm() {
  return {
    id: '',
    label: '',
    description: '',
    definitionType: 'manual_list',
    institutionUnitidsText: '',
    rulesText: '[\n  {"field":"sector","operator":"eq","value":"public_4_year"}\n]',
    notes: ''
  };
}

function parseUnitids(value) {
  return value
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean)
    .map((item) => Number(item));
}

function toPayload(formState) {
  const parsedRules = formState.rulesText.trim() ? JSON.parse(formState.rulesText) : [];
  return {
    id: formState.id.trim(),
    label: formState.label.trim(),
    description: formState.description.trim() || null,
    definition_type: formState.definitionType,
    institution_unitids: parseUnitids(formState.institutionUnitidsText),
    rules: Array.isArray(parsedRules) ? parsedRules : [],
    notes: formState.notes.trim() || null
  };
}

function applyGroupToForm(group) {
  return {
    id: group.id,
    label: group.label,
    description: group.description ?? '',
    definitionType: group.definition_type,
    institutionUnitidsText: (group.institution_unitids ?? []).join(', '),
    rulesText: JSON.stringify(group.rules ?? [], null, 2),
    notes: group.notes ?? ''
  };
}

export function ComparisonGroupsPage() {
  const { data, loading, error, retry } = useAsyncData(fetchComparisonGroups);
  const [selectedId, setSelectedId] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [formState, setFormState] = useState(emptyForm);
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
  }

  function beginCreate() {
    setEditingId('__new__');
    setFormState(emptyForm());
    setActionError('');
  }

  function beginEdit(group) {
    setEditingId(group.id);
    setSelectedId(group.id);
    setFormState(applyGroupToForm(group));
    setActionError('');
  }

  function cancelEdit() {
    setEditingId(null);
    setFormState(emptyForm());
    setActionError('');
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setActionError('');
    setStatusMessage('');

    try {
      const payload = toPayload(formState);
      if (editingId === '__new__') {
        const created = await createComparisonGroup(payload);
        setSelectedId(created.id);
        setEditingId(null);
        await refreshAndReset(`Created comparison group '${created.label}'.`);
        return;
      }

      const updated = await updateComparisonGroup(editingId, payload);
      setSelectedId(updated.id);
      setEditingId(null);
      await refreshAndReset(`Updated comparison group '${updated.label}'.`);
    } catch (submitError) {
      setActionError(submitError.message);
    }
  }

  async function handleDelete(id) {
    setActionError('');
    setStatusMessage('');

    try {
      await deleteComparisonGroup(id);
      if (selectedId === id) {
        setSelectedId(null);
      }
      await refreshAndReset(`Deleted comparison group '${id}'.`);
    } catch (deleteError) {
      setActionError(deleteError.message);
    }
  }

  if (loading) {
    return <LoadingState label="Loading comparison groups…" />;
  }

  if (error) {
    return <ErrorState message={error.message} onRetry={retry} />;
  }

  return (
    <section>
      <h2>Comparison Group Manager</h2>
      <p>Maintain reusable manual lists and rule-based placeholders for TTU benchmark context.</p>

      {statusMessage ? <p role="status">{statusMessage}</p> : null}
      {actionError ? <ErrorState message={actionError} /> : null}

      <div className="grid-two">
        <article className="panel">
          <div className="panel-header">
            <h3>Comparison Groups</h3>
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
            <p className="muted">No comparison groups defined yet.</p>
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
                <strong>Type:</strong> {selectedGroup.definition_type}
              </p>
              <p>
                <strong>UNITIDs:</strong> {(selectedGroup.institution_unitids ?? []).join(', ') || 'None'}
              </p>
              <p>
                <strong>Rules:</strong> {(selectedGroup.rules ?? []).length}
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
          <h3>{editingId === '__new__' ? 'Create Comparison Group' : `Edit ${editingId}`}</h3>
          <form className="stack-form" onSubmit={handleSubmit}>
            <label>
              ID
              <input value={formState.id} onChange={(event) => setFormState((current) => ({ ...current, id: event.target.value }))} required />
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
              Definition type
              <select
                value={formState.definitionType}
                onChange={(event) => setFormState((current) => ({ ...current, definitionType: event.target.value }))}
              >
                {definitionTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Institution UNITIDs (comma-separated)
              <input
                value={formState.institutionUnitidsText}
                onChange={(event) => setFormState((current) => ({ ...current, institutionUnitidsText: event.target.value }))}
              />
            </label>

            <label>
              Rule definitions (JSON array)
              <textarea
                value={formState.rulesText}
                onChange={(event) => setFormState((current) => ({ ...current, rulesText: event.target.value }))}
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
              <textarea value={formState.notes} onChange={(event) => setFormState((current) => ({ ...current, notes: event.target.value }))} />
            </label>

            <div className="button-row">
              <button type="submit">Save</button>
              <button type="button" onClick={cancelEdit}>
                Cancel
              </button>
            </div>
          </form>
        </article>
      ) : null}
    </section>
  );
}
