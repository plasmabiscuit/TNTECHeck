import { NavLink, Outlet } from 'react-router-dom';

const navItems = [
  { to: '/', label: 'Home', end: true },
  { to: '/preset-catalog', label: 'Preset Catalog' },
  { to: '/report-workspace', label: 'Report Workspace' },
  { to: '/explore-builder', label: 'Explore Builder' },
  { to: '/eligibility-profiles', label: 'Eligibility Profile Editor' },
  { to: '/program-groups', label: 'Program Group Manager' },
  { to: '/comparison-groups', label: 'Comparison Group Manager' },
  { to: '/funding-history', label: 'Funding History' },
  { to: '/settings', label: 'Settings/Admin' }
];

export function AppLayout() {
  return (
    <div className="layout">
      <header className="app-header">
        <div>
          <h1>TTU Grant Data Workbench</h1>
          <p className="institution-context">Institution context: Tennessee Technological University (UNITID 221847)</p>
        </div>
      </header>
      <div className="app-main">
        <nav aria-label="Primary" className="primary-nav">
          <ul>
            {navItems.map((item) => (
              <li key={item.to}>
                <NavLink to={item.to} end={item.end} className={({ isActive }) => (isActive ? 'active' : undefined)}>
                  {item.label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
        <main>
          <Outlet />
        </main>
      </div>
    </div>
  );
}
