import MainNav from "../components/MainNav";

const Analytics = () => {
  return (
    <div className="min-h-screen bg-background">
      <MainNav title="SynthLang Analytics" />
      <main className="container mx-auto p-4">
        <div className="glass-panel p-6">
          <h2 className="text-2xl font-bold mb-4">Performance Analytics</h2>
          <p className="text-muted-foreground mb-6">
            Track and analyze prompt performance metrics, token usage, cost savings, and optimization effectiveness across different models.
          </p>
          {/* Analytics dashboard will be implemented here */}
        </div>
      </main>
    </div>
  );
};

export default Analytics;
