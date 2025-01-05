import { TabData, FeatureOption, SynthLangConfig, ResponseFormat, SynthLangFeatures, Framework, FrameworkState, FrameworksConfig } from './types';

export const FRAMEWORK_OPTIONS = [
  // Mathematical Frameworks
  {
    id: 'set_theory',
    name: 'Set Theory',
    description: 'Model complex relationships and hierarchies',
    glyphs: [
      { symbol: '∈', name: 'Element Of', description: 'Indicates membership in a set', usage: 'x ∈ A means x is an element of set A' },
      { symbol: '∉', name: 'Not Element Of', description: 'Indicates non-membership', usage: 'x ∉ A means x is not in set A' },
      { symbol: '∪', name: 'Union', description: 'Combines elements of two sets', usage: 'A ∪ B contains all elements in either A or B' },
      { symbol: '∩', name: 'Intersection', description: 'Common elements between sets', usage: 'A ∩ B contains elements in both A and B' },
      { symbol: '∖', name: 'Set Difference', description: 'Elements in first set but not second', usage: 'A ∖ B contains elements in A but not in B' }
    ],
    examples: ['permissions ∈ userRoles', 'allowedActions = adminRoles ∩ userRoles', 'blockedUsers ∉ activeUsers'],
    group: 'mathematical'
  },
  {
    id: 'category_theory',
    name: 'Category Theory',
    description: 'Define abstract transformations and mappings',
    glyphs: [
      { symbol: '→', name: 'Morphism', description: 'Represents a transformation', usage: 'f: A → B maps from A to B' },
      { symbol: '⇒', name: 'Natural Transform', description: 'Higher-level transformation', usage: 'F ⇒ G transforms between functors' },
      { symbol: '↦', name: 'Maps To', description: 'Specific element mapping', usage: 'x ↦ f(x) shows direct transformation' },
      { symbol: '∘', name: 'Composition', description: 'Combines transformations', usage: 'f ∘ g applies g then f' },
      { symbol: '≅', name: 'Isomorphism', description: 'Two-way equivalence', usage: 'A ≅ B means A and B are equivalent' }
    ],
    examples: ['input ↦ processedOutput', 'validate ∘ transform ∘ normalize', 'sourceModel ≅ targetModel'],
    group: 'mathematical'
  },
  {
    id: 'abstract_algebra',
    name: 'Abstract Algebra',
    description: 'Structure group operations and symmetries',
    glyphs: [
      { symbol: '⊕', name: 'Direct Sum', description: 'Combines structures independently', usage: 'V ⊕ W combines spaces V and W' },
      { symbol: '⊗', name: 'Tensor Product', description: 'Complex multiplication of structures', usage: 'A ⊗ B creates combined structure' },
      { symbol: '⊙', name: 'Circle Product', description: 'Specialized composition', usage: 'G ⊙ H combines group actions' },
      { symbol: '∗', name: 'Convolution', description: 'Blending operation', usage: 'f ∗ g blends functions f and g' },
      { symbol: '⋊', name: 'Semidirect Product', description: 'Asymmetric combination', usage: 'G ⋊ H combines with special action' }
    ],
    examples: ['features ⊕ constraints', 'modelA ⊗ modelB', 'transform ⊙ validate'],
    group: 'mathematical'
  },
  {
    id: 'topology',
    name: 'Topology',
    description: 'Explore continuous transformations and invariants',
    glyphs: [
      { symbol: '∂', name: 'Boundary', description: 'Edge or limit of a space', usage: '∂X represents boundary of X' },
      { symbol: '∮', name: 'Contour Integral', description: 'Path-based analysis', usage: '∮ f measures around a path' },
      { symbol: '≃', name: 'Homotopy', description: 'Continuous deformation', usage: 'X ≃ Y means X deforms to Y' },
      { symbol: '↪', name: 'Embedding', description: 'Structure-preserving map', usage: 'A ↪ B embeds A in B' },
      { symbol: '↠', name: 'Surjection', description: 'Onto mapping', usage: 'f: X ↠ Y maps onto all Y' }
    ],
    examples: ['∂(safetyBounds)', 'sourceSpace ≃ targetSpace', 'subProcess ↪ mainProcess'],
    group: 'mathematical'
  },
  {
    id: 'complex_analysis',
    name: 'Complex Analysis',
    description: 'Handle multi-dimensional relationships',
    glyphs: [
      { symbol: '∮', name: 'Contour Integration', description: 'Path-based analysis', usage: '∮ f(z)dz integrates around path' },
      { symbol: '∯', name: 'Surface Integral', description: '2D integration', usage: '∯ f(x,y) over surface' },
      { symbol: '∰', name: 'Volume Integral', description: '3D integration', usage: '∰ f(x,y,z) through volume' },
      { symbol: '∇', name: 'Gradient', description: 'Direction of steepest change', usage: '∇f shows direction of change' },
      { symbol: '∆', name: 'Laplacian', description: 'Sum of second derivatives', usage: '∆φ measures total curvature' }
    ],
    examples: ['∇(complexity)', '∮ modelResponse', '∆(stability)'],
    group: 'mathematical'
  },
  // Logographic Systems
  {
    id: 'mandarin',
    name: 'Mandarin Chinese',
    description: 'Utilize Chinese characters and structural components',
    glyphs: [
      { symbol: '木', name: 'Tree Radical', description: 'Basic component for nature-related characters', usage: '森 (forest) combines multiple 木' },
      { symbol: '氵', name: 'Water Radical', description: 'Water-related concepts', usage: '海 (sea) uses 氵 with 每' },
      { symbol: '心', name: 'Heart Radical', description: 'Emotions and mind', usage: '想 (think) combines 心 with 相' },
      { symbol: '言', name: 'Speech Radical', description: 'Communication-related', usage: '語 (language) uses 言 with 吾' },
      { symbol: '門', name: 'Gate Radical', description: 'Entrance or division', usage: '開 (open) is based on 門' }
    ],
    examples: ['木 → 森 → 林', '心 + 目 = 想', '言 + 吾 = 語'],
    group: 'logographic'
  },
  {
    id: 'japanese',
    name: 'Japanese',
    description: 'Combine kanji, kana, and structural elements',
    glyphs: [
      { symbol: 'あ', name: 'Hiragana A', description: 'Basic hiragana vowel', usage: 'Basic phonetic writing' },
      { symbol: 'ア', name: 'Katakana A', description: 'Katakana vowel', usage: 'Foreign word adaptation' },
      { symbol: '漢', name: 'Kanji (Han)', description: 'Chinese character', usage: 'Semantic meaning carrier' },
      { symbol: '々', name: 'Iteration Mark', description: 'Character repetition', usage: 'Repeats previous kanji' },
      { symbol: 'ー', name: 'Chōonpu', description: 'Long vowel mark', usage: 'Extends vowel sound' }
    ],
    examples: ['漢字 + かな', 'コード化', '人々'],
    group: 'logographic'
  },
  // Semitic Scripts
  {
    id: 'arabic',
    name: 'Arabic',
    description: 'Utilize Arabic script and morphological patterns',
    glyphs: [
      { symbol: 'ا', name: 'Alif', description: 'First letter, long A', usage: 'Basic letter form' },
      { symbol: 'ب', name: 'Ba', description: 'Basic consonant', usage: 'Initial position' },
      { symbol: 'ـ', name: 'Tatweel', description: 'Extension character', usage: 'Extends connections' },
      { symbol: 'ة', name: 'Ta Marbuta', description: 'Feminine ending', usage: 'Marks feminine nouns' },
      { symbol: 'ّ', name: 'Shadda', description: 'Gemination mark', usage: 'Doubles consonant' }
    ],
    examples: ['كَتَبَ', 'مَكْتُوب', 'كِتَاب'],
    group: 'semitic'
  },
  {
    id: 'hebrew',
    name: 'Hebrew',
    description: 'Work with Hebrew script and root systems',
    glyphs: [
      { symbol: 'א', name: 'Alef', description: 'First letter', usage: 'Silent letter carrier' },
      { symbol: 'ב', name: 'Bet', description: 'House letter', usage: 'Basic consonant' },
      { symbol: 'ָ', name: 'Kamatz', description: 'Vowel point', usage: 'Long A sound' },
      { symbol: 'ּ', name: 'Dagesh', description: 'Point in letter', usage: 'Modifies pronunciation' },
      { symbol: '־', name: 'Maqaf', description: 'Hyphen', usage: 'Connects words' }
    ],
    examples: ['שָׁלוֹם', 'סֵפֶר', 'כָּתַב'],
    group: 'semitic'
  },
  // Classical Languages
  {
    id: 'greek',
    name: 'Ancient Greek',
    description: 'Utilize Greek alphabet and philosophical concepts',
    glyphs: [
      { symbol: 'α', name: 'Alpha', description: 'First letter', usage: 'Beginning or primary' },
      { symbol: 'β', name: 'Beta', description: 'Second letter', usage: 'Secondary or version' },
      { symbol: 'π', name: 'Pi', description: 'Mathematical constant', usage: 'Circle ratio' },
      { symbol: 'φ', name: 'Phi', description: 'Golden ratio', usage: 'Ideal proportion' },
      { symbol: 'Ω', name: 'Omega', description: 'Last letter', usage: 'Ultimate or final' }
    ],
    examples: ['λόγος', 'ἀρχή', 'φύσις'],
    group: 'classical'
  },
  {
    id: 'sanskrit',
    name: 'Sanskrit',
    description: 'Work with Devanagari script and compound formation',
    glyphs: [
      { symbol: 'अ', name: 'A', description: 'Basic vowel', usage: 'First letter' },
      { symbol: 'ॐ', name: 'Om', description: 'Sacred symbol', usage: 'Universal sound' },
      { symbol: '्', name: 'Virama', description: 'Vowel suppressor', usage: 'Consonant joining' },
      { symbol: 'ं', name: 'Anusvara', description: 'Nasal sound', usage: 'Nasalization' },
      { symbol: 'ः', name: 'Visarga', description: 'Aspiration mark', usage: 'Final aspiration' }
    ],
    examples: ['धर्म', 'कर्म', 'योग'],
    group: 'classical'
  },
  // Constructed Languages
  {
    id: 'ithkuil',
    name: 'Ithkuil',
    description: 'Use the precise semantic features of Ithkuil',
    glyphs: [
      { symbol: '▯', name: 'Stem', description: 'Basic concept form', usage: 'Root meaning' },
      { symbol: '◌', name: 'Pattern', description: 'Semantic modification', usage: 'Meaning alteration' },
      { symbol: '△', name: 'Function', description: 'Grammatical role', usage: 'Syntactic marking' },
      { symbol: '⬡', name: 'Specification', description: 'Contextual detail', usage: 'Meaning refinement' },
      { symbol: '⬢', name: 'Configuration', description: 'Arrangement pattern', usage: 'Structural marking' }
    ],
    examples: ['▯◌△', '⬡⬢▯', '△◌⬢'],
    group: 'constructed'
  },

  // Optimization Frameworks
  {
    id: 'super_optimized',
    name: 'Super Optimized Framework',
    description: 'Achieve maximum data density through advanced compression techniques',
    glyphs: [
      { symbol: '⚡', name: 'Compress', description: 'Ultra-dense data compression', usage: 'Compress(data) -> densified output' },
      { symbol: '⚙', name: 'Pack', description: 'Bit-level packing operation', usage: 'Pack(bits) for minimal space' },
      { symbol: '⟪', name: 'Fold', description: 'Semantic folding for density', usage: 'Fold concepts into minimal form' },
      { symbol: '⟫', name: 'Unfold', description: 'Semantic expansion', usage: 'Unfold compressed concepts' },
      { symbol: '⌘', name: 'Optimize', description: 'Multi-level optimization', usage: 'Apply all optimization techniques' }
    ],
    examples: ['⚡data -> compact', '⟪concept⟫ -> dense', '⌘[process] -> optimal'],
    group: 'optimization'
  },
  {
    id: 'machine_language',
    name: 'Machine Language Framework',
    description: 'Low-level optimization using machine-oriented patterns',
    glyphs: [
      { symbol: '⎈', name: 'Register', description: 'Direct register operations', usage: 'Store in fast-access register' },
      { symbol: '⌥', name: 'Bitwise', description: 'Bit-level operations', usage: 'Manipulate individual bits' },
      { symbol: '⌤', name: 'Stack', description: 'Stack operations', usage: 'Push/pop for memory efficiency' },
      { symbol: '⎆', name: 'Cache', description: 'Cache optimization', usage: 'Optimize for cache hits' },
      { symbol: '⎇', name: 'Branch', description: 'Efficient branching', usage: 'Optimize conditional flows' }
    ],
    examples: ['⎈reg -> fast', '⌥bits & mask', '⎆[data] -> cached'],
    group: 'optimization'
  }
] as const;

