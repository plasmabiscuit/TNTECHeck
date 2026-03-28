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
    let calls = 0;

    fetchSpy = vi.spyOn(global, 'fetch').mockImplementation(async (url) => {
      if (url === '/api/metadata/presets') {
        calls += 1;
        if (calls === 1) {
          return new Response('Service Unavailable', { status: 503 });
        }

        return okJson({
          presets: [
            {
              id: 'nih-eligibility-snapshot',
              name: 'NIH Eligibility Snapshot',
              category: 'Eligibility Worksheet',
              funderTags: ['NIH'],
              description: 'Initial NIH-oriented readiness checks for TTU.',
              requiredSources: ['Urban/IPEDS', 'NIH RePORTER']
            }
          ]
        });
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

    expect(await screen.findByText('NIH Eligibility Snapshot')).toBeInTheDocument();
    expect(screen.getByText('Eligibility Worksheet')).toBeInTheDocument();
  });
});
