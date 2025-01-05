import { useRef, useState, useEffect } from "react";
import { Search, Terminal } from "lucide-react";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "../ui/command";
import { ModelSelectorProps } from "./types";

export const ModelSelector = ({ selectedModel, onModelSelect, availableModels }: ModelSelectorProps) => {
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const searchRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setIsSearchOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div className="relative flex-1" ref={searchRef}>
      <button
        className="console-input w-full text-left flex items-center justify-between focus:ring-2 focus:ring-purple-500 focus:outline-none"
        onClick={() => setIsSearchOpen(true)}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            setIsSearchOpen(true);
          }
          if (e.key === 'Escape') {
            setIsSearchOpen(false);
          }
        }}
        aria-haspopup="listbox"
        aria-expanded={isSearchOpen}
        aria-label="Select model"
      >
        <div className="flex items-center gap-2">
          <Terminal className="w-3 h-3 opacity-50" />
          <span>{selectedModel}</span>
          <span className="text-xs text-muted-foreground">
            ({availableModels[selectedModel].litellm_provider})
          </span>
        </div>
        <Search className="h-4 w-4 opacity-50" />
      </button>
      {isSearchOpen && (
        <div className="absolute w-full z-50">
          <Command 
            className="rounded-lg border shadow-md bg-background"
            role="listbox"
            aria-label="Available models"
            onKeyDown={(e) => {
              if (e.key === 'Escape') {
                setIsSearchOpen(false);
                searchRef.current?.querySelector('button')?.focus();
              }
            }}
          >
            <CommandInput 
              placeholder="Search models..." 
              autoFocus
            />
            <CommandList>
              <CommandEmpty>No models found.</CommandEmpty>
              <CommandGroup>
                {Object.entries(availableModels).map(([name, model]) => (
                  <CommandItem
                    key={name}
                    value={name}
                    onSelect={(value) => {
                      onModelSelect(value);
                      setIsSearchOpen(false);
                      searchRef.current?.querySelector('button')?.focus();
                    }}
                  >
                    <div className="flex items-center gap-2">
                      <Terminal className="w-3 h-3 opacity-50" />
                      <div>
                        <span>{name}</span>
                        <span className="ml-2 text-xs text-muted-foreground">
                          ({model.litellm_provider})
                        </span>
                      </div>
                    </div>
                  </CommandItem>
                ))}
              </CommandGroup>
            </CommandList>
          </Command>
        </div>
      )}
    </div>
  );
};

export default ModelSelector;
