import { Calculator, FileText } from "lucide-react";
import { TokenInputProps } from "./types";
import { 
  DEFAULT_TOKEN_COUNT, 
  DEFAULT_WORDS_PER_TOKEN, 
  DEFAULT_WORDS_PER_PAGE,
  calculateTokensFromWords,
  calculateTokensFromPages
} from "./constants";

export const TokenInput = ({
  tokenCount,
  onTokenCountChange,
  onWordsChange,
  onPagesChange
}: TokenInputProps) => {
  // Calculate words and pages from tokens
  const wordCount = Math.round(tokenCount * DEFAULT_WORDS_PER_TOKEN);
  const pageCount = (wordCount / DEFAULT_WORDS_PER_PAGE).toFixed(1);

  const handleTokenChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const tokens = Math.max(0, parseInt(e.target.value) || DEFAULT_TOKEN_COUNT);
    onTokenCountChange(tokens);
  };

  const handleWordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const words = Math.max(0, parseInt(e.target.value) || 0);
    const tokens = calculateTokensFromWords(words);
    onWordsChange(words);
  };

  const handlePageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const pages = Math.max(0, parseFloat(e.target.value) || 0);
    const tokens = calculateTokensFromPages(pages);
    onPagesChange(pages);
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div className="space-y-2">
        <label className="text-sm text-muted-foreground flex items-center gap-2">
          <Calculator className="w-3 h-3" />
          Tokens
        </label>
        <input
          type="number"
          min="0"
          step="1000"
          className="console-input w-full font-mono"
          placeholder="Enter number of tokens..."
          value={tokenCount}
          onChange={handleTokenChange}
          onWheel={(e) => e.currentTarget.blur()}
        />
      </div>
      <div className="space-y-2">
        <label className="text-sm text-muted-foreground flex items-center gap-2">
          <FileText className="w-3 h-3" />
          Words
        </label>
        <input
          type="number"
          min="0"
          step="1"
          className="console-input w-full font-mono"
          placeholder="Enter number of words..."
          value={wordCount}
          onChange={handleWordChange}
          onWheel={(e) => e.currentTarget.blur()}
        />
        <div className="text-xs text-muted-foreground">
          ~{DEFAULT_WORDS_PER_TOKEN} words per token
        </div>
      </div>
      <div className="space-y-2">
        <label className="text-sm text-muted-foreground flex items-center gap-2">
          <FileText className="w-3 h-3" />
          Pages
        </label>
        <input
          type="number"
          min="0"
          step="0.5"
          className="console-input w-full font-mono"
          placeholder="Enter number of pages..."
          value={pageCount}
          onChange={handlePageChange}
          onWheel={(e) => e.currentTarget.blur()}
        />
        <div className="text-xs text-muted-foreground">
          ~{DEFAULT_WORDS_PER_PAGE} words per page
        </div>
      </div>
    </div>
  );
};

export default TokenInput;
