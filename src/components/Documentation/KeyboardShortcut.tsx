import { Command } from "lucide-react";

interface KeyboardShortcutProps {
  shortcut: string;
  description?: string;
  className?: string;
}

export const KeyboardShortcut = ({ shortcut, description, className = "" }: KeyboardShortcutProps) => {
  const keys = shortcut.split('+').map(key => key.trim());
  
  return (
    <div className={`hidden sm:flex items-center gap-1.5 text-sm text-muted-foreground ${className}`}>
      {keys.map((key, index) => (
        <span key={key} className="flex items-center">
          {index > 0 && <span className="mx-0.5">+</span>}
          {key.toLowerCase() === 'cmd' ? (
            <Command className="w-3.5 h-3.5" />
          ) : (
            <kbd className="min-w-[1.5rem] px-1.5 h-6 flex items-center justify-center text-xs 
                         bg-black/20 rounded border border-border/40 font-mono">
              {key}
            </kbd>
          )}
        </span>
      ))}
      {description && (
        <span className="text-xs ml-2 text-muted-foreground/80">{description}</span>
      )}
    </div>
  );
};

export const ShortcutTooltip = ({ shortcut }: { shortcut: string }) => {
  const keys = shortcut.split('+').map(key => key.trim());
  
  return (
    <div className="flex items-center gap-1 text-xs">
      {keys.map((key, index) => (
        <span key={key} className="flex items-center">
          {index > 0 && <span className="mx-0.5">+</span>}
          {key.toLowerCase() === 'cmd' ? (
            <Command className="w-3 h-3" />
          ) : (
            <kbd className="min-w-[1.25rem] px-1 h-5 flex items-center justify-center 
                         bg-black/20 rounded border border-border/40 font-mono">
              {key}
            </kbd>
          )}
        </span>
      ))}
    </div>
  );
};
