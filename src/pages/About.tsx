import React from "react";
import Layout from "../components/Layout";
import { Github } from "lucide-react";
import { Button } from "../components/ui/button";

const About = () => {
  return (
    <Layout title="About">
      <div className="container mx-auto p-4">
        <div className="max-w-3xl mx-auto space-y-8">
          <div className="glass-panel p-8 rounded-lg border border-border/40 bg-card/30 backdrop-blur">
            <div className="space-y-6">
              <div className="space-y-2">
                <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">
                  SynthLang
                </h1>
                <p className="text-xl text-muted-foreground">
                  A hyper-efficient prompt language for LLMs
                </p>
              </div>

              <div className="space-y-4">
                <p className="text-lg">
                  SynthLang is designed to maximize the efficiency and effectiveness of interactions with Large Language Models. Using compact glyphs and logographic scripts, it reduces token usage while improving prompt clarity and reducing potential biases.
                </p>

                <div className="flex flex-col sm:flex-row gap-4 py-4">
                  <Button
                    variant="outline"
                    className="flex items-center gap-2"
                    onClick={() => window.open("https://github.com/ruvnet/SynthLang", "_blank")}
                  >
                    <Github className="w-4 h-4" />
                    GitHub Repository
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => window.open("https://synthlang.fly.dev/demo", "_blank")}
                  >
                    Live Demo
                  </Button>
                </div>

                <div className="space-y-4 pt-4">
                  <h2 className="text-2xl font-semibold">Key Features</h2>
                  <ul className="list-disc list-inside space-y-2 text-muted-foreground">
                    <li>Compact syntax reduces token usage by up to 40%</li>
                    <li>Structured format improves prompt clarity and maintainability</li>
                    <li>Standardized syntax helps minimize unintended biases</li>
                    <li>Fine-grained control over output format and style</li>
                    <li>Easy to combine and chain operations</li>
                  </ul>
                </div>

                <div className="space-y-4 pt-4">
                  <h2 className="text-2xl font-semibold">Creator</h2>
                  <div className="flex items-start gap-4">
                    <div className="space-y-2">
                      <p className="text-lg">
                        Created by ruv, cause he could.
                      </p>
                      <p className="text-muted-foreground">
                        SynthLang represents a new approach to LLM interaction, focusing on efficiency and clarity through structured syntax and semantic compression.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="pt-8 border-t border-border/40">
                  <p className="text-sm text-muted-foreground">
                    Visit{" "}
                    <a
                      href="https://synthlang.fly.dev/demo"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary hover:underline"
                    >
                      synthlang.fly.dev
                    </a>
                    {" "}for more information and live examples.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default About;
