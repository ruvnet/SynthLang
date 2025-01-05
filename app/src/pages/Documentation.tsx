import MainNav from "../components/MainNav";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { FileText, BookOpen, Code, Wand2, Network, Brain, GitBranch, Workflow, Shield } from "lucide-react";

export default function Documentation() {
  return (
    <div className="min-h-screen flex flex-col">
      <MainNav title="Documentation" />
      
      <main className="flex-1 p-4">
        <section className="glass-panel p-6 animate-matrix-fade">
          <div className="flex items-center gap-2 mb-6">
            <FileText className="w-6 h-6 text-console-cyan" />
            <h1 className="text-2xl font-code text-console-cyan">Documentation</h1>
          </div>

          <Tabs defaultValue="getting-started" className="space-y-6">
            <TabsList className="grid grid-cols-2 md:grid-cols-4 gap-4 bg-transparent h-auto p-0">
              <TabsTrigger value="getting-started" className="glass-panel data-[state=active]:border-console-cyan">
                <BookOpen className="w-4 h-4 mr-2" />
                Getting Started
              </TabsTrigger>
              <TabsTrigger value="approaches" className="glass-panel data-[state=active]:border-console-cyan">
                <Brain className="w-4 h-4 mr-2" />
                Prompt Approaches
              </TabsTrigger>
              <TabsTrigger value="frameworks" className="glass-panel data-[state=active]:border-console-cyan">
                <Network className="w-4 h-4 mr-2" />
                Frameworks
              </TabsTrigger>
              <TabsTrigger value="workflows" className="glass-panel data-[state=active]:border-console-cyan">
                <Workflow className="w-4 h-4 mr-2" />
                Workflows
              </TabsTrigger>
              <TabsTrigger value="infosec" className="glass-panel data-[state=active]:border-console-cyan">
                <Shield className="w-4 h-4 mr-2" />
                InfoSec
              </TabsTrigger>
              <TabsTrigger value="red-teaming" className="glass-panel data-[state=active]:border-console-cyan">
                <Shield className="w-4 h-4 mr-2" />
                Red Teaming
              </TabsTrigger>
            </TabsList>

            <TabsContent value="getting-started" className="space-y-6">
              <div className="glass-panel p-6">
                <h2 className="text-xl font-code text-console-cyan mb-4 flex items-center gap-2">
                  <BookOpen className="w-5 h-5" />
                  Quick Start Guide
                </h2>
                <div className="space-y-4 text-console-text">
                  <p>
                    Welcome to Symbolic Scribe! This tool enables security researchers and red team professionals to systematically 
                    test AI systems using advanced mathematical frameworks and symbolic reasoning. Here's a comprehensive guide 
                    to get you started:
                  </p>

                  <div className="space-y-6">
                    <div>
                      <h3 className="text-lg font-semibold text-console-cyan mb-2">1. Setting Up Your Environment</h3>
                      <ul className="list-disc list-inside space-y-2 ml-4">
                        <li>Navigate to the Settings page</li>
                        <li>Configure your OpenRouter API key</li>
                        <li>Select your preferred testing models</li>
                        <li>Verify your configuration with a test prompt</li>
                      </ul>
                    </div>

                    <div>
                      <h3 className="text-lg font-semibold text-console-cyan mb-2">2. Creating Your First Test</h3>
                      <ul className="list-disc list-inside space-y-2 ml-4">
                        <li>Start from the Templates page</li>
                        <li>Choose a framework that matches your testing goals</li>
                        <li>Customize the template for your target system</li>
                        <li>Define your attack vectors and boundaries</li>
                      </ul>
                    </div>

                    <div>
                      <h3 className="text-lg font-semibold text-console-cyan mb-2">3. Running Tests</h3>
                      <ul className="list-disc list-inside space-y-2 ml-4">
                        <li>Use the Preview function to test individual prompts</li>
                        <li>Document responses and unexpected behaviors</li>
                        <li>Iterate on your approach based on results</li>
                        <li>Save successful templates for future use</li>
                      </ul>
                    </div>

                    <div>
                      <h3 className="text-lg font-semibold text-console-cyan mb-2">4. Best Practices</h3>
                      <ul className="list-disc list-inside space-y-2 ml-4">
                        <li>Always start with a clear testing objective</li>
                        <li>Use systematic approaches to document findings</li>
                        <li>Follow responsible disclosure guidelines</li>
                        <li>Share defensive insights with the community</li>
                      </ul>
                    </div>

                    <div className="bg-gray-800/50 p-4 rounded-lg">
                      <h4 className="text-console-green mb-2">Pro Tip:</h4>
                      <p>
                        Start with simpler frameworks and gradually increase complexity as you better understand 
                        the system's responses. This methodical approach helps identify subtle vulnerabilities 
                        that might be missed with more complex initial tests.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="approaches" className="space-y-6">
              <div className="glass-panel p-6">
                <h2 className="text-xl font-code text-console-cyan mb-4 flex items-center gap-2">
                  <Brain className="w-5 h-5" />
                  Prompt Engineering Approaches
                </h2>
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Set-Theoretic Approach</h3>
                    <p className="text-console-text mb-2">
                      A foundational approach for modeling security boundaries and attack surfaces:
                    </p>
                    <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Security Domain Modeling
Let A = {x | x is an attack vector}
Let D = {y | y is a defense mechanism}
Let V = {z | z is a vulnerability}

# Relationship Mapping
R₁ = {(a,v) ∈ A × V | a exploits v}
R₂ = {(d,v) ∈ D × V | d mitigates v}

# Coverage Analysis
∀v ∈ V, ∃d ∈ D: (d,v) ∈ R₂
// Ensure all vulnerabilities have mitigations`}
                    </pre>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Category Theory Approach</h3>
                    <p className="text-console-text mb-2">
                      Advanced framework for analyzing system transformations and attack chains:
                    </p>
                    <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Attack Chain Category
Objects: System States
Morphisms: Attack Transitions
Identity: No-op (system unchanged)
Composition: f ∘ g (chained attacks)

# Defense Category
Objects: Security Controls
Morphisms: Defense Updates
Functor F: AttackCat → DefenseCat
// Maps attacks to corresponding defenses

# Properties
∀ attack ∈ Morphisms, ∃ defense ∈ F(Morphisms)
// Every attack has a corresponding defense`}
                    </pre>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Abstract Algebra Approach</h3>
                    <p className="text-console-text mb-2">
                      Powerful method for encoding attack patterns and system behaviors:
                    </p>
                    <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Attack Pattern Group
Group A = (Actions, ∘)
- Identity: Safe state
- Operation ∘: Chain attacks
- Inverse: Rollback/mitigation

# Homomorphism Properties
φ: A → DefenseGroup
φ(a ∘ b) = φ(a) ∘ φ(b)
// Defense composition matches attack composition

# Ring Structure
R = (Actions, ⊕, ⊗)
- Addition ⊕: Parallel attacks
- Multiplication ⊗: Sequential attacks
- Distributive: a ⊗ (b ⊕ c) = (a ⊗ b) ⊕ (a ⊗ c)`}
                    </pre>
                  </div>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="frameworks" className="space-y-6">
              <div className="glass-panel p-6">
                <h2 className="text-xl font-code text-console-cyan mb-4 flex items-center gap-2">
                  <Network className="w-5 h-5" />
                  Mathematical Frameworks
                </h2>
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Logical Framework</h3>
                    <p className="text-console-text mb-4">
                      A comprehensive system for formal reasoning about AI behaviors and security properties:
                    </p>
                    <div className="space-y-4">
                      <div>
                        <h4 className="text-console-green mb-2">Propositional Logic</h4>
                        <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Basic Security Properties
Let S = "System is secure"
Let A = "Attack is successful"
Let D = "Defense is active"

# Logical Operations
¬A         // Attack prevention
D → S      // Defense implies security
S ∧ ¬A     // Security with no successful attacks
D ∨ B      // Either defense or backup is active`}
                        </pre>
                      </div>

                      <div>
                        <h4 className="text-console-green mb-2">Predicate Logic</h4>
                        <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Quantified Security Statements
∀x ∈ Inputs: Safe(x)           // All inputs are safe
∃d ∈ Defenses: Blocks(d, a)    // Some defense blocks attack a
∀a ∃d: Mitigates(d, a)        // Every attack has a mitigation
∀s ∈ States: ¬Vulnerable(s)    // No state is vulnerable`}
                        </pre>
                      </div>

                      <div>
                        <h4 className="text-console-green mb-2">Modal Logic</h4>
                        <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Necessity and Possibility
□Safe(s)      // System is necessarily safe
◇Breach(s)    // Breach is possible
□(A → B)      // Necessarily, A implies B
¬◇Exploit(x)  // Exploit is impossible`}
                        </pre>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Topological Framework</h3>
                    <p className="text-console-text mb-4">
                      Advanced framework for analyzing security boundaries and transformations:
                    </p>
                    <div className="space-y-4">
                      <div>
                        <h4 className="text-console-green mb-2">Security Boundaries</h4>
                        <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Open and Closed Sets
Let X be the security state space
Let U ⊂ X be an open set of safe states
Let C = X\U be the closed set of unsafe states

# Boundary Analysis
∂U = C̄ ∩ Ū    // Security boundary
int(U)        // Interior (definitely safe)
cl(C)         // Closure (potentially unsafe)`}
                        </pre>
                      </div>

                      <div>
                        <h4 className="text-console-green mb-2">Continuous Transformations</h4>
                        <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Security Mappings
f: X → Y       // State transition function
f⁻¹(Safe)     // Preimage of safe states
f(Unsafe)      // Image of unsafe states

# Continuity Properties
∀ε>0 ∃δ>0: d(x,y)<δ ⟹ d(f(x),f(y))<ε
// Small input changes → small output changes`}
                        </pre>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Complex Analysis Framework</h3>
                    <p className="text-console-text mb-4">
                      Sophisticated tools for analyzing multi-dimensional security relationships:
                    </p>
                    <div className="space-y-4">
                      <div>
                        <h4 className="text-console-green mb-2">Security Functions</h4>
                        <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Complex Security Mapping
f(z) = Security(z) + i·Risk(z)
// z represents system state
// Real part: security level
// Imaginary part: risk level

# Analytic Properties
∂f/∂z̄ = 0    // Cauchy-Riemann equations
∮ f(z)dz = 0  // Path independence
f'(z) exists  // Differentiability`}
                        </pre>
                      </div>

                      <div>
                        <h4 className="text-console-green mb-2">Path Analysis</h4>
                        <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Attack Path Integration
∫γ f(z)dz     // Path integral along attack γ
Res(f,a)      // Residue at vulnerability a

# Conformal Mapping
w = f(z)      // Security domain mapping
f⁻¹(Safe)     // Safe region preimage`}
                        </pre>
                      </div>

                      <div>
                        <h4 className="text-console-green mb-2">Application Tutorial</h4>
                        <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Step 1: Model the Security Space
z = x + iy    // x: defense level, y: attack surface

# Step 2: Define Security Function
f(z) = 1/(z - a) // a: known vulnerability

# Step 3: Analyze Behavior
|f(z)| → ∞ as z → a    // Vulnerability detection
arg(f(z))             // Attack angle analysis
∂|f|/∂x = 0           // Critical points`}
                        </pre>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="workflows" className="space-y-6">
              <div className="glass-panel p-6">
                <h2 className="text-xl font-code text-console-cyan mb-4 flex items-center gap-2">
                  <Workflow className="w-5 h-5" />
                  Common Workflows
                </h2>
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Security Analysis Workflow</h3>
                    <div className="space-y-4">
                      <ol className="list-decimal list-inside space-y-2 ml-4">
                        <li>Define the security domain using set theory</li>
                        <li>Model threat vectors as morphisms</li>
                        <li>Apply categorical composition for attack chains</li>
                        <li>Generate security policy functors</li>
                      </ol>
                      
                      <div className="bg-black/30 p-4 rounded-md text-console-text">
                        <h4 className="text-console-green mb-2">Tutorial Example:</h4>
                        <pre className="font-mono text-sm">
{`# 1. Define Security Domain
Let S = {s₁, s₂, ..., sₙ} be system states
Let A = {a₁, a₂, ..., aₘ} be attack vectors
Let D = {d₁, d₂, ..., dₖ} be defenses

# 2. Model Threat Vectors
φᵢ: S → S where φᵢ represents attack aᵢ
ψⱼ: S → S where ψⱼ represents defense dⱼ

# 3. Compose Attack Chains
γ = φₙ ∘ φₙ₋₁ ∘ ... ∘ φ₁
// Full attack sequence

# 4. Generate Policy Functors
F: AttackCat → DefenseCat
F(φᵢ) = ψⱼ where ψⱼ mitigates φᵢ`}</pre>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Ethical Analysis Workflow</h3>
                    <div className="space-y-4">
                      <ol className="list-decimal list-inside space-y-2 ml-4">
                        <li>Define ethical principles as axioms</li>
                        <li>Model stakeholder relationships using category theory</li>
                        <li>Apply logical frameworks for consistency checking</li>
                        <li>Generate ethical constraint functors</li>
                      </ol>

                      <div className="bg-black/30 p-4 rounded-md text-console-text">
                        <h4 className="text-console-green mb-2">Implementation Guide:</h4>
                        <pre className="font-mono text-sm">
{`# 1. Ethical Axioms
A₁: "Do no harm"
A₂: "Respect privacy"
A₃: "Ensure fairness"

# 2. Stakeholder Category
Objects: Users, System, Data
Morphisms: Interactions
f: Users → Data (data access)
g: System → Users (service provision)

# 3. Consistency Checking
∀x ∈ Actions: 
  Satisfies(x, A₁) ∧ 
  Satisfies(x, A₂) ∧ 
  Satisfies(x, A₃)

# 4. Constraint Functors
E: ActionCat → EthicsCat
E(f) must preserve axioms`}</pre>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">AI System Analysis</h3>
                    <div className="space-y-4">
                      <ol className="list-decimal list-inside space-y-2 ml-4">
                        <li>Define system behaviors using abstract algebra</li>
                        <li>Model state spaces topologically</li>
                        <li>Apply complex analysis for multi-agent interactions</li>
                        <li>Generate system constraint morphisms</li>
                      </ol>

                      <div className="bg-black/30 p-4 rounded-md text-console-text">
                        <h4 className="text-console-green mb-2">Practical Example:</h4>
                        <pre className="font-mono text-sm">
{`# 1. Behavior Algebra
(B, ∘) where B is behavior set
Identity: e (neutral behavior)
Inverse: b⁻¹ (behavior reversal)

# 2. State Space Topology
X = (States, τ)
Open sets U ∈ τ: safe states
Closed sets: potentially unsafe

# 3. Multi-Agent Analysis
f(z) = Σ aᵢzⁱ where:
- z: system state
- aᵢ: agent influences

# 4. Constraints
μ: B → C where:
- B: behaviors
- C: constraints
Preserves safety properties`}</pre>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Testing Workflow Tutorial</h3>
                    <div className="space-y-4">
                      <p className="text-console-text">
                        A step-by-step guide to systematic testing using mathematical frameworks:
                      </p>

                      <div className="bg-black/30 p-4 rounded-md text-console-text">
                        <h4 className="text-console-green mb-2">1. Setup Phase</h4>
                        <pre className="font-mono text-sm">
{`# Define Test Domain
T = {t₁, t₂, ..., tₙ} // Test cases
P = {p₁, p₂, ..., pₘ} // Properties to test
R = {r₁, r₂, ..., rₖ} // Expected results

# Create Test Category
Objects: States
Morphisms: Test transitions
Identity: Initial state
Composition: Test sequences`}</pre>
                      </div>

                      <div className="bg-black/30 p-4 rounded-md text-console-text">
                        <h4 className="text-console-green mb-2">2. Execution Phase</h4>
                        <pre className="font-mono text-sm">
{`# Test Functor
F: TestCat → ResultCat
∀t ∈ T: F(t) ∈ R

# Property Verification
∀p ∈ P: Verify(p, F(t))
Record(Results(F(t)))

# Coverage Analysis
C = |F(T)| / |R| * 100
Track(C, "coverage")`}</pre>
                      </div>

                      <div className="bg-black/30 p-4 rounded-md text-console-text">
                        <h4 className="text-console-green mb-2">3. Analysis Phase</h4>
                        <pre className="font-mono text-sm">
{`# Result Analysis
Let A = {(t,r) | t ∈ T, r = F(t)}
Group(A, "by_property")
Analyze(Patterns(A))

# Report Generation
∀p ∈ P:
  Report(
    Coverage(p),
    Failures(p),
    Recommendations(p)
  )`}</pre>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="infosec" className="space-y-6">
              <div className="glass-panel p-6">
                <h2 className="text-xl font-code text-console-cyan mb-4 flex items-center gap-2">
                  <Shield className="w-5 h-5" />
                  Security Considerations
                </h2>
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">API Key Security</h3>
                    <ul className="list-disc list-inside space-y-2 ml-4">
                      <li>Client-side encryption of API keys using AES-256</li>
                      <li>Optional environment variable configuration</li>
                      <li>No server-side storage of sensitive data</li>
                      <li>Automatic key validation and rotation support</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Data Privacy</h3>
                    <ul className="list-disc list-inside space-y-2 ml-4">
                      <li>All processing happens client-side</li>
                      <li>No data persistence beyond local storage</li>
                      <li>Minimal external API communication</li>
                      <li>No tracking or analytics</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Advanced Security Measures</h3>
                    <div className="space-y-4">
                      <div>
                        <h4 className="text-console-green mb-2">Mathematical Input Analysis</h4>
                        <pre className="bg-black/30 p-4 rounded-md text-console-text">
            {`# Input Validation Pipeline
            1. Parse mathematical structures
            2. Analyze semantic embeddings
            3. Compare with known attack patterns
            4. Validate transformations
            5. Check for semantic shifts`}
                        </pre>
                      </div>

                      <div>
                        <h4 className="text-console-green mb-2">Embedding Space Monitoring</h4>
                        <pre className="bg-black/30 p-4 rounded-md text-console-text">
            {`# Vector Analysis
            1. Track embedding distances
            2. Monitor semantic clusters
            3. Detect anomalous mappings
            4. Validate transformations
            5. Check consistency`}
                        </pre>
                      </div>
                      <div>
                        <h4 className="text-console-green mb-2">API Key Management</h4>
                        <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Recommended key rotation schedule
1. Generate new key monthly
2. Update environment variables
3. Verify key functionality
4. Remove old key access`}
                        </pre>
                      </div>
                      
                      <div>
                        <h4 className="text-console-green mb-2">Prompt Security</h4>
                        <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Prompt security checklist
1. Review for sensitive data
2. Validate mathematical structures
3. Check for injection vectors
4. Test with minimal permissions`}
                        </pre>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">MathPrompt Attack Analysis</h3>
                    <div className="space-y-4">
                      <div>
                        <h4 className="text-console-green mb-2">Core Technique</h4>
                        <p className="text-console-text mb-2">
                          MathPrompt transforms harmful prompts into symbolic mathematics problems that evade detection.
                          Success rates of 73.6% across modern LLMs, compared to 1% with unmodified harmful prompts.
                        </p>
                        <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Mathematical Encoding Components
