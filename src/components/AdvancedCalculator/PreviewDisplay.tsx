import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { SynthLangConfig } from './types';

interface PreviewDisplayProps {
  config: SynthLangConfig;
  getPreviewContent: () => string;
}

export const PreviewDisplay: React.FC<PreviewDisplayProps> = ({ config, getPreviewContent }) => {
  const getHighlightedContent = (content: string) => {
    // Split content into lines for syntax highlighting
    return content.split('\n').map((line, i) => {
      let className = 'text-muted-foreground';

      // Highlight different parts based on content
      if (line.startsWith('↹')) {
        className = 'text-blue-500';
      } else if (line.startsWith('⊕')) {
        className = 'text-green-500';
      } else if (line.startsWith('#')) {
        className = 'text-purple-500 font-semibold';
      } else if (line.includes('[') && line.includes(']')) {
        className = 'text-yellow-500';
      }

      return (
        <div key={i} className={className}>
          {line}
        </div>
      );
    });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Configuration Preview</CardTitle>
        <CardDescription>
          Live preview of your SynthLang configuration
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="bg-accent/10 p-4 rounded-lg">
          <pre className="font-mono text-sm whitespace-pre">
            {getHighlightedContent(getPreviewContent())}
          </pre>
        </div>
        <div className="mt-4 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <span className="text-blue-500">↹</span>
            <span>Model and context settings</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-green-500">⊕</span>
            <span>Framework and feature configurations</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-purple-500">#</span>
            <span>Section headers</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-yellow-500">[ ]</span>
            <span>Configuration parameters</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
