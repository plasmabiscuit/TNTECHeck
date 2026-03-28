import { render, screen } from '@testing-library/react';
import { beforeEach, afterEach, describe, expect, it, vi } from 'vitest';
import { BrowserRouter } from 'react-router-dom';
import { App } from '../App';

function mockFetch(routes = {}) {
  return vi.spyOn(global, 'fetch').mockImplementation(async (url) => {
    const value = routes[url];
    if (!value) {
      return new Response('Not Found', { status: 404 });
    }

    return new Response(JSON.stringify(value), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  });
}

describe('App shell', () => {
  let fetchSpy;

  beforeEach(() => {
    window.history.pushState({}, '', '/');
    fetchSpy = mockFetch({
      '/api/metadata/workbench': {
        quickLinks: [
          { label: 'Institutional Overview', route: '/preset-catalog' },
          { label: 'Funding History', route: '/funding-history' }
        ],
        sourceHealth: [{ source: 'Urban', status: 'healthy' }],
        latestYearBySource: [{ source: 'Urban', latestYear: 2024, lastUpdatedUtc: '2026-03-20T00:00:00Z' }]
      }
    });
  });

  afterEach(() => {
    fetchSpy.mockRestore();
  });

  it('renders global shell with TTU context and module navigation', async () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    expect(screen.getByRole('heading', { name: 'TTU Grant Data Workbench' })).toBeInTheDocument();
    expect(screen.getByText(/Tennessee Technological University/)).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Preset Catalog' })).toBeInTheDocument();
    expect(await screen.findByRole('heading', { name: 'Home' })).toBeInTheDocument();
  });
});