export const CALCULATOR_TABS: TabData[] = [
  {
    id: 'basic',
    label: 'Basic Settings',
    description: 'Configure core SynthLang parameters and model selection'
  },
  {
    id: 'frameworks',
    label: 'Frameworks',
    description: 'Mathematical frameworks and specialized glyphs'
  },
  {
    id: 'advanced',
    label: 'Advanced Features',
    description: 'Fine-tune language processing and optimization settings'
  },
  {
    id: 'optimization',
    label: 'Optimizations',
    description: 'Performance and efficiency settings'
  },
  {
    id: 'metrics',
    label: 'Metrics',
    description: 'View detailed performance and cost metrics'
  },
  {
    id: 'preview',
    label: 'Preview',
    description: 'Preview SynthLang output and configuration'
  }
];

export const DEFAULT_FRAMEWORKS_CONFIG: FrameworksConfig = {
  // Mathematical
  set_theory: { enabled: false, selectedGlyphs: [], customGlyphs: [] },
  category_theory: { enabled: false, selectedGlyphs: [], customGlyphs: [] },
  abstract_algebra: { enabled: false, selectedGlyphs: [], customGlyphs: [] },
  topology: { enabled: false, selectedGlyphs: [], customGlyphs: [] },
  complex_analysis: { enabled: false, selectedGlyphs: [], customGlyphs: [] },
  
  // Logographic
  mandarin: { enabled: false, selectedGlyphs: [], customGlyphs: [] },
  japanese: { enabled: false, selectedGlyphs: [], customGlyphs: [] },
  
  // Semitic
  arabic: { enabled: false, selectedGlyphs: [], customGlyphs: [] },
  hebrew: { enabled: false, selectedGlyphs: [], customGlyphs: [] },
  
  // Classical
  greek: { enabled: false, selectedGlyphs: [], customGlyphs: [] },
  sanskrit: { enabled: false, selectedGlyphs: [], customGlyphs: [] },
  
  // Constructed
  ithkuil: { enabled: false, selectedGlyphs: [], customGlyphs: [] },
  
  // Optimization
  super_optimized: { enabled: false, selectedGlyphs: [], customGlyphs: [] },
  machine_language: { enabled: false, selectedGlyphs: [], customGlyphs: [] }
};

