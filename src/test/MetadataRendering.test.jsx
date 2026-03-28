import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { BrowserRouter } from 'react-router-dom';
import { App } from '../App';

function okJson(data) {
  return new Response(JSON.stringify(data), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  });
}

describe('Metadata-backed pages', () => {
  let fetchSpy;

  afterEach(() => {
    fetchSpy?.mockRestore();
  });

  it('renders metadata on Home page', async () => {
    window.history.pushState({}, '', '/');
    fetchSpy = vi.spyOn(global, 'fetch').mockImplementation(async (url) => {
      if (url === '/api/metadata/workbench') {
        return okJson({
          quickLinks: [{ label: 'Biology Completions', route: '/preset-catalog' }],
          sourceHealth: [{ source: 'IPEDS', status: 'degraded' }],
          latestYearBySource: [{ source: 'IPEDS', latestYear: 2023, lastUpdatedUtc: '2026-03-21T00:00:00Z' }]
        });
      }
      return new Response('Not Found', { status: 404 });
    });

    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    expect(await screen.findByText('Biology Completions')).toBeInTheDocument();
    expect(screen.getByText('degraded')).toBeInTheDocument();
    expect(screen.getByRole('cell', { name: '2023' })).toBeInTheDocument();
  });

  it('renders preset catalog metadata and supports retry on error', async () => {
    window.history.pushState({}, '', '/preset-catalog');
    let presetCalls = 0;

    fetchSpy = vi.spyOn(global, 'fetch').mockImplementation(async (url) => {
      if (url === '/api/meta/presets') {
        presetCalls += 1;
        if (presetCalls === 1) {
          return new Response('Service Unavailable', { status: 503 });
        }

        return okJson({
          data: [
            {
              id: 'nih-eligibility-snapshot',
              label: 'NIH Eligibility Snapshot',
              sponsor_context: ['NIH'],
              description: 'Initial NIH-oriented readiness checks for TTU.',
              sections: [{ indicator_ids: ['pell_share'], program_group_ids: [], comparison_group_id: null }]
            }
          ]
        });
      }

      if (url === '/api/meta/indicators') {
        return okJson({
          data: [
            {
              id: 'pell_share',
              label: 'Pell Share',
              category: 'Student Success',
              source_ids: ['urban_ipeds']
            }
          ]
        });
      }

      if (url === '/api/meta/sources') {
        return okJson({ data: [{ id: 'urban_ipeds', name: 'Urban/IPEDS' }] });
      }

      if (url === '/api/metadata/workbench') {
        return okJson({ quickLinks: [], sourceHealth: [], latestYearBySource: [] });
      }

      return new Response('Not Found', { status: 404 });
    });

    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    expect(await screen.findByRole('alert')).toHaveTextContent('Service Unavailable');
    await userEvent.click(screen.getByRole('button', { name: 'Retry' }));

    expect((await screen.findAllByText('NIH Eligibility Snapshot')).length).toBeGreaterThan(0);
    expect(screen.getAllByText('Student Success').length).toBeGreaterThan(0);
  });
});
