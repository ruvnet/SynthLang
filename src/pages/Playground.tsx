import { Playground as PlaygroundComponent } from "../components/Documentation/Playground";
import { PlaygroundProvider } from "../components/Documentation/PlaygroundContext";
import Layout from "../components/Layout";

const defaultCode = `# Try SynthLang here
↹ text "Write a short story about a robot learning to paint" ^creative ^detailed
⊕ analyze "themes and emotions" ^comprehensive ^deep
⊕ format "narrative structure" ^engaging ^clear
Σ {
  story: ^creative,
  themes: ^detailed,
  emotions: ^analyzed
}`;

const Playground = () => {
  return (
    <PlaygroundProvider initialCode={defaultCode}>
      <Layout title="Playground">
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
      </Layout>
    </PlaygroundProvider>
  );
};

export default Playground;
