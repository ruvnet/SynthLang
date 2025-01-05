import { Link } from "react-router-dom";
import { ArrowRight, Settings } from "lucide-react";
import Layout from "../components/Layout";

const Analytics = () => {
  return (
    <Layout title="Analytics">
      <main className="container mx-auto p-4 space-y-6">
        <div className="glass-panel p-6 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
          <h2 className="text-2xl font-bold mb-4">Performance Analytics</h2>
          <p className="text-muted-foreground mb-6">
            Track and analyze prompt performance metrics, token usage, cost savings, and optimization effectiveness across different models.
          </p>
          {/* Analytics dashboard will be implemented here */}
        </div>

        <div className="glass-panel p-6 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
          <div className="flex items-center gap-3 mb-4">
            <Settings className="w-6 h-6 text-orange-400" />
            <h2 className="text-xl font-semibold">Advanced Optimization Tools</h2>
          </div>
          <p className="text-muted-foreground mb-4">
            Need more detailed analysis? Try our Advanced Calculator for in-depth optimization settings and performance metrics.
          </p>
          <Link 
            to="/advanced-calculator" 
            className="console-button inline-flex items-center gap-2"
          >
            Open Advanced Calculator
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </main>
    </Layout>
  );
};

export default Analytics;
