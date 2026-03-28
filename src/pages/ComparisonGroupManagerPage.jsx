import { useCallback, useMemo, useState } from 'react';
import { ErrorState } from '../components/ErrorState';
import { LoadingState } from '../components/LoadingState';
import { useAsyncData } from '../components/useAsyncData';
import { fetchMetaRegistry } from '../services/api';

function ComparisonGroupCard({ group }) {
  const definitionType = group.definition?.type;

  return (
    <article className="state-card">
      <h3>{group.label}</h3>
      <p className="muted">{group.description}</p>
      <p>
        <strong>ID:</strong> {group.id}
      </p>
      <p>
        <strong>Definition:</strong> {definitionType === 'manual' ? 'Manual institution list' : 'Rule-based placeholder'}
      </p>
      {definitionType === 'manual' ? (
        <p>
          <strong>UNITIDs:</strong> {group.definition.institution_unitids.join(', ')}
        </p>
      ) : (
        <p>
          <strong>Rule:</strong> {group.definition.rule?.rule_type} ({JSON.stringify(group.definition.rule?.params || {})})
        </p>
      )}
    </article>
  );
}

export function ComparisonGroupManagerPage() {
  const loadComparisonGroups = useCallback(() => fetchMetaRegistry('comparison-groups'), []);
  const state = useAsyncData(loadComparisonGroups);
  const [draftMode, setDraftMode] = useState('manual');
  const [draftLabel, setDraftLabel] = useState('');
  const [draftId, setDraftId] = useState('');
  const [draftManualUnitids, setDraftManualUnitids] = useState('');
  const [draftRuleType, setDraftRuleType] = useState('');
  const [draftRuleParams, setDraftRuleParams] = useState('{}');

  const draftPreview = useMemo(() => {
    const base = {
      id: draftId,
      label: draftLabel,
      description: 'Draft-only preview in frontend manager.',
      definition: {
        type: draftMode
      }
    };

    if (draftMode === 'manual') {
      base.definition.institution_unitids = draftManualUnitids
        .split(',')
        .map((value) => Number.parseInt(value.trim(), 10))
        .filter((value) => Number.isInteger(value));
      return base;
    }

    let parsedParams = {};
    try {
      parsedParams = JSON.parse(draftRuleParams || '{}');
    } catch {
      parsedParams = { parse_error: 'Invalid JSON params' };
    }

    base.definition.rule = { rule_type: draftRuleType, params: parsedParams };
    return base;
  }, [draftId, draftLabel, draftManualUnitids, draftMode, draftRuleParams, draftRuleType]);

  if (state.loading) return <LoadingState label="Loading comparison groups…" />;
  if (state.error) return <ErrorState message={state.error.message} onRetry={state.retry} />;

  return (
    <section>
      <h2>Comparison Group Manager</h2>
      <p>Maintain reusable comparison groups with either explicit institution lists or rule-based placeholders.</p>

      <article className="panel">
        <h3>Registry Inventory</h3>
        <div className="grid-two">
          {state.data.data.map((group) => (
            <ComparisonGroupCard key={group.id} group={group} />
          ))}
        </div>
      </article>

      <article className="panel">
        <h3>Draft Definition Builder (local preview)</h3>
        <div className="grid-two">
          <label>
            Definition type
            <select value={draftMode} onChange={(event) => setDraftMode(event.target.value)}>
              <option value="manual">Manual institution list</option>
              <option value="rule_based">Rule-based placeholder</option>
            </select>
          </label>
          <label>
            Draft ID
            <input value={draftId} onChange={(event) => setDraftId(event.target.value)} placeholder="regional_publics" />
          </label>
          <label>
            Label
            <input value={draftLabel} onChange={(event) => setDraftLabel(event.target.value)} placeholder="Regional Publics" />
          </label>

          {draftMode === 'manual' ? (
            <label>
              UNITIDs (comma separated)
              <input
                value={draftManualUnitids}
                onChange={(event) => setDraftManualUnitids(event.target.value)}
                placeholder="220978,221759"
              />
            </label>
          ) : (
            <>
              <label>
                Rule Type
                <input value={draftRuleType} onChange={(event) => setDraftRuleType(event.target.value)} placeholder="carnegie" />
              </label>
              <label>
                Rule Params JSON
                <textarea
                  value={draftRuleParams}
                  onChange={(event) => setDraftRuleParams(event.target.value)}
                  rows={4}
                  placeholder='{"basic_classification":"M1"}'
                />
              </label>
            </>
          )}
        </div>

        <p className="muted">Preview only: persistence API can be added in a later registry-write workflow.</p>
        <pre>{JSON.stringify(draftPreview, null, 2)}</pre>
      </article>
    </section>
  );
}
