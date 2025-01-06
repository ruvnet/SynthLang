import React from "react";
import { Github } from "lucide-react";

export const Footer = () => {
  return (
    <footer className="border-t border-border/40 mt-8">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col items-center space-y-4">
          <div className="text-center">
            <h3 className="text-lg font-semibold">SynthLang Documentation - Version 1.0.0</h3>
            <p className="text-sm text-muted-foreground">
              A hyper-efficient prompt language for optimizing AI interactions
            </p>
          </div>
          
          <div className="flex items-center space-x-2">
            <a
              href="https://github.com/ruvnet/SynthLang"
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-muted-foreground hover:text-primary flex items-center gap-1"
            >
              <Github className="w-4 h-4" />
              GitHub
            </a>
            <span className="text-muted-foreground">•</span>
            <a
              href="https://github.com/ruvnet/SynthLang/blob/main/CONTRIBUTING.md"
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-muted-foreground hover:text-primary"
            >
              Contributing
            </a>
            <span className="text-muted-foreground">•</span>
            <a
              href="https://github.com/ruvnet/SynthLang/blob/main/LICENSE.md"
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-muted-foreground hover:text-primary"
            >
              License
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};
