import { Link } from "react-router-dom";
import { cn } from "../lib/utils";
import { Book, BarChart2, Play, Settings, Info, Menu, X, Languages } from "lucide-react";
import { useState } from "react";
import { Button } from "./ui/button";

interface MainNavProps {
  title?: string;
}

const Logo = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-primary">
    <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

export default function MainNav({ title }: MainNavProps) {
  const [isOpen, setIsOpen] = useState(false);

  const links = [
    {
      href: "/documentation",
      label: "Documentation",
      icon: <Book className="w-4 h-4" />
    },
    {
      href: "/playground",
      label: "Playground",
      icon: <Play className="w-4 h-4" />
    },
    {
      href: "/translate",
      label: "Translate",
      icon: <Languages className="w-4 h-4" />
    },
    {
      href: "/advanced-calculator",
      label: "Analytics",
      icon: <BarChart2 className="w-4 h-4" />
    },
    {
      href: "/settings",
      label: "Settings",
      icon: <Settings className="w-4 h-4" />
    },
    {
      href: "/about",
      label: "About",
      icon: <Info className="w-4 h-4" />
    }
  ];

  return (
    <div className="fixed top-0 left-0 right-0 z-50 border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 max-w-screen-2xl items-center justify-center relative">
        {/* Logo and Navigation */}
        <div className="flex items-center gap-8">
          <Link to="/" className="flex items-center space-x-2">
            <Logo />
            <span className="font-bold text-lg bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">
              SynthLang
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center space-x-6">
            {links.map((link) => (
              <Link
                key={link.href}
                to={link.href}
                className={cn(
                  "transition-colors hover:text-foreground/80",
                  "flex items-center gap-2 px-3 py-2 rounded-md hover:bg-accent"
                )}
              >
                {link.icon}
                <span>{link.label}</span>
              </Link>
            ))}
          </nav>
        </div>

        {/* Mobile Menu Button */}
        <Button
          variant="ghost"
          size="icon"
          className="absolute right-4 lg:hidden"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </Button>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <div className="absolute top-full left-0 right-0 z-50 bg-background/95 backdrop-blur-sm border-b border-border/40 shadow-lg lg:hidden">
          <nav className="container py-4">
            <div className="flex flex-col space-y-4">
              {links.map((link) => (
                <Link
                  key={link.href}
                  to={link.href}
                  className={cn(
                    "transition-colors hover:text-foreground/80",
                    "flex items-center gap-2 px-4 py-2 rounded-md hover:bg-accent"
                  )}
                  onClick={() => setIsOpen(false)}
                >
                  {link.icon}
                  <span>{link.label}</span>
                </Link>
              ))}
            </div>
          </nav>
        </div>
      )}
    </div>
  );
}