1. Set Theory: A = {x | x ∈ Actions}
2. Abstract Algebra: G = (A, •) group structure
3. Symbolic Logic: P(x) ⟹ Q(x) implications`}
                        </pre>
                      </div>

                      <div>
                        <h4 className="text-console-green mb-2">Vulnerability Analysis</h4>
                        <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Attack Vector Components
Let M be the set of mathematical transformations
Let P be the set of prompts
Let S be the set of safety mechanisms

∃m ∈ M: ∀s ∈ S, ∃p ∈ P: s(m(p)) ≠ s(p)
// There exists a transformation that evades all safety checks`}
                        </pre>
                      </div>

                      <div>
                        <h4 className="text-console-green mb-2">Defense Strategy</h4>
                        <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Mitigation Framework
Let D be defensive measures
Let V be validation functions
Let E be embedding space

∀m ∈ M: ∃d ∈ D: d(m(p)) = d(p)
// Ensure defenses are invariant under mathematical transformation`}
                        </pre>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Security Analysis Framework</h3>
                    <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`Let S = {x | x is a security control}
Let T = {y | y is a threat vector}
Let R ⊆ S × T be the mitigation relation

∀t ∈ T, ∃s ∈ S: (s,t) ∈ R
// Every threat has at least one control

// Extended MathPrompt Defense
Let M = {m | m is a mathematical transformation}
Let V = {v | v is a validation function}
∀m ∈ M, ∃v ∈ V: v(m(x)) = v(x)
// Every transformation must be validated`}
                    </pre>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Incident Response</h3>
                    <ol className="list-decimal list-inside space-y-2 ml-4">
                      <li>Immediately rotate compromised API keys</li>
                      <li>Clear local storage if necessary</li>
                      <li>Review access logs in OpenRouter dashboard</li>
                      <li>Update security controls as needed</li>
                    </ol>
                  </div>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="red-teaming" className="space-y-6">
              <div className="glass-panel p-6">
                <h2 className="text-xl font-code text-console-cyan mb-4 flex items-center gap-2">
                  <Shield className="w-5 h-5" />
                  Red Teaming Methodology
                </h2>
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Preparation Phase</h3>
                    <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Initial Setup
