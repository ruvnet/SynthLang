import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "./components/ui/toaster";
import Index from "./pages/Index";
import Documentation from "./pages/Documentation";
import Test from "./pages/Test";
import Playground from "./pages/Playground";
import Analytics from "./pages/Analytics";
import Settings from "./pages/Settings";
import About from "./pages/About";
import Translate from "./pages/Translate";

function App() {
  return (
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
      </Routes>
      <Toaster />
    </Router>
  );
}

export default App;
