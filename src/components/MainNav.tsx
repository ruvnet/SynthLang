import { Link } from "react-router-dom";
import { cn } from "../lib/utils";
import { Book, BarChart2, Play, Settings, Info } from "lucide-react";

interface MainNavProps {
  title?: string;
}

export default function MainNav({ title }: MainNavProps) {
  const links = [
    {
      href: "/",
      label: "Home",
      icon: null
    },
    {
      href: "/documentation",
      label: "Documentation",
      icon: <Book className="w-4 h-4" />
    },
    {
      href: "/playground",
      label: "Playground",  // Changed from "Test" to "Playground"
      icon: <Play className="w-4 h-4" />
    },
    {
      href: "/analytics",
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
    <div className="border-b border-border/40 bg-card/30 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 max-w-screen-2xl items-center">
        <div className="mr-4 hidden md:flex">
          <Link to="/" className="mr-6 flex items-center space-x-2">
            <span className="hidden font-bold sm:inline-block">
              {title || "SynthLang"}
            </span>
          </Link>
        </div>
        <nav className="flex items-center space-x-6 text-sm font-medium">
          {links.map((link) => (
            <Link
              key={link.href}
              to={link.href}
              className={cn(
                "transition-colors hover:text-foreground/80",
                "flex items-center gap-1"
              )}
            >
              {link.icon}
              <span>{link.label}</span>
            </Link>
          ))}
        </nav>
      </div>
    </div>
  );
}
