import Layout from "../components/Layout";
import { AdvancedCalculator } from "../components/AdvancedCalculator";

const AdvancedCalculatorPage = () => {
  return (
    <Layout title="Advanced SynthLang Calculator">
      <main className="container mx-auto p-4">
        <div className="glass-panel p-6 mb-8">
          <h1 className="text-2xl font-bold mb-4">Advanced SynthLang Calculator</h1>
          <p className="text-muted-foreground mb-6">
            Fine-tune your SynthLang implementation with advanced settings and optimizations. 
            Configure model parameters, features, and analyze performance metrics.
          </p>
          <AdvancedCalculator />
        </div>
      </main>
    </Layout>
  );
};

export default AdvancedCalculatorPage;
