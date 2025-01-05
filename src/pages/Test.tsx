import Layout from "../components/Layout";

const Test = () => {
  return (
    <Layout title="Test">
      <main className="container mx-auto p-4">
        <div className="glass-panel p-6 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
          <h2 className="text-2xl font-bold mb-4">Prompt Testing</h2>
          <p className="text-muted-foreground mb-6">
            Test your translated prompts across multiple models using OpenRouter integration. Compare performance, costs, and effectiveness.
          </p>
          {/* Testing interface will be implemented here */}
        </div>
      </main>
    </Layout>
  );
};

export default Test;
