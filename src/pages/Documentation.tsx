import { Suspense, useCallback } from "react";
import { Book, Command } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { SECTIONS } from "../components/Documentation/sections";
import { DocSection, DocSectionSkeleton, DocSectionError } from "../components/Documentation/DocSection";
import { DocSearch, SearchResults } from "../components/Documentation/DocSearch";
import { KeyboardShortcut } from "../components/Documentation/KeyboardShortcut";
import { ScrollToTop } from "../components/Documentation/ScrollToTop";
import { ScrollProgressProvider } from "../components/Documentation/ScrollProgress";
import { PlaygroundProvider } from "../components/Documentation/PlaygroundContext";
import { KeyboardShortcuts } from "../components/Documentation/KeyboardShortcuts";
import { useDocumentation } from "../hooks/useDocumentation";
import { useSynthLang } from "../components/Documentation/useSynthLang";
import Layout from "../components/Layout";

const Documentation = () => {
  const {
    activeSection,
    isLoading,
    error,
    searchResults,
    searchInputRef,
    modalRef,
    handleSectionChange,
    handleSearchResults,
    shortcuts
  } = useDocumentation({
    initialSection: "introduction",
    sections: SECTIONS
  });

  const { executeSynthLang } = useSynthLang();

  const handleRun = useCallback((code: string) => {
    const result = executeSynthLang(code);
    if (result.error) {
      throw new Error(result.error);
    }
    return Promise.resolve(result.output);
  }, [executeSynthLang]);

  return (
    <ScrollProgressProvider>
      <PlaygroundProvider initialCode="" onRun={handleRun}>
        <Layout title="Documentation">
          <main className="container mx-auto p-4">
            <div className="glass-panel p-6 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2">
                  <Book className="w-6 h-6 text-purple-400" />
                  <h1 className="text-2xl font-bold">SynthLang Documentation</h1>
                </div>
                <div className="hidden md:flex items-center gap-4">
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <Command className="w-3 h-3" />
                    <span>+</span>
                    <span>K</span>
                    <span className="ml-1">to search</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <span>J/K</span>
                    <span className="ml-1">to navigate</span>
                  </div>
                </div>
              </div>

              <DocSearch 
                sections={SECTIONS} 
                onSearchResults={handleSearchResults}
                ref={searchInputRef}
              />

              {error ? (
                <DocSectionError error={error} />
              ) : searchResults.length > 0 ? (
                <SearchResults results={searchResults} />
              ) : (
                <Tabs value={activeSection} onValueChange={handleSectionChange} className="w-full">
                  <TabsList className="grid w-full grid-cols-2 lg:grid-cols-4 gap-2 bg-transparent h-auto p-1 mb-6">
                    {Object.entries(SECTIONS).map(([key, section], index) => {
                      const Icon = section.icon;
                      return (
                        <TabsTrigger
                          key={key}
                          value={key}
                          className="data-[state=active]:bg-purple-500/20 h-10 px-4 transition-all 
                                   group relative"
                          disabled={isLoading}
                          data-section={key}
                        >
                          <Icon className="w-4 h-4 mr-2" />
                          <span className="hidden sm:inline">{section.title}</span>
                          <span className="sm:hidden">{section.title.slice(0, 3)}</span>
                          <span className="absolute top-1 right-1 text-[10px] text-muted-foreground/60 
                                         group-hover:text-muted-foreground">
                            {index + 1}
                          </span>
                        </TabsTrigger>
                      );
                    })}
                  </TabsList>

                  <div className="mt-4 space-y-6">
                    {Object.entries(SECTIONS).map(([key, section]) => (
                      <TabsContent key={key} value={key} className="space-y-6">
                        <Suspense fallback={<DocSectionSkeleton />}>
                          {isLoading ? (
                            <DocSectionSkeleton />
                          ) : (
                            <div className="grid gap-6">
                              {section.content.map((item, index) => (
                                <DocSection key={index} item={item} />
                              ))}
                            </div>
                          )}
                        </Suspense>
                      </TabsContent>
                    ))}
                  </div>
                </Tabs>
              )}
            </div>
          </main>

          <ScrollToTop />
          <div ref={modalRef}>
            <KeyboardShortcuts shortcuts={shortcuts} />
          </div>
        </Layout>
      </PlaygroundProvider>
    </ScrollProgressProvider>
  );
};

export default Documentation;
