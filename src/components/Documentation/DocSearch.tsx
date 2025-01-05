import { Search, X } from "lucide-react";
import { useState, useCallback, useEffect, forwardRef } from "react";
import { DocSection, DocItem } from "./types";

interface DocSearchProps {
  sections: Record<string, DocSection>;
  onSearchResults: (results: Array<{ section: string; items: DocItem[] }>) => void;
}

export const DocSearch = forwardRef<HTMLInputElement, DocSearchProps>(
  ({ sections, onSearchResults }, ref) => {
    const [query, setQuery] = useState("");
    const [debouncedQuery, setDebouncedQuery] = useState("");

    // Debounce search query
    useEffect(() => {
      const timer = setTimeout(() => {
        setDebouncedQuery(query);
      }, 300);

      return () => clearTimeout(timer);
    }, [query]);

    // Search implementation
    const searchDocs = useCallback((searchQuery: string) => {
      if (!searchQuery.trim()) {
        onSearchResults([]);
        return;
      }

      const results = Object.entries(sections).map(([sectionKey, section]) => {
        const matchedItems = section.content.filter(item => {
          const searchText = [
            item.title,
            item.text,
            ...(item.items || []),
            item.example,
            item.code
          ].filter(Boolean).join(" ").toLowerCase();

          return searchText.includes(searchQuery.toLowerCase());
        });

        return {
          section: sectionKey,
          items: matchedItems
        };
      }).filter(result => result.items.length > 0);

      onSearchResults(results);
    }, [sections, onSearchResults]);

    // Effect for search
    useEffect(() => {
      searchDocs(debouncedQuery);
    }, [debouncedQuery, searchDocs]);

    const handleClear = () => {
      setQuery("");
      onSearchResults([]);
      if (ref && 'current' in ref && ref.current) {
        ref.current.focus();
      }
    };

    return (
      <div className="relative w-full max-w-2xl mx-auto mb-8">
        <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none">
          <Search className="h-4 w-4 text-muted-foreground" />
        </div>
        <input
          ref={ref}
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search documentation... (⌘ + K)"
          className="w-full pl-10 pr-12 py-2 bg-black/20 border border-border/40 rounded-lg 
                   focus:outline-none focus:ring-2 focus:ring-purple-500/50 
                   text-sm transition-all"
          aria-label="Search documentation"
        />
        {query && (
          <button
            onClick={handleClear}
            className="absolute inset-y-0 right-3 flex items-center text-muted-foreground 
                     hover:text-foreground transition-colors"
            aria-label="Clear search"
          >
            <X className="h-4 w-4" />
          </button>
        )}
      </div>
    );
  }
);

DocSearch.displayName = "DocSearch";

export const SearchResults = ({ 
  results 
}: { 
  results: Array<{ section: string; items: DocItem[] }> 
}) => {
  if (results.length === 0) return null;

  return (
    <div className="space-y-6 mb-8">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Search Results</h2>
        <span className="text-sm text-muted-foreground">
          {results.reduce((acc, curr) => acc + curr.items.length, 0)} results found
        </span>
      </div>
      {results.map((result, index) => (
        <div key={index} className="space-y-4">
          <h3 className="text-md font-medium text-purple-400">
            {result.section.charAt(0).toUpperCase() + result.section.slice(1)}
          </h3>
          <div className="grid gap-4">
            {result.items.map((item, itemIndex) => (
              <div 
                key={itemIndex}
                className="glass-panel p-4 rounded-lg border border-border/40 bg-card/30 backdrop-blur"
              >
                <h4 className="font-medium mb-2">{item.title}</h4>
                {item.text && (
                  <p className="text-sm text-muted-foreground mb-2">{item.text}</p>
                )}
                {item.example && (
                  <pre className="bg-black/20 p-2 rounded text-xs overflow-x-auto">
                    <code className="text-purple-200">{item.example}</code>
                  </pre>
                )}
                {item.code && (
                  <pre className="bg-black/20 p-2 rounded text-xs overflow-x-auto">
                    <code className="text-green-200">{item.code}</code>
                  </pre>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};
