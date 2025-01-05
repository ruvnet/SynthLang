import { DocItem } from "./types";
import { useSynthLang } from "./useSynthLang";
import { useEffect, useState } from "react";

interface DocSectionProps {
  item: DocItem;
}

export const DocSection = ({ item }: DocSectionProps) => {
  const { highlightSyntax } = useSynthLang();
  const [highlightedExample, setHighlightedExample] = useState("");
  const [highlightedCode, setHighlightedCode] = useState("");

  useEffect(() => {
    if (item.example) {
      setHighlightedExample(highlightSyntax(item.example));
    }
    if (item.code) {
      setHighlightedCode(highlightSyntax(item.code));
    }
  }, [item.example, item.code, highlightSyntax]);

  return (
    <div className="glass-panel p-6 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
      <h3 className="text-lg font-semibold mb-3">{item.title}</h3>
      
      {item.text && (
        <p className="text-muted-foreground mb-4 leading-relaxed whitespace-pre-wrap">
          {item.text}
        </p>
      )}
      
      {item.items && (
        <ul className="list-disc list-inside space-y-2 text-muted-foreground mb-4">
          {item.items.map((listItem, i) => (
            <li key={i} className="leading-relaxed">
              <span className="ml-2">{listItem}</span>
            </li>
          ))}
        </ul>
      )}
      
      {item.example && (
        <div className="mt-4 rounded-lg border border-border/40 bg-black/20 overflow-hidden">
          <div className="px-4 py-2 border-b border-border/40 bg-black/20">
            <span className="text-xs font-medium text-muted-foreground">Example</span>
          </div>
          <pre className="p-4 overflow-x-auto font-mono text-sm">
            <code 
              dangerouslySetInnerHTML={{ __html: highlightedExample }}
              className="text-purple-200"
            />
          </pre>
        </div>
      )}
      
      {item.code && (
        <div className="mt-4 rounded-lg border border-border/40 bg-black/20 overflow-hidden">
          <div className="px-4 py-2 border-b border-border/40 bg-black/20">
            <span className="text-xs font-medium text-muted-foreground">Code</span>
          </div>
          <pre className="p-4 overflow-x-auto font-mono text-sm">
            <code 
              dangerouslySetInnerHTML={{ __html: highlightedCode }}
              className="text-green-200"
            />
          </pre>
        </div>
      )}

      {item.component && (
        <div className={`${item.text || item.items ? 'mt-6' : 'mt-0'}`}>
          {item.component()}
        </div>
      )}
    </div>
  );
};

// Loading state component
export const DocSectionSkeleton = () => (
  <div className="glass-panel p-6 rounded-lg border border-border/40 bg-card/30 backdrop-blur animate-pulse">
    <div className="h-6 w-1/3 bg-purple-500/20 rounded mb-4" />
    <div className="space-y-3">
      <div className="h-4 w-full bg-purple-500/10 rounded" />
      <div className="h-4 w-5/6 bg-purple-500/10 rounded" />
      <div className="h-4 w-4/6 bg-purple-500/10 rounded" />
    </div>
    <div className="mt-6 h-24 w-full bg-black/20 rounded" />
  </div>
);

// Error state component
export const DocSectionError = ({ error }: { error: string }) => (
  <div className="glass-panel p-6 rounded-lg border border-red-500/40 bg-card/30 backdrop-blur">
    <h3 className="text-lg font-semibold mb-3 text-red-400">Error Loading Section</h3>
    <p className="text-red-400/80">{error}</p>
  </div>
);
