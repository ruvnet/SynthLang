import React from 'react';
import Layout from '../components/Layout';
import { AdvancedCalculator as Calculator } from '../components/AdvancedCalculator';

export default function AdvancedCalculatorPage() {
  return (
    <Layout title="Advanced Calculator">
      <div className="container mx-auto py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">Advanced Calculator</h1>
          <p className="text-muted-foreground mt-2">
            Configure and optimize your SynthLang implementation with advanced settings and real-time metrics.
          </p>
        </div>
        
        <div className="space-y-8">
          <Calculator />
          
          <div className="bg-accent/10 p-6 rounded-lg">
            <h2 className="text-xl font-semibold mb-4">Tips</h2>
            <ul className="space-y-2 text-muted-foreground">
              <li>• Use presets to quickly load optimized configurations</li>
              <li>• Monitor real-time metrics to optimize performance</li>
              <li>• Enable compression and caching for better efficiency</li>
              <li>• Adjust context size based on your use case</li>
              <li>• Save custom configurations for later use</li>
            </ul>
          </div>
        </div>
      </div>
    </Layout>
  );
}
