import MainNav from "../components/MainNav";
import { Info, Github, Brain, Sparkles } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function About() {
  return (
    <div className="min-h-screen flex flex-col">
      <MainNav title="About" />
      
      <main className="flex-1 p-4">
        <section className="glass-panel p-6 animate-matrix-fade">
          <div className="flex items-center gap-2 mb-6">
            <Info className="w-6 h-6 text-console-cyan" />
            <h1 className="text-2xl font-code text-console-cyan">About Symbolic Scribe</h1>
          </div>

          <div className="space-y-6">
            <div className="prose prose-invert max-w-none">
              <p className="text-console-text text-lg">
                Symbolic Scribe is a cutting-edge security testing platform designed to identify and mitigate vulnerabilities in AI systems. 
                By leveraging advanced mathematical frameworks and symbolic reasoning, it provides a comprehensive toolkit for testing 
                prompt injection vulnerabilities and other exploits across various language models.
              </p>
              <p className="text-console-text text-lg mt-4">
                With integration to the Open Router API, Symbolic Scribe enables testing across dozens of different LLMs, 
                providing a robust platform for evaluating prompt security under diverse conditions. The application 
                prioritizes security by encrypting API keys and storing them locally, with full source code transparency 
                for additional trust and verification.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
              <Card className="glass-panel border-console-cyan">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Brain className="w-5 h-5 text-console-cyan" />
                    <span className="text-console-cyan">Advanced Security Testing</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-console-text">
                    Leverages symbolic reasoning and mathematical frameworks to systematically test and identify 
                    vulnerabilities in AI systems, enabling the development of stronger safety mechanisms and 
                    more resilient models.
                  </p>
                </CardContent>
              </Card>

              <Card className="glass-panel border-console-cyan">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-console-cyan" />
                    <span className="text-console-cyan">Flexible Templates</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-console-text">
                    Provides a variety of mathematical frameworks that can be adapted to different domains,
                    from information security to ethical considerations in AI systems.
                  </p>
                </CardContent>
              </Card>

              <Card className="glass-panel border-console-cyan">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Github className="w-5 h-5 text-console-cyan" />
                    <span className="text-console-cyan">Open Source</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-console-text">
                    Developed as an open-source project, welcoming contributions and improvements from
                    the community to enhance prompt engineering capabilities.
                  </p>
                </CardContent>
              </Card>
            </div>

            <div className="glass-panel p-6 mt-8 bg-background/95">
              <h2 className="text-xl font-code text-console-cyan mb-4">Mission & Goals</h2>
              <ul className="space-y-4 text-console-text dark:text-gray-300">
                <li className="flex items-start gap-2">
                  <span className="text-console-cyan">•</span>
                  Identify and mitigate vulnerabilities in AI systems through systematic testing
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-console-cyan">•</span>
                  Develop robust defenses against prompt injections and semantic attacks
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-console-cyan">•</span>
                  Enable comprehensive security testing across multiple LLM platforms
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-console-cyan">•</span>
                  Foster responsible security research and collaborative defense strategies
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-console-cyan">•</span>
                  Advance the field of AI safety through open-source tools and methodologies
                </li>
              </ul>
            </div>

            <div className="glass-panel p-6 mt-8 bg-background/95">
              <h2 className="text-xl font-code text-console-cyan mb-4">Red-Teaming Methodology</h2>
              <div className="space-y-4">
                <p className="text-console-text dark:text-gray-300">
                  Our red-teaming framework employs a systematic approach to identify and document potential vulnerabilities 
                  in AI systems through mathematical frameworks and symbolic reasoning. The methodology consists of several 
                  key phases:
                </p>

                <div className="space-y-6 mt-4">
                  <div>
                    <h3 className="text-lg font-code text-console-cyan mb-2">1. Preparation Phase</h3>
                    <ul className="list-disc pl-6 space-y-2 text-console-text">
                      <li>Model Analysis: Comprehensive evaluation of target model's architecture and known constraints</li>
                      <li>Framework Selection: Choose appropriate mathematical frameworks based on testing objectives</li>
                      <li>Test Case Design: Development of structured test cases using symbolic reasoning</li>
                      <li>Safety Protocol Implementation: Establish containment measures and ethical boundaries</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="text-lg font-code text-console-cyan mb-2">2. Testing Vectors</h3>
                    <ul className="list-disc pl-6 space-y-2 text-console-text">
                      <li>Semantic Injection: Testing for vulnerabilities in natural language understanding</li>
                      <li>Boundary Analysis: Probing edge cases in model responses</li>
                      <li>Context Manipulation: Testing context window limitations and dependencies</li>
                      <li>Mathematical Encoding: Using symbolic systems to encode potentially harmful content</li>
                      <li>Chain-of-Thought Analysis: Testing reasoning paths and logical vulnerabilities</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="text-lg font-code text-console-cyan mb-2">3. Documentation & Analysis</h3>
                    <ul className="list-disc pl-6 space-y-2 text-console-text">
                      <li>Systematic Recording: Detailed documentation of all test cases and results</li>
                      <li>Impact Assessment: Evaluation of potential security implications</li>
                      <li>Pattern Recognition: Identification of common vulnerability patterns</li>
                      <li>Defense Strategy Development: Formulation of mitigation strategies</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="text-lg font-code text-console-cyan mb-2">4. Ethical Considerations</h3>
                    <ul className="list-disc pl-6 space-y-2 text-console-text">
                      <li>Responsible Disclosure: Following established vulnerability disclosure protocols</li>
                      <li>Harm Prevention: Ensuring testing doesn't create unintended consequences</li>
                      <li>Collaborative Improvement: Sharing findings with the AI safety community</li>
                      <li>Continuous Refinement: Regular updates to testing methodology based on new insights</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <div className="glass-panel p-6 mt-8 bg-background/95">
              <h2 className="text-xl font-code text-console-cyan mb-4">Responsible Usage & Collaboration</h2>
              <p className="text-console-text dark:text-gray-300">
                This tool is designed for protection, not exploitation. We welcome contributions from security researchers, 
                AI developers, and ethical hackers committed to improving AI safety. Join our community in developing better 
                safeguards and making AI systems more secure for everyone.
              </p>
              <p className="text-console-text dark:text-gray-300 mt-4">
                Through techniques like symbolic reasoning, mathematical encoding, and systematic vulnerability testing, 
                we can identify and address security gaps in even the most advanced models. Together, we can build a 
                more secure future for AI technology.
              </p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
