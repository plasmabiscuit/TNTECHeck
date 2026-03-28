import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { BrowserRouter } from 'react-router-dom';
import { App } from '../App';

function okJson(data) {
  return new Response(JSON.stringify(data), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  });
}

describe('Comparison Group Manager', () => {
  let fetchSpy;

  beforeEach(() => {
    fetchSpy = vi.spyOn(global, 'fetch').mockImplementation(async (url) => {
      if (url === '/api/meta/comparison-groups') {
        return okJson({
          data: [
            {
              id: 'tn_public_peers',
              label: 'TN Public Peers',
              description: 'Manual peers.',
              definition: { type: 'manual', institution_unitids: [1, 2] }
            },
            {
              id: 'carnegie_rule',
              label: 'Carnegie Rule',
              description: 'Rule placeholder.',
              definition: { type: 'rule_based', rule: { rule_type: 'carnegie', params: { basic: 'M1' } } }
            }
          ]
        });
      }

      if (url === '/api/metadata/workbench') {
        return okJson({ quickLinks: [], sourceHealth: [], latestYearBySource: [] });
      }

      return new Response('Not Found', { status: 404 });
    });
  });

  afterEach(() => {
    fetchSpy.mockRestore();
  });

  it('renders existing groups and toggles draft builder mode', async () => {
    window.history.pushState({}, '', '/comparison-groups');

    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    expect(await screen.findByText('Comparison Group Manager')).toBeInTheDocument();
    expect(screen.getByText('TN Public Peers')).toBeInTheDocument();
    expect(screen.getByText('Carnegie Rule')).toBeInTheDocument();

    await userEvent.selectOptions(screen.getByLabelText('Definition type'), 'rule_based');
    expect(screen.getByLabelText('Rule Type')).toBeInTheDocument();
  });
});
