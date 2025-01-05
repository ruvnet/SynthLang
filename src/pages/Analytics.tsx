import Layout from "../components/Layout";

const Analytics = () => {
  return (
    <Layout title="Analytics">
      <main className="container mx-auto p-4">
        <div className="glass-panel p-6 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
          <h2 className="text-2xl font-bold mb-4">Performance Analytics</h2>
          <p className="text-muted-foreground mb-6">
            Track and analyze prompt performance metrics, token usage, cost savings, and optimization effectiveness across different models.
          </p>
          {/* Analytics dashboard will be implemented here */}
        </div>
      </main>
    </Layout>
  );
};

export default Analytics;
