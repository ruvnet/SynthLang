import { Link } from "react-router-dom";
import { Terminal, Menu, X } from "lucide-react";
import { useState } from "react";

const navItems = [
  { name: "Home", path: "/" },
  { name: "Templates", path: "/templates" },
  { name: "Documentation", path: "/docs" },
  { name: "Settings", path: "/settings" },
  { name: "About", path: "/about" }
];

interface MainNavProps {
  title: string;
}

const MainNav = ({ title }: MainNavProps) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="glass-panel p-6 m-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4 flex-1 min-w-0">
          <Terminal className="w-6 h-6 text-console-cyan flex-shrink-0" />
          <h1 className="typing-container font-code text-xl truncate">
          {title}
        </h1>
        </div>

        {/* Mobile Menu Button */}
        <button
          className="md:hidden console-button p-2"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-label="Toggle menu"
        >
          {mobileMenuOpen ? (
            <X className="w-5 h-5" />
          ) : (
            <Menu className="w-5 h-5" />
          )}
        </button>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex space-x-6">
          {navItems.map((item) => (
            <Link 
              key={item.name}
              to={item.path}
              className="console-button"
            >
              {item.name}
            </Link>
          ))}
        </nav>
      </div>

      {/* Mobile Navigation */}
      {mobileMenuOpen && (
        <nav className="md:hidden mt-4 space-y-2">
          {navItems.map((item) => (
            <Link 
              key={item.name}
              to={item.path}
              className="console-button w-full text-left block"
              onClick={() => setMobileMenuOpen(false)}
            >
              {item.name}
            </Link>
          ))}
        </nav>
      )}
    </header>
  );
};

export default MainNav;
