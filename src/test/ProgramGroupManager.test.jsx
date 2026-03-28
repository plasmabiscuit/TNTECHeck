import { cleanup, render, screen, waitFor } from '@testing-library/react';
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

describe('Program Group Manager page', () => {
  let fetchSpy;

  beforeEach(() => {
    let groups = [
      {
        id: 'biology_cip_group',
        label: 'Biology',
        scope: 'strict',
        description: 'Biology programs',
        cip_codes: ['26.0101'],
        award_levels: ['bachelor', 'master'],
        notes: 'seed',
        version: 1
      }
    ];

    fetchSpy = vi.spyOn(global, 'fetch').mockImplementation(async (url, options = {}) => {
      if (url === '/api/program-groups' && (!options.method || options.method === 'GET')) {
        return jsonResponse({ data: groups, meta: { version: 'v1', count: groups.length } });
      }

      if (url === '/api/program-groups/preview' && options.method === 'POST') {
        const payload = JSON.parse(options.body);
        if (payload.cip_codes.some((code) => !/^\d{2}(\.\d{2}(\d{2})?)?$/.test(code))) {
          return jsonResponse({ error: { code: 'INVALID_PROGRAM_GROUP_CIP', message: 'invalid', details: {} } }, 422);
        }

        const uniqueLevels = [...new Set(payload.award_levels)];
        return jsonResponse({
          requested_scope: payload.scope,
          total_cip_codes: payload.cip_codes.length,
          total_award_levels: uniqueLevels.length,
          total_combinations: payload.cip_codes.length * uniqueLevels.length,
          items: payload.cip_codes.map((code) => ({ cip_code: code, award_levels: uniqueLevels }))
        });
      }

      if (url === '/api/program-groups' && options.method === 'POST') {
        const payload = JSON.parse(options.body);
        groups = [...groups, { ...payload, version: 1 }];
        return jsonResponse({ ...payload, version: 1 });
      }

      if (url.startsWith('/api/program-groups/') && options.method === 'PUT') {
        const id = url.split('/').at(-1);
        const payload = JSON.parse(options.body);
        groups = groups.map((group) => (group.id === id ? { ...payload, version: group.version + 1 } : group));
        const updated = groups.find((group) => group.id === payload.id);
        return jsonResponse(updated);
      }

      if (url.startsWith('/api/program-groups/') && options.method === 'DELETE') {
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

  it('lists, previews, creates, and deletes program groups', async () => {
    window.history.pushState({}, '', '/program-groups');

    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    expect(await screen.findByRole('heading', { name: 'Program Group Manager' })).toBeInTheDocument();
    expect(screen.getAllByText('Biology').length).toBeGreaterThan(0);

    await userEvent.click(screen.getAllByRole('button', { name: 'New Group' })[0]);
    await userEvent.type(screen.getByLabelText('ID'), 'custom_stem');
    await userEvent.type(screen.getByLabelText('Label'), 'Custom STEM');
    await userEvent.type(screen.getByLabelText('CIP codes (comma-separated)'), '14.0801, 26.0101');
    await userEvent.type(screen.getByLabelText('Award levels (comma-separated)'), 'bachelor, master');

    await userEvent.click(screen.getByRole('button', { name: 'Preview' }));
    expect(await screen.findByText(/4 combinations/)).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: 'Save' }));
    expect(await screen.findByRole('status')).toHaveTextContent("Created program group 'Custom STEM'.");

    await waitFor(() => {
      expect(screen.getAllByText('Custom STEM').length).toBeGreaterThan(0);
    });

    await userEvent.click(screen.getByRole('button', { name: 'Delete' }));
    expect(await screen.findByRole('status')).toHaveTextContent("Deleted program group 'custom_stem'.");
  });

  it('shows validation errors from preview endpoint for malformed CIPs', async () => {
    window.history.pushState({}, '', '/program-groups');

    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    expect(await screen.findByRole('heading', { name: 'Program Group Manager' })).toBeInTheDocument();

    await userEvent.click(screen.getAllByRole('button', { name: 'New Group' })[0]);
    await userEvent.type(screen.getByLabelText('ID'), 'bad_group');
    await userEvent.type(screen.getByLabelText('Label'), 'Bad Group');
    await userEvent.type(screen.getByLabelText('CIP codes (comma-separated)'), 'bad-cip');
    await userEvent.type(screen.getByLabelText('Award levels (comma-separated)'), 'bachelor');
    await userEvent.click(screen.getByRole('button', { name: 'Preview' }));

    expect(await screen.findByRole('alert')).toBeInTheDocument();
  });
});