export const BASE_FRAMEWORKS: Framework[] = [
  // Mathematical Frameworks
  {
    id: 'set_theory',
    name: 'Set Theory',
    description: 'Model complex relationships and hierarchies',
    details: 'Use set theory to model relationships between entities, define clear boundaries, and establish hierarchical structures in your prompts.',
    applications: [
      'Information security - Model threat vectors and attack surfaces',
      'Access control - Define user roles and permissions',
      'Data classification - Organize and categorize information',
      'Entity relationships - Map connections between system components'
    ],
    glyphs: [],
    examples: [],
    group: 'mathematical'
  },
  {
    id: 'category_theory',
    name: 'Category Theory',
    description: 'Define abstract transformations and mappings',
    details: 'Apply category theory to model transformations between different domains, compose operations, and maintain structural relationships.',
    applications: [
      'Ethical analysis - Structure moral frameworks and constraints',
      'Data pipelines - Model transformation sequences',
      'State transitions - Track system changes',
      'Cross-domain mappings - Connect different conceptual spaces'
    ],
    glyphs: [],
    examples: [],
    group: 'mathematical'
  },
  {
    id: 'abstract_algebra',
    name: 'Abstract Algebra',
    description: 'Structure group operations and symmetries',
    details: 'Leverage abstract algebra to define operations, analyze symmetries, and structure transformations.',
    applications: [
      'AI safety - Define system boundaries and constraints',
      'Operation composition - Combine multiple transformations',
      'Symmetry analysis - Identify patterns and invariants',
      'Transformation groups - Model related operations'
    ],
    glyphs: [],
    examples: [],
    group: 'mathematical'
  },
  {
    id: 'topology',
    name: 'Topology',
    description: 'Explore continuous transformations and invariants',
    details: 'Use topology to understand properties that remain unchanged under transformations, analyze boundaries, and map connections.',
    applications: [
      'Boundary analysis - Define system limits and interfaces',
      'Invariant preservation - Maintain critical properties',
      'Connection mapping - Understand relationships',
      'Continuous transformation - Model smooth changes'
    ],
    glyphs: [],
    examples: [],
    group: 'mathematical'
  },
  {
    id: 'complex_analysis',
    name: 'Complex Analysis',
    description: 'Handle multi-dimensional relationships',
    details: 'Apply complex analysis to work with multi-dimensional relationships, analyze phase transitions, and model complex transformations.',
    applications: [
      'Multi-dimensional mapping - Handle complex relationships',
      'Phase transitions - Model state changes',
      'Field theory - Analyze continuous properties',
      'Transform composition - Combine multiple operations'
    ],
    glyphs: [],
    examples: [],
    group: 'mathematical'
  },

  // Logographic Systems
  {
    id: 'mandarin',
    name: 'Mandarin Chinese',
    description: 'Utilize Chinese characters and structural components',
    details: 'Leverage the rich semantic and structural features of Chinese characters for nuanced expression.',
    applications: [
      'Semantic decomposition - Break down complex meanings',
      'Radical analysis - Understand component relationships',
      'Character evolution - Track meaning transformations',
      'Compound formation - Build complex concepts'
    ],
    glyphs: [],
    examples: [],
    group: 'logographic'
  },
  {
    id: 'japanese',
    name: 'Japanese',
    description: 'Combine kanji, kana, and structural elements',
    details: 'Use the multi-script nature of Japanese to express different levels of meaning and formality.',
    applications: [
      'Script interaction - Mix kanji and kana effectively',
      'Semantic layering - Express multiple meaning levels',
      'Phonetic representation - Handle pronunciation variants',
      'Cultural context - Incorporate Japanese concepts'
    ],
    glyphs: [],
    examples: [],
    group: 'logographic'
  },

  // Semitic Scripts
  {
    id: 'arabic',
    name: 'Arabic',
    description: 'Utilize Arabic script and morphological patterns',
    details: 'Leverage the root-pattern morphology and connecting script features of Arabic.',
    applications: [
      'Root analysis - Extract core meanings',
      'Pattern application - Generate related concepts',
      'Script connectivity - Handle joining behaviors',
      'Diacritical marks - Specify precise meanings'
    ],
    glyphs: [],
    examples: [],
    group: 'semitic'
  },
  {
    id: 'hebrew',
    name: 'Hebrew',
    description: 'Work with Hebrew script and root systems',
    details: 'Use the three-letter root system and vowel point features of Hebrew.',
    applications: [
      'Root-based analysis - Understand word relationships',
      'Vowel modification - Alter word meanings',
      'Numerical values - Work with gematria',
      'Script variations - Handle different forms'
    ],
    glyphs: [],
    examples: [],
    group: 'semitic'
  },

  // Classical Languages
  {
    id: 'greek',
    name: 'Ancient Greek',
    description: 'Utilize Greek alphabet and philosophical concepts',
    details: 'Incorporate classical Greek philosophical and mathematical notation.',
    applications: [
      'Mathematical notation - Use Greek symbols',
      'Philosophical concepts - Express abstract ideas',
      'Etymological analysis - Trace word origins',
      'Scientific notation - Apply standard symbols'
    ],
    glyphs: [],
    examples: [],
    group: 'classical'
  },
  {
    id: 'sanskrit',
    name: 'Sanskrit',
    description: 'Work with Devanagari script and compound formation',
    details: 'Leverage Sanskrit\'s precise grammatical and semantic features.',
    applications: [
      'Compound formation - Build complex terms',
      'Phonetic precision - Specify exact sounds',
      'Semantic analysis - Break down word meanings',
      'Grammatical roles - Define relationships'
    ],
    glyphs: [],
    examples: [],
    group: 'classical'
  },

  // Constructed Languages
  {
    id: 'ithkuil',
    name: 'Ithkuil',
    description: 'Use the precise semantic features of Ithkuil',
    details: 'Leverage Ithkuil\'s highly specific and unambiguous expression system.',
    applications: [
      'Cognitive categorization - Express precise concepts',
      'Semantic precision - Eliminate ambiguity',
      'Morphological analysis - Break down meaning components',
      'Logical relationships - Define exact connections'
    ],
    glyphs: [],
    examples: [],
    group: 'constructed'
  },

  // Optimization Frameworks
  {
    id: 'super_optimized',
    name: 'Super Optimized Framework',
    description: 'Achieve maximum data density through advanced compression techniques',
    details: 'Utilize cutting-edge compression and optimization techniques to achieve the highest possible data density while maintaining semantic clarity.',
    applications: [
      'Ultra-dense encoding - Maximize information per token',
      'Semantic compression - Fold complex concepts into minimal forms',
      'Multi-level optimization - Apply layered efficiency techniques',
      'Lossless density - Maintain full meaning in compressed form'
    ],
    glyphs: [],
    examples: [],
    group: 'optimization'
  },
  {
    id: 'machine_language',
    name: 'Machine Language Framework',
    description: 'Low-level optimization using machine-oriented patterns',
    details: 'Apply machine-level optimization patterns to achieve maximum efficiency through direct hardware-inspired operations.',
    applications: [
      'Register optimization - Direct fast-access operations',
      'Cache efficiency - Optimize data locality and access',
      'Stack management - Efficient memory utilization',
      'Branch prediction - Optimize conditional flows'
    ],
    glyphs: [],
    examples: [],
    group: 'optimization'
  }
];

