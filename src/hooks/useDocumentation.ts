import { useState, useRef, useCallback } from 'react';
import { useKeyboardShortcuts } from './useKeyboardShortcuts';
import { DocItem } from '../components/Documentation/types';

interface UseDocumentationProps {
  initialSection: string;
  sections: Record<string, any>;
}

export const useDocumentation = ({ initialSection, sections }: UseDocumentationProps) => {
  const [activeSection, setActiveSection] = useState(initialSection);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchResults, setSearchResults] = useState<Array<{ section: string; items: DocItem[] }>>([]);
  const searchInputRef = useRef<HTMLInputElement>(null);
  const modalRef = useRef<HTMLDivElement>(null);

  const handleSectionChange = useCallback((value: string) => {
    setIsLoading(true);
    setError(null);
    setActiveSection(value);
    // Simulate loading for smoother transitions
    setTimeout(() => setIsLoading(false), 300);
  }, []);

  const handleSearchResults = useCallback((results: Array<{ section: string; items: DocItem[] }>) => {
    setSearchResults(results);
  }, []);

  const clearSearch = useCallback(() => {
    handleSearchResults([]);
  }, [handleSearchResults]);

  const focusSearch = useCallback(() => {
    searchInputRef.current?.focus();
  }, []);

  // Define keyboard shortcuts
  const { getAllShortcuts } = useKeyboardShortcuts([
    // Navigation shortcuts
    {
      key: 'j',
      handler: () => {
        const sectionKeys = Object.keys(sections);
        const currentIndex = sectionKeys.indexOf(activeSection);
        if (currentIndex > 0) {
          handleSectionChange(sectionKeys[currentIndex - 1]);
        }
      },
      description: 'Previous section',
      group: 'Navigation'
    },
    {
      key: 'k',
      handler: () => {
        const sectionKeys = Object.keys(sections);
        const currentIndex = sectionKeys.indexOf(activeSection);
        if (currentIndex < sectionKeys.length - 1) {
          handleSectionChange(sectionKeys[currentIndex + 1]);
        }
      },
      description: 'Next section',
      group: 'Navigation'
    },
    // Section number shortcuts
    ...Array.from({ length: 9 }, (_, i) => ({
      key: (i + 1).toString(),
      handler: () => {
        const sectionKeys = Object.keys(sections);
        if (i < sectionKeys.length) {
          handleSectionChange(sectionKeys[i]);
        }
      },
      description: `Jump to section ${i + 1}`,
      group: 'Navigation'
    })),
    // Search shortcuts
    {
      key: 'k',
      meta: true,
      handler: focusSearch,
      description: 'Focus search',
      group: 'Search'
    },
    {
      key: 'Escape',
      handler: () => {
        if (searchResults.length > 0) {
          clearSearch();
        }
      },
      description: 'Clear search',
      group: 'Search'
    }
  ], {
    ignoreInputs: true,
    ignoreWhenModalOpen: true,
    modalRef
  });

  // Scroll to section
  const scrollToSection = useCallback((sectionKey: string) => {
    const section = document.querySelector(`[data-section="${sectionKey}"]`);
    if (section) {
      section.scrollIntoView({ behavior: 'smooth' });
    }
  }, []);

  // Handle errors
  const setErrorWithTimeout = useCallback((errorMessage: string) => {
    setError(errorMessage);
    setTimeout(() => setError(null), 5000);
  }, []);

  return {
    // State
    activeSection,
    isLoading,
    error,
    searchResults,
    searchInputRef,
    modalRef,

    // Actions
    handleSectionChange,
    handleSearchResults,
    clearSearch,
    focusSearch,
    scrollToSection,
    setError: setErrorWithTimeout,

    // Keyboard shortcuts
    shortcuts: getAllShortcuts()
  };
};

// Helper types for better type inference
export type DocumentationState = ReturnType<typeof useDocumentation>;

export interface DocumentationContextValue extends DocumentationState {
  sections: Record<string, any>;
}
