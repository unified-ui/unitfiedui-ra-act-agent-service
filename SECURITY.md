# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

1. **Do NOT** open a public GitHub issue
2. Email: **rico.goerlitz@gmail.com**
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact

We will respond within **48 hours** and work with you to resolve the issue before any public disclosure.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.x.x   | ✅ Latest only |

## Security Best Practices

This service implements the following security measures:

- **Service-to-Service Authentication**: All requests require a valid `X-Service-Key` header
- **Secret Management**: Credentials stored in secure vaults (Azure Key Vault, HashiCorp Vault)
- **No Secrets in Code**: All secrets loaded from environment or vault at runtime
- **Input Validation**: Pydantic models validate all request payloads
- **Dependency Scanning**: Dependabot monitors for vulnerable dependencies
