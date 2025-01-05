import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import MainNav from "../components/MainNav";
import { BookTemplate, Trash2 } from "lucide-react";
import { SavedPrompt, getSavedPrompts, deletePrompt, SAVED_PROMPTS_KEY } from "../services/storageService";

interface Template {
  title: string;
  content: string;
  filename: string;
}

type GlobModule = {
  [key: string]: () => Promise<string>
}

export default function Templates() {
  const [builtInTemplates, setBuiltInTemplates] = useState<Template[]>([]);
  const [savedTemplates, setSavedTemplates] = useState<SavedPrompt[]>([]);

  const loadSavedTemplates = () => {
    setSavedTemplates(getSavedPrompts());
  };

  useEffect(() => {
    const importTemplates = async () => {
      const templateModules = import.meta.glob<string>('../templates/*.md', { 
        query: '?raw',
        import: 'default'
      }) as GlobModule;
      
      const loadedTemplates: Template[] = [];

      for (const path in templateModules) {
        const content = await templateModules[path]();
        const filename = path.split('/').pop()?.replace('.md', '') || '';
        const title = filename
          .split('-')
          .map(word => word.charAt(0).toUpperCase() + word.slice(1))
          .join(' ');

        loadedTemplates.push({
          title,
          content,
          filename
        });
      }

      setBuiltInTemplates(loadedTemplates);
      loadSavedTemplates();
    };

    importTemplates();
  }, []);

  // Listen for both storage event and custom event
  useEffect(() => {
    const handleStorageChange = () => {
      loadSavedTemplates();
    };

    window.addEventListener('storage', handleStorageChange);
    window.addEventListener('storageChanged', handleStorageChange);
    
    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('storageChanged', handleStorageChange);
    };
  }, []);

  return (
    <div className="min-h-screen flex flex-col">
      <MainNav title="Template Library" />
      
      <main className="flex-1 p-4">
        <section className="glass-panel p-6 animate-matrix-fade">
          <div className="flex items-center gap-2 mb-6">
            <BookTemplate className="w-6 h-6 text-console-cyan" />
            <h1 className="text-2xl font-code text-console-cyan">Available Templates</h1>
          </div>
          
          {/* Built-in Templates */}
          <div className="mb-8">
            <h2 className="text-xl font-code text-console-cyan mb-4">Built-in Templates</h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
              {builtInTemplates.map((template) => (
                <Card key={template.filename} className="glass-panel border-console-cyan hover:shadow-lg transition-shadow bg-gray-900/50">
                  <CardHeader>
                    <CardTitle className="text-console-cyan">{template.title}</CardTitle>
                    <CardDescription className="text-console-green">
                      Mathematical Framework Template
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ScrollArea className="h-[200px] w-full rounded-md border border-console-cyan/20 p-4 bg-gray-900/50">
                      <pre className="text-sm font-code text-console-text">{template.content}</pre>
                    </ScrollArea>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* Saved Templates */}
          {savedTemplates.length > 0 && (
            <div>
              <h2 className="text-xl font-code text-console-cyan mb-4">Saved Templates</h2>
              <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                {savedTemplates.map((template) => (
                  <Card key={template.id} className="glass-panel border-console-cyan hover:shadow-lg transition-shadow bg-gray-900/50">
                    <CardHeader>
                      <div className="flex justify-between items-start">
                        <div>
                          <CardTitle className="text-console-cyan">{template.title}</CardTitle>
                          <CardDescription className="text-console-green">
                            Saved Template - {new Date(template.timestamp).toLocaleDateString()}
                          </CardDescription>
                        </div>
                        <button
                          onClick={(e) => {
                            e.preventDefault();
                            if (window.confirm('Are you sure you want to delete this template?')) {
                              deletePrompt(template.id);
                            }
                          }}
                          className="console-button p-2 hover:bg-red-900/20"
                          title="Delete template"
                        >
                          <Trash2 className="w-4 h-4 text-red-400" />
                        </button>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <ScrollArea className="h-[200px] w-full rounded-md border border-console-cyan/20 p-4 bg-gray-900/50">
                        <pre className="text-sm font-code text-console-text">
                          {template.prompt.overview}
                          {'\n\n'}
                          {template.prompt.content}
                        </pre>
                      </ScrollArea>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
