import { Command, Keyboard, X } from "lucide-react";
import { useState } from "react";
import { formatKeyCombo } from "../../hooks/useKeyboardShortcuts";

interface ShortcutProps {
  keys: string[];
  description: string;
}

const Shortcut = ({ keys, description }: ShortcutProps) => (
  <div className="flex items-center justify-between text-sm py-1">
    <div className="flex items-center gap-1">
      {keys.map((key, index) => (
        <span key={key} className="flex items-center">
          {index > 0 && <span className="text-muted-foreground/60 mx-1">+</span>}
          {key.toLowerCase() === 'cmd' ? (
            <Command className="w-3.5 h-3.5 text-muted-foreground" />
          ) : (
            <kbd className="min-w-[1.5rem] px-1.5 h-6 flex items-center justify-center 
                         text-xs bg-black/20 rounded border border-border/40 
                         text-muted-foreground font-mono">
              {key}
            </kbd>
          )}
        </span>
      ))}
    </div>
    <span className="text-muted-foreground text-xs">{description}</span>
  </div>
);

export interface KeyboardShortcutsProps {
  shortcuts?: Record<string, Array<{ keys: string[]; description: string }>>;
}

export const KeyboardShortcuts = ({ shortcuts = {} }: KeyboardShortcutsProps) => {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <>
      <button
        onClick={() => setIsVisible(true)}
        className="fixed bottom-8 right-8 p-2 rounded-lg border border-border/40 
                  bg-card/30 backdrop-blur-sm z-50 hover:bg-card/40 transition-colors"
        title="Show keyboard shortcuts"
      >
        <Keyboard className="w-5 h-5 text-muted-foreground" />
      </button>

      {isVisible && (
        <>
          <div 
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
            onClick={() => setIsVisible(false)}
          />
          <div className="fixed bottom-8 right-8 p-4 rounded-lg border border-border/40 
                        bg-card/95 backdrop-blur-sm z-50 w-80 shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <h4 className="text-sm font-medium flex items-center gap-2">
                <Keyboard className="w-4 h-4" />
                Keyboard Shortcuts
              </h4>
              <button
                onClick={() => setIsVisible(false)}
                className="p-1 hover:bg-white/5 rounded-full transition-colors"
              >
                <X className="w-4 h-4 text-muted-foreground" />
              </button>
            </div>

            <div className="space-y-4">
              {Object.entries(shortcuts).map(([group, groupShortcuts]) => (
                <div key={group} className="space-y-1">
                  <h5 className="text-xs font-medium text-muted-foreground mb-2">
                    {group}
                  </h5>
                  {groupShortcuts.map((shortcut, index) => (
                    <Shortcut
                      key={index}
                      keys={shortcut.keys}
                      description={shortcut.description}
                    />
                  ))}
                </div>
              ))}
            </div>

            <div className="mt-4 pt-3 border-t border-border/40">
              <button
                onClick={() => setIsVisible(false)}
                className="w-full py-1.5 text-xs text-center text-muted-foreground 
                         hover:text-foreground transition-colors"
              >
                Click anywhere to close
              </button>
            </div>
          </div>
        </>
      )}
    </>
  );
};
