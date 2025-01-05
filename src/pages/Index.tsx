import { Link } from "react-router-dom";
import { ArrowRight, Sparkles, Gauge, Calculator as CalcIcon, Settings } from "lucide-react";
import Calculator from "../components/TokenCalculator/Calculator";
import Layout from "../components/Layout";

const FEATURES = [
  {
    title: "Advanced Calculator",
    description: "Fine-tune your SynthLang implementation with advanced settings and metrics",
    icon: Settings,
    link: "/advanced-calculator",
    color: "text-orange-400"
  },
  {
    title: "Prompt Translation",
    description: "Convert standard prompts into optimized SynthLang format",
    icon: Sparkles,
    link: "/translate",
    color: "text-purple-400"
  },
  {
    title: "Multi-Model Testing",
    description: "Test prompts across different models via OpenRouter",
    icon: Gauge,
    link: "/test",
    color: "text-blue-400"
  }
] as const;

const Index = () => {
  return (
    <Layout title="SynthLang">
      <main className="container mx-auto p-4">
        {/* Hero Section */}
        <div className="glass-panel p-8 mb-8">
          <h1 className="text-4xl font-bold mb-4">
            Optimize Your AI Prompts
          </h1>
          <p className="text-xl text-muted-foreground mb-6">
            Reduce AI costs by up to 70% with SynthLang's efficient prompt optimization.
            Experience up to 233% faster processing while maintaining effectiveness.
          </p>
          <Link 
            to="/translate" 
            className="console-button inline-flex items-center gap-2"
          >
            Get Started
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        {/* Quick Savings Calculator */}
        <div className="glass-panel p-6 mb-8">
          <div className="flex items-center gap-2 mb-4">
            <CalcIcon className="w-6 h-6 text-purple-400" />
            <h2 className="text-xl font-semibold">Quick Savings Calculator</h2>
          </div>
          <Calculator />
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-6">
          {FEATURES.map((feature) => {
            const Icon = feature.icon;
            return (
              <Link 
                key={feature.title}
                to={feature.link}
                className="glass-panel p-6 hover:bg-accent/50 transition-colors"
              >
                <Icon className={`w-8 h-8 ${feature.color} mb-4`} />
                <h2 className="text-xl font-semibold mb-2">{feature.title}</h2>
                <p className="text-muted-foreground">{feature.description}</p>
              </Link>
            );
          })}
        </div>

        {/* Benefits Section */}
        <div className="glass-panel p-8 mt-8">
          <h2 className="text-2xl font-bold mb-6">Why SynthLang?</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-xl font-semibold mb-2">Token Optimization</h3>
              <ul className="list-disc list-inside text-muted-foreground space-y-2">
                <li>Reduce token usage by up to 70%</li>
                <li>Maintain semantic meaning</li>
                <li>Optimize context handling</li>
                <li>Improve response quality</li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-2">Cost Efficiency</h3>
              <ul className="list-disc list-inside text-muted-foreground space-y-2">
                <li>Cut API costs by up to 70%</li>
                <li>Faster response times</li>
                <li>Reduced API calls</li>
                <li>Better resource utilization</li>
              </ul>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
};

export default Index;
