import React from 'react';
import { MainNav } from './MainNav';

interface LayoutProps {
  children: React.ReactNode;
  title?: string;
}

const Layout: React.FC<LayoutProps> = ({ children, title }) => {
  React.useEffect(() => {
    if (title) {
      document.title = `${title} - SynthLang`;
    }
  }, [title]);

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-14 items-center">
          <MainNav />
        </div>
      </header>
      <main className="flex-1">
        {children}
      </main>
    </div>
  );
};

export default Layout;
