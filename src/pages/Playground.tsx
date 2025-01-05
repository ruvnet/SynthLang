import { Playground as PlaygroundComponent } from "../components/Documentation/Playground";
import { PlaygroundProvider } from "../components/Documentation/PlaygroundContext";
import MainNav from "../components/MainNav";

const defaultCode = `# Try SynthLang here
↹ text "Write a short story about a robot learning to paint" ^creative
⊕ analyze_sentiment ^thorough
⊕ extract_themes ^comprehensive
Σ {
  story: ^polished,
  sentiment: ^brief,
  themes: ^bullet_points
}`;

const Playground = () => {
  return (
    <div className="min-h-screen bg-background">
      <MainNav title="Playground" />
      <PlaygroundProvider initialCode={defaultCode}>
        <main className="container mx-auto p-4">
          <div className="glass-panel p-6 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
            <h1 className="text-2xl font-bold mb-6">SynthLang Playground</h1>
            <p className="text-muted-foreground mb-6">
              Experiment with SynthLang commands and see the results in real-time. 
              Try the example below or write your own commands.
            </p>
            <PlaygroundComponent />
          </div>
        </main>
      </PlaygroundProvider>
    </div>
  );
};

export default Playground;