1. Model Architecture Analysis
2. Framework Selection
3. Test Case Design
4. Safety Protocol Implementation`}
                    </pre>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Testing Vectors</h3>
                    <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Core Testing Approaches
1. Semantic Injection Analysis
2. Boundary Testing
3. Context Window Manipulation
4. Mathematical Encoding Tests
5. Chain-of-Thought Analysis`}
                    </pre>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Mathematical Framework Analysis</h3>
                    <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Framework Components
Let M = {m | m is a mathematical transformation}
Let V = {v | v is a validation function}
Let S = {s | s is a security control}

∀m ∈ M, ∃v ∈ V: v(m(x)) = v(x)
// Every transformation must be validated`}
                    </pre>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Documentation & Analysis</h3>
                    <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Analysis Framework
1. Systematic Recording
   - Test case details
   - Results and observations
   - Vulnerability patterns

2. Impact Assessment
   - Security implications
   - Risk categorization
   - Mitigation priorities

3. Pattern Recognition
   - Common vulnerability types
   - Attack vector analysis
   - Defense strategy mapping`}
                    </pre>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Ethical Guidelines</h3>
                    <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Ethical Framework
1. Responsible Disclosure
   - Follow established protocols
   - Coordinate with stakeholders
   - Document findings securely

2. Harm Prevention
   - Containment measures
   - Testing boundaries
   - Safety checkpoints

3. Collaborative Improvement
   - Share findings responsibly
   - Contribute to defense strategies
   - Update methodologies`}
                    </pre>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-console-cyan mb-2">Defense Strategy Development</h3>
                    <pre className="bg-black/30 p-4 rounded-md text-console-text">
{`# Strategy Components
Let D be defensive measures
Let T be threat vectors
Let R be mitigation relation

∀t ∈ T, ∃d ∈ D: (d,t) ∈ R
// Every threat has a corresponding defense

# Implementation Steps
1. Identify vulnerability patterns
2. Develop mitigation strategies
3. Implement security controls
4. Validate effectiveness
5. Document and share findings`}
                    </pre>
                  </div>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </section>
      </main>
    </div>
  );
}
