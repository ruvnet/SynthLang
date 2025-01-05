import { useState, useRef } from "react";
import { X, Copy, Download, Save } from "lucide-react";
import { savePrompt } from "../services/storageService";

interface GenerateDialogProps {
  isOpen: boolean;
  onClose: () => void;
  prompt: {
    domain: string;
    category: string;
    outputType: string;
    outputDescription: string;
    overview: string;
    content: string;
  };
}

type FormatTab = 'markdown' | 'json' | 'toml';

const GenerateDialog = ({ isOpen, onClose, prompt }: GenerateDialogProps) => {
  const [activeFormat, setActiveFormat] = useState<FormatTab>('markdown');
  const [title, setTitle] = useState('');
  const contentRef = useRef<HTMLPreElement>(null);

  if (!isOpen) return null;

  const formatContent = () => {
    switch (activeFormat) {
      case 'markdown':
        return `# ${prompt.domain} Prompt
## Category: ${prompt.category}
## Output: ${prompt.outputType}
${prompt.outputDescription}

### Overview
${prompt.overview}

### Content
${prompt.content}`;

      case 'json':
        return JSON.stringify({
          domain: prompt.domain,
          category: prompt.category,
          output: {
            type: prompt.outputType,
            description: prompt.outputDescription
          },
          overview: prompt.overview,
          content: prompt.content
        }, null, 2);

      case 'toml':
        return `domain = "${prompt.domain}"
category = "${prompt.category}"

[output]
type = "${prompt.outputType}"
description = "${prompt.outputDescription}"

overview = """
${prompt.overview}
"""

content = """
${prompt.content}
"""`;
    }
  };

  const handleCopy = async () => {
    const content = formatContent();
    await navigator.clipboard.writeText(content);
  };

  const handleExport = () => {
    const content = formatContent();
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `prompt-${prompt.domain.toLowerCase().replace(/\s+/g, '-')}.${activeFormat}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="glass-panel w-full max-w-3xl max-h-[80vh] overflow-hidden flex flex-col m-4">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <div className="flex-1">
            <h2 className="text-xl text-console-cyan font-code mb-2">Generated Prompt</h2>
            <input
              type="text"
              placeholder="Enter template title..."
              className="console-input w-full"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </div>
          <button 
            onClick={onClose}
            className="console-button p-1 ml-4"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Format Tabs */}
        <div className="flex border-b border-gray-700">
          {(['markdown', 'json', 'toml'] as const).map((format) => (
            <button
              key={format}
              className={`px-4 py-2 font-code ${
                activeFormat === format 
                  ? 'text-console-cyan border-b-2 border-console-cyan' 
                  : 'text-gray-400 hover:text-gray-300'
              }`}
              onClick={() => setActiveFormat(format)}
            >
              {format.toUpperCase()}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4">
          <pre ref={contentRef} className="console-input w-full min-h-[400px] p-3 font-mono text-sm whitespace-pre-wrap">
            {formatContent()}
          </pre>
        </div>

        {/* Footer */}
        <div className="border-t border-gray-700 p-4 flex justify-end gap-3">
          <button 
            className="console-button flex items-center gap-2"
            onClick={handleCopy}
          >
            <Copy className="w-4 h-4" />
            Copy
          </button>
          <button 
            className="console-button flex items-center gap-2"
            onClick={handleExport}
          >
            <Download className="w-4 h-4" />
            Export
          </button>
          <button 
            className="console-button flex items-center gap-2"
            onClick={() => {
              if (!title.trim()) {
                alert('Please enter a title for the template');
                return;
              }
              savePrompt({
                title: title.trim(),
                format: activeFormat,
                prompt
              });
              onClose();
            }}
          >
            <Save className="w-4 h-4" />
            Save
          </button>
        </div>
      </div>
    </div>
  );
};

export default GenerateDialog;
