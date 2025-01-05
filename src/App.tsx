import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "./components/ui/toaster";
import { SettingsProvider } from "./services/settingsService";
import Index from "./pages/Index";
import Documentation from "./pages/Documentation";
import Playground from "./pages/Playground";
import Analytics from "./pages/Analytics";
import Settings from "./pages/Settings";
import About from "./pages/About";
import Translate from "./pages/Translate";
import AdvancedCalculator from "./pages/AdvancedCalculator";

const App: React.FC = () => {
  return (
    <SettingsProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/documentation" element={<Documentation />} />
          {/* Redirect /test to /playground */}
          <Route path="/test" element={<Navigate to="/playground" replace />} />
          {/* New Playground route */}
          <Route path="/playground" element={<Playground />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/about" element={<About />} />
          <Route path="/translate" element={<Translate />} />
          <Route path="/advanced-calculator" element={<AdvancedCalculator />} />
        </Routes>
        <Toaster />
      </Router>
    </SettingsProvider>
  );
};

export default App;
