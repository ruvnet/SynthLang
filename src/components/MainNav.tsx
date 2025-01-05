import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const NAV_ITEMS = [
  { href: '/', label: 'Home' },
  { href: '/documentation', label: 'Documentation' },
  { href: '/playground', label: 'Playground' },
  { href: '/advanced-calculator', label: 'Advanced Calculator' },
  { href: '/analytics', label: 'Analytics' },
  { href: '/translate', label: 'Translate' },
  { href: '/settings', label: 'Settings' },
  { href: '/about', label: 'About' }
];

export const MainNav: React.FC = () => {
  const location = useLocation();

  return (
    <nav className="flex items-center space-x-4 lg:space-x-6">
      {NAV_ITEMS.map(({ href, label }) => (
        <Link
          key={href}
          to={href}
          className={`text-sm font-medium transition-colors hover:text-primary ${
            location.pathname === href
              ? 'text-primary'
              : 'text-muted-foreground'
          }`}
        >
          {label}
        </Link>
      ))}
    </nav>
  );
};
