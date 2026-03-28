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

const fixture = {
  presets: {
    data: [
      {
        id: 'nih-bio-snapshot',
        label: 'NIH Biology Snapshot',
        sponsor_context: ['NIH'],
        description: 'Biology-focused proposal profile.',
        sections: [
          {
            indicator_ids: ['nih_award_count'],
            program_group_ids: ['biology_cip_group'],
            comparison_group_id: 'tn_public_peers'
          }
        ]
      },
      {
        id: 'nsf-equity-core',
        label: 'NSF Equity Core',
        sponsor_context: ['NSF'],
        description: 'Equity and enrollment baseline for NSF context.',
        sections: [
          {
            indicator_ids: ['pell_share'],
            program_group_ids: [],
            comparison_group_id: null
          }
        ]
      }
    ]
  },
  indicators: {
    data: [
      {
        id: 'nih_award_count',
        label: 'NIH Awards',
        category: 'Research Capacity',
        source_ids: ['nih_reporter']
      },
      {
        id: 'pell_share',
        label: 'Pell Share',
        category: 'Student Success',
        source_ids: ['urban_ipeds']
      }
    ]
  },
  sources: {
    data: [
      { id: 'nih_reporter', name: 'NIH RePORTER' },
      { id: 'urban_ipeds', name: 'Urban/IPEDS' }
    ]
  },
  comparisonGroups: {
    data: [{ id: 'tn_public_peers', label: 'TN Public Peers', institution_unitids: [1, 2] }]
  },
  programGroups: {
    data: [{ id: 'biology_cip_group', label: 'Biology CIP Group', cip_codes: ['26.0101'] }]
  }
};

describe('Preset catalog filtering and launch flow', () => {
  let fetchSpy;

  beforeEach(() => {
    fetchSpy = vi.spyOn(global, 'fetch').mockImplementation(async (url) => {
      if (url === '/api/meta/presets') return okJson(fixture.presets);
      if (url === '/api/meta/indicators') return okJson(fixture.indicators);
      if (url === '/api/meta/sources') return okJson(fixture.sources);
      if (url === '/api/meta/comparison-groups') return okJson(fixture.comparisonGroups);
      if (url === '/api/meta/program-groups') return okJson(fixture.programGroups);
      if (url === '/api/metadata/workbench') {
        return okJson({ quickLinks: [], sourceHealth: [], latestYearBySource: [] });
      }

      return new Response('Not Found', { status: 404 });
    });
  });

  afterEach(() => {
    fetchSpy.mockRestore();
  });

  it('filters presets by funder, category, and source', async () => {
    window.history.pushState({}, '', '/preset-catalog');

    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    expect((await screen.findAllByText('NIH Biology Snapshot')).length).toBeGreaterThan(0);
    expect(screen.getAllByText('NSF Equity Core').length).toBeGreaterThan(0);

    await userEvent.selectOptions(screen.getByLabelText('Filter by funder'), 'NIH');
    expect(screen.getAllByText('NIH Biology Snapshot').length).toBeGreaterThan(0);
    expect(screen.queryByText('NSF Equity Core')).not.toBeInTheDocument();

    await userEvent.selectOptions(screen.getByLabelText('Filter by funder'), 'all');
    await userEvent.selectOptions(screen.getByLabelText('Filter by domain or category'), 'Student Success');
    expect(screen.getAllByText('NSF Equity Core').length).toBeGreaterThan(0);
    expect(screen.queryByText('NIH Biology Snapshot')).not.toBeInTheDocument();

    await userEvent.selectOptions(screen.getByLabelText('Filter by domain or category'), 'all');
    await userEvent.selectOptions(screen.getByLabelText('Filter by source'), 'nih_reporter');
    expect(screen.getAllByText('NIH Biology Snapshot').length).toBeGreaterThan(0);
    expect(screen.queryByText('NSF Equity Core')).not.toBeInTheDocument();
  });

  it('launches a preset into report workspace with metadata context', async () => {
    window.history.pushState({}, '', '/preset-catalog');

    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    expect((await screen.findAllByText('NIH Biology Snapshot')).length).toBeGreaterThan(0);
    await userEvent.click(screen.getAllByRole('button', { name: 'Launch in Report Workspace' })[0]);

    expect(await screen.findByRole('heading', { name: 'Report Workspace' })).toBeInTheDocument();
    expect(screen.getAllByText('Biology-focused proposal profile.').length).toBeGreaterThan(0);
    expect(screen.getAllByText(/NIH RePORTER/).length).toBeGreaterThan(0);
    expect(screen.getByText(/TN Public Peers/)).toBeInTheDocument();
    expect(screen.getByText(/Biology CIP Group/)).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Next Query Controls (Placeholder)' })).toBeInTheDocument();
  });
});
