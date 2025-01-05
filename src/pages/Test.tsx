import MainNav from "../components/MainNav";

const Test = () => {
  return (
    <div className="min-h-screen bg-background">
      <MainNav title="SynthLang Tester" />
      <main className="container mx-auto p-4">
        <div className="glass-panel p-6">
          <h2 className="text-2xl font-bold mb-4">Prompt Testing</h2>
          <p className="text-muted-foreground mb-6">
            Test your translated prompts across multiple models using OpenRouter integration. Compare performance, costs, and effectiveness.
          </p>
          {/* Testing interface will be implemented here */}
        </div>
      </main>
    </div>
  );
};

export default Test;
