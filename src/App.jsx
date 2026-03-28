import { Navigate, Route, Routes } from 'react-router-dom';
import { AppLayout } from './components/AppLayout';
import { HomePage } from './pages/HomePage';
import { PresetCatalogPage } from './pages/PresetCatalogPage';
import { PlaceholderPage } from './pages/PlaceholderPage';

export function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/preset-catalog" element={<PresetCatalogPage />} />
        <Route
          path="/report-workspace"
          element={<PlaceholderPage title="Report Workspace" description="Run presets, inspect outputs, and export proposal-ready artifacts." />}
        />
        <Route
          path="/explore-builder"
          element={<PlaceholderPage title="Explore Builder" description="Build ad hoc indicator queries using normalized metadata and comparison controls." />}
        />
        <Route
          path="/eligibility-profiles"
          element={<PlaceholderPage title="Eligibility Profile Editor" description="Create and update editable eligibility templates with criteria and manual checks." />}
        />
        <Route
          path="/program-groups"
          element={<PlaceholderPage title="Program Group Manager" description="Define CIP-based program groups for strict, broad, and custom reporting contexts." />}
        />
        <Route
          path="/comparison-groups"
          element={<PlaceholderPage title="Comparison Group Manager" description="Maintain reusable peer and benchmark institution groups for TTU comparisons." />}
        />
        <Route
          path="/funding-history"
          element={<PlaceholderPage title="Funding History" description="Review sponsor-specific NIH, NSF, and NIFA historical award context for TTU." />}
        />
        <Route
          path="/settings"
          element={<PlaceholderPage title="Settings/Admin" description="Manage source endpoints, cache behavior, and metadata registries (no-auth local admin)." />}
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
