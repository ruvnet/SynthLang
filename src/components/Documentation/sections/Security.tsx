import { Shield } from "lucide-react";
import { DocSection } from "../types";

export const Security: DocSection = {
  title: "Security",
  icon: Shield,
  content: [
    {
      title: "API Key Management",
      text: `Secure handling of API keys and authentication:`,
      items: [
        "Encrypted local storage using industry-standard algorithms",
        "Environment variable support for secure deployment",
        "No server-side storage of sensitive credentials",
        "Automatic key rotation and validation"
      ],
      example: `Environment Configuration:
# .env file
OPENROUTER_API_KEY=****
KEY_ENCRYPTION_KEY=****
ROTATION_INTERVAL=7d

Runtime Security:
- Memory-safe key storage
- Automatic key expiration
- Access logging and monitoring
- Breach detection and alerts`
    },
    {
      title: "Data Privacy",
      text: `Comprehensive data protection measures:`,
      items: [
        "Client-side only processing for sensitive data",
        "No external data transmission except to OpenRouter API",
        "Zero telemetry or analytics collection",
        "Configurable model selection for data sovereignty"
      ],
      example: `Privacy Controls:
↹ data ^sensitive
⊕ process ^local_only
⊕ audit_log ^compliance

Data Handling:
- Local processing only
- No persistent storage
- Secure memory clearing
- Access controls`
    },
    {
      title: "Compliance Features",
      text: `Built-in support for regulatory compliance:`,
      items: [
        "GDPR-compliant data handling",
        "CCPA-ready data controls",
        "SOC 2 compatible logging",
        "HIPAA-aligned security measures"
      ],
      example: `Compliance Configuration:
↹ data.sensitive ^gdpr
⊕ process.validate [
  pii_detection
  data_minimization
  audit_trail
]
⊕ report ^compliance`
    },
    {
      title: "Security Best Practices",
      text: `Recommended security measures for production deployment:`,
      items: [
        "Regular API key rotation (7-30 days)",
        "Environment variable usage in production",
        "Continuous API usage monitoring",
        "Regular security audits and updates"
      ],
      example: `Security Implementation:
# Key Rotation
↹ api_keys ^audit
⊕ IF age>7d => rotate
⊕ notify.admin

# Usage Monitoring
↹ api_usage ^realtime
⊕ IF anomaly => alert
⊕ log ^detailed`
    },
    {
      title: "Access Control",
      text: `Granular control over system access and operations:`,
      items: [
        "Role-based access control (RBAC)",
        "Fine-grained permission management",
        "Audit logging of all operations",
        "IP-based access restrictions"
      ],
      example: `Access Policies:
roles:
  admin: [read, write, execute, manage]
  user: [read, execute]
  audit: [read, log]

restrictions:
  ip_whitelist: true
  2fa_required: true
  session_timeout: 1h`
    },
    {
      title: "Encryption",
      text: `Multi-layer encryption strategy:`,
      items: [
        "AES-256 for data at rest",
        "TLS 1.3 for data in transit",
        "Key derivation using PBKDF2",
        "Secure key storage with hardware protection"
      ],
      example: `Encryption Layers:
1. Transport Layer:
   - TLS 1.3
   - Certificate pinning
   - Perfect forward secrecy

2. Data Layer:
   - AES-256-GCM
   - Secure key rotation
   - Zero-knowledge architecture`
    },
    {
      title: "Incident Response",
      text: `Automated security incident handling:`,
      items: [
        "Real-time threat detection",
        "Automated response procedures",
        "Incident logging and analysis",
        "Recovery protocols"
      ],
      example: `Incident Workflow:
↹ security.monitor ^realtime
⊕ IF threat_detected => [
  block_access
  notify.admin
  log.incident
  initiate.investigation
]`
    }
  ]
};
