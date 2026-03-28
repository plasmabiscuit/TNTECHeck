import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { BrowserRouter } from 'react-router-dom';
import { App } from '../App';

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' }
  });
}

describe('Comparison Group Manager page', () => {
  let fetchSpy;

  beforeEach(() => {
    let groups = [
      {
        id: 'tn_public_peers',
        label: 'TN Public Peers',
        description: 'seed',
        definition_type: 'manual_list',
        institution_unitids: [220978, 221759],
        rules: [],
        notes: null,
        version: 1
      }
    ];

    fetchSpy = vi.spyOn(global, 'fetch').mockImplementation(async (url, options = {}) => {
      if (url === '/api/comparison-groups' && (!options.method || options.method === 'GET')) {
        return jsonResponse({ data: groups, meta: { version: 'v1', count: groups.length } });
      }

      if (url === '/api/comparison-groups' && options.method === 'POST') {
        const payload = JSON.parse(options.body);
        if (payload.definition_type === 'manual_list' && payload.institution_unitids.length === 0) {
          return jsonResponse({ error: { code: 'EMPTY_COMPARISON_GROUP_UNITIDS', message: 'invalid', details: {} } }, 422);
        }
        groups = [...groups, { ...payload, version: 1 }];
        return jsonResponse({ ...payload, version: 1 });
      }

      if (url.startsWith('/api/comparison-groups/') && options.method === 'PUT') {
        const id = url.split('/').at(-1);
        const payload = JSON.parse(options.body);
        groups = groups.map((group) => (group.id === id ? { ...payload, version: group.version + 1 } : group));
        const updated = groups.find((group) => group.id === payload.id);
        return jsonResponse(updated);
      }

      if (url.startsWith('/api/comparison-groups/') && options.method === 'DELETE') {
        const id = url.split('/').at(-1);
        groups = groups.filter((group) => group.id !== id);
        return new Response(null, { status: 204 });
      }

      if (url === '/api/metadata/workbench') {
        return jsonResponse({ quickLinks: [], sourceHealth: [], latestYearBySource: [] });
      }

      return new Response('Not Found', { status: 404 });
    });
  });

  afterEach(() => {
    cleanup();
    fetchSpy.mockRestore();
  });

  it('lists, creates, and deletes comparison groups', async () => {
    window.history.pushState({}, '', '/comparison-groups');

    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    expect(await screen.findByRole('heading', { name: 'Comparison Group Manager' })).toBeInTheDocument();
    expect(screen.getAllByText('TN Public Peers').length).toBeGreaterThan(0);

    await userEvent.click(screen.getByRole('button', { name: 'New Group' }));
    await userEvent.type(screen.getByLabelText('ID'), 'rule_group');
    await userEvent.type(screen.getByLabelText('Label'), 'Rule Group');
    await userEvent.selectOptions(screen.getByLabelText('Definition type'), 'rule_based_placeholder');
    fireEvent.change(screen.getByLabelText('Rule definitions (JSON array)'), {
      target: { value: '[{\"field\":\"state\",\"operator\":\"eq\",\"value\":\"TN\"}]' }
    });

    await userEvent.click(screen.getByRole('button', { name: 'Save' }));
    expect(await screen.findByRole('status')).toHaveTextContent("Created comparison group 'Rule Group'.");

    await waitFor(() => {
      expect(screen.getAllByText('Rule Group').length).toBeGreaterThan(0);
    });

    await userEvent.click(screen.getByRole('button', { name: 'Delete' }));
    expect(await screen.findByRole('status')).toHaveTextContent("Deleted comparison group 'rule_group'.");
  });
});
