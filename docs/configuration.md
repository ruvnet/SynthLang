# Configuration Guide

## Overview

This guide provides comprehensive information about configuring the SynthLang prompt generator and tester. It covers all available configuration options, their impacts, and recommended settings for different use cases.

## Configuration Structure

```typescript
interface SynthLangConfig {
  translation: TranslationConfig;
  testing: TestingConfig;
  openRouter: OpenRouterConfig;
  storage: StorageConfig;
  analytics: AnalyticsConfig;
}

interface TranslationConfig {
  defaultModel: string;
  optimizationLevel: 'minimal' | 'balanced' | 'aggressive';
  contextPreservation: 'strict' | 'balanced' | 'flexible';
  maxTokens: number;
  temperature: number;
}

interface TestingConfig {
  models: string[];
  metrics: MetricsConfig;
  validation: ValidationConfig;
  reporting: ReportingConfig;
}

interface StorageConfig {
  storageType: 'local' | 'session' | 'persistent';
  maxEntries: number;
  retentionPeriod: number;
  backupEnabled: boolean;
}
```

## Environment Variables

```bash
# API Configuration
OPENROUTER_API_KEY=your-api-key
VITE_APP_VERSION=1.0.0

# Performance Settings
MAX_CONCURRENT_REQUESTS=5
REQUEST_TIMEOUT_MS=30000
RETRY_ATTEMPTS=3

# Storage Settings
STORAGE_TYPE=persistent
MAX_STORAGE_ENTRIES=1000
RETENTION_DAYS=30

# Analytics Settings
ANALYTICS_ENABLED=true
TRACKING_ID=your-tracking-id
```

## Configuration Files

### 1. Main Configuration (config.json)

```json
{
  "translation": {
    "defaultModel": "gpt-3.5-turbo",
    "optimizationLevel": "balanced",
    "contextPreservation": "balanced",
    "maxTokens": 2000,
    "temperature": 0.7
  },
  "testing": {
    "models": [
      "gpt-3.5-turbo",
      "claude-2",
      "palm-2"
    ],
    "metrics": {
      "maxLatency": 5000,
      "maxTokens": 4000,
      "maxCost": 0.05,
      "minSuccessRate": 0.95
    }
  }
}
```

### 2. Model Configuration (models.json)

```json
{
  "models": {
    "gpt-3.5-turbo": {
      "contextWindow": 4096,
      "costPer1kTokens": 0.002,
      "capabilities": ["translation", "optimization"]
    },
    "claude-2": {
      "contextWindow": 100000,
      "costPer1kTokens": 0.008,
      "capabilities": ["translation", "optimization", "analysis"]
    }
  }
}
```

## Use Cases

### 1. Development Environment

```json
{
  "translation": {
    "optimizationLevel": "minimal",
    "contextPreservation": "strict",
    "maxTokens": 4000,
    "temperature": 0.7
  },
  "testing": {
    "models": ["gpt-3.5-turbo"],
    "metrics": {
      "maxLatency": 10000,
      "maxTokens": 8000,
      "maxCost": 0.1
    }
  },
  "storage": {
    "storageType": "local",
    "maxEntries": 100
  }
}
```

### 2. Production Environment

```json
{
  "translation": {
    "optimizationLevel": "aggressive",
    "contextPreservation": "balanced",
    "maxTokens": 2000,
    "temperature": 0.5
  },
  "testing": {
    "models": ["gpt-3.5-turbo", "claude-2"],
    "metrics": {
      "maxLatency": 3000,
      "maxTokens": 4000,
      "maxCost": 0.02
    }
  },
  "storage": {
    "storageType": "persistent",
    "maxEntries": 10000,
    "backupEnabled": true
  }
}
```

## Configuration Options

### 1. Translation Settings

#### Optimization Levels
- **minimal**: Preserves most original content
- **balanced**: Moderate optimization
- **aggressive**: Maximum token reduction

#### Context Preservation
- **strict**: Maintains all context
- **balanced**: Selective context retention
- **flexible**: Minimal context preservation

#### Temperature Settings
- **0.3**: More focused, deterministic
- **0.7**: Balanced creativity
- **1.0**: Maximum creativity

### 2. Testing Settings

#### Metrics Configuration
- Latency thresholds
- Token limits
- Cost constraints
- Success rate requirements

#### Validation Settings
- Similarity thresholds
- Custom validators
- Error tolerances
- Quality metrics

### 3. Storage Settings

#### Storage Types
- **local**: Browser storage
- **session**: Temporary storage
- **persistent**: Database storage

#### Retention Settings
- Entry limits
- Retention periods
- Backup frequency
- Cleanup policies

## Best Practices

### 1. Environment-Specific Configuration

```typescript
const config = {
  development: {
    optimizationLevel: 'minimal',
    storage: 'local',
    metrics: {
      strict: false
    }
  },
  production: {
    optimizationLevel: 'aggressive',
    storage: 'persistent',
    metrics: {
      strict: true
    }
  }
};
```

### 2. Dynamic Configuration

```typescript
class ConfigurationManager {
  private config: SynthLangConfig;

  constructor(environment: string) {
    this.config = this.loadConfig(environment);
  }

  updateConfig(updates: Partial<SynthLangConfig>) {
    this.config = {
      ...this.config,
      ...updates
    };
    this.validateConfig();
    this.saveConfig();
  }

  private validateConfig() {
    // Implement configuration validation
  }
}
```

### 3. Configuration Validation

```typescript
function validateConfig(config: SynthLangConfig): ValidationResult {
  return {
    isValid: checkConfigValidity(config),
    errors: findConfigErrors(config),
    warnings: findConfigWarnings(config)
  };
}
```

## Security Considerations

### 1. API Key Management
- Use environment variables
- Implement key rotation
- Monitor usage
- Set up alerts

### 2. Access Control
- Role-based access
- Permission levels
- Audit logging
- Security policies

### 3. Data Protection
- Encryption at rest
- Secure transmission
- Data retention
- Privacy compliance

## Troubleshooting

### Common Issues

1. **Configuration Loading**
   - Check file paths
   - Verify JSON syntax
   - Validate values
   - Check permissions

2. **Environment Variables**
   - Verify presence
   - Check formatting
   - Update as needed
   - Monitor changes

3. **Performance Issues**
   - Adjust timeouts
   - Optimize settings
   - Monitor metrics
   - Scale resources

## Maintenance

### 1. Regular Updates
- Review settings
- Update thresholds
- Adjust limits
- Optimize performance

### 2. Monitoring
- Track usage
- Monitor errors
- Analyze metrics
- Generate reports

### 3. Backup
- Configuration backup
- Version control
- Recovery procedures
- Audit trails
