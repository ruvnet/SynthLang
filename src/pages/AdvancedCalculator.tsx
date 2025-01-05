import { useState, useEffect } from "react";
import Layout from "../components/Layout";
import { AdvancedCalculator } from "../components/AdvancedCalculator";
import { PreviewDisplay } from "../components/AdvancedCalculator/PreviewDisplay";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { Link } from "react-router-dom";
import { 
  Gauge, 
  Cpu, 
  Brain, 
  Settings, 
  Download, 
  Upload,
  BookOpen,
  Code,
  Lightbulb,
  ArrowRight
} from "lucide-react";
import { QuickActions } from "../components/AdvancedCalculator/QuickActions";
import { SynthLangConfig } from "../components/AdvancedCalculator/types";

const AdvancedCalculatorPage = () => {
  const [activeTab, setActiveTab] = useState("calculator");
  const [config, setConfig] = useState<SynthLangConfig | undefined>();

  useEffect(() => {
    // Load initial config from localStorage
    const savedConfig = localStorage.getItem('synthLang.calculatorConfig');
    if (savedConfig) {
      try {
        setConfig(JSON.parse(savedConfig));
      } catch (err) {
        console.error('Failed to parse saved config:', err);
      }
    }

    // Listen for config changes
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'synthLang.calculatorConfig' && e.newValue) {
        try {
          setConfig(JSON.parse(e.newValue));
        } catch (err) {
          console.error('Failed to parse updated config:', err);
        }
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  return (
    <Layout title="Advanced SynthLang Calculator">
      <main className="container mx-auto p-4 space-y-6">
        {/* Header Section */}
        <div className="glass-panel p-6">
          <h1 className="text-3xl font-bold mb-4">Advanced SynthLang Calculator</h1>
          <p className="text-muted-foreground text-lg mb-6">
            Fine-tune your SynthLang implementation with advanced settings and optimizations. 
            Configure model parameters, features, and analyze performance metrics.
          </p>
          <div className="grid md:grid-cols-3 gap-4 mb-6">
            <div className="glass-panel p-4">
              <div className="flex items-center gap-2 mb-2">
                <Gauge className="w-5 h-5 text-purple-400" />
                <h3 className="font-semibold">Token Efficiency</h3>
              </div>
              <p className="text-sm text-muted-foreground">Up to 3.33× improvement (233% increase)</p>
            </div>
            <div className="glass-panel p-4">
              <div className="flex items-center gap-2 mb-2">
                <Cpu className="w-5 h-5 text-blue-400" />
                <h3 className="font-semibold">Processing Speed</h3>
              </div>
              <p className="text-sm text-muted-foreground">84% reduction in latency</p>
            </div>
            <div className="glass-panel p-4">
              <div className="flex items-center gap-2 mb-2">
                <Brain className="w-5 h-5 text-green-400" />
                <h3 className="font-semibold">Memory Usage</h3>
              </div>
              <p className="text-sm text-muted-foreground">60% reduction in attention matrices</p>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="glass-panel p-6">
          <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
          <QuickActions />
        </div>

        {/* Main Content */}
        <div className="glass-panel p-6">
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="calculator">Calculator</TabsTrigger>
              <TabsTrigger value="preview">Preview</TabsTrigger>
            </TabsList>
            <TabsContent value="calculator">
              <AdvancedCalculator onTabChange={(tab) => {
                if (tab === 'preview') {
                  setActiveTab('preview');
                }
              }} />
            </TabsContent>
            <TabsContent value="preview">
              <PreviewDisplay config={config} />
            </TabsContent>
          </Tabs>
        </div>

        {/* Additional Resources */}
        <div className="glass-panel p-6">
          <h2 className="text-xl font-semibold mb-4">Additional Resources</h2>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="glass-panel p-4">
              <div className="flex items-center gap-2 mb-2">
                <BookOpen className="w-5 h-5 text-purple-400" />
                <h3 className="font-semibold">Documentation</h3>
              </div>
              <p className="text-sm text-muted-foreground mb-2">Learn more about advanced features and optimizations</p>
              <Link to="/documentation" className="text-sm text-primary hover:underline inline-flex items-center gap-1">
                View Docs <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            <div className="glass-panel p-4">
              <div className="flex items-center gap-2 mb-2">
                <Code className="w-5 h-5 text-blue-400" />
                <h3 className="font-semibold">Examples</h3>
              </div>
              <p className="text-sm text-muted-foreground mb-2">See real-world examples of optimized configurations</p>
              <Link to="/examples" className="text-sm text-primary hover:underline inline-flex items-center gap-1">
                View Examples <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            <div className="glass-panel p-4">
              <div className="flex items-center gap-2 mb-2">
                <Lightbulb className="w-5 h-5 text-green-400" />
                <h3 className="font-semibold">Best Practices</h3>
              </div>
              <p className="text-sm text-muted-foreground mb-2">Tips for getting the most out of SynthLang</p>
              <Link to="/best-practices" className="text-sm text-primary hover:underline inline-flex items-center gap-1">
                Learn More <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
};

export default AdvancedCalculatorPage;