export const FEATURE_OPTIONS: FeatureOption[] = [
  {
    id: 'responseFormat',
    name: 'Response Format',
    description: 'Output format for model responses',
    defaultValue: 'json',
    type: 'string'
  },
  {
    id: 'contextWindow',
    name: 'Context Window',
    description: 'Maximum number of tokens for context',
    defaultValue: 4096,
    type: 'number'
  },
  {
    id: 'temperature',
    name: 'Temperature',
    description: 'Controls randomness in output (0.0-1.0)',
    defaultValue: 0.7,
    type: 'number'
  },
  {
    id: 'streamingMode',
    name: 'Streaming Mode',
    description: 'Enable token streaming for real-time output',
    defaultValue: true,
    type: 'boolean'
  },
  {
    id: 'customPrompt',
    name: 'Custom Prompt',
    description: 'Custom system prompt override',
    defaultValue: '',
    type: 'string'
  }
];

export const OPTIMIZATION_OPTIONS: FeatureOption[] = [
  {
    id: 'caching',
    name: 'Response Caching',
    description: 'Cache responses for improved performance',
    defaultValue: true,
    type: 'boolean'
  },
  {
    id: 'batchProcessing',
    name: 'Batch Processing',
    description: 'Process multiple requests in batches',
    defaultValue: false,
    type: 'boolean'
  },
  {
    id: 'compression',
    name: 'Token Compression',
    description: 'Compress tokens for reduced API costs',
    defaultValue: true,
    type: 'boolean'
  }
];

export const DEFAULT_CONFIG: SynthLangConfig = {
  model: 'gpt-4',
  contextSize: 4096,
  features: {
    contextWindow: 4096,
    temperature: 0.7,
    streamingMode: true,
    customPrompt: '',
    responseFormat: 'json' as ResponseFormat
  } as SynthLangFeatures,
  optimizations: {
    caching: true,
    batchProcessing: false,
    compression: true
  },
  frameworks: DEFAULT_FRAMEWORKS_CONFIG,
  customFrameworks: []
};
